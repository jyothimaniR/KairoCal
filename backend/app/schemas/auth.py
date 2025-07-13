from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenRequest(BaseModel):
    access_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserAuthInfo(BaseModel):
    cognito_sub: str
    email: EmailStr
    full_name: Optional[str] = None
    email_verified: bool = False

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class AuthResponse(BaseModel):
    user: UserAuthInfo
    token: TokenResponse
    message: str = "Authentication successful"
