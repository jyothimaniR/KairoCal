# backend/app/models/reminder.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models import BaseModel, GUID

class Reminder(BaseModel):
    """Reminder model for event notifications"""
    __tablename__ = "reminders"
    
    # Foreign key to event
    event_id = Column(GUID(), ForeignKey("events.id"), nullable=False, index=True)
    
    # Reminder timing (minutes before event)
    minutes_before = Column(Integer, nullable=False)
    
    # Notification type
    notification_type = Column(String(50), default="in_app", nullable=False)
    # Types: 'in_app', 'email', 'sms'
    
    # Status tracking
    is_sent = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="reminders")
    
    def __repr__(self):
        return f"<Reminder(event_id='{self.event_id}', minutes_before={self.minutes_before})>"