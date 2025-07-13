from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.event import Event
from app.schemas import EventCreate, EventUpdate, EventResponse, EventWithReminders
from uuid import UUID

router = APIRouter(prefix="/api/v1/events", tags=["events"])

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, user_id: UUID, db: Session = Depends(get_db)):
    """Create a new event"""
    # Create new event
    event = Event(**event_data.dict(), user_id=user_id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/{event_id}", response_model=EventWithReminders)
def get_event(event_id: UUID, db: Session = Depends(get_db)):
    """Get event by ID with reminders"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@router.get("/", response_model=List[EventResponse])
def list_events(
    user_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List events with optional filtering"""
    query = db.query(Event)
    
    if user_id:
        query = query.filter(Event.user_id == user_id)
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.end_time <= end_date)
    
    events = query.offset(skip).limit(limit).all()
    return events

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: UUID, event_data: EventUpdate, db: Session = Depends(get_db)):
    """Update event information"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Update event fields
    for field, value in event_data.dict(exclude_unset=True).items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}")
def delete_event(event_id: UUID, db: Session = Depends(get_db)):
    """Delete event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}
