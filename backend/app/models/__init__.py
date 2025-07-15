# backend/app/models/__init__.py
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class BaseModel(Base):
    """Base model class with common fields for all models"""
    __abstract__ = True
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

# Import all models in correct order to ensure proper relationship resolution
from .user import User
from .event import Event  
from .reminder import Reminder

# Make them available for imports
__all__ = ["BaseModel", "User", "Event", "Reminder"]