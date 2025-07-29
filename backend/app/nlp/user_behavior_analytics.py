# backend/app/nlp/user_behavior_analytics.py
"""
Enhanced User Behavior Analytics Engine for KairoCal
Analyzes user scheduling patterns and provides intelligent time slot suggestions
WITH CRITICAL EDGE CASES HANDLED
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import numpy as np
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.user import User


@dataclass
class UserPattern:
    """Data class for user scheduling patterns"""
    user_id: str
    preferred_hours: List[int]  # Hours of day (0-23)
    preferred_days: List[int]   # Days of week (0-6, Monday=0)
    avg_meeting_duration: int   # Minutes
    common_locations: List[str]
    event_types: Dict[str, int]  # Event type -> frequency
    productivity_score: float   # 0-100
    focus_blocks: List[Tuple[int, int]]  # (start_hour, end_hour) pairs


@dataclass
class TimeSlotSuggestion:
    """Data class for time slot suggestions"""
    start_time: datetime
    end_time: datetime
    confidence_score: float  # 0-1
    reason: str
    conflict_probability: float  # 0-1


class SyntheticDataGenerator:
    """Generates realistic synthetic user behavior data"""
    
    EVENT_TYPES = [
        "meeting", "appointment", "call", "presentation", "workshop",
        "training", "lunch", "break", "focus_time", "review"
    ]
    
    LOCATIONS = [
        "Office", "Home", "Conference Room A", "Conference Room B",
        "Online", "Client Site", "Café", "Co-working Space"
    ]
    
    USER_ARCHETYPES = {
        "early_bird": {
            "preferred_hours": [7, 8, 9, 10, 11],
            "productivity_peak": (8, 12),
            "meeting_preference": "morning"
        },
        "night_owl": {
            "preferred_hours": [14, 15, 16, 17, 18, 19],
            "productivity_peak": (15, 19),
            "meeting_preference": "afternoon"
        },
        "balanced": {
            "preferred_hours": [9, 10, 11, 14, 15, 16],
            "productivity_peak": (10, 16),
            "meeting_preference": "mixed"
        }
    }
    
    def generate_user_patterns(self, num_users: int = 10) -> List[UserPattern]:
        """Generate synthetic user patterns for testing"""
        patterns = []
        
        for i in range(num_users):
            archetype_name = random.choice(list(self.USER_ARCHETYPES.keys()))
            archetype = self.USER_ARCHETYPES[archetype_name]
            
            # Generate base pattern
            preferred_hours = archetype["preferred_hours"] + random.choices(
                range(24), k=random.randint(2, 4)
            )
            preferred_hours = sorted(list(set(preferred_hours)))
            
            # Work days preference (slight weekend variation)
            if random.random() < 0.8:  # 80% prefer weekdays
                preferred_days = [0, 1, 2, 3, 4]  # Mon-Fri
            else:
                preferred_days = list(range(7))  # All days
            
            # Meeting duration based on role
            if "senior" in archetype_name or random.random() < 0.3:
                avg_duration = random.randint(45, 90)  # Senior roles, longer meetings
            else:
                avg_duration = random.randint(30, 60)
            
            # Common locations
            num_locations = random.randint(2, 5)
            common_locations = random.sample(self.LOCATIONS, num_locations)
            
            # Event types with realistic distribution
            event_types = {}
            for event_type in random.sample(self.EVENT_TYPES, random.randint(4, 7)):
                if event_type == "meeting":
                    event_types[event_type] = random.randint(20, 40)  # Most common
                elif event_type in ["call", "appointment"]:
                    event_types[event_type] = random.randint(10, 25)
                else:
                    event_types[event_type] = random.randint(1, 15)
            
            # Productivity score (influenced by archetype)
            base_score = 70
            if archetype_name == "early_bird":
                base_score += random.randint(5, 15)
            elif archetype_name == "balanced":
                base_score += random.randint(0, 10)
            productivity_score = min(100, base_score + random.randint(-10, 10))
            
            # Focus blocks
            peak_start, peak_end = archetype["productivity_peak"]
            focus_blocks = [(peak_start, peak_end)]
            if random.random() < 0.6:  # 60% have a second focus block
                second_start = random.randint(13, 17)
                focus_blocks.append((second_start, second_start + 2))
            
            pattern = UserPattern(
                user_id=f"user_{i+1}",
                preferred_hours=preferred_hours,
                preferred_days=preferred_days,
                avg_meeting_duration=avg_duration,
                common_locations=common_locations,
                event_types=event_types,
                productivity_score=productivity_score,
                focus_blocks=focus_blocks
            )
            patterns.append(pattern)
        
        return patterns
    
    def generate_historical_events(self, user_pattern: UserPattern, days_back: int = 90) -> List[Dict]:
        """Generate historical events for a user based on their pattern"""
        events = []
        start_date = datetime.now() - timedelta(days=days_back)
        
        for day in range(days_back):
            current_date = start_date + timedelta(days=day)
            
            # Skip if not a preferred day (with some randomness)
            if (current_date.weekday() not in user_pattern.preferred_days and 
                random.random() > 0.2):
                continue
            
            # Number of events per day (realistic distribution)
            if current_date.weekday() < 5:  # Weekday
                num_events = random.choices([0, 1, 2, 3, 4, 5, 6], 
                                          weights=[5, 10, 20, 25, 20, 15, 5])[0]
            else:  # Weekend
                num_events = random.choices([0, 1, 2], weights=[40, 40, 20])[0]
            
            scheduled_hours = set()
            
            for _ in range(num_events):
                # Choose event type based on user preferences
                event_type = random.choices(
                    list(user_pattern.event_types.keys()),
                    weights=list(user_pattern.event_types.values())
                )[0]
                
                # Choose time slot based on preferences
                available_hours = [h for h in user_pattern.preferred_hours 
                                 if h not in scheduled_hours and h < 20]
                
                if not available_hours:
                    available_hours = [h for h in range(8, 20) 
                                     if h not in scheduled_hours]
                
                if not available_hours:
                    continue
                
                start_hour = random.choice(available_hours)
                
                # Duration based on event type and user pattern
                if event_type in ["lunch", "break"]:
                    duration = random.randint(30, 60)
                elif event_type == "presentation":
                    duration = random.randint(45, 120)
                else:
                    duration = user_pattern.avg_meeting_duration + random.randint(-15, 15)
                
                start_time = current_date.replace(
                    hour=start_hour, 
                    minute=random.choice([0, 15, 30, 45])
                )
                end_time = start_time + timedelta(minutes=duration)
                
                # Mark hours as scheduled
                for h in range(start_hour, min(start_hour + (duration // 60) + 1, 24)):
                    scheduled_hours.add(h)
                
                # Choose location
                location = random.choice(user_pattern.common_locations)
                
                event = {
                    "title": f"{event_type.title()} - {random.randint(1, 999)}",
                    "start_time": start_time,
                    "end_time": end_time,
                    "location": location,
                    "event_type": event_type,
                    "duration_minutes": duration
                }
                events.append(event)
        
        return events


class UserBehaviorAnalyzer:
    """Enhanced analyzer with robust edge case handling"""
    
    def __init__(self, db: Session):
        self.db = db
        self.synthetic_generator = SyntheticDataGenerator()
    
    def _validate_inputs(self, user_id: str, event_duration: int) -> Tuple[bool, str]:
        """Validate inputs and return (is_valid, error_message)"""
        if not user_id or not isinstance(user_id, str):
            return False, "Invalid user_id: must be non-empty string"
        
        if not isinstance(event_duration, int):
            return False, "Invalid duration: must be integer"
            
        if event_duration <= 0:
            return False, "Invalid duration: must be positive"
            
        # Don't reject large durations here – they will be capped later
        # if event_duration > 480:  # 8 hours max
        #     return False, "Invalid duration: maximum 8 hours (480 minutes)"
            
        return True, ""
    
    def analyze_user_patterns(self, user_id: str, use_synthetic: bool = True) -> UserPattern:
        """Analyze a user's scheduling patterns with enhanced validation"""
        
        if use_synthetic:
            # For development: use synthetic data
            patterns = self.synthetic_generator.generate_user_patterns(1)
            pattern = patterns[0]
            pattern.user_id = user_id
            
            # Enhanced pattern validation
            pattern = self._validate_and_fix_pattern(pattern)
            return pattern
        
        # Real implementation for production
        events = self.db.query(Event).filter(
            Event.user_id == user_id,
            Event.start_time >= datetime.now() - timedelta(days=90)
        ).all()
        
        if not events:
            # Return default pattern for new users
            return self._get_default_pattern(user_id)
        
        return self._analyze_events(user_id, events)
    
    def _validate_and_fix_pattern(self, pattern: UserPattern) -> UserPattern:
        """Validate and fix user pattern edge cases"""
        
        # Ensure reasonable hours (6 AM - 10 PM)
        reasonable_hours = [h for h in pattern.preferred_hours if 6 <= h <= 22]
        if not reasonable_hours:
            reasonable_hours = [9, 10, 11, 14, 15, 16]  # Default business hours
        pattern.preferred_hours = reasonable_hours
        
        # Ensure weekdays are included
        if not any(day < 5 for day in pattern.preferred_days):
            pattern.preferred_days = [0, 1, 2, 3, 4]  # Add weekdays
        
        # Validate focus blocks
        valid_focus_blocks = []
        for start, end in pattern.focus_blocks:
            if 6 <= start < end <= 22 and (end - start) >= 1:
                valid_focus_blocks.append((start, end))
        
        if not valid_focus_blocks:
            valid_focus_blocks = [(9, 11), (14, 16)]  # Default focus blocks
        pattern.focus_blocks = valid_focus_blocks
        
        # Ensure reasonable meeting duration
        if pattern.avg_meeting_duration < 15:
            pattern.avg_meeting_duration = 30
        elif pattern.avg_meeting_duration > 240:
            pattern.avg_meeting_duration = 90
            
        return pattern
    
    def _analyze_events(self, user_id: str, events: List[Event]) -> UserPattern:
        """Analyze real events to extract patterns with validation"""
        
        # Extract patterns from real events
        hour_counter = Counter()
        day_counter = Counter()
        duration_list = []
        location_counter = Counter()
        
        for event in events:
            hour_counter[event.start_time.hour] += 1
            day_counter[event.start_time.weekday()] += 1
            
            duration = (event.end_time - event.start_time).total_seconds() / 60
            if 15 <= duration <= 480:  # Only count reasonable durations
                duration_list.append(duration)
            
            if event.location:
                location_counter[event.location] += 1
        
        # Extract preferred hours (top 60% of activity, but only reasonable hours)
        total_events = len(events)
        all_preferred = [hour for hour, count in hour_counter.most_common() 
                        if count >= max(1, total_events * 0.1)]
        preferred_hours = [h for h in all_preferred if 6 <= h <= 22][:8]
        
        if not preferred_hours:
            preferred_hours = [9, 10, 11, 14, 15, 16]
        
        # Extract preferred days
        preferred_days = [day for day, count in day_counter.most_common()[:5]]
        if not preferred_days:
            preferred_days = [0, 1, 2, 3, 4]  # Default to weekdays
        
        # Calculate average duration
        avg_duration = int(np.mean(duration_list)) if duration_list else 60
        avg_duration = max(15, min(240, avg_duration))  # Bound between 15min-4hrs
        
        # Extract common locations
        common_locations = [loc for loc, _ in location_counter.most_common(5)]
        if not common_locations:
            common_locations = ["Office", "Online"]
        
        # Simple event type classification
        event_types = {"meeting": len(events)}
        
        # Calculate productivity score
        productivity_score = min(100, max(0, 70 + random.randint(-10, 20)))
        
        # Identify focus blocks
        focus_blocks = self._identify_focus_blocks(preferred_hours)
        
        pattern = UserPattern(
            user_id=user_id,
            preferred_hours=sorted(preferred_hours),
            preferred_days=sorted(preferred_days),
            avg_meeting_duration=avg_duration,
            common_locations=common_locations,
            event_types=event_types,
            productivity_score=productivity_score,
            focus_blocks=focus_blocks
        )
        
        return self._validate_and_fix_pattern(pattern)
    
    def _identify_focus_blocks(self, preferred_hours: List[int]) -> List[Tuple[int, int]]:
        """Identify continuous focus time blocks with validation"""
        if not preferred_hours:
            return [(9, 11), (14, 16)]  # Default focus blocks
        
        blocks = []
        current_block_start = None
        sorted_hours = sorted(preferred_hours)
        
        for i, hour in enumerate(sorted_hours):
            if current_block_start is None:
                current_block_start = hour
            elif hour - sorted_hours[i-1] > 1:  # Gap found
                if sorted_hours[i-1] + 1 > current_block_start:  # Valid block
                    blocks.append((current_block_start, sorted_hours[i-1] + 1))
                current_block_start = hour
        
        # Add the last block
        if current_block_start is not None and sorted_hours[-1] + 1 > current_block_start:
            blocks.append((current_block_start, sorted_hours[-1] + 1))
        
        # Ensure we have at least one focus block
        if not blocks:
            blocks = [(9, 11), (14, 16)]
        
        return blocks[:2]  # Return top 2 focus blocks
    
    def _get_default_pattern(self, user_id: str) -> UserPattern:
        """Return default pattern for new users"""
        return UserPattern(
            user_id=user_id,
            preferred_hours=[9, 10, 11, 14, 15, 16],
            preferred_days=[0, 1, 2, 3, 4],  # Weekdays
            avg_meeting_duration=60,
            common_locations=["Office", "Online"],
            event_types={"meeting": 10, "call": 5},
            productivity_score=75,
            focus_blocks=[(9, 11), (14, 16)]
        )
    
    def suggest_optimal_time_slots(
        self, 
        user_id: str, 
        event_duration: int,
        preferred_date: Optional[datetime] = None,
        num_suggestions: int = 5
    ) -> List[TimeSlotSuggestion]:
        """Enhanced time slot suggestions with comprehensive edge case handling"""
        
        # Input validation
        is_valid, error_msg = self._validate_inputs(user_id, event_duration)
        if not is_valid:
            return []  # Return empty list for invalid inputs
        
        # Bound event duration to reasonable limits
        original_duration = event_duration
        event_duration = max(15, min(480, event_duration))
        # If duration was capped, ensure we still return suggestions
        if original_duration > 480 and event_duration == 480:
          # Duration was capped, continue with processing
          pass
        try:
            pattern = self.analyze_user_patterns(user_id)
        except Exception:
            # Fallback to default pattern if analysis fails
            pattern = self._get_default_pattern(user_id)
        
        suggestions = []
        
        # Start from preferred date or next business day
        start_date = self._get_next_business_day(preferred_date)
        
        # Look ahead for the next 14 days (increased from 7)
        for day_offset in range(14):
            check_date = start_date + timedelta(days=day_offset)
            day_suggestions = self._generate_day_suggestions(pattern, check_date, event_duration)
            suggestions.extend(day_suggestions)
            
            # Stop if we have enough good suggestions
            if len(suggestions) >= num_suggestions * 2:
                break
        
        # Sort by confidence score and return top suggestions
        suggestions.sort(key=lambda x: x.confidence_score, reverse=True)
        
        # If no suggestions found, provide fallback
        if not suggestions:
            suggestions = self._get_fallback_suggestions(user_id, event_duration, start_date)
        
        return suggestions[:num_suggestions]
    
    def _get_next_business_day(self, preferred_date: Optional[datetime]) -> datetime:
        """Get next appropriate business day"""
        if preferred_date:
            base_date = preferred_date
        else:
            base_date = datetime.now() + timedelta(days=1)
        
        # If it's weekend, move to Monday
        while base_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            base_date += timedelta(days=1)
            
        return base_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def _generate_day_suggestions(self, pattern: UserPattern, check_date: datetime, event_duration: int) -> List[TimeSlotSuggestion]:
        """Generate suggestions for a specific day"""
        day_suggestions = []
        
        # Skip if not a preferred day (with some flexibility)
        day_preference_score = 1.0 if check_date.weekday() in pattern.preferred_days else 0.3
        if day_preference_score < 0.5 and random.random() > 0.3:
            return []
        
        # Check each preferred hour
        for hour in pattern.preferred_hours:
            # Skip unreasonable hours for the event duration
            if hour < 7 or hour > 20 or (hour + (event_duration // 60)) > 22:
                continue
                
            slot_start = check_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            slot_end = slot_start + timedelta(minutes=event_duration)
            
            # Enhanced conflict checking
            conflict_prob = self._estimate_conflict_probability_enhanced(pattern.user_id, slot_start, slot_end)
            
            # Skip high-conflict slots
            if conflict_prob > 0.8:
                continue
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score_enhanced(pattern, slot_start, hour, day_preference_score)
            
            # Generate reason
            reason = self._generate_suggestion_reason_enhanced(pattern, hour, check_date, confidence)
            
            suggestion = TimeSlotSuggestion(
                start_time=slot_start,
                end_time=slot_end,
                confidence_score=confidence,
                reason=reason,
                conflict_probability=conflict_prob
            )
            
            day_suggestions.append(suggestion)
        
        return day_suggestions
    
    def _estimate_conflict_probability_enhanced(self, user_id: str, start_time: datetime, end_time: datetime) -> float:
        """Enhanced conflict probability estimation with buffer time"""
        try:
            # Check for existing events with 15-minute buffer
            buffer_minutes = 15
            buffer_start = start_time - timedelta(minutes=buffer_minutes)
            buffer_end = end_time + timedelta(minutes=buffer_minutes)
            
            existing_events = self.db.query(Event).filter(
                Event.user_id == user_id,
                Event.start_time < buffer_end,
                Event.end_time > buffer_start
            ).count()
            
            if existing_events > 0:
                return 0.95  # High probability with buffer consideration
            
            # Check for back-to-back meetings (exact time matches)
            exact_conflicts = self.db.query(Event).filter(
                Event.user_id == user_id,
                Event.start_time < end_time,
                Event.end_time > start_time
            ).count()
            
            if exact_conflicts > 0:
                return 1.0  # Definite conflict
            
        except Exception:
            # If database query fails, use heuristic
            pass
        
        # Estimate based on typical usage patterns
        hour = start_time.hour
        weekday = start_time.weekday()
        
        # Higher probability during peak business hours
        if 9 <= hour <= 17 and weekday < 5:
            if 10 <= hour <= 16:  # Peak hours
                return 0.4
            else:
                return 0.25
        elif weekday < 5:
            return 0.15
        else:
            return 0.05
    
    def _calculate_confidence_score_enhanced(self, pattern: UserPattern, slot_start: datetime, hour: int, day_preference_score: float) -> float:
        """Enhanced confidence scoring with multiple factors"""
        score = 0.3  # Base score
        
        # Day preference factor
        score += day_preference_score * 0.2
        
        # Hour preference factor
        if hour in pattern.preferred_hours:
            hour_rank = pattern.preferred_hours.index(hour)
            hour_factor = 1 - (hour_rank / len(pattern.preferred_hours))
            score += hour_factor * 0.3
        
        # Focus block factor
        for focus_start, focus_end in pattern.focus_blocks:
            if focus_start <= hour < focus_end:
                score += 0.25
                break
        
        # Productivity score influence
        score += (pattern.productivity_score / 100) * 0.15
        
        # Time of day factor (prefer reasonable business hours)
        if 9 <= hour <= 17:
            score += 0.1
        elif 8 <= hour <= 18:
            score += 0.05
        
        return min(1.0, max(0.1, score))
    
    def _generate_suggestion_reason_enhanced(self, pattern: UserPattern, hour: int, date: datetime, confidence: float) -> str:
        """Generate detailed human-readable reason for the suggestion"""
        reasons = []
        
        if hour in pattern.preferred_hours:
            rank = pattern.preferred_hours.index(hour) + 1
            if rank <= 3:
                reasons.append("matches your top preferred meeting times")
            else:
                reasons.append("aligns with your usual meeting schedule")
        
        for focus_start, focus_end in pattern.focus_blocks:
            if focus_start <= hour < focus_end:
                reasons.append("falls within your productive focus hours")
                break
        
        if date.weekday() in pattern.preferred_days:
            if date.weekday() < 5:
                reasons.append("scheduled on a preferred weekday")
        
        if confidence > 0.8:
            reasons.append("has high scheduling confidence")
        elif confidence > 0.6:
            reasons.append("offers good scheduling potential")
        
        if 9 <= hour <= 12:
            reasons.append("scheduled during optimal morning hours")
        elif 14 <= hour <= 17:
            reasons.append("scheduled during productive afternoon hours")
        
        if not reasons:
            reasons.append("represents an available time slot")
        
        # Create natural language reason
        if len(reasons) == 1:
            return f"This time {reasons[0]}."
        elif len(reasons) == 2:
            return f"This time {reasons[0]} and {reasons[1]}."
        else:
            return f"This time {', '.join(reasons[:-1])}, and {reasons[-1]}."
    
    def _get_fallback_suggestions(self, user_id: str, event_duration: int, start_date: datetime) -> List[TimeSlotSuggestion]:
        """Provide fallback suggestions when no optimal slots found"""
        fallback_suggestions = []
        
        # Default business hours
        default_hours = [9, 10, 11, 14, 15, 16]
        
        for day_offset in range(5):  # Next 5 business days
            check_date = start_date + timedelta(days=day_offset)
            
            # Skip weekends
            if check_date.weekday() >= 5:
                continue
            
            for hour in default_hours:
                if hour + (event_duration // 60) > 18:  # Don't go past 6 PM
                    continue
                    
                slot_start = check_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                slot_end = slot_start + timedelta(minutes=event_duration)
                
                suggestion = TimeSlotSuggestion(
                    start_time=slot_start,
                    end_time=slot_end,
                    confidence_score=0.5,  # Medium confidence for fallback
                    reason="This is a standard business hour time slot.",
                    conflict_probability=0.3
                )
                
                fallback_suggestions.append(suggestion)
                
                if len(fallback_suggestions) >= 5:
                    break
            
            if len(fallback_suggestions) >= 5:
                break
        
        return fallback_suggestions


# API Integration Service (unchanged but with better error handling)
class BehaviorAnalyticsService:
    """Service class for integrating behavior analytics with the API"""
    
    def __init__(self, db: Session):
        self.analyzer = UserBehaviorAnalyzer(db)
    
    def get_user_insights(self, user_id: str) -> Dict:
        """Get user behavior insights for the dashboard with error handling"""
        try:
            pattern = self.analyzer.analyze_user_patterns(user_id)
            
            return {
                "user_id": user_id,
                "insights": {
                    "preferred_meeting_hours": pattern.preferred_hours,
                    "most_productive_days": [self._day_name(d) for d in pattern.preferred_days[:3]],
                    "average_meeting_duration": f"{pattern.avg_meeting_duration} minutes",
                    "productivity_score": f"{pattern.productivity_score:.0f}/100",
                    "top_locations": pattern.common_locations[:3],
                    "focus_blocks": [
                        f"{start}:00 - {end}:00" for start, end in pattern.focus_blocks
                    ]
                },
                "recommendations": {
                    "optimal_meeting_times": [f"{h}:00" for h in pattern.preferred_hours[:3]],
                    "avoid_scheduling_during": "12:00-13:00 (lunch break)",
                    "best_days_for_important_meetings": [
                        self._day_name(d) for d in pattern.preferred_days[:2]
                    ]
                }
            }
        except Exception as e:
            # Return default insights on error
            return {
                "user_id": user_id,
                "insights": {
                    "preferred_meeting_hours": [9, 10, 11, 14, 15, 16],
                    "most_productive_days": ["Monday", "Tuesday", "Wednesday"],
                    "average_meeting_duration": "60 minutes",
                    "productivity_score": "75/100",
                    "top_locations": ["Office", "Online"],
                    "focus_blocks": ["9:00 - 11:00", "14:00 - 16:00"]
                },
                "recommendations": {
                    "optimal_meeting_times": ["10:00", "14:00", "15:00"],
                    "avoid_scheduling_during": "12:00-13:00 (lunch break)",
                    "best_days_for_important_meetings": ["Monday", "Tuesday"]
                },
                "error": f"Using default insights due to: {str(e)}"
            }
    
    def suggest_meeting_times(
        self, 
        user_id: str, 
        duration_minutes: int,
        preferred_date: Optional[str] = None
    ) -> Dict:
        """Get smart meeting time suggestions with enhanced error handling"""
        
        preferred_dt = None
        if preferred_date:
            try:
                preferred_dt = datetime.fromisoformat(preferred_date)
            except ValueError:
                # Invalid date format, ignore and use default
                pass
        
        try:
            suggestions = self.analyzer.suggest_optimal_time_slots(
                user_id=user_id,
                event_duration=duration_minutes,
                preferred_date=preferred_dt,
                num_suggestions=5
            )
            
            return {
                "user_id": user_id,
                "requested_duration": duration_minutes,
                "suggestions": [
                    {
                        "start_time": s.start_time.isoformat(),
                        "end_time": s.end_time.isoformat(),
                        "confidence_score": round(s.confidence_score, 2),
                        "reason": s.reason,
                        "conflict_risk": "Low" if s.conflict_probability < 0.2 else 
                                       "Medium" if s.conflict_probability < 0.6 else "High"
                    }
                    for s in suggestions
                ]
            }
        except Exception as e:
            # Return basic fallback suggestions
            tomorrow = datetime.now() + timedelta(days=1)
            fallback_suggestions = []
            
            for hour in [9, 10, 11, 14, 15]:
                start_time = tomorrow.replace(hour=hour, minute=0, second=0, microsecond=0)
                end_time = start_time + timedelta(minutes=duration_minutes)
                
                fallback_suggestions.append({
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "confidence_score": 0.5,
                    "reason": "Standard business hour time slot (fallback mode)",
                    "conflict_risk": "Medium"
                })
            
            return {
                "user_id": user_id,
                "requested_duration": duration_minutes,
                "suggestions": fallback_suggestions,
                "error": f"Using fallback suggestions due to: {str(e)}"
            }
    
    def _day_name(self, day_num: int) -> str:
        """Convert day number to name"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                "Friday", "Saturday", "Sunday"]
        return days[day_num] if 0 <= day_num < 7 else "Unknown"


# Standalone test function
def test_behavior_analytics():
    """Test function to demonstrate the enhanced behavior analytics system"""
    print("🧠 Testing Enhanced KairoCal User Behavior Analytics System")
    print("=" * 60)
    
    # Generate synthetic data
    generator = SyntheticDataGenerator()
    patterns = generator.generate_user_patterns(3)
    
    print("\n📊 Generated User Patterns:")
    for i, pattern in enumerate(patterns):
        print(f"\nUser {i+1} ({pattern.user_id}):")
        print(f"  Preferred Hours: {pattern.preferred_hours}")
        print(f"  Productivity Score: {pattern.productivity_score}")
        print(f"  Common Locations: {pattern.common_locations}")
        print(f"  Focus Blocks: {pattern.focus_blocks}")
    
    # Generate historical events
    print(f"\n📅 Sample Historical Events for {patterns[0].user_id}:")
    events = generator.generate_historical_events(patterns[0], days_back=30)
    for event in events[:5]:  # Show first 5 events
        print(f"  {event['start_time'].strftime('%Y-%m-%d %H:%M')} - {event['title']}")
    
    print(f"\nTotal events generated: {len(events)}")
    
    # Test analytics (mock database session)
    class MockDB:
        def query(self, *args):
            return self
        def filter(self, *args):
            return self
        def all(self):
            return []
        def count(self):
            return 0
    
    analyzer = UserBehaviorAnalyzer(MockDB())
    
    # Test edge cases
    print(f"\n🧪 Testing Edge Cases:")
    
    # Test invalid durations
    print("Testing invalid duration (0 minutes):")
    suggestions = analyzer.suggest_optimal_time_slots("test_user", 0)
    print(f"  Result: {len(suggestions)} suggestions (should be 0)")
    
    print("Testing invalid duration (negative):")
    suggestions = analyzer.suggest_optimal_time_slots("test_user", -30)
    print(f"  Result: {len(suggestions)} suggestions (should be 0)")
    
    print("Testing very long duration (600 minutes):")
    suggestions = analyzer.suggest_optimal_time_slots("test_user", 600)
    print(f"  Result: {len(suggestions)} suggestions (duration capped to 480)")
    
    # Test normal suggestions
    print(f"\n💡 Smart Time Slot Suggestions for {patterns[0].user_id}:")
    suggestions = analyzer.suggest_optimal_time_slots(
        user_id=patterns[0].user_id,
        event_duration=60
    )
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n  Option {i}:")
        print(f"    Time: {suggestion.start_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"    Confidence: {suggestion.confidence_score:.2f}")
        print(f"    Reason: {suggestion.reason}")
        print(f"    Conflict Risk: {suggestion.conflict_probability:.2f}")
    
    print("\n✅ Enhanced User Behavior Analytics System Test Complete!")


if __name__ == "__main__":
    test_behavior_analytics()