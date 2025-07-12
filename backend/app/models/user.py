# backend/app/models/user.py
from sqlalchemy import Column, String, JSON, Boolean
from sqlalchemy.orm import relationship
from app.models import BaseModel

class User(BaseModel):
    """User model linked to AWS Cognito"""
    __tablename__ = "users"
    
    # Cognito identifier (unique)
    cognito_sub = Column(String(255), unique=True, nullable=False, index=True)
    
    # User information
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    
    # User preferences stored as JSON
    preferences = Column(JSON, default=dict)
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(email='{self.email}', full_name='{self.full_name}')>"