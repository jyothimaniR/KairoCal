# backend/app/models/event.py
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models import BaseModel

class Event(BaseModel):
    """Event model for calendar events"""
    __tablename__ = "events"
    
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Event details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Event timing
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False, index=True)
    is_all_day = Column(Boolean, default=False, nullable=False)
    
    # Event location
    location = Column(String(255), nullable=True)
    
    # Recurrence rule (for repeating events)
    recurrence_rule = Column(String(255), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="events")
    reminders = relationship("Reminder", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Event(title='{self.title}', start_time='{self.start_time}')>"