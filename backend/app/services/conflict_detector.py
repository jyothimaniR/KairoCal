# backend/app/services/conflict_detector.py
"""
Smart Conflict Detection with BERT-powered Priority Classification
Enhanced version integrating advanced BERT priority inference
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import json

# Import the new BERT classifier
try:
    from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False
    
# Remove the ConflictAnalytics import that was causing the error
# try:
#     from app.nlp.user_behavior_analytics import UserBehaviorAnalyzer
#     USER_ANALYTICS_AVAILABLE = True
# except ImportError:
#     USER_ANALYTICS_AVAILABLE = False

logger = logging.getLogger(__name__)

class ConflictType(Enum):
    """Types of calendar conflicts"""
    TIME_OVERLAP = "time_overlap"
    LOCATION_CONFLICT = "location_conflict"
    PRIORITY_CONFLICT = "priority_conflict"
    BUFFER_VIOLATION = "buffer_violation"
    PRODUCTIVITY_IMPACT = "productivity_impact"

class ConflictSeverity(Enum):
    """Severity levels for conflicts"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ConflictDetection:
    """Represents a detected scheduling conflict"""
    conflict_type: ConflictType
    severity: ConflictSeverity
    existing_event_id: str
    new_event_data: Dict[str, Any]
    impact_score: float
    description: str
    suggested_resolutions: List[str]
    confidence: float = 0.0

