# backend/app/api/conflicts.py
"""
Smart Conflict Detection & Auto-Resolution API Endpoints
Provides RESTful interface for conflict management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

from app.core.database import get_db
from app.models.user import User
from app.models.event import Event
from app.services.conflict_detector import (
    SmartConflictDetector,
    ConflictDetection,
    ConflictResolution,
    ConflictAnalytics,
    ConflictType,
    ConflictSeverity
)
from app.schemas.event import EventCreate, EventResponse
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/conflicts", tags=["conflicts"])

# Pydantic schemas for conflict API
class ConflictCheckRequest(BaseModel):
    """Request schema for conflict detection"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = Field(None, max_length=255)
    is_all_day: bool = False
    buffer_minutes: Optional[int] = Field(15, ge=0, le=120)

class ConflictDetectionResponse(BaseModel):
    """Response schema for detected conflicts"""
    conflict_id: str
    conflict_type: str
    severity: str
    affected_event_ids: List[str]
    description: str
    buffer_minutes: int
    confidence: float
    impact_score: float

class TimeSlotAlternative(BaseModel):
    """Alternative time slot suggestion"""
    start_time: datetime
    end_time: datetime
    confidence: float
    reasoning: str
    productivity_score: Optional[float] = None

class ConflictResolutionResponse(BaseModel):
    """Response schema for conflict resolution"""
    resolution_id: str
    conflict_id: str
    alternatives: List[TimeSlotAlternative]
    auto_resolution: Optional[TimeSlotAlternative] = None
    strategy: str
    confidence: float
    reasoning: str

class ConflictReportResponse(BaseModel):
    """Response schema for conflict analysis report"""
    total_conflicts: int
    severity_breakdown: Dict[str, int]
    type_breakdown: Dict[str, int]
    average_impact_score: Optional[float]
    recommendations: List[str]

class BatchConflictCheckRequest(BaseModel):
    """Request schema for batch conflict checking"""
    events: List[ConflictCheckRequest]
    global_buffer_minutes: Optional[int] = Field(15, ge=0, le=120)

def get_user_from_cognito(cognito_sub: str, db: Session) -> User:
    """Helper function to get user from Cognito sub ID"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User profile not found. Please create your profile first."
        )
    return user

@router.post("/check", response_model=List[ConflictDetectionResponse])
def check_conflicts(
    cognito_sub: str,
    conflict_request: ConflictCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Check for conflicts with a proposed new event
    
    This endpoint analyzes a potential new event against the user's existing
    schedule and returns any detected conflicts with detailed information.
    """
    try:
        # Get user
        user = get_user_from_cognito(cognito_sub, db)
        
        # Initialize conflict detector
        detector = SmartConflictDetector(db)
        
        # Convert request to event data
        event_data = {
            "title": conflict_request.title,
            "description": conflict_request.description,
            "start_time": conflict_request.start_time,
            "end_time": conflict_request.end_time,
            "location": conflict_request.location,
            "is_all_day": conflict_request.is_all_day
        }
        
        # Detect conflicts
        conflicts = detector.detect_conflicts(
            user=user,
            new_event_data=event_data,
            buffer_minutes=conflict_request.buffer_minutes
        )
        
        # Convert to response format
        conflict_responses = []
        for conflict in conflicts:
            conflict_responses.append(ConflictDetectionResponse(
                conflict_id=conflict.conflict_id,
                conflict_type=conflict.conflict_type.value,
                severity=conflict.severity.value,
                affected_event_ids=[str(event.id) for event in conflict.affected_events],
                description=conflict.description,
                buffer_minutes=conflict.buffer_minutes,
                confidence=conflict.confidence,
                impact_score=conflict.impact_score
            ))
        
        return conflict_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting conflicts: {str(e)}"
        )

