# backend/app/schemas/__init__.py
from .user import UserCreate, UserUpdate, UserResponse, UserInDB
from .event import (
    EventCreate, 
    EventUpdate, 
    EventResponse, 
    EventWithReminders,
    ReminderCreate,
    ReminderResponse
)
from .auth import (
    TokenRequest,
    TokenResponse, 
    UserAuthInfo,
    LoginRequest,
    RegisterRequest,
    AuthResponse
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate", 
    "UserResponse",
    "UserInDB",
    
    # Event schemas
    "EventCreate",
    "EventUpdate",
    "EventResponse", 
    "EventWithReminders",
    "ReminderCreate",
    "ReminderResponse",
    
    # Auth schemas
    "TokenRequest",
    "TokenResponse",
    "UserAuthInfo", 
    "LoginRequest",
    "RegisterRequest",
    "AuthResponse"
]