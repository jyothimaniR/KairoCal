from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = Field(None, max_length=255)
    is_all_day: bool = False
    recurrence_rule: Optional[str] = Field(None, max_length=255)
    priority_level: Optional[int] = Field(3, ge=1, le=5)  # 1=Very Low, 2=Low, 3=Medium, 4=High, 5=Critical
    priority_confidence: Optional[float] = Field(0.0, ge=0.0, le=1.0)
    classification_method: Optional[str] = Field('manual', max_length=50)
    
    # Analytics fields for productivity insights
    meeting_outcome: Optional[str] = Field('neutral', pattern='^(productive|waste|neutral)$')
    effectiveness_rating: Optional[int] = Field(3, ge=1, le=5)  # 1-5 scale
    energy_level: Optional[int] = Field(3, ge=1, le=5)  # 1-5 scale  
    created_via: Optional[str] = Field('manual', pattern='^(voice|text|manual|imported)$')
    actual_duration: Optional[int] = Field(None, ge=0)  # Actual duration in minutes
    planned_duration: Optional[int] = Field(None, ge=0)  # Planned duration in minutes

    @validator("end_time")
    def end_time_must_be_after_start_time(cls, v, values):
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v

class EventCreate(EventBase):
    # Make priority fields optional for creation
    priority_level: Optional[int] = Field(None, ge=1, le=5)
    priority_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    classification_method: Optional[str] = Field(None, max_length=50)
    
    # Analytics fields optional for creation
    meeting_outcome: Optional[str] = Field(None, pattern='^(productive|waste|neutral)$')
    effectiveness_rating: Optional[int] = Field(None, ge=1, le=5)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    created_via: Optional[str] = Field(None, pattern='^(voice|text|manual|imported)$')
    actual_duration: Optional[int] = Field(None, ge=0)
    planned_duration: Optional[int] = Field(None, ge=0)

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=255)
    is_all_day: Optional[bool] = None
    recurrence_rule: Optional[str] = Field(None, max_length=255)
    priority_level: Optional[int] = Field(None, ge=1, le=5)
    priority_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    classification_method: Optional[str] = Field(None, max_length=50)
    
    # Analytics fields for updates
    meeting_outcome: Optional[str] = Field(None, pattern='^(productive|waste|neutral)$')
    effectiveness_rating: Optional[int] = Field(None, ge=1, le=5)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    created_via: Optional[str] = Field(None, pattern='^(voice|text|manual|imported)$')
    actual_duration: Optional[int] = Field(None, ge=0)
    planned_duration: Optional[int] = Field(None, ge=0)

class EventResponse(EventBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReminderBase(BaseModel):
    minutes_before: int = Field(..., ge=0)
    notification_type: str = Field(default="in_app")

class ReminderCreate(ReminderBase):
    pass

class ReminderResponse(ReminderBase):
    id: UUID
    event_id: UUID
    is_sent: bool
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class EventWithReminders(EventResponse):
    reminders: List[ReminderResponse] = []
    model_config = ConfigDict(from_attributes=True)