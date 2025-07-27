# backend/app/api/reminders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.reminder import Reminder
from app.models.event import Event
from app.models.user import User
from app.schemas import ReminderCreate, ReminderResponse
from uuid import UUID

router = APIRouter(prefix="/api/v1/reminders", tags=["reminders"])

def get_user_from_cognito(cognito_sub: str, db: Session) -> User:
    """Helper function to get user from Cognito sub ID"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User profile not found. Please create your profile first."
        )
    return user

def verify_event_ownership(event_id: UUID, user: User, db: Session) -> Event:
    """Helper function to verify user owns the event"""
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

@router.post("/{event_id}", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_reminder(
    event_id: UUID,
    cognito_sub: str,
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db)
):
    """Create a new reminder for an event"""
    user = get_user_from_cognito(cognito_sub, db)
    
    # Verify user owns the event
    event = verify_event_ownership(event_id, user, db)
    
    # Create reminder
    reminder = Reminder(**reminder_data.dict(), event_id=event.id)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

@router.get("/", response_model=List[ReminderResponse])
def list_my_reminders(
    cognito_sub: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all reminders for the user's events"""
    user = get_user_from_cognito(cognito_sub, db)
    
    # Get reminders for all user's events
    reminders = db.query(Reminder).join(Event).filter(
        Event.user_id == user.id
    ).offset(skip).limit(limit).all()
    
    return reminders

@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: UUID,
    cognito_sub: str,
    db: Session = Depends(get_db)
):
    """Get a specific reminder (only if user owns the associated event)"""
    user = get_user_from_cognito(cognito_sub, db)
    
    # Get reminder and verify ownership through event
    reminder = db.query(Reminder).join(Event).filter(
        Reminder.id == reminder_id,
        Event.user_id == user.id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found or you don't have permission to access it"
        )
    
    return reminder

@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: UUID,
    cognito_sub: str,
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db)
):
    """Update a reminder (only if user owns the associated event)"""
    user = get_user_from_cognito(cognito_sub, db)
    
    # Get reminder and verify ownership
    reminder = db.query(Reminder).join(Event).filter(
        Reminder.id == reminder_id,
        Event.user_id == user.id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found or you don't have permission to modify it"
        )
    
    # Update reminder fields
    for field, value in reminder_data.dict(exclude_unset=True).items():
        setattr(reminder, field, value)
    
    db.commit()
    db.refresh(reminder)
    return reminder

@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: UUID,
    cognito_sub: str,
    db: Session = Depends(get_db)
):
    """Delete a reminder (only if user owns the associated event)"""
    user = get_user_from_cognito(cognito_sub, db)
    
    # Get reminder and verify ownership
    reminder = db.query(Reminder).join(Event).filter(
        Reminder.id == reminder_id,
        Event.user_id == user.id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found or you don't have permission to delete it"
        )
    
    db.delete(reminder)
    db.commit()
    return {"message": "Reminder deleted successfully"}

@router.patch("/{reminder_id}/mark-sent")
def mark_reminder_sent(
    reminder_id: UUID,
    cognito_sub: str,
    db: Session = Depends(get_db)
):
    """Mark a reminder as sent (for notification system)"""
    user = get_user_from_cognito(cognito_sub, db)
    
    # Get reminder and verify ownership
    reminder = db.query(Reminder).join(Event).filter(
        Reminder.id == reminder_id,
        Event.user_id == user.id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found or you don't have permission to modify it"
        )
    
    reminder.is_sent = True
    db.commit()
    db.refresh(reminder)
    return {"message": "Reminder marked as sent", "reminder": reminder}