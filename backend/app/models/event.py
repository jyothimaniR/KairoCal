# backend/app/models/event.py
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Integer, Float
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
    
    # Priority classification fields
    priority_level = Column(Integer, default=3, nullable=False)  # Default: Medium
    priority_confidence = Column(Float, default=0.0, nullable=False)
    classification_method = Column(String(50), default='manual', nullable=False)  # manual, bert, rule_based
    
    # Analytics fields for productivity insights
    meeting_outcome = Column(String(50), default='neutral', nullable=False)  # productive, waste, neutral
    effectiveness_rating = Column(Integer, default=3, nullable=False)  # 1-5 scale
    energy_level = Column(Integer, default=3, nullable=False)  # 1-5 scale
    created_via = Column(String(20), default='manual', nullable=False)  # voice, text, manual, imported
    actual_duration = Column(Integer, nullable=True)  # Actual duration in minutes
    planned_duration = Column(Integer, nullable=True)  # Planned duration in minutes
    
    # Relationships
    user = relationship("User", back_populates="events")
    reminders = relationship("Reminder", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Event(title='{self.title}', start_time='{self.start_time}')>"