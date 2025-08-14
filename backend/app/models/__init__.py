# backend/app/models/__init__.py
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import types
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class GUID(types.TypeDecorator):
    """Portable GUID/UUID column.
    Uses native PostgreSQL UUID; stores as CHAR(36) elsewhere."""
    impl = types.CHAR
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(types.CHAR(36))
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == 'postgresql':
            return value
        # For SQLite, always store as string
        return str(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if dialect.name == 'postgresql':
            return value
        # For SQLite, return as string for consistency
        return str(value)

class BaseModel(Base):
    """Base model class with common fields for all models"""
    __abstract__ = True
    
    id = Column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

# Import all models in correct order to ensure proper relationship resolution
from .user import User
from .event import Event  
from .reminder import Reminder

# Make them available for imports
__all__ = ["BaseModel", "User", "Event", "Reminder"]