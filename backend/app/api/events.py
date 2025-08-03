# backend/app/api/events.py - Enhanced with Real-time WebSocket Broadcasting
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging
import asyncio

from app.core.database import get_db
from app.models.event import Event
from app.models.user import User
from app.schemas import EventCreate, EventUpdate, EventResponse, EventWithReminders
from uuid import UUID

# Import BERT integration components
from app.nlp.nlp_service import NLPService

# Import WebSocket server for real-time broadcasting
from app.websocket.ultimate_socket_server import get_socket_server

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/events", tags=["events"])

def get_user_from_cognito(cognito_sub: str, db: Session) -> User:
    """Helper function to get user from Cognito sub ID"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User profile not found. Please create your profile first using POST /api/v1/users/"
        )
    return user

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    cognito_sub: str,
    event_data: EventCreate, 
    auto_classify_priority: bool = Query(True, description="Automatically classify event priority using BERT"),
    db: Session = Depends(get_db)
):
    """
    Create a new event for the specified user with optional BERT priority classification
    Enhanced with real-time WebSocket broadcasting
    
    Args:
        cognito_sub: User's Cognito sub ID
        event_data: Event creation data
        auto_classify_priority: Whether to automatically classify priority using BERT
        db: Database session
        
    Returns:
        Created event with priority classification and real-time notifications
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    # Convert to dict for processing
    event_dict = event_data.dict()
    
    # Auto-classify priority if requested and not already specified
    priority_classification_data = {}
    
    if auto_classify_priority and (not event_data.priority_level or event_data.priority_level == 3):
        try:
            logger.info(f"🤖 Auto-classifying priority for event: {event_data.title}")
            
            # Initialize NLP service for priority classification
            nlp_service = NLPService()
            
            # Classify priority
            priority, confidence, method = nlp_service.classify_priority(event_dict)
            
            # Update event data with classification results
            event_dict.update({
                'priority_level': priority,
                'priority_confidence': confidence,
                'classification_method': method
            })
            
            # Prepare priority classification data for WebSocket broadcast
            priority_classification_data = {
                'priority': priority,
                'confidence': confidence,
                'method': method,
                'event_text': f"{event_data.title} - {event_data.description or ''}",
                'original_priority': event_data.priority_level,
                'classification_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Priority classified: {priority} (confidence: {confidence:.3f}, method: {method})")
            
        except Exception as e:
            logger.error(f"❌ Priority classification failed: {str(e)}")
            # Set default values if classification fails
            event_dict.update({
                'priority_level': event_data.priority_level or 3,
                'priority_confidence': 0.0,
                'classification_method': 'fallback'
            })
    else:
        # Use provided values or defaults
        event_dict.update({
            'priority_level': event_data.priority_level or 3,
            'priority_confidence': event_data.priority_confidence or 0.0,
            'classification_method': event_data.classification_method or 'manual'
        })
    
    # Create event associated with the user
    event = Event(**event_dict, user_id=user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    
    logger.info(f"📅 Event created: {event.title} (Priority: {event.priority_level})")
    
    # Real-time WebSocket Broadcasting
    try:
        socket_server = await get_socket_server()
        
        # Prepare event data for broadcasting
        event_broadcast_data = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'start_time': event.start_time.isoformat() if event.start_time else None,
            'end_time': event.end_time.isoformat() if event.end_time else None,
            'location': event.location,
            'priority_level': event.priority_level,
            'priority_confidence': event.priority_confidence,
            'classification_method': event.classification_method,
            'user_id': user.id,
            'created_at': event.created_at.isoformat() if event.created_at else None,
            'event_type': 'event_creation'
        }
        
        # Broadcast event creation to user's connected devices
        await socket_server.broadcast_event_created(event_broadcast_data)
        
        # If priority was classified using BERT/AI, broadcast priority classification
        if priority_classification_data:
            await socket_server.broadcast_priority_classified(user.id, priority_classification_data)
        
        logger.info(f"🔔 Real-time notifications sent for event: {event.title}")
        
    except Exception as e:
        logger.error(f"❌ WebSocket broadcasting failed: {e}")
        # Continue anyway - event was created successfully
    
    return event

@router.get("/", response_model=List[EventResponse])
def list_my_events(
    cognito_sub: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_priority: Optional[int] = Query(None, ge=1, le=5, description="Minimum priority level (1=Critical, 5=Very Low)"),
    max_priority: Optional[int] = Query(None, ge=1, le=5, description="Maximum priority level (1=Critical, 5=Very Low)"),
    priority_levels: Optional[List[int]] = Query(None, description="Specific priority levels to include"),
    classification_method: Optional[str] = Query(None, description="Filter by classification method (bert, rule_based, manual)"),
    include_priority_stats: bool = Query(False, description="Include priority distribution statistics"),
    sort_by: str = Query("start_time", description="Sort by: start_time, priority, confidence"),
    sort_order: str = Query("asc", description="Sort order: asc, desc"),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    List events for the specified user with enhanced priority filtering and statistics
    
    Enhanced features:
    - Filter by priority ranges or specific levels
    - Filter by classification method (BERT vs manual vs rule-based)
    - Sort by priority, confidence, or time
    - Include priority distribution statistics
    - BERT-enhanced metadata in responses
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    # Query events only for the user
    query = db.query(Event).filter(Event.user_id == user.id)
    
    # Apply date filters if provided
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.end_time <= end_date)
    
    # Apply priority filters
    if min_priority is not None:
        query = query.filter(Event.priority_level >= min_priority)
    
    if max_priority is not None:
        query = query.filter(Event.priority_level <= max_priority)
    
    if priority_levels:
        query = query.filter(Event.priority_level.in_(priority_levels))
    
    if classification_method:
        query = query.filter(Event.classification_method == classification_method)
    
    # Apply sorting
    if sort_by == "priority":
        if sort_order == "desc":
            query = query.order_by(Event.priority_level.desc())
        else:
            query = query.order_by(Event.priority_level.asc())
    elif sort_by == "confidence":
        if sort_order == "desc":
            query = query.order_by(Event.priority_confidence.desc())
        else:
            query = query.order_by(Event.priority_confidence.asc())
    else:  # default to start_time
        if sort_order == "desc":
            query = query.order_by(Event.start_time.desc())
        else:
            query = query.order_by(Event.start_time.asc())
    
    # Get total count for pagination info
    total_count = query.count()
    
    # Apply pagination
    events = query.offset(skip).limit(limit).all()
    
    # Calculate priority statistics if requested
    if include_priority_stats:
        priority_stats = _calculate_priority_statistics(user.id, db, start_date, end_date)
        
        # Add statistics to response headers (or return as metadata)
        # For now, log the statistics
        logger.info(f"📊 Priority statistics for user {user.id}: {priority_stats}")
    
    logger.info(f"📋 Retrieved {len(events)} events (filtered from {total_count} total) for user {user.id}")
    
    return events

@router.get("/{event_id}", response_model=EventWithReminders)
def get_event(
    event_id: UUID, 
    cognito_sub: str,
    db: Session = Depends(get_db)
):
    """Get a specific event (only if it belongs to the specified user)"""
    user = get_user_from_cognito(cognito_sub, db)
    
    event = db.query(Event).filter(
        Event.id == event_id, 
        Event.user_id == user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Event not found or you don't have permission to access it"
        )
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: UUID, 
    cognito_sub: str,
    event_data: EventUpdate, 
    db: Session = Depends(get_db)
):
    """Update an event (only if it belongs to the specified user)"""
    user = get_user_from_cognito(cognito_sub, db)
    
    event = db.query(Event).filter(
        Event.id == event_id, 
        Event.user_id == user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Event not found or you don't have permission to modify it"
        )
    
    # Update event fields
    for field, value in event_data.dict(exclude_unset=True).items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}")