class SmartConflictDetector:
    """
    Enhanced Smart Conflict Detection with BERT-powered Priority Classification
    
    Features:
    - BERT-based priority inference with confidence scoring
    - Multi-dimensional conflict detection
    - User behavior pattern integration
    - Intelligent resolution suggestions
    - Performance analytics
    """
    
    def __init__(self, db_session=None, bert_model_path: str = None):
        self.db = db_session
        
        # Initialize BERT priority classifier
        if BERT_AVAILABLE:
            try:
                self.bert_classifier = AdvancedEventPriorityClassifier(bert_model_path)
                self.use_bert = True
                logger.info("BERT Priority Classifier initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize BERT classifier: {e}")
                self.bert_classifier = None
                self.use_bert = False
        else:
            logger.warning("BERT classifier not available, using fallback classification")
            self.bert_classifier = None
            self.use_bert = False
            
        # Note: UserBehaviorAnalyzer removed for now to fix import error
        self.user_behavior_analyzer = None
            
    def detect_conflicts(self, user, new_event_data: Dict[str, Any]) -> List[ConflictDetection]:
        """
        Enhanced conflict detection with BERT priority classification
        
        Args:
            user: User object
            new_event_data: Dictionary containing event information
            
        Returns:
            List of detected conflicts with enhanced analysis
        """
        conflicts = []
        
        try:
            # Get user's existing events in the time window
            existing_events = self._get_user_events_in_timeframe(
                user, 
                new_event_data.get('start_time'),
                new_event_data.get('end_time')
            )
            
            # Get user context for enhanced priority classification
            user_context = self._get_user_context(user)
            
            # Classify priority of new event using BERT
            new_event_priority, priority_confidence = self._infer_event_priority_enhanced(
                new_event_data, 
                user_context
            )
            
            logger.info(f"New event priority: {new_event_priority} (confidence: {priority_confidence:.3f})")
            
            # Check for conflicts with each existing event
            for existing_event in existing_events:
                # Time overlap detection
                time_conflicts = self._detect_time_conflicts(existing_event, new_event_data)
                conflicts.extend(time_conflicts)
                
                # Location conflict detection
                location_conflicts = self._detect_location_conflicts(existing_event, new_event_data)
                conflicts.extend(location_conflicts)
                
                # Priority-based conflict detection (enhanced with BERT)
                priority_conflicts = self._detect_priority_conflicts(
                    existing_event, 
                    new_event_data, 
                    new_event_priority,
                    priority_confidence,
                    user_context
                )
                conflicts.extend(priority_conflicts)
                
                # Buffer time violation detection
                buffer_conflicts = self._detect_buffer_violations(existing_event, new_event_data)
                conflicts.extend(buffer_conflicts)
                
                # Productivity impact analysis
                productivity_conflicts = self._detect_productivity_impacts(
                    existing_event, 
                    new_event_data, 
                    user_context
                )
                conflicts.extend(productivity_conflicts)
                
        except Exception as e:
            logger.error(f"Error in conflict detection: {e}")
            
        return conflicts
        
    def _infer_event_priority_enhanced(self, 
                                     event_data: Dict[str, Any], 
                                     user_context: Optional[Dict] = None) -> Tuple[int, float]:
        """
        Enhanced priority inference using BERT classifier
        
        Args:
            event_data: Event information
            user_context: User behavioral context
            
        Returns:
            Tuple of (priority: int 1-5, confidence: float 0-1)
        """
        if self.use_bert and self.bert_classifier:
            try:
                priority, confidence = self.bert_classifier.predict(event_data, user_context)
                logger.debug(f"BERT priority inference: {priority} (confidence: {confidence:.3f})")
                return priority, confidence
            except Exception as e:
                logger.warning(f"BERT priority inference failed: {e}, falling back to keyword-based")
                
        # Fallback to enhanced keyword-based classification
        return self._infer_event_priority_fallback(event_data)
        
    def _infer_event_priority_fallback(self, event_data: Dict[str, Any]) -> Tuple[int, float]:
        """
        Enhanced fallback priority classification
        Improved version of the original keyword-based system
        """
        title = (event_data.get('title') or '').lower()
        description = (event_data.get('description') or '').lower()
        text = f"{title} {description}"
        
        # Enhanced keyword categories with confidence scoring
        priority_keywords = {
            5: {  # Critical
                'keywords': ['urgent', 'critical', 'emergency', 'deadline', 'ceo', 'crisis', 'asap'],
                'confidence': 0.8
            },
            4: {  # High
                'keywords': ['important', 'presentation', 'client', 'interview', 'boss', 'director', 'executive'],
                'confidence': 0.7
            },
            3: {  # Medium  
                'keywords': ['meeting', 'work', 'project', 'team', 'review', 'planning', 'training'],
                'confidence': 0.6
            },
            2: {  # Low
                'keywords': ['lunch', 'personal', 'hobby', 'exercise', 'shopping', 'social', 'casual'],
                'confidence': 0.5
            },
            1: {  # Very Low
                'keywords': ['break', 'coffee', 'casual', 'optional', 'free time', 'leisure'],
                'confidence': 0.4
            }
        }
        
        # Check for keyword matches
        for priority in [5, 4, 3, 2, 1]:
            keywords = priority_keywords[priority]['keywords']
            confidence = priority_keywords[priority]['confidence']
            
            if any(keyword in text for keyword in keywords):
                logger.debug(f"Keyword-based priority: {priority} (confidence: {confidence})")
                return priority, confidence
                
        # Default medium priority with low confidence
        return 3, 0.3
        
    def _get_user_context(self, user) -> Dict[str, Any]:
        """Get user behavioral context for enhanced priority classification"""
        context = {}
        
        if self.user_behavior_analyzer:
            try:
                # Get user patterns
                user_patterns = self.user_behavior_analyzer.analyze_user_patterns(user.id)
                context.update({
                    'preferred_meeting_times': user_patterns.get('preferred_meeting_times', []),
                    'productivity_patterns': user_patterns.get('productivity_patterns', {}),
                    'scheduling_habits': user_patterns.get('scheduling_habits', {}),
                    'priority_preferences': user_patterns.get('priority_preferences', {})
                })
            except Exception as e:
                logger.warning(f"Failed to get user behavior context: {e}")
                
        return context
        
    def _detect_priority_conflicts(self, 
                                  existing_event, 
                                  new_event_data: Dict[str, Any],
                                  new_event_priority: int,
                                  priority_confidence: float,
                                  user_context: Optional[Dict] = None) -> List[ConflictDetection]:
        """Enhanced priority conflict detection using BERT classifications"""
        conflicts = []
        
        try:
            # Get existing event priority
            existing_event_data = {
                'title': getattr(existing_event, 'title', ''),
                'description': getattr(existing_event, 'description', ''),
                'start_time': getattr(existing_event, 'start_time', None),
                'end_time': getattr(existing_event, 'end_time', None),
                'location': getattr(existing_event, 'location', '')
            }
            
            existing_priority, existing_confidence = self._infer_event_priority_enhanced(
                existing_event_data, 
                user_context
            )
            
            # Calculate priority difference
            priority_difference = abs(new_event_priority - existing_priority)
            
            # Determine if this constitutes a priority conflict
            if priority_difference >= 2:  # Significant priority difference
                # Determine severity based on priority levels and confidence
                if max(new_event_priority, existing_priority) >= 4:  # High/Critical priority involved
                    severity = ConflictSeverity.HIGH
                    impact_score = 0.8 + (priority_difference * 0.1)
                elif priority_difference >= 3:  # Very large difference
                    severity = ConflictSeverity.MEDIUM
                    impact_score = 0.6 + (priority_difference * 0.1)
                else:
                    severity = ConflictSeverity.LOW
                    impact_score = 0.4 + (priority_difference * 0.1)
                
                # Generate description
                priority_labels = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}
                description = (
                    f"Priority conflict detected: New event ({priority_labels[new_event_priority]}) "
                    f"conflicts with existing event ({priority_labels[existing_priority]})"
                )
                
                # Generate resolution suggestions
                resolutions = self._generate_priority_resolution_suggestions(
                    existing_event, 
                    new_event_data, 
                    existing_priority, 
                    new_event_priority
                )
                
                conflict = ConflictDetection(
                    conflict_type=ConflictType.PRIORITY_CONFLICT,
                    severity=severity,
                    existing_event_id=str(getattr(existing_event, 'id', '')),
                    new_event_data=new_event_data,
                    impact_score=impact_score,
                    description=description,
                    suggested_resolutions=resolutions,
                    confidence=min(priority_confidence, existing_confidence)
                )
                
                conflicts.append(conflict)
                
        except Exception as e:
            logger.error(f"Error in priority conflict detection: {e}")
            
        return conflicts
        
    def _generate_priority_resolution_suggestions(self, 
                                                 existing_event, 
                                                 new_event_data: Dict[str, Any],
                                                 existing_priority: int, 
                                                 new_priority: int) -> List[str]:
        """Generate intelligent resolution suggestions based on priorities"""
        suggestions = []
        
        if new_priority > existing_priority:
            suggestions.extend([
                f"Consider rescheduling the existing lower-priority event",
                f"Move the existing event to a different time slot",
                f"Shorten the existing event if possible"
            ])
        elif existing_priority > new_priority:
            suggestions.extend([
                f"Consider scheduling the new event at a different time",
                f"Find an alternative time slot for the new event",
                f"Evaluate if the new event can be postponed"
            ])
        else:
            suggestions.extend([
                f"Both events have similar priority - consider user preferences",
                f"Check if either event can be moved to avoid overlap",
                f"Consider combining or consolidating if events are related"
            ])
            
        # Add time-specific suggestions
        start_time = new_event_data.get('start_time')
        if isinstance(start_time, str):
            try:
                start_dt = datetime.fromisoformat(start_time)
                # Suggest alternative time slots
                alt_time_1 = start_dt + timedelta(hours=1)
                alt_time_2 = start_dt + timedelta(hours=2)
                suggestions.extend([
                    f"Alternative time slot: {alt_time_1.strftime('%H:%M')}",
                    f"Alternative time slot: {alt_time_2.strftime('%H:%M')}"
                ])
            except:
                pass
                
        return suggestions
        
    def _get_user_events_in_timeframe(self, user, start_time, end_time):
        """Get user's existing events in the specified timeframe"""
        # Mock implementation - replace with actual database query
        # This would typically query your events table
        return []
        
    def _detect_time_conflicts(self, existing_event, new_event_data):
        """Detect time overlap conflicts"""
        # Implementation for time conflict detection
        return []
        
    def _detect_location_conflicts(self, existing_event, new_event_data):
        """Detect location-based conflicts"""
        # Implementation for location conflict detection
        return []
        
    def _detect_buffer_violations(self, existing_event, new_event_data):
        """Detect buffer time violations"""
        # Implementation for buffer time conflict detection
        return []
        
    def _detect_productivity_impacts(self, existing_event, new_event_data, user_context):
        """Detect productivity impact conflicts"""
        # Implementation for productivity impact analysis
        return []
        
    def get_conflict_resolution_suggestions(self, conflicts: List[ConflictDetection]) -> Dict[str, Any]:
        """
        Generate comprehensive conflict resolution suggestions
        
        Args:
            conflicts: List of detected conflicts
            
        Returns:
            Dictionary with resolution strategies and recommendations
        """
        if not conflicts:
            return {"status": "no_conflicts", "suggestions": []}
            
        # Analyze conflict patterns
        conflict_types = [c.conflict_type for c in conflicts]
        severity_levels = [c.severity for c in conflicts]
        
        # Generate prioritized suggestions
        suggestions = {
            "critical_actions": [],
            "recommended_actions": [],
            "optional_actions": [],
            "alternative_times": []
        }
        
        # Critical actions for high-severity conflicts
        critical_conflicts = [c for c in conflicts if c.severity == ConflictSeverity.HIGH]
        for conflict in critical_conflicts:
            suggestions["critical_actions"].extend(conflict.suggested_resolutions[:2])
            
        # Recommended actions for medium-severity conflicts
        medium_conflicts = [c for c in conflicts if c.severity == ConflictSeverity.MEDIUM]
        for conflict in medium_conflicts:
            suggestions["recommended_actions"].extend(conflict.suggested_resolutions[:3])
            
        # Optional actions for low-severity conflicts
        low_conflicts = [c for c in conflicts if c.severity == ConflictSeverity.LOW]
        for conflict in low_conflicts:
            suggestions["optional_actions"].extend(conflict.suggested_resolutions)
            
        return {
            "status": "conflicts_detected",
            "conflict_count": len(conflicts),
            "severity_breakdown": {
                "critical": len([c for c in conflicts if c.severity == ConflictSeverity.CRITICAL]),
                "high": len([c for c in conflicts if c.severity == ConflictSeverity.HIGH]),
                "medium": len([c for c in conflicts if c.severity == ConflictSeverity.MEDIUM]),
                "low": len([c for c in conflicts if c.severity == ConflictSeverity.LOW])
            },
            "suggestions": suggestions,
            "conflicts": [
                {
                    "type": c.conflict_type.value,
                    "severity": c.severity.value,
                    "description": c.description,
                    "impact_score": c.impact_score,
                    "confidence": c.confidence
                } for c in conflicts
            ]
        }
    
    def resolve_conflict_by_priority(self, conflicting_events: List[Any]) -> Dict[str, Any]:
        """
        Resolve conflicts based on event priorities using BERT-enhanced analysis
        
        Args:
            conflicting_events: List of Event objects in conflict
            
        Returns:
            Dictionary with resolution suggestions and reasoning
        """
        logger.info(f"🔀 Resolving conflicts for {len(conflicting_events)} events using priority analysis")
        
        try:
            # Analyze priorities of all conflicting events
            event_priorities = []
            
            for event in conflicting_events:
                if hasattr(event, 'priority_level') and event.priority_level:
                    priority = event.priority_level
                    confidence = getattr(event, 'priority_confidence', 0.5)
                else:
                    # Infer priority if not stored
                    event_data = {
                        'title': event.title,
                        'description': event.description or '',
                        'location': event.location or ''
                    }
                    priority, confidence = self._infer_event_priority_enhanced(event_data)
                
                event_priorities.append({
                    'event': event,
                    'priority': priority,
                    'confidence': confidence,
                    'priority_weight': self._get_priority_weight(priority)
                })
            
            # Sort by priority (1 = highest priority)
            event_priorities.sort(key=lambda x: (x['priority'], -x['confidence']))
            
            highest_priority_event = event_priorities[0]
            other_events = event_priorities[1:]
            
            # Generate resolution suggestions
            resolution = {
                'resolution_type': 'priority_based',
                'recommended_action': 'keep_highest_priority',
                'keep_event': {
                    'title': highest_priority_event['event'].title,
                    'priority': highest_priority_event['priority'],
                    'priority_label': self._get_priority_label(highest_priority_event['priority']),
                    'confidence': highest_priority_event['confidence'],
                    'reasoning': f"Highest priority event (P{highest_priority_event['priority']}) should be preserved"
                },
                'reschedule_events': [],
                'priority_analysis': {
                    'total_conflicts': len(conflicting_events),
                    'priority_distribution': {ep['priority']: 1 for ep in event_priorities},
                    'recommendation_confidence': highest_priority_event['confidence']
                }
            }
            
            # Add rescheduling suggestions for other events
            for event_priority in other_events:
                event = event_priority['event']
                priority_diff = event_priority['priority'] - highest_priority_event['priority']
                
                reschedule_suggestion = {
                    'title': event.title,
                    'current_priority': event_priority['priority'],
                    'priority_label': self._get_priority_label(event_priority['priority']),
                    'priority_difference': priority_diff,
                    'action': 'reschedule' if priority_diff >= 2 else 'consider_reschedule',
                    'reasoning': f"Priority {event_priority['priority']} event can be rescheduled to accommodate priority {highest_priority_event['priority']} event"
                }
                
                resolution['reschedule_events'].append(reschedule_suggestion)
            
            logger.info(f"✅ Priority-based resolution generated: Keep P{highest_priority_event['priority']}, reschedule {len(other_events)} events")
            return resolution
            
        except Exception as e:
            logger.error(f"❌ Priority-based conflict resolution failed: {str(e)}")
            return {
                'resolution_type': 'fallback',
                'error': str(e),
                'recommended_action': 'manual_review',
                'reasoning': 'Automated priority resolution failed, manual review required'
            }
    
    def get_priority_based_alternatives(self, event: Any, conflicts: List[Any]) -> List[Dict[str, Any]]:
        """
        Generate priority-aware alternative time suggestions
        
        Args:
            event: The new event to schedule
            conflicts: List of conflicting events
            
        Returns:
            List of alternative time slot suggestions
        """
        logger.info(f"🕐 Generating priority-based alternative times for '{event.title if hasattr(event, 'title') else 'New Event'}'")
        
        try:
            # Get priority of the new event
            if hasattr(event, 'priority_level') and event.priority_level:
                new_event_priority = event.priority_level
            else:
                event_data = {
                    'title': getattr(event, 'title', ''),
                    'description': getattr(event, 'description', ''),
                    'location': getattr(event, 'location', '')
                }
                new_event_priority, _ = self._infer_event_priority_enhanced(event_data)
            
            # Get event duration
            if hasattr(event, 'start_time') and hasattr(event, 'end_time'):
                duration = event.end_time - event.start_time
                base_start = event.start_time
            else:
                duration = timedelta(hours=1)  # Default 1 hour
                base_start = datetime.now()
            
            alternatives = []
            
            # Generate time slot alternatives
            for hours_offset in [-2, -1, 1, 2, 4, 8, 24]:
                alternative_start = base_start + timedelta(hours=hours_offset)
                alternative_end = alternative_start + duration
                
                # Check if this alternative would conflict with existing events
                conflicts_at_time = self._check_conflicts_at_time(alternative_start, alternative_end, conflicts)
                
                # Calculate priority score for this time slot
                priority_score = self._calculate_time_slot_priority_score(
                    alternative_start, alternative_end, conflicts_at_time, new_event_priority
                )
                
                alternative = {
                    'suggested_start_time': alternative_start.isoformat(),
                    'suggested_end_time': alternative_end.isoformat(),
                    'time_offset_hours': hours_offset,
                    'conflicts_count': len(conflicts_at_time),
                    'priority_score': priority_score,
                    'recommendation_level': self._get_recommendation_level(priority_score),
                    'conflicting_events': [
                        {
                            'title': conf.title if hasattr(conf, 'title') else 'Unknown',
                            'priority': getattr(conf, 'priority_level', 3)
                        } for conf in conflicts_at_time
                    ],
                    'reasoning': self._generate_alternative_reasoning(hours_offset, conflicts_at_time, new_event_priority)
                }
                
                alternatives.append(alternative)
            
            # Sort by priority score (higher is better)
            alternatives.sort(key=lambda x: x['priority_score'], reverse=True)
            
            # Add ranking
            for i, alt in enumerate(alternatives):
                alt['rank'] = i + 1
            
            logger.info(f"✅ Generated {len(alternatives)} alternative time suggestions")
            return alternatives[:5]  # Return top 5 alternatives
            
        except Exception as e:
            logger.error(f"❌ Alternative time generation failed: {str(e)}")
            return [{
                'error': str(e),
                'reasoning': 'Failed to generate alternative times, manual scheduling required'
            }]
    
    def _get_priority_weight(self, priority: int) -> float:
        """Get priority weight for calculations"""
        weights = {1: 1.0, 2: 0.8, 3: 0.6, 4: 0.4, 5: 0.2}
        return weights.get(priority, 0.5)
    
    def _get_priority_label(self, priority: int) -> str:
        """Get human-readable priority label"""
        labels = {1: 'Critical', 2: 'High', 3: 'Medium', 4: 'Low', 5: 'Very Low'}
        return labels.get(priority, 'Unknown')
    
    def _check_conflicts_at_time(self, start_time: datetime, end_time: datetime, existing_events: List[Any]) -> List[Any]:
        """Check for conflicts at a specific time slot"""
        conflicts = []
        
        for event in existing_events:
            if hasattr(event, 'start_time') and hasattr(event, 'end_time'):
                if (start_time < event.end_time and end_time > event.start_time):
                    conflicts.append(event)
        
        return conflicts
    
    def _calculate_time_slot_priority_score(self, start_time: datetime, end_time: datetime, 
                                          conflicts: List[Any], new_event_priority: int) -> float:
        """Calculate priority-based score for a time slot"""
        if not conflicts:
            return 10.0  # Perfect score for no conflicts
        
        # Calculate score based on priority differences
        score = 5.0  # Base score
        
        for conflict in conflicts:
            conflict_priority = getattr(conflict, 'priority_level', 3)
            priority_diff = conflict_priority - new_event_priority
            
            if priority_diff > 0:  # Conflicting event has lower priority
                score += priority_diff * 1.5
            else:  # Conflicting event has higher/equal priority
                score += priority_diff * 2.0  # Negative impact
        
        # Consider time of day (business hours preference)
        hour = start_time.hour
        if 9 <= hour <= 17:  # Business hours
            score += 1.0
        elif 8 <= hour <= 18:  # Extended business hours
            score += 0.5
        
        return max(0.0, min(10.0, score))  # Clamp between 0-10
    
    def _get_recommendation_level(self, priority_score: float) -> str:
        """Get recommendation level based on priority score"""
        if priority_score >= 8.0:
            return 'highly_recommended'
        elif priority_score >= 6.0:
            return 'recommended'
        elif priority_score >= 4.0:
            return 'acceptable'
        else:
            return 'not_recommended'
    
    def _generate_alternative_reasoning(self, hours_offset: int, conflicts: List[Any], new_priority: int) -> str:
        """Generate human-readable reasoning for alternative suggestions"""
        if not conflicts:
            return f"No conflicts at this time - {abs(hours_offset)} hours {'earlier' if hours_offset < 0 else 'later'}"
        
        high_priority_conflicts = [c for c in conflicts if getattr(c, 'priority_level', 3) <= 2]
        
        if high_priority_conflicts:
            return f"Conflicts with {len(high_priority_conflicts)} high-priority event(s) - may require negotiation"
        else:
            return f"Conflicts with {len(conflicts)} lower-priority event(s) - reschedule possible"
        
    def explain_priority_decision(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide detailed explanation for priority classification decision
        
        Args:
            event_data: Event information
            
        Returns:
            Detailed explanation of priority classification
        """
        if self.use_bert and self.bert_classifier:
            try:
                return self.bert_classifier.explain_prediction(event_data)
            except Exception as e:
                logger.warning(f"BERT explanation failed: {e}")
                
        # Fallback explanation
        priority, confidence = self._infer_event_priority_fallback(event_data)
        return {
            'priority': priority,
            'priority_label': {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Critical"}[priority],
            'confidence': confidence,
            'reasoning': {
                'method': 'Keyword-based classification',
                'text_analysis': f"Analysis of event title and description",
                'confidence_note': f"{confidence:.1%} confident based on keyword matching"
            }
        }