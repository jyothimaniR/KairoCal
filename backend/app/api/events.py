# backend/app/api/events.py - Updated with Authentication
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.event import Event
from app.models.user import User
from app.schemas import EventCreate, EventUpdate, EventResponse, EventWithReminders
from uuid import UUID

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
def create_event(
    event_data: EventCreate, 
    db: Session = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new event for the authenticated user"""
    user = get_user_from_cognito(current_user["cognito_sub"], db)
    
    # Create event associated with the authenticated user
    event = Event(**event_data.dict(), user_id=user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/", response_model=List[EventResponse])
def list_my_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List all events for the authenticated user"""
    user = get_user_from_cognito(current_user["cognito_sub"], db)
    
    # Query events only for the authenticated user
    query = db.query(Event).filter(Event.user_id == user.id)
    
    # Apply date filters if provided
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.end_time <= end_date)
    
    events = query.offset(skip).limit(limit).all()
    return events

@router.get("/{event_id}", response_model=EventWithReminders)
def get_event(
    event_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific event (only if it belongs to the authenticated user)"""
    user = get_user_from_cognito(current_user["cognito_sub"], db)
    
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
    event_data: EventUpdate, 
    db: Session = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update an event (only if it belongs to the authenticated user)"""
    user = get_user_from_cognito(current_user["cognito_sub"], db)
    
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
    db: Session = Depends(get_db), 
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete an event (only if it belongs to the authenticated user)"""
    user = get_user_from_cognito(current_user["cognito_sub"], db)
    
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