def delete_event(
    event_id: UUID, 
    cognito_sub: str,
    db: Session = Depends(get_db)
):
    """Delete an event (only if it belongs to the specified user)"""
    user = get_user_from_cognito(cognito_sub, db)
    
    event = db.query(Event).filter(
        Event.id == event_id, 
        Event.user_id == user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Event not found or you don't have permission to delete it"
        )
    
    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}

# Helper Functions
def _calculate_priority_statistics(user_id: int, db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> dict:
    """Calculate priority distribution statistics for a user's events"""
    query = db.query(Event).filter(Event.user_id == user_id)
    
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.end_time <= end_date)
    
    events = query.all()
    total_events = len(events)
    
    if total_events == 0:
        return {"total_events": 0, "priority_distribution": {}, "classification_stats": {}}
    
    # Priority distribution
    priority_counts = {}
    method_counts = {}
    confidence_stats = {}
    
    for event in events:
        priority = event.priority_level or 3
        method = event.classification_method or 'unknown'
        confidence = event.priority_confidence or 0.0
        
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        method_counts[method] = method_counts.get(method, 0) + 1
        
        if priority not in confidence_stats:
            confidence_stats[priority] = []
        confidence_stats[priority].append(confidence)
    
    # Calculate average confidence per priority level
    avg_confidence = {}
    for priority, confidences in confidence_stats.items():
        avg_confidence[priority] = sum(confidences) / len(confidences) if confidences else 0.0
    
    return {
        "total_events": total_events,
        "priority_distribution": {
            str(p): {"count": priority_counts.get(p, 0), "percentage": round(priority_counts.get(p, 0) / total_events * 100, 1)}
            for p in [1, 2, 3, 4, 5]
        },
        "classification_stats": {
            method: {"count": count, "percentage": round(count / total_events * 100, 1)}
            for method, count in method_counts.items()
        },
        "average_confidence_by_priority": {
            str(p): round(avg_confidence.get(p, 0.0), 3) for p in [1, 2, 3, 4, 5]
        },
        "bert_classification_rate": round(method_counts.get('bert', 0) / total_events * 100, 1)
    }

