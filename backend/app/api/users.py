# backend/app/api/users.py - Simplified without authentication
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.schemas import UserCreate, UserUpdate, UserResponse
from uuid import UUID

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    """Create a new user (simplified - no auth required for now)"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.cognito_sub == user_data.cognito_sub).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User profile already exists"
        )
    
    # Create new user
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    cognito_sub: str,
    db: Session = Depends(get_db)
):
    """Get user profile by cognito_sub (simplified)"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User profile not found. Please create your profile first."
        )
    return user

@router.put("/me", response_model=UserResponse)
def update_current_user(
    cognito_sub: str,
    user_data: UserUpdate, 
    db: Session = Depends(get_db)
):
    """Update user profile by cognito_sub (simplified)"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User profile not found. Please create your profile first."
        )
    
    # Update user fields
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/me")
def delete_current_user(
    cognito_sub: str,
    db: Session = Depends(get_db)
):
    """Delete user profile by cognito_sub (simplified)"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User profile not found"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "User profile deleted successfully"}

# Admin endpoints (keep existing for development)
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """Get user by ID (admin/development only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all users (admin/development only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users