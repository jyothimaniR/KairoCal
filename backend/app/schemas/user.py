from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)

class UserCreate(UserBase):
    cognito_sub: str = Field(..., description="AWS Cognito user identifier")

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: UUID
    cognito_sub: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserResponse):
    """Internal representation (identical currently)."""
    model_config = ConfigDict(from_attributes=True)
