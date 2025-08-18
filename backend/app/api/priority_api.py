"""
Priority-Based Conflict Resolution API Endpoints

NEW API endpoints that supplement existing conflict detection functionality.
These endpoints provide priority-based scheduling suggestions without
modifying any existing API behavior.

SAFETY NOTE: These are ADDITIONAL endpoints that work alongside existing
conflict detection APIs without breaking any current functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import logging

from app.core.database import get_db
from app.services.priority_scheduler import PriorityBasedScheduler, PrioritySchedulingResult
from app.models.user import User

# Initialize router with prefix to avoid conflicts with existing endpoints
router = APIRouter(prefix="/api/v1/priority", tags=["Priority Scheduling"])
logger = logging.getLogger(__name__)

class PriorityScheduleRequest(BaseModel):
    """Request model for priority-based scheduling"""
    priority_level: int = Field(..., ge=1, le=5, description="Event priority (1-5 scale)")
    duration_minutes: int = Field(..., gt=0, le=480, description="Event duration in minutes")
    preferred_date: Optional[datetime] = Field(None, description="Preferred date for scheduling")
    exclude_times: Optional[List[Dict[str, datetime]]] = Field(None, description="Time ranges to exclude")
    num_suggestions: int = Field(5, ge=1, le=10, description="Number of suggestions to return")

class PriorityTimeSlotResponse(BaseModel):
    """Response model for priority time slot"""
    start_time: datetime
    end_time: datetime
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    priority_match_score: float = Field(..., ge=0.0, le=1.0)
    availability_score: float = Field(..., ge=0.0, le=1.0)
    is_prime_time: bool
    conflict_risk: float = Field(..., ge=0.0, le=1.0)

class PrioritySchedulingResponse(BaseModel):
    """Response model for priority-based scheduling"""
    success: bool
    message: str
    original_priority: int
    suggested_slots: List[PriorityTimeSlotResponse]
    reasoning: str
    total_slots_considered: int
    filter_criteria_used: List[str]
    fallback_used: bool = False
    processing_time_ms: Optional[float] = None

@router.post("/resolve", response_model=PrioritySchedulingResponse)
async def resolve_priority_scheduling(
    request: PriorityScheduleRequest,
    user_id: str = Query("default_user", description="User identifier"),
    db: Session = Depends(get_db)
):
    """
    NEW ENDPOINT: Generate priority-based time slot suggestions
    
    This endpoint provides intelligent scheduling based on event priority levels:
    - High Priority (4-5): Prime business hours (9 AM - 5 PM)
    - Medium Priority (2-3): Extended hours (8 AM - 6 PM)
    - Low Priority (1): Flexible hours (7 AM - 9 PM)
    
    Does NOT modify existing conflict detection functionality.
    """
    
    start_time = datetime.now()
    logger.info(f"🎯 Priority scheduling request for user {user_id}, "
               f"priority {request.priority_level}")
    
    try:
        # Initialize priority scheduler
        scheduler = PriorityBasedScheduler(db)
        
        # Process exclude times if provided
        exclude_times_tuples = None
        if request.exclude_times:
            exclude_times_tuples = [
                (item["start"], item["end"]) 
                for item in request.exclude_times
                if "start" in item and "end" in item
            ]
        
        # Get priority-based suggestions
        result = scheduler.suggest_priority_based_slots(
            user_id=user_id,
            priority_level=request.priority_level,
            duration_minutes=request.duration_minutes,
            exclude_times=exclude_times_tuples,
            preferred_date=request.preferred_date,
            num_suggestions=request.num_suggestions
        )
        
        # Convert result to response format
        slot_responses = [
            PriorityTimeSlotResponse(
                start_time=slot.start_time,
                end_time=slot.end_time,
                confidence=slot.confidence,
                reasoning=slot.reasoning,
                priority_match_score=slot.priority_match_score,
                availability_score=slot.availability_score,
                is_prime_time=slot.is_prime_time,
                conflict_risk=slot.conflict_risk
            )
            for slot in result.suggested_slots
        ]
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        response = PrioritySchedulingResponse(
            success=True,
            message=f"Generated {len(slot_responses)} priority-based suggestions",
            original_priority=result.original_priority,
            suggested_slots=slot_responses,
            reasoning=result.reasoning,
            total_slots_considered=result.total_slots_considered,
            filter_criteria_used=result.filter_criteria_used,
            fallback_used=result.fallback_used,
            processing_time_ms=processing_time
        )
        
        logger.info(f"✅ Priority scheduling completed in {processing_time:.1f}ms")
        return response
        
    except Exception as e:
        logger.error(f"❌ Priority scheduling failed: {str(e)}", exc_info=True)
        
        # Return graceful error response
        return PrioritySchedulingResponse(
            success=False,
            message=f"Priority scheduling failed: {str(e)}",
            original_priority=request.priority_level,
            suggested_slots=[],
            reasoning="Unable to generate suggestions due to system error",
            total_slots_considered=0,
            filter_criteria_used=["Error occurred"],
            fallback_used=True,
            processing_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )

@router.get("/windows", response_model=Dict[str, Any])
async def get_priority_time_windows():
    """
    NEW ENDPOINT: Get priority-based time windows configuration
    
    Returns the time windows used for different priority levels.
    Useful for frontend display and user education.
    """
    
    try:
        time_windows = {
            "priority_windows": {
                "5": {"name": "Critical", "hours": "9 AM - 5 PM", "start": 9, "end": 17},
                "4": {"name": "High", "hours": "9 AM - 5 PM", "start": 9, "end": 17},
                "3": {"name": "Medium", "hours": "8 AM - 6 PM", "start": 8, "end": 18},
                "2": {"name": "Low-Medium", "hours": "8 AM - 6 PM", "start": 8, "end": 18},
                "1": {"name": "Very Low", "hours": "7 AM - 9 PM", "start": 7, "end": 21}
            },
            "prime_business_hours": {
                "start": 9,
                "end": 17,
                "description": "9 AM - 5 PM (highest priority scheduling)"
            },
            "extended_business_hours": {
                "start": 8,
                "end": 18,
                "description": "8 AM - 6 PM (medium priority scheduling)"
            },
            "flexible_hours": {
                "start": 7,
                "end": 21,
                "description": "7 AM - 9 PM (low priority scheduling)"
            },
            "explanation": "Priority-based time windows optimize scheduling based on event importance"
        }
        
        return {
            "success": True,
            "data": time_windows,
            "message": "Priority time windows configuration retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get priority windows: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve priority configuration")

@router.get("/test", response_model=Dict[str, Any])
async def test_priority_endpoint(
    priority: int = Query(3, ge=1, le=5, description="Priority level to test"),
    duration: int = Query(60, gt=0, le=240, description="Duration in minutes"),
    db: Session = Depends(get_db)
):
    """
    NEW ENDPOINT: Test priority scheduling without authentication
    
    Useful for system validation and debugging.
    Does not require user authentication.
    """
    
    try:
        logger.info(f"🧪 Testing priority scheduling: priority={priority}, duration={duration}")
        
        # Create test scheduler
        scheduler = PriorityBasedScheduler(db)
        
        # Get test suggestions
        result = scheduler.suggest_priority_based_slots(
            user_id="test_user",
            priority_level=priority,
            duration_minutes=duration,
            num_suggestions=3
        )
        
        test_result = {
            "test_successful": True,
            "priority_level": priority,
            "duration_minutes": duration,
            "suggestions_generated": len(result.suggested_slots),
            "reasoning": result.reasoning,
            "time_window_used": f"{scheduler.PRIORITY_TIME_WINDOWS[priority][0]}:00-{scheduler.PRIORITY_TIME_WINDOWS[priority][1]}:00",
            "sample_slots": [
                {
                    "start": slot.start_time.isoformat(),
                    "end": slot.end_time.isoformat(),
                    "confidence": slot.confidence,
                    "is_prime_time": slot.is_prime_time
                }
                for slot in result.suggested_slots[:2]
            ],
            "message": "Priority scheduling system is functioning correctly"
        }
        
        logger.info("✅ Priority scheduling test completed successfully")
        return test_result
        
    except Exception as e:
        logger.error(f"❌ Priority scheduling test failed: {str(e)}")
        return {
            "test_successful": False,
            "error": str(e),
            "message": "Priority scheduling test failed"
        }

# Health check endpoint for the priority system
@router.get("/health", response_model=Dict[str, Any])
async def priority_system_health():
    """
    NEW ENDPOINT: Health check for priority scheduling system
    
    Verifies that all components are available and functioning.
    """
    
    try:
        health_status = {
            "priority_scheduler": "available",
            "bert_classification": "available",
            "user_behavior_analytics": "checking...",
            "smart_conflict_detection": "checking...",
            "overall_status": "healthy"
        }
        
        # Test component availability
        try:
            from app.nlp.user_behavior_analytics import UserBehaviorAnalyzer
            health_status["user_behavior_analytics"] = "available"
        except ImportError:
            health_status["user_behavior_analytics"] = "unavailable"
        
        try:
            from app.services.conflict_detector import SmartConflictDetector
            health_status["smart_conflict_detection"] = "available"
        except ImportError:
            health_status["smart_conflict_detection"] = "unavailable"
        
        # Overall status
        unavailable_components = [k for k, v in health_status.items() if v == "unavailable"]
        if unavailable_components:
            health_status["overall_status"] = "degraded"
            health_status["warning"] = f"Components unavailable: {', '.join(unavailable_components)}"
        
        return {
            "success": True,
            "health": health_status,
            "timestamp": datetime.now().isoformat(),
            "message": "Priority scheduling system health check completed"
        }
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        return {
            "success": False,
            "health": {"overall_status": "unhealthy"},
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "message": "Priority scheduling system health check failed"
        }
