# backend/app/api/analytics.py
"""
Analytics Dashboard API endpoints for comprehensive calendar productivity insights
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging
import statistics
from collections import defaultdict, Counter

from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.nlp.user_behavior_analytics import BehaviorAnalyticsService
from app.models.user import User
from app.models.event import Event

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


def get_user_from_cognito(cognito_sub: str, db: Session) -> User:
    """Helper function to get user from Cognito sub ID"""
    user = db.query(User).filter(User.cognito_sub == cognito_sub).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User profile not found"
        )
    return user


# ========================================
# PRODUCTIVITY ANALYTICS DASHBOARD ENDPOINTS  
# ========================================

@router.get("/productivity/metrics")
def get_productivity_metrics(
    cognito_sub: str,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    period: Optional[str] = Query("week", description="Period: week, month, quarter"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive productivity metrics for Analytics Dashboard
    
    Returns:
        Complete productivity analysis including scores, patterns, and recommendations
    """
    user = get_user_from_cognito(cognito_sub, db)
    analytics_service = AnalyticsService(db)
    
    # Parse date range
    if not start_date or not end_date:
        end_dt = datetime.utcnow()
        if period == "week":
            start_dt = end_dt - timedelta(days=7)
        elif period == "month":
            start_dt = end_dt - timedelta(days=30)
        elif period == "quarter":
            start_dt = end_dt - timedelta(days=90)
        else:
            start_dt = end_dt - timedelta(days=7)
    else:
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    logger.info(f"📊 Getting productivity metrics for user {user.id} from {start_dt} to {end_dt}")
    
    try:
        metrics = analytics_service.get_productivity_metrics(user.id, start_dt, end_dt)
        
        return {
            "status": "success",
            "user_id": str(user.id),
            "period": {
                "start_date": start_dt.isoformat(),
                "end_date": end_dt.isoformat(),
                "period_type": period
            },
            "metrics": {
                "overall_score": metrics.overall_score,
                "components": {
                    "meeting_efficiency": metrics.meeting_efficiency,
                    "energy_management": metrics.energy_management,
                    "time_utilization": metrics.time_utilization,
                    "focus_score": metrics.focus_score
                },
                "accuracy": {
                    "duration_accuracy": metrics.duration_accuracy
                },
                "patterns": {
                    "weekly_effectiveness": metrics.weekly_patterns,
                    "hourly_effectiveness": metrics.hourly_patterns
                },
                "outcomes": metrics.meeting_outcomes,
                "recommendations": metrics.recommendations
            },
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get productivity metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate metrics: {str(e)}")


@router.get("/productivity/patterns")
def get_time_patterns(
    cognito_sub: str,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    period: Optional[str] = Query("month", description="Period: week, month, quarter"),
    db: Session = Depends(get_db)
):
    """
    Get time-based productivity patterns for optimal scheduling
    """
    user = get_user_from_cognito(cognito_sub, db)
    analytics_service = AnalyticsService(db)
    
    # Parse date range
    if not start_date or not end_date:
        end_dt = datetime.utcnow()
        if period == "week":
            start_dt = end_dt - timedelta(days=7)
        elif period == "month":
            start_dt = end_dt - timedelta(days=30)
        elif period == "quarter":
            start_dt = end_dt - timedelta(days=90)
        else:
            start_dt = end_dt - timedelta(days=30)
    else:
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    logger.info(f"📅 Getting time patterns for user {user.id}")
    
    try:
        patterns = analytics_service.get_time_patterns(user.id, start_dt, end_dt)
        
        return {
            "status": "success",
            "user_id": str(user.id),
            "period": {
                "start_date": start_dt.isoformat(),
                "end_date": end_dt.isoformat()
            },
            "patterns": {
                "peak_productivity_hours": patterns.peak_hours,
                "low_energy_periods": patterns.low_energy_periods,
                "optimal_meeting_duration": patterns.optimal_meeting_duration,
                "preferred_days": patterns.preferred_days,
                "schedule_density": {
                    "score": patterns.meeting_density_score,
                    "interpretation": _interpret_density_score(patterns.meeting_density_score)
                }
            },
            "scheduling_recommendations": _generate_scheduling_recommendations(patterns),
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get time patterns: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze patterns: {str(e)}")


@router.get("/productivity/insights")
def get_behavior_insights(
    cognito_sub: str,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    period: Optional[str] = Query("month", description="Period: week, month, quarter"),
    db: Session = Depends(get_db)
):
    """
    Get behavioral insights from calendar patterns
    """
    user = get_user_from_cognito(cognito_sub, db)
    analytics_service = AnalyticsService(db)
    
    # Parse date range
    if not start_date or not end_date:
        end_dt = datetime.utcnow()
        if period == "week":
            start_dt = end_dt - timedelta(days=7)
        elif period == "month":
            start_dt = end_dt - timedelta(days=30)
        elif period == "quarter":
            start_dt = end_dt - timedelta(days=90)
        else:
            start_dt = end_dt - timedelta(days=30)
    else:
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    logger.info(f"🧠 Getting behavior insights for user {user.id}")
    
    try:
        insights = analytics_service.get_behavior_insights(user.id, start_dt, end_dt)
        
        return {
            "status": "success",
            "user_id": str(user.id),
            "period": {
                "start_date": start_dt.isoformat(),
                "end_date": end_dt.isoformat()
            },
            "insights": {
                "meeting_statistics": {
                    "average_meetings_per_day": insights.average_meetings_per_day,
                    "average_duration_minutes": insights.average_meeting_duration,
                    "duration_category": _categorize_duration(insights.average_meeting_duration)
                },
                "productivity_patterns": {
                    "most_productive_meeting_type": insights.most_productive_meeting_type,
                    "energy_trend": insights.energy_trend,
                    "effectiveness_trend": insights.effectiveness_trend,
                    "scheduling_pattern": insights.scheduling_pattern
                },
                "behavioral_indicators": _generate_behavioral_indicators(insights),
                "improvement_areas": _identify_improvement_areas(insights)
            },
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get behavior insights: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")


@router.get("/dashboard/weekly-summary")
def get_weekly_analytics_summary(
    cognito_sub: str,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive weekly analytics summary for main dashboard
    """
    user = get_user_from_cognito(cognito_sub, db)
    analytics_service = AnalyticsService(db)
    
    logger.info(f"📋 Getting weekly summary for user {user.id}")
    
    try:
        summary = analytics_service.get_weekly_analytics_summary(user.id)
        
        return {
            "status": "success",
            "user_id": str(user.id),
            "summary": summary,
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get weekly summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")


@router.get("/ai/insights")
def get_ai_insights(
    cognito_sub: str,
    period_days: int = Query(30, ge=7, le=90, description="Analysis period in days"),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered insights using machine learning algorithms
    """
    user = get_user_from_cognito(cognito_sub, db)
    analytics_service = AnalyticsService(db)
    
    logger.info(f"🤖 Generating AI insights for user {user.id} over {period_days} days")
    
    try:
        ai_insights = analytics_service.generate_ai_insights(user.id, period_days)
        
        return {
            "status": "success",
            "user_id": str(user.id),
            "analysis_period": f"{period_days} days",
            "ai_insights": ai_insights,
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to generate AI insights: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate AI insights: {str(e)}")


@router.get("/trends/comparison")
def get_productivity_trends(
    cognito_sub: str,
    compare_periods: int = Query(4, ge=2, le=12, description="Number of periods to compare"),
    period_type: str = Query("week", description="Period type: week, month"),
    db: Session = Depends(get_db)
):
    """
    Get productivity trends comparing multiple periods
    """
    user = get_user_from_cognito(cognito_sub, db)
    analytics_service = AnalyticsService(db)
    
    logger.info(f"📈 Getting productivity trends for user {user.id}")
    
    try:
        # Calculate period duration
        period_days = 7 if period_type == "week" else 30
        
        trends = []
        end_date = datetime.utcnow()
        
        for i in range(compare_periods):
            period_end = end_date - timedelta(days=i * period_days)
            period_start = period_end - timedelta(days=period_days)
            
            metrics = analytics_service.get_productivity_metrics(user.id, period_start, period_end)
            
            trends.append({
                "period": i + 1,
                "start_date": period_start.isoformat(),
                "end_date": period_end.isoformat(),
                "overall_score": metrics.overall_score,
                "meeting_efficiency": metrics.meeting_efficiency,
                "energy_management": metrics.energy_management,
                "time_utilization": metrics.time_utilization,
                "focus_score": metrics.focus_score,
                "total_meetings": sum(metrics.meeting_outcomes.values())
            })
        
        # Calculate trend direction
        recent_avg = sum(t["overall_score"] for t in trends[:2]) / 2
        older_avg = sum(t["overall_score"] for t in trends[-2:]) / 2
        trend_direction = "improving" if recent_avg > older_avg + 5 else "declining" if recent_avg < older_avg - 5 else "stable"
        
        return {
            "status": "success",
            "user_id": str(user.id),
            "comparison": {
                "period_type": period_type,
                "periods_analyzed": compare_periods,
                "trend_direction": trend_direction,
                "average_change": round(recent_avg - older_avg, 1)
            },
            "trends": list(reversed(trends)),  # Show oldest to newest
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get productivity trends: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze trends: {str(e)}")


# ========================================
# BERT PRIORITY ANALYTICS ENDPOINTS  
# ========================================

@router.get("/priority/trends")
def get_priority_trends(
    cognito_sub: str,
    days_back: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    granularity: str = Query("weekly", description="Granularity: daily, weekly, monthly"),
    db: Session = Depends(get_db)
):
    """
    Analyze priority distribution trends over time
    
    Returns:
        Priority distribution patterns, trend analysis, and insights
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    logger.info(f"📈 Analyzing priority trends for user {user.id} over {days_back} days")
    
    # Get all events in the period
    events = db.query(Event).filter(
        Event.user_id == user.id,
        Event.start_time >= start_date,
        Event.start_time <= end_date
    ).order_by(Event.start_time).all()
    
    if not events:
        return {
            "user_id": user.id,
            "period": {"start_date": start_date.isoformat(), "end_date": end_date.isoformat()},
            "message": "No events found in the specified period",
            "trends": []
        }
    
    # Group events by time periods
    time_buckets = defaultdict(lambda: defaultdict(int))
    
    for event in events:
        if granularity == "daily":
            bucket = event.start_time.date().isoformat()
        elif granularity == "weekly":
            # Get start of week (Monday)
            week_start = event.start_time.date() - timedelta(days=event.start_time.weekday())
            bucket = week_start.isoformat()
        else:  # monthly
            bucket = event.start_time.strftime("%Y-%m")
        
        priority = event.priority_level or 3
        time_buckets[bucket][priority] += 1
        time_buckets[bucket]['total'] += 1
    
    # Calculate trends
    trends = []
    for period, priorities in sorted(time_buckets.items()):
        total = priorities['total']
        trend_data = {
            "period": period,
            "total_events": total,
            "priority_distribution": {
                str(p): {"count": priorities.get(p, 0), "percentage": round(priorities.get(p, 0) / total * 100, 1)}
                for p in [1, 2, 3, 4, 5]
            },
            "high_priority_percentage": round((priorities.get(1, 0) + priorities.get(2, 0)) / total * 100, 1),
            "critical_events": priorities.get(1, 0)
        }
        trends.append(trend_data)
    
    # Calculate overall insights
    total_events = len(events)
    high_priority_events = len([e for e in events if (e.priority_level or 3) <= 2])
    critical_events = len([e for e in events if e.priority_level == 1])
    
    insights = {
        "total_events_analyzed": total_events,
        "average_events_per_period": round(total_events / len(trends), 1) if trends else 0,
        "high_priority_rate": round(high_priority_events / total_events * 100, 1),
        "critical_event_rate": round(critical_events / total_events * 100, 1),
        "trend_direction": _calculate_trend_direction(trends),
        "busiest_period": max(trends, key=lambda x: x['total_events'])['period'] if trends else None
    }
    
    return {
        "user_id": user.id,
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "granularity": granularity
        },
        "trends": trends,
        "insights": insights
    }


@router.get("/bert/performance")
def get_bert_performance_metrics(
    cognito_sub: str,
    days_back: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    include_confidence_distribution: bool = Query(True, description="Include confidence score distribution"),
    db: Session = Depends(get_db)
):
    """
    Analyze BERT classification performance and accuracy metrics
    
    Returns:
        BERT classification statistics, confidence patterns, and performance insights
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    logger.info(f"🤖 Analyzing BERT performance for user {user.id} over {days_back} days")
    
    # Get events with BERT classifications
    bert_events = db.query(Event).filter(
        Event.user_id == user.id,
        Event.classification_method == 'bert',
        Event.start_time >= start_date,
        Event.start_time <= end_date
    ).all()
    
    # Get all events for comparison
    all_events = db.query(Event).filter(
        Event.user_id == user.id,
        Event.start_time >= start_date,
        Event.start_time <= end_date
    ).all()
    
    if not all_events:
        return {
            "user_id": user.id,
            "message": "No events found in the specified period",
            "bert_metrics": {}
        }
    
    total_events = len(all_events)
    bert_classified = len(bert_events)
    
    # Classification method distribution
    method_counts = Counter(e.classification_method or 'unknown' for e in all_events)
    
    # BERT confidence analysis
    confidences = [e.priority_confidence for e in bert_events if e.priority_confidence is not None]
    
    confidence_stats = {}
    if confidences:
        confidence_stats = {
            "average": round(statistics.mean(confidences), 3),
            "median": round(statistics.median(confidences), 3),
            "min": round(min(confidences), 3),
            "max": round(max(confidences), 3),
            "std_dev": round(statistics.stdev(confidences), 3) if len(confidences) > 1 else 0
        }
    
    # Confidence distribution buckets
    confidence_distribution = {}
    if include_confidence_distribution and confidences:
        buckets = {"0.0-0.2": 0, "0.2-0.4": 0, "0.4-0.6": 0, "0.6-0.8": 0, "0.8-1.0": 0}
        
        for conf in confidences:
            if conf < 0.2:
                buckets["0.0-0.2"] += 1
            elif conf < 0.4:
                buckets["0.2-0.4"] += 1
            elif conf < 0.6:
                buckets["0.4-0.6"] += 1
            elif conf < 0.8:
                buckets["0.6-0.8"] += 1
            else:
                buckets["0.8-1.0"] += 1
        
        confidence_distribution = {
            bucket: {"count": count, "percentage": round(count / len(confidences) * 100, 1)}
            for bucket, count in buckets.items()
        }
    
    # Priority distribution comparison
    bert_priority_dist = Counter(e.priority_level for e in bert_events)
    
    # Performance insights
    high_confidence_events = len([e for e in bert_events if (e.priority_confidence or 0) >= 0.8])
    low_confidence_events = len([e for e in bert_events if (e.priority_confidence or 0) < 0.5])
    
    return {
        "user_id": user.id,
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        },
        "classification_overview": {
            "total_events": total_events,
            "bert_classified": bert_classified,
            "bert_adoption_rate": round(bert_classified / total_events * 100, 1) if total_events > 0 else 0,
            "method_distribution": {
                method: {"count": count, "percentage": round(count / total_events * 100, 1)}
                for method, count in method_counts.items()
            }
        },
        "bert_performance": {
            "confidence_statistics": confidence_stats,
            "confidence_distribution": confidence_distribution,
            "high_confidence_rate": round(high_confidence_events / bert_classified * 100, 1) if bert_classified > 0 else 0,
            "low_confidence_rate": round(low_confidence_events / bert_classified * 100, 1) if bert_classified > 0 else 0,
            "priority_distribution": {
                str(p): bert_priority_dist.get(p, 0) for p in [1, 2, 3, 4, 5]
            }
        },
        "recommendations": _generate_bert_recommendations(confidence_stats, confidence_distribution, bert_classified, total_events)
    }


@router.get("/conflicts/resolution-effectiveness")
def get_conflict_resolution_effectiveness(
    cognito_sub: str,
    days_back: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Analyze effectiveness of priority-based conflict resolution
    
    Returns:
        Conflict resolution statistics and effectiveness metrics
    """
    user = get_user_from_cognito(cognito_sub, db)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    logger.info(f"⚡ Analyzing conflict resolution effectiveness for user {user.id}")
    
    events = db.query(Event).filter(
        Event.user_id == user.id,
        Event.start_time >= start_date,
        Event.start_time <= end_date
    ).order_by(Event.start_time).all()
    
    # Detect conflicts
    conflicts_detected = 0
    priority_conflicts = 0
    resolved_by_priority = 0
    
    conflict_details = []
    
    for i, event1 in enumerate(events):
        for event2 in events[i+1:]:
            # Check for time overlap
            if (event1.start_time < event2.end_time and event1.end_time > event2.start_time):
                conflicts_detected += 1
                
                priority1 = event1.priority_level or 3
                priority2 = event2.priority_level or 3
                priority_diff = abs(priority1 - priority2)
                
                if priority_diff >= 1:
                    priority_conflicts += 1
                    
                    # Assume higher priority wins (lower number = higher priority)
                    if priority_diff >= 2:
                        resolved_by_priority += 1
                    
                    conflict_details.append({
                        "event1_priority": priority1,
                        "event2_priority": priority2,
                        "priority_difference": priority_diff,
                        "resolution_confidence": "high" if priority_diff >= 2 else "medium",
                        "overlap_duration": int((min(event1.end_time, event2.end_time) - max(event1.start_time, event2.start_time)).total_seconds() / 60)
                    })
    
    effectiveness_metrics = {
        "conflict_analysis": {
            "total_conflicts_detected": conflicts_detected,
            "priority_based_conflicts": priority_conflicts,
            "clear_priority_resolutions": resolved_by_priority,
            "resolution_effectiveness_rate": round(resolved_by_priority / priority_conflicts * 100, 1) if priority_conflicts > 0 else 0
        },
        "conflict_patterns": {
            "average_priority_difference": round(statistics.mean([c["priority_difference"] for c in conflict_details]), 1) if conflict_details else 0,
            "high_confidence_resolutions": len([c for c in conflict_details if c["resolution_confidence"] == "high"]),
            "average_overlap_minutes": round(statistics.mean([c["overlap_duration"] for c in conflict_details]), 1) if conflict_details else 0
        },
        "recommendations": _generate_conflict_recommendations(conflicts_detected, priority_conflicts, resolved_by_priority)
    }
    
    return {
        "user_id": user.id,
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        },
        "effectiveness_metrics": effectiveness_metrics,
        "conflict_details": conflict_details[:10]  # Return top 10 for review
    }


# User Behavior Analytics Endpoints (Existing)


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


# Analytics Dashboard Helper Functions

def _interpret_density_score(score: float) -> str:
    """Interpret meeting density score"""
    if score >= 80:
        return "Optimal - Well-balanced schedule"
    elif score >= 60:
        return "Good - Minor optimization possible"
    elif score >= 40:
        return "Fair - Consider schedule adjustments"
    else:
        return "Poor - Schedule needs significant optimization"


def _generate_scheduling_recommendations(patterns) -> List[str]:
    """Generate scheduling recommendations based on patterns"""
    recommendations = []
    
    if len(patterns.peak_hours) > 0:
        peak_range = f"{min(patterns.peak_hours)}-{max(patterns.peak_hours)}"
        recommendations.append(f"Schedule important meetings during peak hours: {peak_range}:00")
    
    if len(patterns.low_energy_periods) > 0:
        low_range = f"{min(patterns.low_energy_periods)}-{max(patterns.low_energy_periods)}"
        recommendations.append(f"Avoid scheduling during low energy periods: {low_range}:00")
    
    if patterns.optimal_meeting_duration != 60:
        recommendations.append(f"Optimal meeting length for you is {patterns.optimal_meeting_duration} minutes")
    
    if len(patterns.preferred_days) > 0:
        recommendations.append(f"Your most productive days are: {', '.join(patterns.preferred_days)}")
    
    if patterns.meeting_density_score < 60:
        recommendations.append("Consider spreading meetings more evenly throughout the week")
    
    return recommendations


def _generate_behavioral_indicators(insights) -> Dict[str, str]:
    """Generate behavioral indicators from insights"""
    indicators = {}
    
    # Meeting frequency indicator
    if insights.average_meetings_per_day > 8:
        indicators["meeting_load"] = "High - Consider reducing meeting frequency"
    elif insights.average_meetings_per_day > 5:
        indicators["meeting_load"] = "Moderate - Well-balanced"
    else:
        indicators["meeting_load"] = "Light - Could accommodate more meetings"
    
    # Duration preference
    if insights.average_meeting_duration > 90:
        indicators["duration_preference"] = "Long meetings - Consider breaking into shorter sessions"
    elif insights.average_meeting_duration < 30:
        indicators["duration_preference"] = "Short meetings - Efficient time usage"
    else:
        indicators["duration_preference"] = "Standard meetings - Good balance"
    
    # Energy management
    indicators["energy_management"] = f"Energy trend: {insights.energy_trend.replace('_', ' ').title()}"
    
    # Effectiveness improvement
    indicators["effectiveness"] = f"Effectiveness: {insights.effectiveness_trend.replace('_', ' ').title()}"
    
    # Schedule pattern
    indicators["schedule_pattern"] = f"Schedule pattern: {insights.scheduling_pattern.replace('_', ' ').title()}"
    
    return indicators


def _identify_improvement_areas(insights) -> List[str]:
    """Identify areas for improvement based on insights"""
    improvements = []
    
    if insights.energy_trend == "decreasing":
        improvements.append("Energy levels are declining - consider reviewing workload and rest patterns")
    
    if insights.effectiveness_trend == "declining":
        improvements.append("Meeting effectiveness is declining - review meeting quality and preparation")
    
    if insights.average_meetings_per_day > 8:
        improvements.append("High meeting frequency detected - consider consolidating or declining unnecessary meetings")
    
    if insights.average_meeting_duration > 90:
        improvements.append("Long average meeting duration - try breaking meetings into focused shorter sessions")
    
    if insights.scheduling_pattern == "back_loaded":
        improvements.append("Many late meetings detected - consider earlier scheduling for better work-life balance")
    
    if insights.most_productive_meeting_type != "manual":
        improvements.append(f"Consider using more {insights.most_productive_meeting_type} meeting types for better outcomes")
    
    return improvements


# BERT Analytics Helper Functions

def _calculate_trend_direction(trends: List[Dict]) -> str:
    """Calculate overall trend direction for priority patterns"""
    if len(trends) < 2:
        return "insufficient_data"
    
    recent_periods = trends[-3:] if len(trends) >= 3 else trends[-2:]
    earlier_periods = trends[:3] if len(trends) >= 6 else trends[:len(trends)//2] if len(trends) > 2 else [trends[0]]
    
    recent_high_priority = statistics.mean([p["high_priority_percentage"] for p in recent_periods])
    earlier_high_priority = statistics.mean([p["high_priority_percentage"] for p in earlier_periods])
    
    diff = recent_high_priority - earlier_high_priority
    
    if diff > 5:
        return "increasing_high_priority"
    elif diff < -5:
        return "decreasing_high_priority"
    else:
        return "stable"


def _generate_bert_recommendations(confidence_stats: Dict, confidence_distribution: Dict, bert_classified: int, total_events: int) -> List[str]:
    """Generate recommendations based on BERT performance"""
    recommendations = []
    
    if bert_classified / total_events < 0.7:
        recommendations.append("Consider enabling auto-classification for more events to improve priority accuracy")
    
    if confidence_stats.get("average", 0) < 0.6:
        recommendations.append("Low average confidence detected - consider reviewing and correcting classifications to improve model performance")
    
    if confidence_distribution.get("0.0-0.4", {}).get("percentage", 0) > 20:
        recommendations.append("High percentage of low-confidence classifications - manual review recommended")
    
    if confidence_stats.get("std_dev", 0) > 0.3:
        recommendations.append("High confidence variance detected - model may need additional training data")
    
    return recommendations


def _generate_conflict_recommendations(total_conflicts: int, priority_conflicts: int, resolved: int) -> List[str]:
    """Generate conflict resolution recommendations"""
    recommendations = []
    
    if total_conflicts > 10:
        recommendations.append("High number of scheduling conflicts detected - consider calendar optimization")
    
    if priority_conflicts > 0 and resolved / priority_conflicts < 0.7:
        recommendations.append("Many conflicts cannot be clearly resolved by priority - consider improving priority classification")
    
    if resolved > 0:
        recommendations.append("Priority-based conflict resolution is working effectively - continue using priority classifications")
    
    return recommendations


# Health check endpoint
@router.get("/health")
def analytics_health_check():
    """Health check for analytics service"""
    return {
        "service": "User Behavior Analytics & BERT Priority Analytics",
        "status": "healthy",
        "version": "2.0.0",
        "features": [
            "User Pattern Analysis",
            "Smart Time Suggestions", 
            "Productivity Scoring",
            "Schedule Optimization",
            "BERT Priority Trends",
            "Classification Performance",
            "Conflict Resolution Analytics"
        ],
        "timestamp": datetime.now().isoformat()
    }