# New Priority-Focused Endpoints

@router.get("/priority/statistics", response_model=dict)
def get_priority_statistics(
    cognito_sub: str,
    start_date: Optional[datetime] = Query(None, description="Start date for statistics"),
    end_date: Optional[datetime] = Query(None, description="End date for statistics"),
    db: Session = Depends(get_db)
):
    """
    Get detailed priority classification statistics for user's events
    
    Returns:
        Comprehensive statistics about priority distribution, classification methods,
        BERT performance, and confidence scores
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    stats = _calculate_priority_statistics(user.id, db, start_date, end_date)
    
    logger.info(f"📊 Priority statistics requested for user {user.id}")
    return {
        "user_id": user.id,
        "period": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        },
        "statistics": stats
    }

@router.get("/priority/high-priority", response_model=List[EventResponse])
def get_high_priority_events(
    cognito_sub: str,
    max_priority: int = Query(2, ge=1, le=5, description="Maximum priority level (1=Critical, 2=High)"),
    limit: int = Query(50, description="Maximum number of events to return"),
    include_upcoming_only: bool = Query(True, description="Include only upcoming events"),
    db: Session = Depends(get_db)
):
    """
    Get high-priority events (Priority 1-2) for immediate attention
    
    Useful for:
    - Dashboard priority widgets
    - Mobile app quick views
    - Urgent task notifications
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    query = db.query(Event).filter(
        Event.user_id == user.id,
        Event.priority_level <= max_priority
    )
    
    if include_upcoming_only:
        query = query.filter(Event.start_time >= datetime.now())
    
    events = query.order_by(Event.priority_level.asc(), Event.start_time.asc()).limit(limit).all()
    
    logger.info(f"🔴 Retrieved {len(events)} high-priority events (≤P{max_priority}) for user {user.id}")
    return events

