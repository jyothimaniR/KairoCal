from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class EventBase(BaseModel):
    """Base event schema with common fields"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = Field(None, max_length=255)
    is_all_day: bool = False
    recurrence_rule: Optional[str] = Field(None, max_length=255)

    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        """Ensure end time is after start time"""
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class EventCreate(EventBase):
    """Schema for creating a new event"""
    pass

class EventUpdate(BaseModel):
    """Schema for updating an event"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=255)
    is_all_day: Optional[bool] = None
    recurrence_rule: Optional[str] = Field(None, max_length=255)

class EventResponse(EventBase):
    """Schema for event response (what we return to client)"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventInDB(EventResponse):
    """Schema for event as stored in database (internal use)"""
    pass

# Reminder schemas (nested in event responses)
class ReminderBase(BaseModel):
    """Base reminder schema"""
    minutes_before: int = Field(..., ge=0, description="Minutes before event to remind")
    notification_type: str = Field(default="in_app", pattern="^(in_app|email|sms)$")

class ReminderCreate(ReminderBase):
    """Schema for creating a reminder"""
    pass

class ReminderResponse(ReminderBase):
    """Schema for reminder response"""
    id: UUID
    event_id: UUID
    is_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Event with reminders
class EventWithReminders(EventResponse):
    """Event response including reminders"""
    reminders: List[ReminderResponse] = []