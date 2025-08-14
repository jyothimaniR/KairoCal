# backend/app/api/conflicts.py
"""
Smart Conflict Detection & Auto-Resolution API Endpoints
Provides RESTful interface for conflict management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from uuid import UUID

from app.core.database import get_db
from app.models.user import User
from app.models.event import Event
# Note: Advanced conflict detection is available in services, but these endpoints
# provide safe fallbacks that won't raise if ML components are unavailable.
try:
    from app.services.conflict_detector import (
        SmartConflictDetector,
        ConflictDetection,
        ConflictType,
        ConflictSeverity,
    )
except Exception:
    SmartConflictDetector = None  # type: ignore
    ConflictDetection = None  # type: ignore
    ConflictType = None  # type: ignore
    ConflictSeverity = None  # type: ignore
from app.schemas.event import EventCreate, EventResponse
from pydantic import BaseModel, Field
from datetime import timezone as _tz
import logging
log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/conflicts", tags=["conflicts"])

# Import schemas from dedicated schemas module
from app.schemas.conflicts import (
    ConflictCheckRequest,
    ConflictDetectionResponse,
    ConflictTypeEnum,
    ConflictSeverityEnum
)

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

class ConflictCheckWrappedResponse(BaseModel):
    """Wrapped response for /conflicts/check to standardize contract."""
    conflicts: List[ConflictDetectionResponse]
    engine: str = "basic_v1"
    correlation_id: Optional[str]

class ConflictResolveWrappedResponse(BaseModel):
    """Wrapped response for /conflicts/resolve to standardize contract."""
    resolutions: List[ConflictResolutionResponse]
    engine: str = "basic_v1"
    correlation_id: Optional[str]

def get_user_from_cognito(cognito_sub: str, db: Session) -> User:
    """Helper function to get user from Cognito sub ID"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User profile not found. Please create your profile first."
        )
    return user

def _current_correlation_id() -> Optional[str]:
    """Attempt to fetch correlation id from main app context (set by middleware)."""
    try:
        import app.main as main  # local import to avoid circular at module load
        return getattr(main, "_correlation_id_ctx", None).get()  # type: ignore[attr-defined]
    except Exception:
        return None