@router.post("/resolve", response_model=List[ConflictResolutionResponse])
def resolve_conflicts(
    cognito_sub: str,
    conflict_request: ConflictCheckRequest,
    auto_resolve: bool = Query(False, description="Automatically select best resolution"),
    max_alternatives: int = Query(5, ge=1, le=10, description="Maximum alternatives to return"),
    db: Session = Depends(get_db)
):
    """
    Get intelligent resolutions for scheduling conflicts
    
    This endpoint first detects conflicts and then generates smart alternatives
    using AI-powered analysis of user behavior patterns.
    """
    try:
        # Get user
        user = get_user_from_cognito(cognito_sub, db)
        
        # Initialize conflict detector
        detector = SmartConflictDetector(db)
        
        # Convert request to event data
        event_data = {
            "title": conflict_request.title,
            "description": conflict_request.description,
            "start_time": conflict_request.start_time,
            "end_time": conflict_request.end_time,
            "location": conflict_request.location,
            "is_all_day": conflict_request.is_all_day
        }
        
        # Detect conflicts
        conflicts = detector.detect_conflicts(
            user=user,
            new_event_data=event_data,
            buffer_minutes=conflict_request.buffer_minutes
        )
        
        if not conflicts:
            return []  # No conflicts, no resolutions needed
        
        # Generate resolutions
        resolutions = detector.resolve_conflicts(
            conflicts=conflicts,
            user=user,
            auto_resolve=auto_resolve
        )
        
        # Convert to response format
        resolution_responses = []
        for resolution in resolutions:
            # Convert alternatives
            alternatives = []
            for alt in resolution.alternatives[:max_alternatives]:
                alternatives.append(TimeSlotAlternative(
                    start_time=alt.start_time,
                    end_time=alt.end_time,
                    confidence=alt.confidence,
                    reasoning=alt.reasoning,
                    productivity_score=getattr(alt, 'productivity_score', None)
                ))
            
            # Convert auto resolution
            auto_resolution = None
            if resolution.auto_resolution:
                auto_resolution = TimeSlotAlternative(
                    start_time=resolution.auto_resolution.start_time,
                    end_time=resolution.auto_resolution.end_time,
                    confidence=resolution.auto_resolution.confidence,
                    reasoning=resolution.auto_resolution.reasoning,
                    productivity_score=getattr(resolution.auto_resolution, 'productivity_score', None)
                )
            
            resolution_responses.append(ConflictResolutionResponse(
                resolution_id=resolution.resolution_id,
                conflict_id=resolution.original_conflict.conflict_id,
                alternatives=alternatives,
                auto_resolution=auto_resolution,
                strategy=resolution.strategy,
                confidence=resolution.confidence,
                reasoning=resolution.reasoning
            ))
        
        return resolution_responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error resolving conflicts: {str(e)}"
        )

@router.post("/analyze", response_model=ConflictReportResponse)
def analyze_conflicts(
    cognito_sub: str,
    conflict_request: ConflictCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Generate comprehensive conflict analysis report
    
    This endpoint provides detailed analysis of conflicts including severity
    breakdown, impact assessment, and actionable recommendations.
    """
    try:
        # Get user
        user = get_user_from_cognito(cognito_sub, db)
        
        # Initialize conflict detector
        detector = SmartConflictDetector(db)
        
        # Convert request to event data
        event_data = {
            "title": conflict_request.title,
            "description": conflict_request.description,
            "start_time": conflict_request.start_time,
            "end_time": conflict_request.end_time,
            "location": conflict_request.location,
            "is_all_day": conflict_request.is_all_day
        }
        
        # Detect conflicts
        conflicts = detector.detect_conflicts(
            user=user,
            new_event_data=event_data,
            buffer_minutes=conflict_request.buffer_minutes
        )
        
        # Generate analysis report
        report = ConflictAnalytics.generate_conflict_report(conflicts)
        
        return ConflictReportResponse(**report)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing conflicts: {str(e)}"
        )

@router.post("/batch-check", response_model=Dict[str, Any])
def batch_check_conflicts(
    cognito_sub: str,
    batch_request: BatchConflictCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Check conflicts for multiple events at once
    
    This endpoint allows bulk conflict checking for multiple proposed events,
    useful for schedule planning and bulk event creation.
    """
    try:
        # Get user
        user = get_user_from_cognito(cognito_sub, db)
        
        # Initialize conflict detector
        detector = SmartConflictDetector(db)
        
        results = {
            "total_events_checked": len(batch_request.events),
            "events_with_conflicts": 0,
            "total_conflicts": 0,
            "results": []
        }
        
        for i, event_request in enumerate(batch_request.events):
            # Convert request to event data
            event_data = {
                "title": event_request.title,
                "description": event_request.description,
                "start_time": event_request.start_time,
                "end_time": event_request.end_time,
                "location": event_request.location,
                "is_all_day": event_request.is_all_day
            }
            
            # Use event-specific buffer or global buffer
            buffer_minutes = event_request.buffer_minutes or batch_request.global_buffer_minutes
            
            # Detect conflicts
            conflicts = detector.detect_conflicts(
                user=user,
                new_event_data=event_data,
                buffer_minutes=buffer_minutes
            )
            
            # Track statistics
            if conflicts:
                results["events_with_conflicts"] += 1
                results["total_conflicts"] += len(conflicts)
            
            # Convert conflicts to response format
            conflict_responses = []
            for conflict in conflicts:
                conflict_responses.append({
                    "conflict_id": conflict.conflict_id,
                    "conflict_type": conflict.conflict_type.value,
                    "severity": conflict.severity.value,
                    "description": conflict.description,
                    "confidence": conflict.confidence,
                    "impact_score": conflict.impact_score
                })
            
            results["results"].append({
                "event_index": i,
                "event_title": event_request.title,
                "conflicts_detected": len(conflicts),
                "conflicts": conflict_responses
            })
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in batch conflict check: {str(e)}"
        )

