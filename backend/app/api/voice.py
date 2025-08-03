"""
Voice-to-Text API endpoints for KairoCal
Integrates with BERT priority classification system and real-time WebSocket broadcasting
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field, validator
import re
import asyncio

from ..core.database import get_db
from ..services.nlp_service import NLPService
from app.models.event import Event
from app.models.user import User
from sqlalchemy.orm import Session

# Import WebSocket server for real-time broadcasting
from ..websocket.ultimate_socket_server import get_socket_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
voice_router = APIRouter(prefix="/api/v1/voice", tags=["voice"])

# Request/Response Models
class VoiceTranscribeRequest(BaseModel):
    """Voice transcription request model"""
    text: str = Field(..., min_length=1, max_length=5000, description="Raw voice input text")
    user_id: Optional[int] = Field(None, description="User ID for personalized processing")
    language: str = Field("en", description="Language code (default: en)")
    confidence_threshold: float = Field(0.5, ge=0.0, le=1.0, description="Minimum confidence threshold")
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()

class VoiceTranscribeResponse(BaseModel):
    """Voice transcription response model"""
    transcribed_text: str
    cleaned_text: str
    confidence: float
    processing_time: float
    timestamp: str
    metadata: Dict[str, Any]

class VoiceCreateEventRequest(BaseModel):
    """Voice event creation request model"""
    voice_text: str = Field(..., min_length=1, max_length=5000, description="Voice input describing the event")
    user_id: int = Field(..., description="User ID for event creation")
    auto_schedule: bool = Field(True, description="Automatically schedule if time is detected")
    priority_override: Optional[int] = Field(None, ge=1, le=5, description="Manual priority override (1-5)")
    
    @validator('voice_text')
    def validate_voice_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Voice text cannot be empty")
        return v.strip()

class VoiceEventResponse(BaseModel):
    """Voice event creation response model"""
    success: bool
    event_id: Optional[int]
    event_data: Dict[str, Any]
    nlp_analysis: Dict[str, Any]
    bert_classification: Dict[str, Any]
    processing_details: Dict[str, Any]
    message: str

# Voice Processing Service
class VoiceProcessor:
    """Handles voice-specific text processing and cleaning"""
    
    def __init__(self):
        self.filler_words = {
            'en': ['um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'well', 'actually', 
                   'basically', 'literally', 'totally', 'really', 'just', 'kinda', 'sorta']
        }
        self.nlp_service = NLPService()
    
    def clean_voice_text(self, text: str, language: str = 'en') -> Dict[str, Any]:
        """Clean voice input text by removing filler words and normalizing"""
        start_time = datetime.now()
        
        original_text = text
        cleaned_text = text.lower()
        
        # Remove filler words
        filler_words = self.filler_words.get(language, self.filler_words['en'])
        for filler in filler_words:
            pattern = r'\b' + re.escape(filler) + r'\b'
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
        
        # Clean up extra spaces and punctuation
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Multiple spaces to single
        cleaned_text = re.sub(r'[,]{2,}', ',', cleaned_text)  # Multiple commas
        cleaned_text = re.sub(r'[.]{2,}', '.', cleaned_text)  # Multiple periods
        cleaned_text = cleaned_text.strip()
        
        # Normalize common voice patterns
        voice_patterns = {
            r'\bremind me to\b': 'reminder:',
            r'\bschedule\s+(a\s+)?meeting\b': 'meeting',
            r'\bset up\s+(a\s+)?call\b': 'call',
            r'\bmake\s+(an\s+)?appointment\b': 'appointment',
            r'\b(tomorrow|next week|next month)\b': lambda m: self._normalize_time_reference(m.group(1)),
            r'\b(urgent|asap|immediately|right away)\b': 'URGENT',
            r'\b(important|critical|high priority)\b': 'HIGH_PRIORITY'
        }
        
        for pattern, replacement in voice_patterns.items():
            if callable(replacement):
                cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.IGNORECASE)
            else:
                cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.IGNORECASE)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'original_text': original_text,
            'cleaned_text': cleaned_text,
            'removed_words': len(original_text.split()) - len(cleaned_text.split()),
            'processing_time': processing_time,
            'confidence': self._calculate_cleaning_confidence(original_text, cleaned_text)
        }
    
    def _normalize_time_reference(self, time_ref: str) -> str:
        """Normalize relative time references"""
        time_map = {
            'tomorrow': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'next week': (datetime.now() + timedelta(weeks=1)).strftime('%Y-%m-%d'),
            'next month': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        }
        return time_map.get(time_ref.lower(), time_ref)
    
    def _calculate_cleaning_confidence(self, original: str, cleaned: str) -> float:
        """Calculate confidence score for text cleaning"""
        if not original:
            return 0.0
        
        # Base confidence on how much meaningful content remains
        original_words = len(original.split())
        cleaned_words = len(cleaned.split())
        
        if original_words == 0:
            return 0.0
        
        retention_ratio = cleaned_words / original_words
        
        # Higher confidence for more content retention (but not too high if nothing was cleaned)
        if retention_ratio > 0.8:
            return 0.9
        elif retention_ratio > 0.6:
            return 0.95  # Good cleaning
        elif retention_ratio > 0.4:
            return 0.85  # Moderate cleaning
        else:
            return 0.7   # Heavy cleaning, might be less reliable

# API Endpoints
@voice_router.post("/transcribe", response_model=VoiceTranscribeResponse)
async def transcribe_voice(
    request: VoiceTranscribeRequest,
    db: Session = Depends(get_db)
) -> VoiceTranscribeResponse:
    """
    Process voice input text (simulating transcription)
    Cleans and normalizes voice input for better NLP processing
    """
    try:
        logger.info(f"🎤 Processing voice transcription for text: '{request.text[:50]}...'")
        start_time = datetime.now()
        
        # Initialize voice processor
        processor = VoiceProcessor()
        
        # Clean and process voice text
        cleaning_result = processor.clean_voice_text(request.text, request.language)
        
        # Calculate overall confidence
        base_confidence = 0.8  # Simulated transcription confidence
        cleaning_confidence = cleaning_result['confidence']
        overall_confidence = (base_confidence + cleaning_confidence) / 2
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Prepare metadata
        metadata = {
            'original_word_count': len(request.text.split()),
            'cleaned_word_count': len(cleaning_result['cleaned_text'].split()),
            'words_removed': cleaning_result['removed_words'],
            'language': request.language,
            'cleaning_confidence': cleaning_confidence,
            'transcription_confidence': base_confidence
        }
        
        logger.info(f"✅ Voice transcription completed in {processing_time:.3f}s")
        
        return VoiceTranscribeResponse(
            transcribed_text=request.text,
            cleaned_text=cleaning_result['cleaned_text'],
            confidence=overall_confidence,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat(),
            metadata=metadata
        )
        
    except Exception as e:
        logger.error(f"❌ Voice transcription failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice transcription failed: {str(e)}"
        )

@voice_router.post("/create-event", response_model=VoiceEventResponse)
async def create_event_from_voice(
    request: VoiceCreateEventRequest,
    db: Session = Depends(get_db)
) -> VoiceEventResponse:
    """
    Create calendar event from voice input
    Full pipeline: Voice → NLP → BERT → Database
    """
    try:
        logger.info(f"🎤➡️📅 Creating event from voice: '{request.voice_text[:50]}...'")
        start_time = datetime.now()
        
        # Step 1: Process voice input
        processor = VoiceProcessor()
        cleaning_result = processor.clean_voice_text(request.voice_text)
        cleaned_text = cleaning_result['cleaned_text']
        
        logger.info(f"🧹 Cleaned voice text: '{cleaned_text}'")
        
        # Step 2: NLP Processing with voice-specific enhancements
        nlp_service = NLPService()
        nlp_result = await nlp_service.process_voice_input(cleaned_text)
        
        # Step 3: Enhanced Hybrid Priority Classification
        from ..nlp.model_loader import get_global_bert_model
        bert_model = get_global_bert_model()
        
        # Prepare event data for BERT
        event_for_bert = {
            'title': nlp_result.get('title', 'Voice Event'),
            'description': nlp_result.get('description', cleaned_text),
            'start_time': nlp_result.get('start_time', datetime.now().isoformat()),
            'location': nlp_result.get('location', '')
        }
        
        # Get both NLP enhanced priority and BERT priority
        nlp_priority = nlp_result.get('priority', 3)  # Our enhanced keyword detection
        logger.info(f"🔍 Enhanced NLP Priority: {nlp_priority}")
        
        # Get BERT priority prediction
        if bert_model and bert_model.is_trained:
            bert_priority, bert_confidence = bert_model.predict(event_for_bert)
            logger.info(f"🤖 BERT Classification: Priority {bert_priority}, Confidence {bert_confidence:.3f}")
            
            # HYBRID DECISION: Use the higher priority between NLP enhanced and BERT
            # This ensures critical keywords (CEO, surgery) are never downgraded
            if nlp_priority >= 4 and nlp_priority > bert_priority:
                # Trust enhanced NLP for high-priority events (CEO, surgery, emergency)
                final_priority = nlp_priority
                hybrid_confidence = 0.9  # High confidence in keyword-based detection
                logger.info(f"🎯 HYBRID: Using enhanced NLP priority {nlp_priority} (keyword-based critical event)")
            elif bert_confidence >= 0.7 and bert_priority >= nlp_priority:
                # Trust BERT for high-confidence predictions
                final_priority = bert_priority
                hybrid_confidence = bert_confidence
                logger.info(f"🎯 HYBRID: Using BERT priority {bert_priority} (high confidence)")
            else:
                # Use weighted average for moderate cases
                final_priority = round((nlp_priority * 0.6) + (bert_priority * 0.4))
                final_priority = max(1, min(5, final_priority))  # Ensure valid range
                hybrid_confidence = (0.8 + bert_confidence) / 2
                logger.info(f"🎯 HYBRID: Using weighted priority {final_priority} (NLP: {nlp_priority}, BERT: {bert_priority})")
        else:
            # Fallback to enhanced NLP-based priority
            final_priority = nlp_priority
            hybrid_confidence = 0.8
            logger.warning("⚠️ BERT model not available, using enhanced NLP priority")
        
        # Apply priority override if specified
        if request.priority_override:
            final_priority = request.priority_override
            logger.info(f"🔧 Priority override applied: {final_priority}")
        
        bert_priority = final_priority  # For compatibility with existing response structure
        bert_confidence = hybrid_confidence
        
        # Step 4: Create event in database
        try:
            # Verify user exists
            user = db.query(User).filter(User.id == request.user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {request.user_id} not found"
                )
            
            # Create event object
            event_data = {
                'title': nlp_result.get('title', 'Voice Event'),
                'description': f"Created from voice: {request.voice_text}",
                'start_time': nlp_result.get('start_time', datetime.now()),
                'end_time': nlp_result.get('end_time', datetime.now() + timedelta(hours=1)),
                'location': nlp_result.get('location', ''),
                'priority': final_priority,
                'user_id': request.user_id,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            new_event = Event(**event_data)
            db.add(new_event)
            db.commit()
            db.refresh(new_event)
            
            event_created = True
            event_id = new_event.id
            message = f"✅ Event created successfully from voice input with priority {final_priority}"
            
            logger.info(f"📅 Event created with ID: {event_id}")
            
        except Exception as db_error:
            logger.error(f"❌ Database error: {str(db_error)}")
            event_created = False
            event_id = None
            message = f"❌ Failed to create event: {str(db_error)}"
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Prepare response
        response_data = {
            'success': event_created,
            'event_id': event_id,
            'event_data': event_data if event_created else {},
            'nlp_analysis': {
                'original_text': request.voice_text,
                'cleaned_text': cleaned_text,
                'extracted_title': nlp_result.get('title', ''),
                'extracted_time': nlp_result.get('start_time', ''),
                'extracted_location': nlp_result.get('location', ''),
                'nlp_confidence': nlp_result.get('confidence', 0.7)
            },
            'bert_classification': {
                'priority': bert_priority,
                'confidence': bert_confidence,
                'model_used': 'BERT' if bert_model and bert_model.is_trained else 'Fallback',
                'final_priority': final_priority,
                'priority_override': request.priority_override is not None
            },
            'processing_details': {
                'total_processing_time': processing_time,
                'voice_cleaning_time': cleaning_result['processing_time'],
                'words_removed': cleaning_result['removed_words'],
                'auto_scheduled': request.auto_schedule
            },
            'message': message
        }
        
        logger.info(f"🎉 Voice event creation completed in {processing_time:.3f}s")
        
        return VoiceEventResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Voice event creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice event creation failed: {str(e)}"
        )

@voice_router.get("/health")
async def voice_health_check():
    """Health check for voice API"""
    try:
        # Test NLP service
        nlp_service = NLPService()
        nlp_status = "available"
        
        # Test BERT model
        from ..nlp.model_loader import get_global_bert_model
        bert_model = get_global_bert_model()
        bert_status = "trained" if bert_model and bert_model.is_trained else "not_available"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "voice_processor": "available",
                "nlp_service": nlp_status,
                "bert_model": bert_status
            },
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"❌ Voice health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Voice service health check failed: {str(e)}"
        )

# Additional utility endpoints
@voice_router.post("/analyze-voice")
async def analyze_voice_input(
    voice_text: str,
    user_id: Optional[int] = None
):
    """
    Analyze voice input without creating an event
    Useful for testing and validation
    """
    try:
        logger.info(f"🔍 Analyzing voice input: '{voice_text[:50]}...'")
        
        # Process voice text
        processor = VoiceProcessor()
        cleaning_result = processor.clean_voice_text(voice_text)
        
        # NLP analysis
        nlp_service = NLPService()
        nlp_result = await nlp_service.process_voice_input(cleaning_result['cleaned_text'])
        
        # BERT analysis
        from ..nlp.model_loader import get_global_bert_model
        bert_model = get_global_bert_model()
        
        if bert_model and bert_model.is_trained:
            event_for_bert = {
                'title': nlp_result.get('title', 'Voice Event'),
                'description': nlp_result.get('description', cleaning_result['cleaned_text']),
                'start_time': nlp_result.get('start_time', datetime.now().isoformat()),
                'location': nlp_result.get('location', '')
            }
            bert_priority, bert_confidence = bert_model.predict(event_for_bert)
        else:
            bert_priority = nlp_result.get('priority', 3)
            bert_confidence = 0.6
        
        return {
            'voice_cleaning': cleaning_result,
            'nlp_analysis': nlp_result,
            'bert_analysis': {
                'priority': bert_priority,
                'confidence': bert_confidence,
                'available': bert_model and bert_model.is_trained
            },
            'recommended_event': {
                'title': nlp_result.get('title', 'Voice Event'),
                'description': cleaning_result['cleaned_text'],
                'priority': bert_priority,
                'confidence': bert_confidence
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Voice analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice analysis failed: {str(e)}"
        )