@router.get("/priority/low-confidence", response_model=List[EventResponse])
def get_low_confidence_classifications(
    cognito_sub: str,
    max_confidence: float = Query(0.6, ge=0.0, le=1.0, description="Maximum confidence threshold"),
    limit: int = Query(20, description="Maximum number of events to return"),
    db: Session = Depends(get_db)
):
    """
    Get events with low classification confidence for manual review
    
    Useful for:
    - Quality assurance of BERT classifications
    - Training data improvement
    - Manual verification workflows
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    events = db.query(Event).filter(
        Event.user_id == user.id,
        Event.priority_confidence <= max_confidence,
        Event.classification_method == 'bert'
    ).order_by(Event.priority_confidence.asc()).limit(limit).all()
    
    logger.info(f"🤔 Retrieved {len(events)} low-confidence classifications (≤{max_confidence}) for user {user.id}")
    return events

@router.post("/{event_id}/reclassify", response_model=EventResponse)
def reclassify_event_priority(
    event_id: UUID,
    cognito_sub: str,
    force_bert: bool = Query(False, description="Force BERT reclassification even if already classified"),
    db: Session = Depends(get_db)
):
    """
    Reclassify an event's priority using the latest BERT model
    
    Useful for:
    - Updating classifications after model improvements
    - Fixing incorrect classifications
    - Batch reclassification workflows
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.user_id == user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found or you don't have permission to access it"
        )
    
    # Skip if already classified by BERT and not forcing
    if not force_bert and event.classification_method == 'bert' and event.priority_confidence > 0.7:
        logger.info(f"⏭️ Skipping reclassification for high-confidence BERT event: {event.title}")
        return event
    
    try:
        logger.info(f"🔄 Reclassifying event priority: {event.title}")
        
        # Initialize NLP service
        nlp_service = NLPService()
        
        # Create event data for classification
        event_data = {
            'title': event.title,
            'description': event.description or '',
            'location': event.location or ''
        }
        
        # Classify priority
        priority, confidence, method = nlp_service.classify_priority(event_data)
        
        # Update event
        event.priority_level = priority
        event.priority_confidence = confidence
        event.classification_method = method
        
        db.commit()
        db.refresh(event)
        
        logger.info(f"✅ Event reclassified: {event.title} -> P{priority} (confidence: {confidence:.3f}, method: {method})")
        return event
        
    except Exception as e:
        logger.error(f"❌ Reclassification failed for event {event.title}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Priority reclassification failed: {str(e)}"
        )

@router.get("/priority/conflicts", response_model=dict)
def detect_priority_conflicts(
    cognito_sub: str,
    start_date: Optional[datetime] = Query(None, description="Start date for conflict detection"),
    end_date: Optional[datetime] = Query(None, description="End date for conflict detection"),
    min_priority_diff: int = Query(2, description="Minimum priority difference to consider as conflict"),
    db: Session = Depends(get_db)
):
    """
    Detect scheduling conflicts between events with different priorities
    
    Useful for:
    - Identifying scheduling optimization opportunities
    - Priority-based conflict resolution
    - Calendar efficiency analysis
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    # Get events in the specified period
    query = db.query(Event).filter(Event.user_id == user.id)
    
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.end_time <= end_date)
    
    events = query.order_by(Event.start_time).all()
    
    # Detect overlapping events with priority differences
    conflicts = []
    
    for i, event1 in enumerate(events):
        for event2 in events[i+1:]:
            # Check for time overlap
            if (event1.start_time < event2.end_time and event1.end_time > event2.start_time):
                priority_diff = abs((event1.priority_level or 3) - (event2.priority_level or 3))
                
                if priority_diff >= min_priority_diff:
                    conflicts.append({
                        "event1": {
                            "id": str(event1.id),
                            "title": event1.title,
                            "priority": event1.priority_level,
                            "start_time": event1.start_time.isoformat(),
                            "end_time": event1.end_time.isoformat()
                        },
                        "event2": {
                            "id": str(event2.id),
                            "title": event2.title,
                            "priority": event2.priority_level,
                            "start_time": event2.start_time.isoformat(),
                            "end_time": event2.end_time.isoformat()
                        },
                        "priority_difference": priority_diff,
                        "overlap_duration_minutes": int((min(event1.end_time, event2.end_time) - max(event1.start_time, event2.start_time)).total_seconds() / 60),
                        "recommendation": "Consider rescheduling lower priority event" if priority_diff >= 2 else "Review scheduling manually"
                    })
    
    logger.info(f"⚡ Detected {len(conflicts)} priority conflicts for user {user.id}")
    
    return {
        "user_id": user.id,
        "period": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        },
        "conflicts_detected": len(conflicts),
        "conflicts": conflicts,
        "summary": {
            "total_events_analyzed": len(events),
            "conflicts_requiring_attention": len([c for c in conflicts if c["priority_difference"] >= 3]),
            "average_priority_difference": round(sum(c["priority_difference"] for c in conflicts) / len(conflicts), 1) if conflicts else 0
        }
    }