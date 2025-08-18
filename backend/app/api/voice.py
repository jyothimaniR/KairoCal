"""
Voice-to-Text API endpoints for KairoCal
Integrates with BERT priority classification system and real-time WebSocket broadcasting
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field, validator
import re
import asyncio
import uuid

from ..core.database import get_db
from ..services.nlp_service import NLPService
from app.models.event import Event
from app.models.user import User
from sqlalchemy.orm import Session
from ..nlp.temporal_resolver import TemporalResolver

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
    user_id: Optional[Union[str, uuid.UUID]] = Field(None, description="User ID (UUID) for personalized processing")
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
    user_id: Union[str, uuid.UUID] = Field(..., description="User ID (UUID) for event creation")
    auto_schedule: bool = Field(True, description="Automatically schedule if time is detected")
    priority_override: Optional[int] = Field(None, ge=1, le=5, description="Manual priority override (1-5)")
    duration_preference: Optional[Union[str, int]] = Field(None, description="Duration preference: 'smart' or fixed minutes (30, 60, 90, 120)")
    
    @validator('voice_text')
    def validate_voice_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Voice text cannot be empty")
        return v.strip()

class VoiceEventResponse(BaseModel):
    """Voice event creation response model"""
    success: bool
    event_id: Optional[Union[str, uuid.UUID]]
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
        nlp_result = await nlp_service.process_voice_input(cleaned_text, request.duration_preference)

        # Step 4: Resolve temporal info (date/time) with TemporalResolver for tz-aware, AM/PM-correct times
        # Extract simple date/time candidates from cleaned_text and normalize AM/PM variants
        def _extract_date_token(text: str) -> Optional[str]:
            import re as _re
            patterns = [
                r"\b(today|tomorrow|yesterday|next week|next month|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
                r"\b\d{4}-\d{2}-\d{2}\b",                 # 2025-08-09
                r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b"       # 8/9 or 8/9/2025
            ]
            for p in patterns:
                m = _re.search(p, text, flags=_re.IGNORECASE)
                if m:
                    return m.group(0)
            return None

        def _extract_time_token(text: str) -> Optional[str]:
            import re as _re
            # Support "6 pm", "6:00 pm", "6 p.m.", "noon", "midnight", "evening" etc.
            patterns = [
                r"\b\d{1,2}:\d{2}\s*(?:a\.?m\.?|p\.?m\.?|am|pm)\b",
                r"\b\d{1,2}\s*(?:a\.?m\.?|p\.?m\.?|am|pm)\b",
                r"\b\d{1,2}:\d{2}\b",
                r"\b(noon|midnight|morning|afternoon|evening|night)\b"
            ]
            for p in patterns:
                m = _re.search(p, text, flags=_re.IGNORECASE)
                if m:
                    return m.group(0)
            return None

        def _normalize_ampm(t: Optional[str]) -> Optional[str]:
            if not t:
                return t
            # Convert "p.m."/"a.m." -> "pm"/"am" - IMPROVED NORMALIZATION
            normalized = t.lower()
            normalized = normalized.replace("p.m.", "pm")
            normalized = normalized.replace("a.m.", "am")
            normalized = normalized.replace("p. m.", "pm") 
            normalized = normalized.replace("a. m.", "am")
            normalized = normalized.replace(" p. m.", " pm")
            normalized = normalized.replace(" a. m.", " am")
            # Handle spaces between number and am/pm
            normalized = re.sub(r'(\d+)\s+(am|pm)', r'\1\2', normalized)
            return normalized

        # Lightweight intent / scheduling relevance guard
        def _is_schedule_like(text: str) -> bool:
            # Expanded verbs/nouns to avoid false negatives (e.g., "set up", "lunch")
            kw = [
                "schedule", "meeting", "call", "submit", "send", "review", "remind",
                "appointment", "task", "deadline", "set up", "setup", "arrange",
                "organize", "plan", "book", "meet", "lunch", "dinner", "interview",
                "class", "lesson", "coffee", "break", "session", "training",
                "workshop", "presentation", "conference", "seminar"
            ]
            t = text.lower()
            return any(k in t for k in kw)

        # Detect if any explicit or implicit time token exists (excluding broad parts of day)
        def _has_explicit_time(text: str) -> bool:
            import re
            # FIXED: Support both "am/pm" and "a.m./p.m." formats
            explicit = re.search(r"\b(\d{1,2}(:\d{2})?\s*(?:a\.?m\.?|p\.?m\.?|am|pm)|noon|midnight)\b", text, re.IGNORECASE)
            return bool(explicit)

        # Detect broad daytime phrases (morning/afternoon/evening) -> candidate for date-only
        def _broad_day_reference(text: str) -> bool:
            import re
            return bool(re.search(r"\b(morning|afternoon|evening|night)\b", text, re.IGNORECASE))

        has_time = _has_explicit_time(cleaned_text)
        # Consider explicit time or explicit date mention as sufficient scheduling intent
        scheduling_intent = _is_schedule_like(cleaned_text) or has_time or bool(_extract_date_token(cleaned_text))
        broad_only = _broad_day_reference(cleaned_text) and not has_time

        if not scheduling_intent:
            # Return a graceful non-creation response
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info("🛈 Voice text not considered a scheduling command; skipping event creation")
            return VoiceEventResponse(
                success=False,
                event_id=None,
                event_data={},
                nlp_analysis={
                    'original_text': request.voice_text,
                    'cleaned_text': cleaned_text,
                    'extracted_title': '',
                    'extracted_time': '',
                    'extracted_location': ''
                },
                bert_classification={
                    'priority': 3,
                    'confidence': 0.0,
                    'model_used': 'none',
                    'final_priority': 3,
                    'priority_override': False
                },
                processing_details={
                    'total_processing_time': processing_time,
                    'auto_scheduled': False
                },
                message='Ignored: not a scheduling command'
            )
        
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

            # FIXED HYBRID DECISION: Always trust BERT for high-confidence predictions
            # This prevents keyword-based overrides from corrupting BERT's semantic understanding
            if bert_confidence >= 0.7:
                # Trust BERT for high-confidence predictions (confidence >= 0.7)
                final_priority = bert_priority
                hybrid_confidence = bert_confidence
                logger.info(f"🎯 HYBRID: Using BERT priority {bert_priority} (high confidence: {bert_confidence:.3f})")
            elif nlp_priority >= 4 and nlp_priority > bert_priority:
                # Only use NLP for critical events (CEO, surgery, emergency) when BERT confidence is low
                final_priority = nlp_priority
                hybrid_confidence = 0.9  # High confidence in keyword-based detection
                logger.info(f"🎯 HYBRID: Using enhanced NLP priority {nlp_priority} (keyword-based critical event)")
            else:
                # Use BERT as primary, with slight NLP influence for very low confidence
                final_priority = bert_priority
                hybrid_confidence = max(0.6, bert_confidence)
                logger.info(f"🎯 HYBRID: Using BERT priority {bert_priority} (primary classification)")
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

        # Step 4: Resolve temporal info (date/time) with TemporalResolver for tz-aware, AM/PM-correct times
        # Normalize AM/PM markers in the cleaned text before token extraction
        cleaned_text_norm = _normalize_ampm(cleaned_text)

        date_token = _extract_date_token(cleaned_text_norm)
        time_token = _extract_time_token(cleaned_text_norm)

        resolver = TemporalResolver()  # defaults to UTC
        start_dt_resolved: Optional[datetime] = None
        end_dt_resolved: Optional[datetime] = None

        # Extract duration from NLP result to pass to temporal resolver
        nlp_duration_minutes = nlp_result.get('duration', 60)
        duration_text = f"{nlp_duration_minutes} minutes" if nlp_duration_minutes else None
        logger.info(f"⏱️ Passing duration to temporal resolver: {duration_text}")

        try:
            start_dt_resolved, end_dt_resolved = resolver.resolve_full_temporal(
                date_text=date_token or "",
                time_text=time_token or "",
                duration_text=duration_text,
                event_type=nlp_result.get('event_type', 'default')
            )
            logger.info(f"🔧 Temporal resolver result - Start: {start_dt_resolved}, End: {end_dt_resolved}")
        except Exception as e:
            logger.warning(f"⚠️ Temporal resolver failed: {e}")
            # Fallback handled below
            start_dt_resolved, end_dt_resolved = None, None

        # Helper to parse ISO-like strings to aware datetimes (UTC when 'Z')
        def _parse_dt(val: Any) -> Optional[datetime]:
            if isinstance(val, datetime):
                return val
            if isinstance(val, str):
                try:
                    s = val.strip()
                    if s.endswith('Z'):
                        # fromisoformat can't parse trailing Z; replace with +00:00
                        s = s[:-1] + '+00:00'
                    return datetime.fromisoformat(s)
                except Exception:
                    return None
            return None

        # Step 5: Create event in database
        try:
            # Resolve user: accept UUID (users.id) or cognito_sub string
            user: Optional[User] = None
            user_uuid: Optional[uuid.UUID] = None
            if isinstance(request.user_id, uuid.UUID):
                user_uuid = request.user_id
                user = db.query(User).filter(User.id == user_uuid).first()
            elif isinstance(request.user_id, str):
                try:
                    user_uuid = uuid.UUID(request.user_id)
                    user = db.query(User).filter(User.id == user_uuid).first()
                except Exception:
                    # Treat as cognito_sub
                    user = db.query(User).filter(User.cognito_sub == request.user_id).first()
                    if user:
                        user_uuid = user.id
            else:
                # Unsupported type
                pass

            if not user or not user_uuid:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found (accepts UUID or cognito_sub)"
                )
            
            # Prefer resolver times if available; otherwise fall back to NLP times (parsed)

            # Use NLP's start_time and end_time if present and valid, fallback only if both missing
            nlp_start = nlp_result.get('start_time')
            nlp_end = nlp_result.get('end_time')
            logger.info(f"[DEBUG] NLP start_time: {nlp_start} (type: {type(nlp_start)})")
            logger.info(f"[DEBUG] NLP end_time: {nlp_end} (type: {type(nlp_end)})")
            # Convert to datetime if string
            if isinstance(nlp_start, str):
                try:
                    nlp_start = datetime.fromisoformat(nlp_start.replace('Z', '+00:00'))
                except Exception:
                    logger.warning(f"[DEBUG] Failed to parse nlp_start: {nlp_start}")
                    nlp_start = None
            if isinstance(nlp_end, str):
                try:
                    nlp_end = datetime.fromisoformat(nlp_end.replace('Z', '+00:00'))
                except Exception:
                    logger.warning(f"[DEBUG] Failed to parse nlp_end: {nlp_end}")
                    nlp_end = None

            logger.info(f"⏱️ Duration already extracted: {nlp_duration_minutes} minutes")

            # Priority: resolver > NLP > fallback
            start_time_dt = start_dt_resolved or nlp_start or datetime.now()
            # Robustly use NLP's end_time if present, or calculate from duration if possible
            if end_dt_resolved is not None:
                end_time_dt = end_dt_resolved
                logger.info(f"🕐 Using temporal resolver end time: {end_time_dt}")
            elif nlp_end is not None and nlp_start is not None:
                end_time_dt = nlp_end
                logger.info(f"🕐 Using NLP end time: {end_time_dt}")
            elif nlp_start is not None and nlp_duration_minutes:
                end_time_dt = nlp_start + timedelta(minutes=nlp_duration_minutes)
                logger.info(f"🕐 Calculated end time from NLP start + duration: {end_time_dt}")
            else:
                # Fallback: use now + duration
                end_time_dt = start_time_dt + timedelta(minutes=nlp_duration_minutes or 60)
                logger.info(f"🕐 Fallback: Calculated end time using duration fallback: {end_time_dt}")

            # Your original logic with warning for edge case:
            # 1. Has start time + duration → Use both ✅
            # 2. Has start time, no duration → Use start time + default duration ✅  
            # 3. No start time → All-day event ✅
            # 4. Special case: No start time but has specific duration → Show warning
            
            has_specific_duration = nlp_duration_minutes and nlp_duration_minutes != 60  # Not default
            is_all_day = False
            warning_message = None
            
            if scheduling_intent and not has_time:
                if has_specific_duration:
                    # Special case: No start time but has specific duration → Warning + All-day
                    warning_message = f"⚠️ Duration specified ({nlp_duration_minutes} min) but no start time provided. Please specify start time for better scheduling. Creating as all-day event."
                    logger.warning(warning_message)
                
                # No start time mentioned → All-day task (regardless of duration)
                day_anchor = start_time_dt
                start_time_dt = day_anchor.replace(hour=0, minute=0, second=0, microsecond=0)
                end_time_dt = start_time_dt + timedelta(hours=23, minutes=59)
                is_all_day = True
                logger.info(f"📅 Creating all-day event (no start time specified)")
            else:
                # Has start time → Use duration (specified or default)
                logger.info(f"⏰ Event has start time, using duration: {nlp_duration_minutes} minutes")

            # Create proper description with location and duration info
            description_parts = []
            if nlp_result.get('location'):
                description_parts.append(f"Location: {nlp_result.get('location')}")
            if nlp_duration_minutes and nlp_duration_minutes != 60:  # Only show if not default
                if nlp_duration_minutes >= 60:
                    hours = nlp_duration_minutes // 60
                    remaining_minutes = nlp_duration_minutes % 60
                    if remaining_minutes > 0:
                        duration_str = f"{hours}h {remaining_minutes}m"
                    else:
                        duration_str = f"{hours}h"
                else:
                    duration_str = f"{nlp_duration_minutes}m"
                description_parts.append(f"Duration: {duration_str}")
            
            # Create description
            if description_parts:
                description = " | ".join(description_parts)
            else:
                description = f"Created from voice input"

            # Create event object

            logger.info(f"[DEBUG] About to create Event: start_time={start_time_dt}, end_time={end_time_dt}, duration={(end_time_dt-start_time_dt).total_seconds()/60 if start_time_dt and end_time_dt else 'N/A'} min")
            event_data = {
                'title': nlp_result.get('title', 'Voice Event'),
                'description': description,
                'start_time': start_time_dt,
                'end_time': end_time_dt,
                'location': nlp_result.get('location', ''),
                'priority_level': final_priority,
                'priority_confidence': bert_confidence,
                'classification_method': 'voice_bert' if bert_model and bert_model.is_trained else 'voice_nlp',
                'created_via': 'voice',
                'is_all_day': is_all_day,
                'user_id': user_uuid,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            new_event = Event(**event_data)
            db.add(new_event)
            db.commit()
            db.refresh(new_event)
            logger.info(f"[DEBUG] Created Event in DB: start_time={new_event.start_time}, end_time={new_event.end_time}, duration={(new_event.end_time-new_event.start_time).total_seconds()/60 if new_event.start_time and new_event.end_time else 'N/A'} min")
            
            event_created = True
            event_id = str(new_event.id)  # Convert UUID to string for response
            
            # Include warning message if applicable
            base_message = f"✅ Event created successfully from voice input with priority {final_priority}"
            if warning_message:
                message = f"{base_message}\n\n{warning_message}"
            else:
                message = base_message
            
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
class VoiceAnalysisRequest(BaseModel):
    """Voice analysis request model"""
    voice_text: str = Field(..., min_length=1, max_length=5000, description="Voice input to analyze")
    user_id: Optional[Union[str, uuid.UUID]] = Field(None, description="User ID (UUID) for personalized analysis")
    include_bert: bool = Field(True, description="Include BERT classification in analysis")
    detailed_analysis: bool = Field(False, description="Include detailed analysis information")
    
    @validator('voice_text')
    def validate_voice_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Voice text cannot be empty")
        return v.strip()

@voice_router.post("/analyze-voice")
async def analyze_voice_input(
    request: VoiceAnalysisRequest
):
    """
    Analyze voice input without creating an event
    Useful for testing and validation
    """
    try:
        logger.info(f"🔍 Analyzing voice input: '{request.voice_text[:50]}...'")
        
        # Process voice text
        processor = VoiceProcessor()
        cleaning_result = processor.clean_voice_text(request.voice_text)
        
        # NLP analysis
        nlp_service = NLPService()
        nlp_result = await nlp_service.process_voice_input(cleaning_result['cleaned_text'])
        
        # BERT analysis if requested
        bert_analysis = {}
        if request.include_bert:
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
                bert_analysis = {
                    'priority': bert_priority,
                    'confidence': bert_confidence,
                    'reasoning': f"BERT classified this as priority {bert_priority} with {bert_confidence:.1%} confidence",
                    'available': True
                }
            else:
                bert_priority = nlp_result.get('priority', 3)
                bert_confidence = 0.6
                bert_analysis = {
                    'priority': bert_priority,
                    'confidence': bert_confidence,
                    'reasoning': "BERT model not available, using NLP-based priority",
                    'available': False
                }
        
        # Prepare response based on what the frontend expects
        response = {
            'bert_classification': bert_analysis,
            'nlp_analysis': {
                'keywords': nlp_result.get('keywords', []),
                'sentiment': nlp_result.get('sentiment', 'neutral'),
                'urgency_score': nlp_result.get('urgency', 0.5)
            }
        }
        
        if request.detailed_analysis:
            response.update({
                'voice_cleaning': cleaning_result,
                'full_nlp_analysis': nlp_result,
                'recommended_event': {
                    'title': nlp_result.get('title', 'Voice Event'),
                    'description': cleaning_result['cleaned_text'],
                    'priority': bert_analysis.get('priority', 3),
                    'confidence': bert_analysis.get('confidence', 0.6)
                }
            })
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Voice analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice analysis failed: {str(e)}"
        )
