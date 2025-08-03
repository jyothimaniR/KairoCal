# backend/app/schemas/conflicts.py
"""
Pydantic schemas for conflict detection API
Provides comprehensive data validation and serialization
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ConflictTypeEnum(str, Enum):
    """Enumeration of conflict types"""
    TIME_OVERLAP = "time_overlap"
    LOCATION_CONFLICT = "location_conflict"
    PRIORITY_CONFLICT = "priority_conflict"
    BUFFER_VIOLATION = "buffer_violation"
    PRODUCTIVITY_IMPACT = "productivity_impact"

class ConflictSeverityEnum(str, Enum):
    """Enumeration of conflict severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ConflictCheckRequest(BaseModel):
    """Request schema for conflict detection"""
    title: str = Field(..., min_length=1, max_length=255, description="Event title")
    description: Optional[str] = Field(None, max_length=1000, description="Event description")
    start_time: datetime = Field(..., description="Event start time")
    end_time: datetime = Field(..., description="Event end time")
    location: Optional[str] = Field(None, max_length=255, description="Event location")
    is_all_day: bool = Field(False, description="Whether this is an all-day event")
    buffer_minutes: Optional[int] = Field(
        15, ge=0, le=120, 
        description="Required buffer time before/after event (0-120 minutes)"
    )

    @validator("end_time")
    def end_time_must_be_after_start_time(cls, v, values):
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("title cannot be empty or whitespace only")
        return v.strip()

class ConflictDetectionResponse(BaseModel):
    """Response schema for detected conflicts"""
    conflict_id: str = Field(..., description="Unique identifier for the conflict")
    conflict_type: ConflictTypeEnum = Field(..., description="Type of conflict detected")
    severity: ConflictSeverityEnum = Field(..., description="Severity level of the conflict")
    affected_event_ids: List[str] = Field(..., description="IDs of events involved in the conflict")
    description: str = Field(..., description="Human-readable description of the conflict")
    buffer_minutes: int = Field(..., ge=0, description="Buffer time considered for this conflict")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for conflict detection")
    impact_score: float = Field(..., ge=0.0, le=1.0, description="Impact score of the conflict")

class TimeSlotAlternative(BaseModel):
    """Alternative time slot suggestion"""
    start_time: datetime = Field(..., description="Alternative start time")
    end_time: datetime = Field(..., description="Alternative end time")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for this alternative")
    reasoning: str = Field(..., description="Explanation for why this alternative is suggested")
    productivity_score: Optional[float] = Field(
        None, ge=0.0, le=1.0, 
        description="Productivity score based on user patterns"
    )

    @validator("end_time")
    def end_time_must_be_after_start_time(cls, v, values):
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v

class ConflictResolutionResponse(BaseModel):
    """Response schema for conflict resolution"""
    resolution_id: str = Field(..., description="Unique identifier for the resolution")
    conflict_id: str = Field(..., description="ID of the original conflict")
    alternatives: List[TimeSlotAlternative] = Field(..., description="List of alternative time slots")
    auto_resolution: Optional[TimeSlotAlternative] = Field(
        None, description="Automatically selected best alternative"
    )
    strategy: str = Field(..., description="Resolution strategy used")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence in the resolution")
    reasoning: str = Field(..., description="Detailed reasoning for the resolution approach")

class ConflictReportResponse(BaseModel):
    """Response schema for conflict analysis report"""
    total_conflicts: int = Field(..., ge=0, description="Total number of conflicts detected")
    severity_breakdown: Dict[str, int] = Field(..., description="Count of conflicts by severity level")
    type_breakdown: Dict[str, int] = Field(..., description="Count of conflicts by type")
    average_impact_score: Optional[float] = Field(
        None, ge=0.0, le=1.0, 
        description="Average impact score across all conflicts"
    )
    recommendations: List[str] = Field(..., description="Actionable recommendations")

class BatchConflictCheckRequest(BaseModel):
    """Request schema for batch conflict checking"""
    events: List[ConflictCheckRequest] = Field(
        ..., min_items=1, max_items=50,
        description="List of events to check for conflicts (max 50)"
    )
    global_buffer_minutes: Optional[int] = Field(
        15, ge=0, le=120,
        description="Default buffer time for all events if not specified individually"
    )

    @validator("events")
    def events_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("events list cannot be empty")
        return v

class BatchConflictResult(BaseModel):
    """Result for a single event in batch conflict check"""
    event_index: int = Field(..., ge=0, description="Index of the event in the original request")
    event_title: str = Field(..., description="Title of the event")
    conflicts_detected: int = Field(..., ge=0, description="Number of conflicts detected")
    conflicts: List[ConflictDetectionResponse] = Field(..., description="List of detected conflicts")

class BatchConflictCheckResponse(BaseModel):
    """Response schema for batch conflict checking"""
    total_events_checked: int = Field(..., ge=0, description="Total number of events processed")
    events_with_conflicts: int = Field(..., ge=0, description="Number of events that have conflicts")
    total_conflicts: int = Field(..., ge=0, description="Total conflicts across all events")
    results: List[BatchConflictResult] = Field(..., description="Detailed results for each event")

class UserConflictPattern(BaseModel):
    """User's conflict pattern analysis"""
    hour: int = Field(..., ge=0, le=23, description="Hour of day (0-23)")
    conflict_count: int = Field(..., ge=0, description="Number of conflicts at this hour")

class LocationUsage(BaseModel):
    """Location usage statistics"""
    location: str = Field(..., description="Location name")
    count: int = Field(..., ge=0, description="Number of times used")

class DayPreference(BaseModel):
    """Day preference statistics"""
    day: str = Field(..., description="Day of week")
    count: int = Field(..., ge=0, description="Number of events on this day")

