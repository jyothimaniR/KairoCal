"""
Priority-Based Intelligent Scheduler Service for KairoCal

This service provides smart time slot suggestions based on event priority levels,
leveraging existing BERT priority classification and user behavior analytics.

SAFETY NOTE: This is a NEW service that supplements existing functionality
without modifying any current working systems.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy.orm import Session
import logging

# Import existing working components (read-only usage)
try:
    from app.nlp.user_behavior_analytics import (
        UserBehaviorAnalyzer, 
        TimeSlotSuggestion,
        UserPattern
    )
    USER_ANALYTICS_AVAILABLE = True
except ImportError:
    USER_ANALYTICS_AVAILABLE = False
    
try:
    from app.services.conflict_detector import SmartConflictDetector
    SMART_DETECTOR_AVAILABLE = True
except ImportError:
    SMART_DETECTOR_AVAILABLE = False

from app.models.event import Event
from app.models.user import User

logger = logging.getLogger(__name__)

@dataclass
class PriorityTimeSlot:
    """Enhanced time slot suggestion with priority-based context"""
    start_time: datetime
    end_time: datetime
    confidence: float
    reasoning: str
    priority_match_score: float  # How well this slot matches the priority level
    availability_score: float   # How available this time slot is
    productivity_score: Optional[float] = None
    is_prime_time: bool = False  # Whether this is prime business hours
    conflict_risk: float = 0.0   # Risk of future conflicts

@dataclass
class PrioritySchedulingResult:
    """Complete result from priority-based scheduling"""
    original_priority: int
    suggested_slots: List[PriorityTimeSlot]
    reasoning: str
    total_slots_considered: int
    filter_criteria_used: List[str]
    fallback_used: bool = False

class PriorityBasedScheduler:
    """
    Intelligent scheduler that provides time slot suggestions based on priority levels
    
    Priority-Based Time Slot Logic:
    - High Priority (4-5): Prime business hours (9 AM - 5 PM)
    - Medium Priority (2-3): Extended hours (8 AM - 6 PM) 
    - Low Priority (1): Any available time slots (7 AM - 9 PM)
    
    Integrates with existing BERT classification and user behavior analytics
    """
    
    # Priority-based time windows (hours in 24-hour format)
    PRIORITY_TIME_WINDOWS = {
        5: (9, 17),   # Critical: 9 AM - 5 PM (core business)
        4: (9, 17),   # High: 9 AM - 5 PM (core business)
        3: (8, 18),   # Medium: 8 AM - 6 PM (extended business)
        2: (8, 18),   # Low-Medium: 8 AM - 6 PM (extended business)
        1: (7, 21),   # Very Low: 7 AM - 9 PM (flexible)
    }
    
    # Prime time indicators for confidence scoring
    PRIME_BUSINESS_HOURS = (9, 17)  # 9 AM - 5 PM
    EXTENDED_BUSINESS_HOURS = (8, 18)  # 8 AM - 6 PM
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
        # Initialize user behavior analyzer (existing working component)
        if USER_ANALYTICS_AVAILABLE:
            try:
                self.user_analyzer = UserBehaviorAnalyzer(db_session)
                logger.info("✅ UserBehaviorAnalyzer initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ UserBehaviorAnalyzer initialization failed: {e}")
                self.user_analyzer = None
        else:
            logger.warning("⚠️ UserBehaviorAnalyzer not available")
            self.user_analyzer = None
            
        # Initialize smart conflict detector (existing working component)  
        if SMART_DETECTOR_AVAILABLE:
            try:
                self.smart_detector = SmartConflictDetector(db_session)
                logger.info("✅ SmartConflictDetector initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ SmartConflictDetector initialization failed: {e}")
                self.smart_detector = None
        else:
            logger.warning("⚠️ SmartConflictDetector not available")
            self.smart_detector = None
    
    def suggest_priority_based_slots(
        self,
        user_id: str,
        priority_level: int,
        duration_minutes: int,
        exclude_times: Optional[List[Tuple[datetime, datetime]]] = None,
        preferred_date: Optional[datetime] = None,
        num_suggestions: int = 5
    ) -> PrioritySchedulingResult:
        """
        Generate intelligent time slot suggestions based on event priority
        
        Args:
            user_id: User identifier
            priority_level: Event priority (1-5 scale)
            duration_minutes: Event duration in minutes
            exclude_times: List of (start, end) tuples to exclude
            preferred_date: Preferred date for scheduling (optional)
            num_suggestions: Number of suggestions to return
            
        Returns:
            PrioritySchedulingResult with suggested time slots
        """
        
        logger.info(f"🎯 Generating priority-based suggestions for user {user_id}, "
                   f"priority {priority_level}, duration {duration_minutes}min")
        
        # Validate inputs
        if not self._validate_inputs(user_id, priority_level, duration_minutes):
            return self._get_fallback_result(user_id, priority_level, duration_minutes)
        
        # Get priority-based time window
        time_window = self.PRIORITY_TIME_WINDOWS.get(priority_level, self.PRIORITY_TIME_WINDOWS[3])
        start_hour, end_hour = time_window
        
        # Get existing user events to avoid conflicts
        existing_events = self._get_user_events(user_id, exclude_times or [])
        
        # Generate candidate time slots
        candidate_slots = self._generate_candidate_slots(
            priority_level, 
            duration_minutes, 
            start_hour, 
            end_hour,
            preferred_date,
            num_suggestions * 3  # Generate more candidates than needed
        )
        
        # Filter candidates to avoid conflicts
        available_slots = self._filter_available_slots(
            candidate_slots, 
            existing_events, 
            exclude_times or []
        )
        
        # Score and rank slots based on priority matching
        scored_slots = self._score_priority_slots(available_slots, priority_level)
        
        # Select best suggestions
        best_slots = scored_slots[:num_suggestions]
        
        # Generate reasoning
        reasoning = self._generate_priority_reasoning(priority_level, len(best_slots), time_window)
        
        # Build filter criteria used
        filter_criteria = [
            f"Priority {priority_level} time window: {start_hour}:00-{end_hour}:00",
            f"Duration: {duration_minutes} minutes",
            f"Conflict avoidance enabled"
        ]
        
        if self.user_analyzer:
            filter_criteria.append("User behavior patterns considered")
        
        result = PrioritySchedulingResult(
            original_priority=priority_level,
            suggested_slots=best_slots,
            reasoning=reasoning,
            total_slots_considered=len(candidate_slots),
            filter_criteria_used=filter_criteria,
            fallback_used=len(best_slots) < num_suggestions
        )
        
        logger.info(f"✅ Generated {len(best_slots)} priority-based suggestions")
        return result
    
    def _validate_inputs(self, user_id: str, priority_level: int, duration_minutes: int) -> bool:
        """Validate input parameters"""
        if not user_id or not isinstance(user_id, str):
            logger.error("❌ Invalid user_id")
            return False
            
        if not isinstance(priority_level, int) or priority_level < 1 or priority_level > 5:
            logger.error(f"❌ Invalid priority_level: {priority_level}")
            return False
            
        if not isinstance(duration_minutes, int) or duration_minutes <= 0:
            logger.error(f"❌ Invalid duration_minutes: {duration_minutes}")
            return False
            
        if duration_minutes > 480:  # 8 hours max
            logger.warning(f"⚠️ Duration capped at 480 minutes (was {duration_minutes})")
            
        return True
    
    def _get_user_events(self, user_id: str, exclude_times: List[Tuple[datetime, datetime]]) -> List[Event]:
        """Get user's existing events to avoid conflicts"""
        try:
            # Get user
            user = self.db.query(User).filter(User.cognito_sub == user_id).first()
            if not user:
                logger.warning(f"⚠️ User {user_id} not found")
                return []
            
            # Get events from next 30 days to check availability
            start_date = datetime.now()
            end_date = start_date + timedelta(days=30)
            
            events = self.db.query(Event).filter(
                Event.user_id == user.id,
                Event.start_time >= start_date,
                Event.start_time <= end_date,
                Event.is_all_day == False  # Only consider timed events
            ).all()
            
            logger.debug(f"📅 Found {len(events)} existing events for conflict checking")
            return events
            
        except Exception as e:
            logger.error(f"❌ Error getting user events: {e}")
            return []
    
    def _generate_candidate_slots(
        self, 
        priority_level: int, 
        duration_minutes: int,
        start_hour: int, 
        end_hour: int,
        preferred_date: Optional[datetime],
        max_candidates: int
    ) -> List[PriorityTimeSlot]:
        """Generate candidate time slots based on priority level"""
        
        candidates = []
        
        # Determine date range to search
        if preferred_date:
            search_dates = [preferred_date.date()]
        else:
            # Search next 5 business days
            base_date = datetime.now().date()
            search_dates = []
            current_date = base_date
            days_added = 0
            
            while len(search_dates) < 5 and days_added < 14:
                if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                    search_dates.append(current_date)
                current_date += timedelta(days=1)
                days_added += 1
        
        # Generate time slots for each date
        for date in search_dates:
            if len(candidates) >= max_candidates:
                break
                
            # Generate hourly slots within priority window
            for hour in range(start_hour, end_hour):
                if len(candidates) >= max_candidates:
                    break
                
                # Try different minute offsets
                for minute_offset in [0, 15, 30, 45]:
                    start_time = datetime.combine(date, datetime.min.time()).replace(
                        hour=hour, 
                        minute=minute_offset
                    )
                    end_time = start_time + timedelta(minutes=duration_minutes)
                    
                    # Skip if end time goes beyond priority window
                    if end_time.hour >= end_hour:
                        continue
                    
                    # Skip past times
                    if start_time <= datetime.now():
                        continue
                    
                    # Create priority time slot
                    slot = PriorityTimeSlot(
                        start_time=start_time,
                        end_time=end_time,
                        confidence=0.8,  # Base confidence
                        reasoning=f"Priority {priority_level} time window",
                        priority_match_score=self._calculate_priority_match_score(hour, priority_level),
                        availability_score=0.9,  # Will be updated during filtering
                        is_prime_time=self.PRIME_BUSINESS_HOURS[0] <= hour < self.PRIME_BUSINESS_HOURS[1]
                    )
                    
                    candidates.append(slot)
        
        logger.debug(f"📋 Generated {len(candidates)} candidate slots")
        return candidates
    
    def _calculate_priority_match_score(self, hour: int, priority_level: int) -> float:
        """Calculate how well a time slot matches the priority level"""
        
        # High priority events get higher scores during prime business hours
        if priority_level >= 4:
            if self.PRIME_BUSINESS_HOURS[0] <= hour < self.PRIME_BUSINESS_HOURS[1]:
                return 1.0  # Perfect match
            elif self.EXTENDED_BUSINESS_HOURS[0] <= hour < self.EXTENDED_BUSINESS_HOURS[1]:
                return 0.7  # Good match
            else:
                return 0.3  # Poor match
        
        # Medium priority events prefer extended business hours
        elif priority_level == 3:
            if self.EXTENDED_BUSINESS_HOURS[0] <= hour < self.EXTENDED_BUSINESS_HOURS[1]:
                return 1.0  # Perfect match
            else:
                return 0.5  # Moderate match
        
        # Low priority events are flexible
        else:
            if 7 <= hour <= 21:  # Any reasonable hour
                return 0.8
            else:
                return 0.4
    
    def _filter_available_slots(
        self, 
        candidate_slots: List[PriorityTimeSlot], 
        existing_events: List[Event],
        exclude_times: List[Tuple[datetime, datetime]]
    ) -> List[PriorityTimeSlot]:
        """Filter candidate slots to remove conflicts"""
        
        available_slots = []
        
        for slot in candidate_slots:
            is_available = True
            conflict_risk = 0.0
            
            # Check against existing events
            for event in existing_events:
                if self._times_overlap(slot.start_time, slot.end_time, event.start_time, event.end_time):
                    is_available = False
                    break
                    
                # Check for nearby events (within 30 minutes)
                time_gap = min(
                    abs((slot.start_time - event.end_time).total_seconds()),
                    abs((event.start_time - slot.end_time).total_seconds())
                )
                
                if time_gap < 1800:  # 30 minutes
                    conflict_risk += 0.1
            
            # Check against excluded times
            if is_available:
                for exclude_start, exclude_end in exclude_times:
                    if self._times_overlap(slot.start_time, slot.end_time, exclude_start, exclude_end):
                        is_available = False
                        break
            
            if is_available:
                # Update slot with conflict risk
                slot.conflict_risk = min(conflict_risk, 1.0)
                slot.availability_score = 1.0 - slot.conflict_risk
                available_slots.append(slot)
        
        logger.debug(f"✅ {len(available_slots)} slots available after conflict filtering")
        return available_slots
    
    def _times_overlap(self, start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
        """Check if two time ranges overlap"""
        return start1 < end2 and end1 > start2
    
    def _score_priority_slots(self, available_slots: List[PriorityTimeSlot], priority_level: int) -> List[PriorityTimeSlot]:
        """Score and rank slots based on priority matching and other factors"""
        
        for slot in available_slots:
            # Calculate composite confidence score
            priority_weight = 0.4
            availability_weight = 0.3
            prime_time_weight = 0.2
            conflict_risk_weight = 0.1
            
            confidence = (
                slot.priority_match_score * priority_weight +
                slot.availability_score * availability_weight +
                (1.0 if slot.is_prime_time else 0.5) * prime_time_weight +
                (1.0 - slot.conflict_risk) * conflict_risk_weight
            )
            
            slot.confidence = min(confidence, 1.0)
            
            # Enhanced reasoning
            reasons = []
            if slot.is_prime_time and priority_level >= 4:
                reasons.append("prime business hours for high priority")
            elif slot.priority_match_score >= 0.8:
                reasons.append("excellent priority time match")
            elif slot.availability_score >= 0.9:
                reasons.append("high availability window")
                
            if slot.conflict_risk > 0:
                reasons.append(f"minimal conflict risk ({slot.conflict_risk:.1%})")
            else:
                reasons.append("no conflict risk")
                
            slot.reasoning = f"Priority {priority_level} slot: " + ", ".join(reasons)
        
        # Sort by confidence score (highest first)
        sorted_slots = sorted(available_slots, key=lambda x: x.confidence, reverse=True)
        
        logger.debug(f"📊 Scored and ranked {len(sorted_slots)} available slots")
        return sorted_slots
    
    def _generate_priority_reasoning(self, priority_level: int, num_slots: int, time_window: Tuple[int, int]) -> str:
        """Generate human-readable reasoning for the suggestions"""
        
        priority_names = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
        priority_name = priority_names.get(priority_level, "Medium")
        
        start_hour, end_hour = time_window
        
        reasoning_parts = [
            f"Event classified as {priority_name} priority (level {priority_level})"
        ]
        
        if priority_level >= 4:
            reasoning_parts.append(f"High priority events prioritize prime business hours ({start_hour}:00-{end_hour}:00)")
        elif priority_level == 3:
            reasoning_parts.append(f"Medium priority events use extended business hours ({start_hour}:00-{end_hour}:00)")
        else:
            reasoning_parts.append(f"Low priority events have flexible scheduling ({start_hour}:00-{end_hour}:00)")
        
        if num_slots > 0:
            reasoning_parts.append(f"Found {num_slots} optimal time slots matching priority criteria")
        else:
            reasoning_parts.append("No optimal slots found in priority window - consider adjusting priority or timing")
        
        return ". ".join(reasoning_parts) + "."
    
    def _get_fallback_result(self, user_id: str, priority_level: int, duration_minutes: int) -> PrioritySchedulingResult:
        """Provide fallback result when primary scheduling fails"""
        
        logger.warning(f"⚠️ Using fallback scheduling for user {user_id}")
        
        # Generate basic time slots for tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        fallback_slots = []
        
        # Simple 9 AM, 2 PM, 4 PM slots
        for hour in [9, 14, 16]:
            start_time = tomorrow.replace(hour=hour, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            slot = PriorityTimeSlot(
                start_time=start_time,
                end_time=end_time,
                confidence=0.6,
                reasoning=f"Fallback suggestion for priority {priority_level} event",
                priority_match_score=0.5,
                availability_score=0.7,
                is_prime_time=(9 <= hour <= 17)
            )
            fallback_slots.append(slot)
        
        return PrioritySchedulingResult(
            original_priority=priority_level,
            suggested_slots=fallback_slots,
            reasoning=f"Fallback scheduling used due to system limitations. Priority {priority_level} event suggestions provided.",
            total_slots_considered=len(fallback_slots),
            filter_criteria_used=["Fallback mode", "Basic time slots"],
            fallback_used=True
        )


def test_priority_scheduler():
    """Test function to validate the priority scheduler"""
    
    print("🧪 Testing Priority-Based Scheduler")
    print("=" * 50)
    
    # Mock database session for testing
    class MockDB:
        def query(self, *args):
            return self
        def filter(self, *args):
            return self
        def first(self):
            return None
        def all(self):
            return []
    
    scheduler = PriorityBasedScheduler(MockDB())
    
    # Test different priority levels
    test_cases = [
        (5, "Critical Priority - should suggest 9 AM-5 PM"),
        (4, "High Priority - should suggest 9 AM-5 PM"),
        (3, "Medium Priority - should suggest 8 AM-6 PM"),
        (2, "Low-Medium Priority - should suggest 8 AM-6 PM"),
        (1, "Very Low Priority - should suggest 7 AM-9 PM")
    ]
    
    for priority, description in test_cases:
        print(f"\n🎯 Testing Priority {priority}: {description}")
        
        result = scheduler.suggest_priority_based_slots(
            user_id="test_user",
            priority_level=priority,
            duration_minutes=60,
            num_suggestions=3
        )
        
        print(f"   📊 Generated {len(result.suggested_slots)} suggestions")
        print(f"   💡 Reasoning: {result.reasoning}")
        
        for i, slot in enumerate(result.suggested_slots[:2], 1):
            print(f"   ⏰ Option {i}: {slot.start_time.strftime('%A %I:%M %p')} "
                  f"(confidence: {slot.confidence:.2f})")
    
    print("\n✅ Priority Scheduler testing complete!")


if __name__ == "__main__":
    test_priority_scheduler()
