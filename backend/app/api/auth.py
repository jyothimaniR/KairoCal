# backend/app/schemas/auth.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenRequest(BaseModel):
    """Schema for token validation request"""
    access_token: str

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserAuthInfo(BaseModel):
    """Schema for authenticated user information"""
    cognito_sub: str
    email: EmailStr
    full_name: Optional[str] = None
    email_verified: bool = False

class LoginRequest(BaseModel):
    """Schema for login request (if using custom auth)"""
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    """Schema for user registration (if using custom auth)"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class AuthResponse(BaseModel):
    """Schema for authentication response"""
    user: UserAuthInfo
    token: TokenResponse
    message: str = "Authentication successful"