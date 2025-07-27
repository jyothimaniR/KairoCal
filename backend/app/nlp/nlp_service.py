# backend/app/nlp/nlp_service.py
"""
Main NLP Service - Orchestrates all NLP components for intelligent event creation
"""

import time
from typing import Optional, Dict, Any
from datetime import datetime, timezone

from .entities import ExtractedEvent, NLPResponse, IntentType, TemporalContext, ProcessingStats
from .text_processor import TextProcessor
from .pattern_matcher import PatternMatcher
from .temporal_resolver import TemporalResolver


class NLPService:
    """
    Main orchestrator for the NLP pipeline
    Converts natural language input into structured event data
    """
    
    def __init__(self, current_time: Optional[datetime] = None, user_timezone: str = "UTC"):
        self.text_processor = TextProcessor()
        self.pattern_matcher = PatternMatcher()
        self.temporal_resolver = TemporalResolver(current_time, user_timezone)
        
        # Confidence thresholds
        self.auto_create_threshold = 0.8
        self.confirmation_threshold = 0.6
        
        # Default event durations by type
        self.default_durations = {
            "appointment": 30,
            "doctor appointment": 30,
            "dentist appointment": 45,
            "meeting": 60,
            "team meeting": 60,
            "lunch": 90,
            "dinner": 120,
            "coffee": 30,
            "call": 30,
            "interview": 60,
            "default": 60
        }
    
    def process_text(self, text: str, context: Optional[TemporalContext] = None) -> NLPResponse:
        """
        Main entry point for processing natural language text
        
        Args:
            text: Natural language input from user
            context: Optional temporal context for processing
            
        Returns:
            NLPResponse with extracted event data or error information
        """
        start_time = time.time()
        
        try:
            # Step 1: Validate input
            is_valid, error_msg = self.text_processor.validate_input(text)
            if not is_valid:
                return NLPResponse(
                    success=False,
                    error_message=error_msg,
                    confidence_score=0.0
                )
            
            # Step 2: Clean and preprocess text
            cleaned_text = self.text_processor.clean_text(text)
            
            # Step 3: Extract entities
            entities = self.pattern_matcher.extract_entities(cleaned_text)
            
            # Step 4: Build extracted event object
            extracted_event = self._build_event_from_entities(
                entities, cleaned_text, text, context
            )
            
            # Step 5: Calculate overall confidence
            confidence_score = self._calculate_confidence(extracted_event, entities)
            extracted_event.confidence_score = confidence_score
            
            # Step 6: Determine if clarification is needed
            clarification_needed, questions = self._check_clarification_needed(extracted_event)
            
            # Step 7: Generate processing statistics
            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return NLPResponse(
                success=True,
                extracted_event=extracted_event,
                confidence_score=confidence_score,
                clarification_needed=clarification_needed,
                suggested_questions=questions,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            return NLPResponse(
                success=False,
                error_message=f"Processing error: {str(e)}",
                confidence_score=0.0,
                processing_time_ms=(time.time() - start_time) * 1000
            )
    
    def _build_event_from_entities(self, entities, cleaned_text: str, 
                                 original_text: str, context: Optional[TemporalContext]) -> ExtractedEvent:
        """Build an ExtractedEvent object from extracted entities"""
        
        # Initialize event object
        event = ExtractedEvent(
            original_text=original_text,
            extracted_entities=entities
        )
        
        # Extract entity values by type
        entity_values = self._group_entities_by_type(entities)
        
        # Process event title
        event.title = self._extract_title(entity_values, cleaned_text)
        
        # Process temporal information
        date_text = entity_values.get("date", [None])[0]
        time_text = entity_values.get("time", [None])[0]
        duration_text = entity_values.get("duration", [None])[0]
        
        event.date_text = date_text
        event.time_text = time_text
        event.duration_text = duration_text
        
        # Resolve temporal information
        event_type = entity_values.get("event_type", [event.title or "default"])[0]
        start_time, end_time = self.temporal_resolver.resolve_full_temporal(
            date_text, time_text, duration_text, event_type
        )
        
        event.start_time = start_time
        event.end_time = end_time
        
        # Check if this is an all-day event
        if duration_text and "all day" in duration_text.lower():
            event.is_all_day = True
        
        # Process location
        location_entities = entity_values.get("location", [])
        if location_entities:
            event.location = location_entities[0]
        
        # Process participants
        participant_entities = entity_values.get("participants", [])
        if participant_entities:
            # Store participants in description for now
            participants_text = ", ".join(participant_entities)
            event.description = f"Participants: {participants_text}"
        
        # Determine intent (for now, assume create)
        event.intent = IntentType.CREATE_EVENT
        
        # Identify missing fields
        event.missing_fields = self._identify_missing_fields(event)
        
        # Generate suggestions for missing fields
        event.suggestions = self._generate_suggestions(event)
        
        return event
    
    def _group_entities_by_type(self, entities) -> Dict[str, list]:
        """Group entities by their type"""
        grouped = {}
        for entity in entities:
            if entity.type not in grouped:
                grouped[entity.type] = []
            grouped[entity.type].append(entity.normalized_value or entity.value)
        return grouped
    
    def _extract_title(self, entity_values: Dict, cleaned_text: str) -> Optional[str]:
        """Extract event title from entities and text"""
        
        # Check for explicit event type
        event_types = entity_values.get("event_type", [])
        if event_types:
            return event_types[0].title()
        
        # Try to extract title from remaining text after removing other entities
        # This is a simplified approach - could be enhanced
        words = cleaned_text.split()
        
        # Remove common scheduling words
        title_words = []
        skip_words = {"at", "on", "in", "tomorrow", "today", "next", "this", "am", "pm"}
        
        for word in words:
            # Skip time patterns
            if any(char.isdigit() for char in word) and (":" in word or "am" in word or "pm" in word):
                continue
            # Skip date-related words
            if word.lower() in skip_words:
                continue
            # Skip location prepositions
            if word.lower() in ["at", "in"] and title_words:
                break
            
            title_words.append(word)
        
        if title_words:
            return " ".join(title_words).title()
        
        return None
    
    def _calculate_confidence(self, event: ExtractedEvent, entities) -> float:
        """Calculate overall confidence score for the extracted event"""
        
        if not entities:
            return 0.0
        
        # Base confidence from entity extraction
        entity_confidence = sum(e.confidence for e in entities) / len(entities)
        
        # Bonus points for having key information
        bonus = 0.0
        
        if event.title:
            bonus += 0.2
        if event.start_time:
            bonus += 0.3
        if event.end_time:
            bonus += 0.2
        if event.location:
            bonus += 0.1
        
        # Penalty for missing critical information
        penalty = 0.0
        if not event.start_time:
            penalty += 0.3
        if not event.title:
            penalty += 0.2
        
        final_confidence = min(1.0, entity_confidence + bonus - penalty)
        return round(final_confidence, 2)
    
    def _identify_missing_fields(self, event: ExtractedEvent) -> list:
        """Identify which required fields are missing"""
        missing = []
        
        if not event.title:
            missing.append("title")
        if not event.start_time:
            missing.append("time")
        if not event.start_time and not event.date_text:
            missing.append("date")
        
        return missing
    
    def _generate_suggestions(self, event: ExtractedEvent) -> list:
        """Generate helpful suggestions for missing or unclear information"""
        suggestions = []
        
        if not event.title:
            suggestions.append("What type of event is this? (e.g., meeting, appointment, lunch)")
        
        if not event.start_time:
            if not event.date_text:
                suggestions.append("When would you like to schedule this? (e.g., tomorrow, next Friday)")
            if not event.time_text:
                suggestions.append("What time works for you? (e.g., 2pm, morning, afternoon)")
        
        if not event.location and event.title and "appointment" in event.title.lower():
            suggestions.append("Where is this appointment? (e.g., clinic name, address)")
        
        if not event.end_time and not event.duration_text:
            default_duration = self.default_durations.get(
                event.title.lower() if event.title else "default", 60
            )
            suggestions.append(f"Duration not specified - assuming {default_duration} minutes")
        
        return suggestions
    
    def _check_clarification_needed(self, event: ExtractedEvent) -> tuple:
        """Determine if user clarification is needed"""
        
        # High confidence events can be auto-created
        if event.confidence_score >= self.auto_create_threshold:
            return False, []
        
        # Medium confidence events need confirmation
        if event.confidence_score >= self.confirmation_threshold:
            questions = [f"I understand you want to schedule: {self._format_event_summary(event)}. Is this correct?"]
            return True, questions
        
        # Low confidence events need more information
        questions = event.suggestions[:3]  # Limit to top 3 suggestions
        return True, questions
    
    def _format_event_summary(self, event: ExtractedEvent) -> str:
        """Format a human-readable summary of the extracted event"""
        parts = []
        
        if event.title:
            parts.append(f'"{event.title}"')
        
        if event.start_time:
            formatted_time = self.temporal_resolver.format_relative_time(event.start_time)
            parts.append(f"on {formatted_time}")
        elif event.date_text and event.time_text:
            parts.append(f"on {event.date_text} at {event.time_text}")
        
        if event.location:
            parts.append(f"at {event.location}")
        
        return " ".join(parts) if parts else "an event"
    
    def create_event_from_nlp(self, text: str, user_id: str = None) -> Dict[str, Any]:
        """
        Convenience method to create a database-ready event object
        
        Returns:
            Dictionary ready for event creation API
        """
        result = self.process_text(text)
        
        if not result.success or not result.extracted_event:
            return {
                "error": result.error_message or "Failed to process text",
                "confidence": result.confidence_score
            }
        
        event = result.extracted_event
        
        # Build event data for database
        event_data = {
            "title": event.title or "Untitled Event",
            "description": event.description,
            "start_time": event.start_time.isoformat() if event.start_time else None,
            "end_time": event.end_time.isoformat() if event.end_time else None,
            "location": event.location,
            "is_all_day": event.is_all_day,
            "confidence_score": event.confidence_score,
            "original_text": event.original_text,
            "requires_clarification": result.clarification_needed,
            "suggestions": result.suggested_questions
        }
        
        return event_data