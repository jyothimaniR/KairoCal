# backend/app/nlp/entities.py
"""
Pydantic models for NLP entity extraction and event construction
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class IntentType(str, Enum):
    """Types of user intentions detected from text"""
    CREATE_EVENT = "create_event"
    UPDATE_EVENT = "update_event" 
    QUERY_EVENT = "query_event"
    DELETE_EVENT = "delete_event"
    UNKNOWN = "unknown"

class ExtractedEntity(BaseModel):
    """Individual entity extracted from text"""
    type: str = Field(..., description="Type of entity (time, date, location, etc.)")
    value: str = Field(..., description="Raw extracted text value")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    start_pos: int = Field(..., ge=0, description="Start position in original text")
    end_pos: int = Field(..., ge=0, description="End position in original text")
    normalized_value: Optional[str] = Field(None, description="Processed/normalized value")

class ExtractedEvent(BaseModel):
    """Complete event data extracted from natural language"""
    # Core event data
    title: Optional[str] = Field(None, description="Event title/name")
    description: Optional[str] = Field(None, description="Event description")
    location: Optional[str] = Field(None, description="Event location")
    
    # Raw temporal data (as extracted from text)
    date_text: Optional[str] = Field(None, description="Raw date text from input")
    time_text: Optional[str] = Field(None, description="Raw time text from input")
    duration_text: Optional[str] = Field(None, description="Raw duration text from input")
    
    # Resolved temporal data (processed into datetime objects)
    start_time: Optional[datetime] = Field(None, description="Calculated start datetime")
    end_time: Optional[datetime] = Field(None, description="Calculated end datetime")
    is_all_day: bool = Field(False, description="Whether this is an all-day event")
    
    # Processing metadata
    intent: IntentType = Field(IntentType.CREATE_EVENT, description="Detected user intent")
    confidence_score: float = Field(0.0, ge=0.0, le=1.0, description="Overall confidence")
    extracted_entities: List[ExtractedEntity] = Field(default_factory=list)
    original_text: str = Field("", description="Original input text")
    
    # Processing flags and feedback
    requires_clarification: bool = Field(False, description="Whether clarification is needed")
    missing_fields: List[str] = Field(default_factory=list, description="Required fields that are missing")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for missing data")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class NLPResponse(BaseModel):
    """Response from NLP processing pipeline"""
    success: bool = Field(..., description="Whether processing was successful")
    extracted_event: Optional[ExtractedEvent] = Field(None, description="Extracted event data")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    confidence_score: float = Field(0.0, ge=0.0, le=1.0, description="Overall confidence score")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    
    # For cases requiring user interaction
    clarification_needed: bool = Field(False, description="Whether user clarification is required")
    suggested_questions: List[str] = Field(default_factory=list, description="Questions to ask user")
    
    # For conflict detection (will be populated later)
    has_conflicts: bool = Field(False, description="Whether scheduling conflicts detected")
    conflicting_events: List[Dict[str, Any]] = Field(default_factory=list, description="Conflicting events")
    alternative_times: List[str] = Field(default_factory=list, description="Alternative time suggestions")

class TemporalContext(BaseModel):
    """Context for temporal resolution (current time, timezone, etc.)"""
    current_time: datetime = Field(..., description="Current datetime for relative calculations")
    user_timezone: str = Field("UTC", description="User's timezone")
    default_duration_minutes: int = Field(60, description="Default event duration in minutes")
    default_start_time: str = Field("09:00", description="Default start time for events")
    
class ProcessingStats(BaseModel):
    """Statistics about the NLP processing"""
    total_entities_found: int = Field(0, description="Total number of entities extracted")
    entities_by_type: Dict[str, int] = Field(default_factory=dict, description="Count of each entity type")
    confidence_by_type: Dict[str, float] = Field(default_factory=dict, description="Average confidence by type")
    processing_steps: List[str] = Field(default_factory=list, description="Steps performed during processing")