@router.get("/user-patterns", response_model=Dict[str, Any])
def get_user_conflict_patterns(
    cognito_sub: str,
    days_back: int = Query(30, ge=7, le=90, description="Days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Analyze user's historical conflict patterns
    
    This endpoint analyzes the user's scheduling patterns and common sources
    of conflicts to provide insights for better scheduling.
    """
    try:
        # Get user
        user = get_user_from_cognito(cognito_sub, db)
        
        # Initialize conflict detector
        detector = SmartConflictDetector(db)
        
        # Get historical events
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        historical_events = db.query(Event).filter(
            Event.user_id == user.id,
            Event.start_time >= cutoff_date
        ).order_by(Event.start_time).all()
        
        if len(historical_events) < 5:
            return {
                "message": "Insufficient historical data for pattern analysis",
                "events_analyzed": len(historical_events),
                "recommendations": [
                    "Schedule more events to enable pattern analysis",
                    "Use the system for at least 2 weeks for meaningful insights"
                ]
            }
        
        # Analyze patterns using behavior analytics
        from app.nlp.user_behavior_analytics import UserBehaviorAnalyzer
        analyzer = UserBehaviorAnalyzer()
        user_patterns = analyzer.analyze_user_patterns(historical_events)
        
        # Simulate conflict analysis on historical events
        conflict_hotspots = {}
        common_conflict_types = {}
        
        for event in historical_events[-20:]:  # Analyze last 20 events
            # Simulate what conflicts this event would have had
            event_data = {
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time,
                "end_time": event.end_time,
                "location": event.location,
                "is_all_day": event.is_all_day
            }
            
            # Get events that were scheduled around the same time
            nearby_events = detector._get_user_events_in_range(
                user, event.start_time, event.end_time, 15
            )
            nearby_events = [e for e in nearby_events if e.id != event.id]
            
            if nearby_events:
                # Track hour when conflicts occur
                hour = event.start_time.hour
                conflict_hotspots[hour] = conflict_hotspots.get(hour, 0) + 1
        
        # Generate insights
        busiest_hours = sorted(conflict_hotspots.items(), key=lambda x: x[1], reverse=True)[:3]
        
        insights = {
            "analysis_period_days": days_back,
            "events_analyzed": len(historical_events),
            "conflict_hotspots": {
                "busiest_hours": [{"hour": hour, "conflict_count": count} for hour, count in busiest_hours],
                "recommendations": []
            },
            "scheduling_patterns": {
                "average_event_duration": sum(
                    (event.end_time - event.start_time).total_seconds() / 60 
                    for event in historical_events
                ) / len(historical_events) if historical_events else 0,
                "most_common_locations": _get_common_locations(historical_events),
                "preferred_days": _get_preferred_days(historical_events)
            },
            "recommendations": [
                "Consider longer buffer times during busy hours",
                "Use alternative time slots during peak conflict periods",
                "Schedule important events during your less busy hours"
            ]
        }
        
        # Add specific recommendations based on patterns
        if busiest_hours:
            busiest_hour = busiest_hours[0][0]
            insights["conflict_hotspots"]["recommendations"].append(
                f"Consider avoiding {busiest_hour}:00-{busiest_hour+1}:00 for new events"
            )
        
        return insights
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing user patterns: {str(e)}"
        )

@router.post("/smart-reschedule/{event_id}")
def smart_reschedule_event(
    event_id: UUID,
    cognito_sub: str,
    preferred_date: Optional[datetime] = Query(None, description="Preferred date for rescheduling"),
    max_alternatives: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Intelligently reschedule an existing event to avoid conflicts
    
    This endpoint analyzes an existing event and suggests optimal times
    to reschedule it, taking into account user patterns and preferences.
    """
    try:
        # Get user
        user = get_user_from_cognito(cognito_sub, db)
        
        # Get the event to reschedule
        event = db.query(Event).filter(
            Event.id == event_id,
            Event.user_id == user.id
        ).first()
        
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found or you don't have permission to reschedule it"
            )
        
        # Initialize conflict detector and behavior analyzer
        detector = SmartConflictDetector(db)
        from app.nlp.user_behavior_analytics import UserBehaviorAnalyzer
        analyzer = UserBehaviorAnalyzer()
        
        # Get user patterns
        historical_events = detector._get_user_historical_events(user, days=30)
        user_patterns = analyzer.analyze_user_patterns(historical_events)
        
        # Calculate event duration
        duration_minutes = int((event.end_time - event.start_time).total_seconds() / 60)
        
        # Generate smart alternatives
        reference_date = preferred_date.date() if preferred_date else event.start_time.date()
        
        alternatives = analyzer.suggest_optimal_times(
            duration_minutes=duration_minutes,
            event_type=event.title,
            user_patterns=user_patterns,
            avoid_conflicts=True,
            reference_date=reference_date
        )
        
        # Filter out alternatives that would create new conflicts
        event_data = {
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time,  # Will be updated for each alternative
            "end_time": event.end_time,      # Will be updated for each alternative
            "location": event.location,
            "is_all_day": event.is_all_day
        }
        
        conflict_free_alternatives = []
        for alternative in alternatives[:max_alternatives * 2]:  # Check more than needed
            # Update event data with alternative time
            temp_event_data = event_data.copy()
            temp_event_data['start_time'] = alternative.start_time
            temp_event_data['end_time'] = alternative.end_time
            
            # Check for conflicts (excluding the original event)
            conflicts = detector.detect_conflicts(user, temp_event_data)
            
            # Filter out conflicts with the original event itself
            conflicts = [c for c in conflicts if not any(
                affected_event.id == event.id for affected_event in c.affected_events
            )]
            
            # Only include if no significant conflicts
            if not conflicts or all(c.severity.value in ['low'] for c in conflicts):
                conflict_free_alternatives.append(alternative)
            
            if len(conflict_free_alternatives) >= max_alternatives:
                break
        
        # Convert to response format
        alternative_responses = []
        for alt in conflict_free_alternatives:
            alternative_responses.append({
                "start_time": alt.start_time,
                "end_time": alt.end_time,
                "confidence": alt.confidence,
                "reasoning": alt.reasoning,
                "productivity_score": getattr(alt, 'productivity_score', None)
            })
        
        return {
            "event_id": str(event.id),
            "event_title": event.title,
            "current_time": {
                "start_time": event.start_time,
                "end_time": event.end_time
            },
            "alternatives": alternative_responses,
            "recommendation": alternative_responses[0] if alternative_responses else None,
            "message": f"Found {len(alternative_responses)} conflict-free alternatives" if alternative_responses else "No suitable alternatives found"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rescheduling event: {str(e)}"
        )

# Helper functions
def _get_common_locations(events: List[Event]) -> List[Dict[str, Any]]:
    """Get most common locations from events"""
    location_counts = {}
    for event in events:
        if event.location:
            location = event.location.strip()
            location_counts[location] = location_counts.get(location, 0) + 1
    
    sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
    return [{"location": loc, "count": count} for loc, count in sorted_locations[:5]]

def _get_preferred_days(events: List[Event]) -> List[Dict[str, Any]]:
    """Get preferred days of week from events"""
    day_counts = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for event in events:
        day_name = days[event.start_time.weekday()]
        day_counts[day_name] = day_counts.get(day_name, 0) + 1
    
    sorted_days = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
    return [{"day": day, "count": count} for day, count in sorted_days]