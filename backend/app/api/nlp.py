# backend/app/api/nlp.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.models.user import User
from app.models.event import Event
from app.nlp.nlp_service import NLPService
from app.schemas import EventResponse
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/nlp", tags=["nlp"])

# Request/Response schemas
class NLPProcessRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="Natural language text to process")
    cognito_sub: str = Field(..., description="User's Cognito sub ID")

class NLPProcessResponse(BaseModel):
    success: bool
    confidence_score: float
    event: Optional[EventResponse] = None
    clarification_needed: bool = False
    suggested_questions: list[str] = []
    error_message: Optional[str] = None

class NLPSuggestionsRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    cognito_sub: str = Field(..., description="User's Cognito sub ID")

class NLPSuggestionsResponse(BaseModel):
    suggestions: list[str]
    entities_found: dict
    confidence_score: float

# Initialize NLP service (singleton)
nlp_service = NLPService()

def get_user_from_cognito(cognito_sub: str, db: Session) -> User:
    """Helper function to get user from Cognito sub ID"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User profile not found. Please create your profile first using POST /api/v1/users/"
        )
    return user

@router.post("/process", response_model=NLPProcessResponse, status_code=status.HTTP_201_CREATED)
def process_natural_language_event(
    request: NLPProcessRequest,
    db: Session = Depends(get_db)
):
    """
    Process natural language text and create an event if successful.
    
    Examples:
    - "Doctor appointment tomorrow at 2pm at Brownlow Clinic"
    - "Team meeting next Friday at 3:30pm"
    - "Lunch with Sarah on Thursday at noon"
    """
    try:
        # Get user
        user = get_user_from_cognito(request.cognito_sub, db)
        
        # Process the text with NLP
        nlp_result = nlp_service.process_text(request.text)
        
        if not nlp_result.success:
            return NLPProcessResponse(
                success=False,
                confidence_score=0.0,
                error_message=nlp_result.error_message
            )
        
        # If confidence is too low, ask for clarification
        if nlp_result.confidence_score < 0.7:
            return NLPProcessResponse(
                success=False,
                confidence_score=nlp_result.confidence_score,
                clarification_needed=True,
                suggested_questions=nlp_result.suggested_questions,
                error_message="Please provide more details to create the event"
            )
        
        # Create the event in database
        event_data = nlp_result.extracted_event
        
        # Convert to database model with explicit timestamps
        from datetime import datetime, timezone
        
        event = Event(
            user_id=user.id,
            title=event_data.title,
            description=event_data.description,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            location=event_data.location,
            is_all_day=event_data.is_all_day,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)  # This ensures all fields are properly populated
        
        logger.info(f"Created event via NLP for user {user.email}: {event.title}")
        
        # Convert to Pydantic model (Pydantic v2 syntax)
        event_response = EventResponse.model_validate(event)
        
        return NLPProcessResponse(
            success=True,
            confidence_score=nlp_result.confidence_score,
            event=event_response,
            clarification_needed=nlp_result.clarification_needed,
            suggested_questions=nlp_result.suggested_questions
        )
        
    except Exception as e:
        logger.error(f"NLP processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process natural language input: {str(e)}"
        )

@router.post("/suggestions", response_model=NLPSuggestionsResponse)
def get_nlp_suggestions(
    request: NLPSuggestionsRequest,
    db: Session = Depends(get_db)
):
    """
    Get suggestions and entity analysis without creating an event.
    Useful for auto-complete and helping users improve their input.
    """
    try:
        # Get user (validate they exist)
        user = get_user_from_cognito(request.cognito_sub, db)
        
        # Process the text
        nlp_result = nlp_service.process_text(request.text)
        
        # Extract entities for analysis
        from app.nlp.pattern_matcher import PatternMatcher
        from app.nlp.text_processor import TextProcessor
        
        processor = TextProcessor()
        matcher = PatternMatcher()
        
        cleaned_text = processor.clean_text(request.text)
        entities = matcher.extract_entities(cleaned_text)
        
        entities_dict = {
            entity.type: {
                "value": entity.value,
                "confidence": entity.confidence
            }
            for entity in entities
        }
        
        # Generate suggestions
        suggestions = []
        if nlp_result.suggested_questions:
            suggestions.extend(nlp_result.suggested_questions)
        else:
            suggestions = [
                "Try adding a specific time (e.g., 'at 2pm')",
                "Consider mentioning a location",
                "Be more specific about the date (e.g., 'tomorrow', 'next Friday')"
            ]
        
        return NLPSuggestionsResponse(
            suggestions=suggestions,
            entities_found=entities_dict,
            confidence_score=nlp_result.confidence_score
        )
        
    except Exception as e:
        logger.error(f"NLP suggestions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestions: {str(e)}"
        )

@router.get("/health")
def nlp_health_check():
    """Check if NLP service is working"""
    try:
        # Test with a simple phrase
        result = nlp_service.process_text("test meeting tomorrow")
        return {
            "status": "healthy",
            "nlp_service": "operational",
            "test_processed": True,
            "confidence": result.confidence_score
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"NLP service error: {str(e)}"
        )