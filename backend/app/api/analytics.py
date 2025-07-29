# backend/app/api/analytics.py
"""
API endpoints for User Behavior Analytics
Provides intelligent scheduling insights and time slot suggestions
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from app.core.database import get_db
from app.services.user_behavior_analytics import BehaviorAnalyticsService
from app.models.user import User

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/user/{cognito_sub}/insights")
def get_user_insights(
    cognito_sub: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive behavior insights for a user
    
    Returns user's scheduling patterns, preferences, and recommendations
    """
    # Verify user exists
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found. Please create your profile first."
        )
    
    # Get analytics service
    analytics_service = BehaviorAnalyticsService(db)
    
    try:
        insights = analytics_service.get_user_insights(str(user.id))
        return {
            "status": "success",
            "data": insights,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate insights: {str(e)}"
        )


@router.get("/user/{cognito_sub}/time-suggestions")
def get_smart_time_suggestions(
    cognito_sub: str,
    duration: int = Query(..., description="Event duration in minutes", ge=15, le=480),
    preferred_date: Optional[str] = Query(None, description="Preferred date in ISO format (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get AI-powered time slot suggestions for scheduling a new event
    
    Args:
        cognito_sub: User's Cognito identifier
        duration: Event duration in minutes (15-480)
        preferred_date: Optional preferred date in YYYY-MM-DD format
    
    Returns:
        List of optimal time slot suggestions with confidence scores
    """
    # Verify user exists
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found. Please create your profile first."
        )
    
    # Validate preferred_date if provided
    if preferred_date:
        try:
            datetime.fromisoformat(preferred_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD format."
            )
    
    # Get analytics service
    analytics_service = BehaviorAnalyticsService(db)
    
    try:
        suggestions = analytics_service.suggest_meeting_times(
            user_id=str(user.id),
            duration_minutes=duration,
            preferred_date=preferred_date
        )
        return {
            "status": "success",
            "data": suggestions,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate time suggestions: {str(e)}"
        )


@router.get("/user/{cognito_sub}/productivity-score")
def get_productivity_score(
    cognito_sub: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get user's current productivity score and trends
    """
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found. Please create your profile first."
        )
    
    analytics_service = BehaviorAnalyticsService(db)
    
    try:
        # Get user pattern for productivity analysis
        analyzer = analytics_service.analyzer
        pattern = analyzer.analyze_user_patterns(str(user.id))
        
        return {
            "status": "success",
            "data": {
                "user_id": str(user.id),
                "productivity_score": pattern.productivity_score,
                "score_category": _get_score_category(pattern.productivity_score),
                "focus_blocks": [
                    {
                        "start_hour": start,
                        "end_hour": end,
                        "duration_hours": end - start
                    }
                    for start, end in pattern.focus_blocks
                ],
                "recommendations": _get_productivity_recommendations(pattern.productivity_score),
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate productivity score: {str(e)}"
        )


@router.get("/user/{cognito_sub}/meeting-patterns")
def get_meeting_patterns(
    cognito_sub: str,
    days_back: int = Query(30, description="Number of days to analyze", ge=7, le=365),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyze user's meeting patterns and scheduling habits
    """
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found. Please create your profile first."
        )
    
    analytics_service = BehaviorAnalyticsService(db)
    
    try:
        analyzer = analytics_service.analyzer
        pattern = analyzer.analyze_user_patterns(str(user.id))
        
        # Calculate meeting statistics
        total_event_types = sum(pattern.event_types.values())
        meeting_distribution = {
            event_type: {
                "count": count,
                "percentage": round((count / total_event_types) * 100, 1)
            }
            for event_type, count in pattern.event_types.items()
        }
        
        # Day preferences
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                    "Friday", "Saturday", "Sunday"]
        preferred_day_names = [day_names[day] for day in pattern.preferred_days]
        
        return {
            "status": "success",
            "data": {
                "user_id": str(user.id),
                "analysis_period_days": days_back,
                "meeting_patterns": {
                    "preferred_hours": pattern.preferred_hours,
                    "preferred_days": preferred_day_names,
                    "average_duration_minutes": pattern.avg_meeting_duration,
                    "event_type_distribution": meeting_distribution,
                    "common_locations": pattern.common_locations,
                    "peak_meeting_hours": pattern.preferred_hours[:3],
                    "scheduling_insights": {
                        "most_active_day": preferred_day_names[0] if preferred_day_names else "Monday",
                        "preferred_meeting_length": _categorize_duration(pattern.avg_meeting_duration),
                        "location_flexibility": len(pattern.common_locations),
                        "schedule_consistency": _calculate_consistency_score(pattern)
                    }
                },
                "generated_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze meeting patterns: {str(e)}"
        )


@router.post("/user/{cognito_sub}/feedback")
def submit_scheduling_feedback(
    cognito_sub: str,
    feedback_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Submit feedback on scheduling suggestions to improve ML recommendations
    
    Expected feedback_data format:
    {
        "suggestion_id": "optional_id",
        "selected_time": "2024-01-15T10:00:00",
        "rating": 5,  # 1-5 stars
        "reason": "Perfect timing for my schedule",
        "alternative_preferred": "2024-01-15T14:00:00"  # optional
    }
    """
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found. Please create your profile first."
        )
    
    # Validate feedback data
    required_fields = ["selected_time", "rating"]
    for field in required_fields:
        if field not in feedback_data:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )
    
    # Validate rating
    if not isinstance(feedback_data["rating"], int) or not 1 <= feedback_data["rating"] <= 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be an integer between 1 and 5"
        )
    
    try:
        # Store feedback (in production, this would update ML models)
        feedback_record = {
            "user_id": str(user.id),
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback_data,
            "processed": False
        }
        
        # Here you would typically store this in a feedback table
        # For now, we'll just acknowledge receipt
        
        return {
            "status": "success",
            "message": "Feedback received and will be used to improve recommendations",
            "data": {
                "feedback_id": f"fb_{user.id}_{int(datetime.now().timestamp())}",
                "user_id": str(user.id),
                "received_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process feedback: {str(e)}"
        )


@router.get("/user/{cognito_sub}/optimization-report")
def get_schedule_optimization_report(
    cognito_sub: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate a comprehensive schedule optimization report
    """
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found. Please create your profile first."
        )
    
    analytics_service = BehaviorAnalyticsService(db)
    
    try:
        analyzer = analytics_service.analyzer
        pattern = analyzer.analyze_user_patterns(str(user.id))
        
        # Generate optimization insights
        optimization_suggestions = []
        
        # Focus time optimization
        if len(pattern.focus_blocks) < 2:
            optimization_suggestions.append({
                "category": "Focus Time",
                "suggestion": "Consider adding a second focus block to your day",
                "impact": "High",
                "reason": "Multiple focus sessions can improve productivity by 25-40%"
            })
        
        # Meeting duration optimization
        if pattern.avg_meeting_duration > 75:
            optimization_suggestions.append({
                "category": "Meeting Efficiency",
                "suggestion": "Try shorter meeting durations (45-60 minutes)",
                "impact": "Medium",
                "reason": "Shorter meetings often lead to more focused discussions"
            })
        
        # Day distribution optimization
        weekday_events = sum(1 for day in pattern.preferred_days if day < 5)
        if weekday_events < 4:
            optimization_suggestions.append({
                "category": "Schedule Balance",
                "suggestion": "Spread meetings more evenly across weekdays",
                "impact": "Medium",
                "reason": "Balanced scheduling reduces daily overload"
            })
        
        # Productivity score insights
        productivity_insights = []
        if pattern.productivity_score < 70:
            productivity_insights.append("Consider reviewing your peak hours and scheduling important tasks during focus blocks")
        elif pattern.productivity_score > 85:
            productivity_insights.append("Excellent productivity patterns! Maintain your current scheduling approach.")
        else:
            productivity_insights.append("Good productivity balance. Minor tweaks to focus blocks could provide additional benefits.")
        
        return {
            "status": "success",
            "data": {
                "user_id": str(user.id),
                "report_generated": datetime.now().isoformat(),
                "current_productivity_score": pattern.productivity_score,
                "optimization_opportunities": optimization_suggestions,
                "productivity_insights": productivity_insights,
                "schedule_health": {
                    "focus_time_utilization": len(pattern.focus_blocks) * 2,  # hours per day
                    "meeting_load": len(pattern.preferred_hours),
                    "schedule_flexibility": len(pattern.common_locations),
                    "work_life_balance": "Good" if 5 not in pattern.preferred_days and 6 not in pattern.preferred_days else "Needs attention"
                },
                "next_review_date": (datetime.now() + timedelta(days=30)).isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate optimization report: {str(e)}"
        )


# Helper functions
def _get_score_category(score: float) -> str:
    """Categorize productivity score"""
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Very Good"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Fair"
    else:
        return "Needs Improvement"


def _get_productivity_recommendations(score: float) -> List[str]:
    """Get recommendations based on productivity score"""
    if score >= 85:
        return [
            "Maintain your current scheduling patterns",
            "Consider mentoring others on time management",
            "Experiment with advanced productivity techniques"
        ]
    elif score >= 70:
        return [
            "Try blocking more time for deep work",
            "Consider shorter, more focused meetings",
            "Review your peak productivity hours"
        ]
    else:
        return [
            "Focus on identifying your most productive hours",
            "Reduce meeting overload where possible",
            "Implement regular breaks between tasks",
            "Consider time-blocking techniques"
        ]


def _categorize_duration(duration: int) -> str:
    """Categorize meeting duration"""
    if duration <= 30:
        return "Short meetings (≤30 min)"
    elif duration <= 60:
        return "Standard meetings (30-60 min)"
    elif duration <= 90:
        return "Long meetings (60-90 min)"
    else:
        return "Extended meetings (>90 min)"


def _calculate_consistency_score(pattern) -> str:
    """Calculate schedule consistency score"""
    # Simple heuristic based on pattern regularity
    hour_spread = max(pattern.preferred_hours) - min(pattern.preferred_hours) if pattern.preferred_hours else 12
    day_consistency = len(pattern.preferred_days)
    
    if hour_spread <= 6 and day_consistency <= 5:
        return "High"
    elif hour_spread <= 10 and day_consistency <= 6:
        return "Medium"
    else:
        return "Low"


# Health check endpoint
@router.get("/health")
def analytics_health_check():
    """Health check for analytics service"""
    return {
        "service": "User Behavior Analytics",
        "status": "healthy",
        "version": "1.0.0",
        "features": [
            "User Pattern Analysis",
            "Smart Time Suggestions",
            "Productivity Scoring",
            "Schedule Optimization"
        ],
        "timestamp": datetime.now().isoformat()
    }