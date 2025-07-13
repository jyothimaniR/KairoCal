from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    full_name: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)

class UserCreate(UserBase):
    """Schema for creating a new user"""
    cognito_sub: str = Field(..., description="AWS Cognito user identifier")

class UserUpdate(BaseModel):
    """Schema for updating user information"""
    full_name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """Schema for user response (what we return to client)"""
    id: UUID
    cognito_sub: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy models

class UserInDB(UserResponse):
    """Schema for user as stored in database (internal use)"""
    pass