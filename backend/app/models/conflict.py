# backend/app/models/conflict.py
"""
Conflict model for persistent conflict tracking and analytics
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class Conflict(Base):
    """
    Represents a detected scheduling conflict with full analytics
    """
    __tablename__ = "conflicts"

    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    primary_event_id = Column(String(36), ForeignKey('events.id'), nullable=True)
    conflicting_event_id = Column(String(36), ForeignKey('events.id'), nullable=True)
    
    # Conflict metadata
    conflict_type = Column(String(50), nullable=False)  # time_overlap, location_conflict, etc.
    severity = Column(String(20), nullable=False)       # low, medium, high, critical
    confidence = Column(Float, nullable=False, default=0.0)  # 0.0 to 1.0
    impact_score = Column(Float, nullable=False, default=0.0)  # 0.0 to 1.0
    
    # Conflict details
    description = Column(Text, nullable=True)
    conflict_start_time = Column(DateTime, nullable=True)
    conflict_end_time = Column(DateTime, nullable=True)
    overlap_minutes = Column(Integer, nullable=True)
    buffer_minutes = Column(Integer, default=15)
    
    # BERT Analysis
    bert_analysis = Column(JSON, nullable=True)  # Store BERT reasoning and confidence
    priority_analysis = Column(JSON, nullable=True)  # Priority comparison data
    
    # Resolution tracking
    is_resolved = Column(Boolean, default=False, nullable=False)
    resolution_method = Column(String(50), nullable=True)  # manual, auto_reschedule, ignored
    resolution_timestamp = Column(DateTime, nullable=True)
    alternative_suggestions = Column(JSON, nullable=True)  # Store suggested alternatives
    
    # System metadata
    detection_method = Column(String(50), default='basic_v1')  # basic_v1, bert_enhanced, etc.
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="conflicts")
    primary_event = relationship("Event", foreign_keys=[primary_event_id])
    conflicting_event = relationship("Event", foreign_keys=[conflicting_event_id])
    
    def __repr__(self):
        return f"<Conflict(id='{self.id}', type='{self.conflict_type}', severity='{self.severity}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'primary_event_id': self.primary_event_id,
            'conflicting_event_id': self.conflicting_event_id,
            'conflict_type': self.conflict_type,
            'severity': self.severity,
            'confidence': self.confidence,
            'impact_score': self.impact_score,
            'description': self.description,
            'conflict_start_time': self.conflict_start_time.isoformat() if self.conflict_start_time else None,
            'conflict_end_time': self.conflict_end_time.isoformat() if self.conflict_end_time else None,
            'overlap_minutes': self.overlap_minutes,
            'buffer_minutes': self.buffer_minutes,
            'bert_analysis': self.bert_analysis,
            'priority_analysis': self.priority_analysis,
            'is_resolved': self.is_resolved,
            'resolution_method': self.resolution_method,
            'resolution_timestamp': self.resolution_timestamp.isoformat() if self.resolution_timestamp else None,
            'alternative_suggestions': self.alternative_suggestions,
            'detection_method': self.detection_method,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

class ConflictResolution(Base):
    """
    Track conflict resolution attempts and outcomes
    """
    __tablename__ = "conflict_resolutions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conflict_id = Column(String(36), ForeignKey('conflicts.id'), nullable=False)
    
    # Resolution details
    resolution_type = Column(String(50), nullable=False)  # reschedule, priority_change, ignore
    old_start_time = Column(DateTime, nullable=True)
    old_end_time = Column(DateTime, nullable=True)
    new_start_time = Column(DateTime, nullable=True)
    new_end_time = Column(DateTime, nullable=True)
    
    # Success tracking
    was_successful = Column(Boolean, default=False)
    user_accepted = Column(Boolean, default=False)
    auto_applied = Column(Boolean, default=False)
    
    # Analytics
    resolution_confidence = Column(Float, nullable=True)
    alternatives_offered = Column(Integer, default=0)
    user_choice_index = Column(Integer, nullable=True)  # Which alternative was chosen
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    conflict = relationship("Conflict")
    
    def to_dict(self):
        return {
            'id': self.id,
            'conflict_id': self.conflict_id,
            'resolution_type': self.resolution_type,
            'old_start_time': self.old_start_time.isoformat() if self.old_start_time else None,
            'old_end_time': self.old_end_time.isoformat() if self.old_end_time else None,
            'new_start_time': self.new_start_time.isoformat() if self.new_start_time else None,
            'new_end_time': self.new_end_time.isoformat() if self.new_end_time else None,
            'was_successful': self.was_successful,
            'user_accepted': self.user_accepted,
            'auto_applied': self.auto_applied,
            'resolution_confidence': self.resolution_confidence,
            'alternatives_offered': self.alternatives_offered,
            'user_choice_index': self.user_choice_index,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