@router.post("/check", response_model=ConflictCheckWrappedResponse)
def check_conflicts(
    cognito_sub: str,
    conflict_request: ConflictCheckRequest,
    engine: str = Query("fallback", description="Conflict engine: fallback|basic_v1"),
    db: Session = Depends(get_db)
):
    """
    Check for conflicts with a proposed new event
    
    This endpoint analyzes a potential new event against the user's existing
    schedule and returns any detected conflicts with detailed information.
    """
    try:
        user = get_user_from_cognito(cognito_sub, db)
        # Normalize engine: treat 'fallback' as 'basic_v1' for now
        engine_norm = "basic_v1" if engine in ("fallback", "basic_v1") else None
        if engine_norm is None:
            raise HTTPException(status_code=400, detail=f"Unsupported engine '{engine}'. Use 'basic_v1' or 'fallback'.")

    # Normalize request datetimes to naive UTC (strip tzinfo) for consistent comparisons
        from datetime import timedelta
        def _naive(dt: datetime) -> datetime:
            return dt.replace(tzinfo=None)
        phase = "init"
        req_start = _naive(conflict_request.start_time)
        req_end = _naive(conflict_request.end_time)
        buf = conflict_request.buffer_minutes or 0
        start = req_start - timedelta(minutes=buf)
        end = req_end + timedelta(minutes=buf)

    # Use naive for both sides of comparisons (DB stores aware but Python comparison handled)
        start_q = start
        end_q = end
        phase = "query_overlapping"
        try:
            # CRITICAL FIX: Exclude all-day events from time-specific conflict detection
            # All-day events should only conflict with other all-day events
            print(f"🔍 DEBUG: Checking conflicts for user {user.id}")
            print(f"🔍 DEBUG: Query range: {start_q} to {end_q}")
            
            # Query all events first to see what we have
            all_events = db.query(Event).filter(Event.user_id == user.id).all()
            print(f"🔍 DEBUG: All user events ({len(all_events)}):")
            for ev in all_events:
                print(f"   - {ev.title}: is_all_day={ev.is_all_day}, start={ev.start_time}, end={ev.end_time}")
            
            overlapping = db.query(Event).filter(
                Event.user_id == user.id,
                Event.is_all_day == False,  # 🔧 FIX: Only check non-all-day events
                Event.start_time < end_q,
                Event.end_time > start_q,
                # 🔧 FIX: Exclude self-conflicts (events with same time and title)
                ~(
                    (Event.start_time == req_start) & 
                    (Event.end_time == req_end) & 
                    (Event.title == conflict_request.title)
                )
            ).all()
            
            print(f"🔍 DEBUG: Overlapping non-all-day events found: {len(overlapping)}")
            for ev in overlapping:
                print(f"   - CONFLICT: {ev.title} ({ev.start_time} to {ev.end_time})")
        except Exception as qe:
            import traceback
            tb = traceback.format_exc(limit=5)
            raise RuntimeError(f"phase={phase} query_error: {qe} types start_q={type(start_q)} end_q={type(end_q)} start_q.tz={getattr(start_q,'tzinfo',None)} end_q.tz={getattr(end_q,'tzinfo',None)} tb={tb}")
        phase = "post_query"

        if overlapping:
            sample = overlapping[0]
            log.debug(
                "[conflicts.check.debug] req_start=%r tz=%r req_end=%r tz=%r sample_start=%r tz=%r sample_end=%r tz=%r overlap_count=%d",
                req_start, req_start.tzinfo, req_end, req_end.tzinfo,
                sample.start_time, getattr(sample.start_time,'tzinfo', None),
                sample.end_time, getattr(sample.end_time,'tzinfo', None), len(overlapping)
            )

        responses: List[ConflictDetectionResponse] = []
        req_duration_minutes = max(1, int((req_end - req_start).total_seconds() // 60))
        
        # Initialize BERT-powered SmartConflictDetector for enhanced reasoning
        bert_reasoning = None
        smart_detector = None
        try:
            if SmartConflictDetector:
                smart_detector = SmartConflictDetector(db)
                # Analyze the proposed event for priority insights
                event_data = {
                    'title': conflict_request.title,
                    'description': conflict_request.description or '',
                    'start_time': conflict_request.start_time.isoformat(),
                    'end_time': conflict_request.end_time.isoformat(),
                    'location': conflict_request.location
                }
                priority, ai_confidence = smart_detector._infer_event_priority_enhanced(event_data)
                bert_reasoning = {
                    'proposed_event_priority': priority,
                    'ai_confidence': ai_confidence,
                    'analysis_method': 'BERT' if smart_detector.use_bert else 'keyword_fallback'
                }
        except Exception as e:
            log.warning(f"BERT analysis failed: {e}, proceeding with basic detection")
        
        phase = "compute_overlaps"
        for ev in overlapping:
            # Ensure event times are coerced to naive for python-side comparison
            ev_start = ev.start_time.replace(tzinfo=None) if ev.start_time else None
            ev_end = ev.end_time.replace(tzinfo=None) if ev.end_time else None
            if not ev_start or not ev_end:
                continue
            overlap_minutes = _overlap_minutes((req_start, req_end), (ev_start, ev_end))
            if overlap_minutes <= 0:
                continue
                
            # Enhanced severity classification with BERT insights
            severity, impact = _classify_severity(overlap_minutes, req_duration_minutes, ev)
            
            # Generate reasoning for this conflict
            reasoning_parts = []
            existing_priority = getattr(ev, 'priority_level', 3)
            
            if bert_reasoning:
                proposed_priority = bert_reasoning['proposed_event_priority']
                if proposed_priority <= 2 and existing_priority <= 2:
                    reasoning_parts.append("High priority events conflicting")
                elif proposed_priority <= 2:
                    reasoning_parts.append(f"High priority proposed event conflicts with existing event")
                elif existing_priority <= 2:
                    reasoning_parts.append(f"Proposed event conflicts with high priority existing event")
                else:
                    reasoning_parts.append("Time overlap detected")
                    
                if overlap_minutes >= 30:
                    reasoning_parts.append("Significant overlap duration")
                elif overlap_minutes >= 15:
                    reasoning_parts.append("Moderate overlap duration")
                    
            # Enhanced priority analysis for conflicting events
            priority_analysis = {}
            if bert_reasoning:
                priority_analysis = {
                    'proposed_event': {
                        'priority': bert_reasoning['proposed_event_priority'],
                        'confidence': bert_reasoning['ai_confidence'],
                        'method': bert_reasoning['analysis_method']
                    },
                    'existing_event': {
                        'priority': existing_priority,
                        'title': ev.title,
                        'duration_minutes': int((ev_end - ev_start).total_seconds() / 60) if ev_end and ev_start else 0
                    }
                }
            
            responses.append(ConflictDetectionResponse(
                conflict_id=f"time-{str(ev.id)}",
                conflict_type=ConflictTypeEnum.TIME_OVERLAP,
                severity=severity,
                affected_event_ids=[str(ev.id)],
                description=f"Overlaps {overlap_minutes} min with '{ev.title}'",
                buffer_minutes=buf,
                confidence=0.7,
                impact_score=impact,
                priority_analysis=priority_analysis if priority_analysis else None,
                reasoning=reasoning_parts if reasoning_parts else None,
                ai_confidence=bert_reasoning['ai_confidence'] if bert_reasoning else None
            ))
        return ConflictCheckWrappedResponse(
            conflicts=responses,
            engine=engine_norm,
            correlation_id=_current_correlation_id()
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        tb = traceback.format_exc(limit=6)
        raise HTTPException(status_code=500, detail=f"Error detecting conflicts: {e} (phase={locals().get('phase','unknown')}) trace={tb}")

@router.post("/resolve", response_model=ConflictResolveWrappedResponse)
def resolve_conflicts(
    cognito_sub: str,
    conflict_request: ConflictCheckRequest,
    auto_resolve: bool = Query(False, description="Automatically select best resolution"),
    max_alternatives: int = Query(5, ge=1, le=10, description="Maximum alternatives to return"),
    engine: str = Query("fallback", description="Conflict engine: fallback|basic_v1"),
    db: Session = Depends(get_db)
):
    """
    Get intelligent resolutions for scheduling conflicts
    
    This endpoint first detects conflicts and then generates smart alternatives
    using AI-powered analysis of user behavior patterns.
    """
    try:
        user = get_user_from_cognito(cognito_sub, db)
        engine_norm = "basic_v1" if engine in ("fallback", "basic_v1") else None
        if engine_norm is None:
            raise HTTPException(status_code=400, detail=f"Unsupported engine '{engine}'. Use 'basic_v1' or 'fallback'.")

        # Reuse check logic to get conflicts (basic_v1)
        # Internally call detection logic directly (without wrapper) by reproducing minimal steps
        detection_wrapper = check_conflicts(
            cognito_sub=cognito_sub,
            conflict_request=conflict_request,
            engine="basic_v1",
            db=db,
        )
        checks = detection_wrapper.conflicts
        if not checks:
            return ConflictResolveWrappedResponse(resolutions=[], engine="basic_v1", correlation_id=_current_correlation_id())

        alts = _suggest_alternatives_basic_v1(user, conflict_request, checks, max_alternatives, db)
        auto = alts[0] if (auto_resolve and alts) else None
        return ConflictResolveWrappedResponse(
            resolutions=[
                ConflictResolutionResponse(
                    resolution_id="basic_v1",
                    conflict_id=checks[0].conflict_id,
                    alternatives=alts,
                    auto_resolution=auto,
                    strategy="nearest_free_slot",
                    confidence=0.7,
                    reasoning="Resolved by finding nearest non-overlapping slots respecting buffer"
                )
            ],
            engine=engine_norm,
            correlation_id=_current_correlation_id()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resolving conflicts: {e}")

def _generate_conflict_report(conflicts: List[Any]) -> Dict[str, Any]:
    """Lightweight conflict analysis fallback (no external dependency)."""
    total = len(conflicts)
    severity_breakdown: Dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    type_breakdown: Dict[str, int] = {}
    impact_scores: List[float] = []

    for c in conflicts:
        sev = getattr(c.severity, "value", str(c.severity)).lower()
        if sev in severity_breakdown:
            severity_breakdown[sev] += 1
        t = getattr(c.conflict_type, "value", str(c.conflict_type))
        type_breakdown[t] = type_breakdown.get(t, 0) + 1
        impact = getattr(c, "impact_score", None)
        if isinstance(impact, (int, float)):
            impact_scores.append(float(impact))

    avg_impact = sum(impact_scores) / len(impact_scores) if impact_scores else None

    recommendations: List[str] = []
    if severity_breakdown.get("high", 0) + severity_breakdown.get("critical", 0) > 0:
        recommendations.append("Prioritize high/critical conflicts first and consider rescheduling lower-priority events.")
    if type_breakdown.get("time_overlap", 0) > 0:
        recommendations.append("Increase buffer times around dense periods to reduce time overlaps.")
    if type_breakdown.get("priority_conflict", 0) > 0:
        recommendations.append("Use priority-based resolution to keep higher-priority events and move the others.")
    if not recommendations:
        recommendations.append("No significant conflicts detected; proceed with scheduling.")

    return {
        "total_conflicts": total,
        "severity_breakdown": severity_breakdown,
        "type_breakdown": type_breakdown,
        "average_impact_score": avg_impact,
        "recommendations": recommendations,
    }


@router.post("/analyze", response_model=ConflictReportResponse)
def analyze_conflicts(
    cognito_sub: str,
    conflict_request: ConflictCheckRequest,
    engine: str = Query("fallback", description="Conflict engine: fallback|basic_v1"),
    db: Session = Depends(get_db)
):
    """
    Generate comprehensive conflict analysis report
    
    This endpoint provides detailed analysis of conflicts including severity
    breakdown, impact assessment, and actionable recommendations.
    """
    try:
        _ = get_user_from_cognito(cognito_sub, db)
        if engine in ("fallback", "basic_v1"):
            wrapper = check_conflicts(cognito_sub, conflict_request, engine="basic_v1", db=db)
            conflicts_list = wrapper.conflicts
        else:
            conflicts_list = []
        # Map to minimal objects expected by report generator
        report = _generate_conflict_report(conflicts_list)  # type: ignore[arg-type]
        return ConflictReportResponse(**report)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing conflicts: {e}")

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
        
        # Initialize conflict detector (guard if unavailable)
        if not SmartConflictDetector:
            raise HTTPException(status_code=503, detail="Smart conflict detector engine not available")
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

        # Get historical events (last N days)
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
        
        # Analyze patterns using behavior analytics (best-effort)
        try:
            from app.nlp.user_behavior_analytics import UserBehaviorAnalyzer
            analyzer = UserBehaviorAnalyzer(db)
            # Use real events we already fetched for accuracy
            _ = analyzer._analyze_events(user_id=str(user.id), events=historical_events)
        except Exception:
            pass
        
        # Simple hotspot analysis by hour bucket of overlapping events within 15 minutes
        conflict_hotspots: Dict[int, int] = {}
        for event in historical_events[-50:]:  # Analyze last up to 50 events
            # Count any overlaps within +/- 15 minutes window
            window_start = event.start_time - timedelta(minutes=15)
            window_end = event.end_time + timedelta(minutes=15)
            overlaps = db.query(Event).filter(
                Event.user_id == user.id,
                Event.id != event.id,
                Event.start_time < window_end,
                Event.end_time > window_start,
            ).count()
            if overlaps > 0 and event.start_time:
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
        
        # Calculate event duration
        duration_minutes = int((event.end_time - event.start_time).total_seconds() / 60)
        
        # EMERGENCY FIX: Use simple, direct slot finding instead of complex analyzer
        # This ensures we find obvious available times today/tomorrow first
        
        conflict_free_alternatives = _find_simple_available_slots(
            user, event, duration_minutes, max_alternatives, db
        )
        
        # Fallback to original method if simple method fails
        if not conflict_free_alternatives:
            # Initialize behavior analyzer
            from app.nlp.user_behavior_analytics import UserBehaviorAnalyzer
            analyzer = UserBehaviorAnalyzer(db)

            # Generate smart alternatives using analyzer
            reference_dt = preferred_date or event.start_time
            suggestions = analyzer.suggest_optimal_time_slots(
                user_id=str(user.id),
                event_duration=duration_minutes,
                preferred_date=reference_dt,
                num_suggestions=max_alternatives * 2,
            )
            
            # Filter with no buffer
            for s in suggestions:
                overlap_count = db.query(Event).filter(
                    Event.user_id == user.id,
                    Event.id != event.id,
                    Event.start_time < s.end_time,
                    Event.end_time > s.start_time,
                ).count()
                
                if overlap_count == 0:
                    conflict_free_alternatives.append(TimeSlotAlternative(
                        start_time=s.start_time,
                        end_time=s.end_time,
                        confidence=s.confidence_score,
                        reasoning=s.reason,
                        productivity_score=None,
                    ))
                if len(conflict_free_alternatives) >= max_alternatives:
                    break
        
        # Convert to response format
        return {
            "event_id": str(event.id),
            "event_title": event.title,
            "current_time": {
                "start_time": event.start_time,
                "end_time": event.end_time
            },
            "alternatives": [a.dict() for a in conflict_free_alternatives],
            "recommendation": (conflict_free_alternatives[0].dict() if conflict_free_alternatives else None),
            "message": (
                f"Found {len(conflict_free_alternatives)} conflict-free alternatives"
                if conflict_free_alternatives else "No suitable alternatives found"
            )
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rescheduling event: {str(e)}"
        )

def _find_simple_available_slots(user, current_event, duration_minutes: int, max_alternatives: int, db) -> List[TimeSlotAlternative]:
    """
    EMERGENCY FIX: Simple, direct slot finding that prioritizes today/tomorrow
    """
    from datetime import timedelta
    
    alternatives = []
    now = datetime.now()
    
    # Priority dates: Today (if time left), Tomorrow, Day after tomorrow
    candidate_dates = []
    
    # Add today if there's time left (after current hour + 1)
    if now.hour < 20:  # Before 8 PM
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        candidate_dates.append(today)
    
    # Add next few business days
    for day_offset in range(1, 8):  # Check next 7 days
        candidate_date = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=day_offset)
        if candidate_date.weekday() < 5:  # Weekday only
            candidate_dates.append(candidate_date)
    
    # Try different time slots for each date
    time_slots = [9, 10, 11, 12, 13, 14, 15, 16, 17]  # 9 AM to 5 PM
    
    for check_date in candidate_dates:
        if len(alternatives) >= max_alternatives:
            break
            
        for hour in time_slots:
            if len(alternatives) >= max_alternatives:
                break
                
            slot_start = check_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            slot_end = slot_start + timedelta(minutes=duration_minutes)
            
            # Skip past times for today
            if check_date.date() == now.date() and slot_start <= now + timedelta(hours=1):
                continue
            
            # Check for conflicts - SMART: Ignore all-day events for regular time slots
            overlap_count = db.query(Event).filter(
                Event.user_id == user.id,
                Event.id != current_event.id,
                Event.is_all_day == False,  # Only check non-all-day events for conflicts
                Event.start_time < slot_end,
                Event.end_time > slot_start,
            ).count()
            
            if overlap_count == 0:
                # Calculate days from now
                days_away = (check_date.date() - now.date()).days
                
                if days_away == 0:
                    date_desc = "today"
                elif days_away == 1:
                    date_desc = "tomorrow"
                else:
                    date_desc = f"in {days_away} days"
                
                reason = f"Available slot {date_desc} at {slot_start.strftime('%I:%M %p')} - no conflicts detected"
                
                alternatives.append(TimeSlotAlternative(
                    start_time=slot_start,
                    end_time=slot_end,
                    confidence=1.0,
                    reasoning=reason,
                    productivity_score=None,
                ))
    
    return alternatives

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

# --- basic_v1 helpers ---

def _overlap_minutes(a: Tuple[datetime, datetime], b: Tuple[datetime, datetime]) -> int:
    # Assume all datetimes are naive UTC (tzinfo removed) before calling, but add guards.
    a0, a1 = a
    b0, b1 = b
    if (a0.tzinfo or a1.tzinfo or b0.tzinfo or b1.tzinfo):
        # Fallback to converting all to naive by dropping tzinfo
        a0 = a0.replace(tzinfo=None)
        a1 = a1.replace(tzinfo=None)
        b0 = b0.replace(tzinfo=None)
        b1 = b1.replace(tzinfo=None)
    try:
        start = max(a0, b0)
        end = min(a1, b1)
    except TypeError as te:  # Likely naive/aware mismatch scenario
        import logging
        log.warning("_overlap_minutes TypeError %s a0=%r a0.tz=%r b0=%r b0.tz=%r", te, a0, a0.tzinfo, b0, b0.tzinfo)
        # Convert via timestamp as last resort
        import math
        start_ts = max(a0.timestamp(), b0.timestamp())
        end_ts = min(a1.timestamp(), b1.timestamp())
        if end_ts <= start_ts:
            return 0
        return int(math.floor((end_ts - start_ts) / 60))
    if end <= start:
        return 0
    return int((end - start).total_seconds() // 60)

def _classify_severity(overlap_minutes: int, req_duration_minutes: int, ev: Event) -> Tuple[ConflictSeverityEnum, float]:
    duration = req_duration_minutes or 1
    ratio = overlap_minutes / max(duration, 1)
    # Priority difference (lower number = higher priority)
    ev_priority = getattr(ev, "priority_level", 3) or 3
    req_priority = 3  # unknown new event priority; assume medium
    diff = abs(req_priority - ev_priority)
    # Severity rules
    if ratio >= 0.75 or diff >= 3 or getattr(ev, "is_all_day", False):
        return (ConflictSeverityEnum.HIGH, min(1.0, 0.8 + ratio * 0.2))
    if ratio >= 0.4 or diff == 2:
        return (ConflictSeverityEnum.MEDIUM, 0.6 + ratio * 0.3)
    return (ConflictSeverityEnum.LOW, 0.4 + ratio * 0.4)

def _suggest_alternatives_basic_v1(
    user: User,
    req: ConflictCheckRequest,
    checks: List[ConflictDetectionResponse],
    max_alternatives: int,
    db: Session,
) -> List[TimeSlotAlternative]:
    from datetime import timedelta
    alts: List[TimeSlotAlternative] = []
    duration = req.end_time - req.start_time
    buf = req.buffer_minutes or 0

    # Search window: +/- a few hours, then next day same slot
    offsets = [timedelta(hours=h) for h in (-2, -1, 1, 2, 3, 4)] + [timedelta(days=1), timedelta(days=2)]
    for off in offsets:
        s = req.start_time + off
        e = s + duration
        # Quick overlap check with DB
        s_buf = s - timedelta(minutes=buf)
        e_buf = e + timedelta(minutes=buf)
        overlap_count = db.query(Event).filter(
            Event.user_id == user.id,
            Event.start_time < e_buf,
            Event.end_time > s_buf,
        ).count()
        if overlap_count == 0:
            alts.append(TimeSlotAlternative(
                start_time=s,
                end_time=e,
                confidence=0.7,
                reasoning="No overlaps found in window",
                productivity_score=None,
            ))
        if len(alts) >= max_alternatives:
            break
    return alts