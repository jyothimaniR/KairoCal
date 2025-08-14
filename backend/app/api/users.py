# backend/app/api/users.py - Simplified without authentication
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import logging
logger = logging.getLogger(__name__)
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
    """Create a new user (simplified - no auth required for now).

    Robust duplicate handling & normalization to avoid 500s from constraint violations.
    """
    # Normalize inputs
    email_normalized = user_data.email.strip().lower()
    # Quick duplicate pre-checks (best-effort – race still possible, handled by IntegrityError)
    if db.query(User).filter(User.email == email_normalized).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.cognito_sub == user_data.cognito_sub).first():
        raise HTTPException(status_code=400, detail="Cognito user already registered")

    try:
        # Use model_dump for Pydantic v2
        payload = user_data.model_dump()
        payload["email"] = email_normalized
        user = User(**payload)
        db.add(user)
        db.commit()
        db.refresh(user)
        # Ensure timestamps loaded (fallback populate if still None)
        if not user.created_at or not user.updated_at:
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)
            if not user.created_at:
                user.created_at = now
            if not user.updated_at:
                user.updated_at = now
            try:
                db.add(user)
                db.commit()
                db.refresh(user)
            except Exception:
                db.rollback()
        logger.debug("user_post_refresh_timestamps", extra={"created_at": str(user.created_at), "updated_at": str(user.updated_at)})
        # Coerce preferences to dict if DB driver returned string
        if isinstance(user.preferences, str):
            import json
            try:
                user.preferences = json.loads(user.preferences) if user.preferences else {}
            except Exception:
                user.preferences = {}
        logger.debug("user_create_success", extra={"id": str(user.id), "email": user.email})
        return user
    except IntegrityError as ie:
        db.rollback()
        logger.warning("user_create_integrity_error", extra={"error": str(ie), "email": email_normalized})
        # Generic message (do not leak raw constraint names)
        raise HTTPException(status_code=400, detail="Duplicate email or cognito_sub")
    except Exception as e:
        db.rollback()
        logger.exception("user_create_unexpected_error")
        raise HTTPException(status_code=500, detail="Failed to create user")

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