class SchedulingPatterns(BaseModel):
    """User's scheduling pattern analysis"""
    average_event_duration: float = Field(..., ge=0, description="Average event duration in minutes")
    most_common_locations: List[LocationUsage] = Field(..., description="Most frequently used locations")
    preferred_days: List[DayPreference] = Field(..., description="Preferred days of week")

class ConflictHotspots(BaseModel):
    """Analysis of when conflicts most commonly occur"""
    busiest_hours: List[UserConflictPattern] = Field(..., description="Hours with most conflicts")
    recommendations: List[str] = Field(..., description="Recommendations for avoiding conflicts")

class UserPatternsResponse(BaseModel):
    """Response schema for user conflict patterns analysis"""
    analysis_period_days: int = Field(..., ge=0, description="Number of days analyzed")
    events_analyzed: int = Field(..., ge=0, description="Number of events included in analysis")
    conflict_hotspots: ConflictHotspots = Field(..., description="Analysis of conflict-prone times")
    scheduling_patterns: SchedulingPatterns = Field(..., description="User's scheduling patterns")
    recommendations: List[str] = Field(..., description="General recommendations for better scheduling")

class SmartRescheduleRequest(BaseModel):
    """Request schema for smart rescheduling"""
    preferred_date: Optional[datetime] = Field(None, description="Preferred date for rescheduling")
    max_alternatives: Optional[int] = Field(
        5, ge=1, le=10,
        description="Maximum number of alternatives to return"
    )

class CurrentEventTime(BaseModel):
    """Current event timing information"""
    start_time: datetime = Field(..., description="Current start time")
    end_time: datetime = Field(..., description="Current end time")

class SmartRescheduleResponse(BaseModel):
    """Response schema for smart rescheduling"""
    event_id: str = Field(..., description="ID of the event being rescheduled")
    event_title: str = Field(..., description="Title of the event")
    current_time: CurrentEventTime = Field(..., description="Current event timing")
    alternatives: List[TimeSlotAlternative] = Field(..., description="Alternative time slots")
    recommendation: Optional[TimeSlotAlternative] = Field(
        None, description="Best recommended alternative"
    )
    message: str = Field(..., description="Summary message about the rescheduling options")

# Error response schemas
class ConflictDetectionError(BaseModel):
    """Error response schema for conflict detection endpoints"""
    error_code: str = Field(..., description="Error code identifier")
    error_message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    suggestions: Optional[List[str]] = Field(None, description="Suggestions for resolving the error")

class ValidationError(BaseModel):
    """Validation error details"""
    field: str = Field(..., description="Field that failed validation")
    message: str = Field(..., description="Validation error message")
    value: Optional[Any] = Field(None, description="Value that failed validation")

class ConflictDetectionValidationError(BaseModel):
    """Validation error response for conflict detection"""
    error_type: str = Field("validation_error", description="Type of error")
    message: str = Field(..., description="Overall error message")
    validation_errors: List[ValidationError] = Field(..., description="Specific validation failures")

# Success response wrappers
class ConflictDetectionSuccess(BaseModel):
    """Generic success response wrapper"""
    success: bool = Field(True, description="Indicates successful operation")
    message: str = Field(..., description="Success message")
    data: Optional[Any] = Field(None, description="Response data")

# Configuration schemas
class ConflictDetectionConfig(BaseModel):
    """Configuration options for conflict detection"""
    default_buffer_minutes: int = Field(15, ge=0, le=120)
    max_alternatives_per_resolution: int = Field(5, ge=1, le=20)
    confidence_threshold_for_auto_resolution: float = Field(0.8, ge=0.0, le=1.0)
    enable_productivity_analysis: bool = Field(True)
    enable_location_fuzzy_matching: bool = Field(True)
    enable_priority_inference: bool = Field(True)

# Analytics schemas
class ConflictTrend(BaseModel):
    """Conflict trend over time"""
    date: datetime = Field(..., description="Date of the trend data point")
    conflict_count: int = Field(..., ge=0, description="Number of conflicts on this date")
    average_severity: float = Field(..., ge=0.0, le=4.0, description="Average severity score")

class ConflictAnalytics(BaseModel):
    """Advanced conflict analytics"""
    trends: List[ConflictTrend] = Field(..., description="Conflict trends over time")
    most_problematic_hours: List[UserConflictPattern] = Field(..., description="Hours with most issues")
    conflict_resolution_success_rate: float = Field(
        ..., ge=0.0, le=1.0,
        description="Success rate of auto-resolutions"
    )
    average_resolution_confidence: float = Field(
        ..., ge=0.0, le=1.0,
        description="Average confidence of resolutions"
    )

# Export all schemas for easy importing
__all__ = [
    # Enums
    "ConflictTypeEnum",
    "ConflictSeverityEnum",
    
    # Request schemas
    "ConflictCheckRequest",
    "BatchConflictCheckRequest", 
    "SmartRescheduleRequest",
    
    # Response schemas
    "ConflictDetectionResponse",
    "ConflictResolutionResponse",
    "ConflictReportResponse",
    "BatchConflictCheckResponse",
    "UserPatternsResponse",
    "SmartRescheduleResponse",
    
    # Component schemas
    "TimeSlotAlternative",
    "BatchConflictResult",
    "UserConflictPattern",
    "LocationUsage",
    "DayPreference",
    "SchedulingPatterns",
    "ConflictHotspots",
    "CurrentEventTime",
    
    # Error schemas
    "ConflictDetectionError",
    "ValidationError",
    "ConflictDetectionValidationError",
    
    # Utility schemas
    "ConflictDetectionSuccess",
    "ConflictDetectionConfig",
    "ConflictTrend",
    "ConflictAnalytics"
]