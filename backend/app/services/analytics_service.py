# backend/app/services/analytics_service.py
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, text
from uuid import UUID
import numpy as np
from dataclasses import dataclass

from app.models.event import Event
from app.models.user import User


@dataclass
class ProductivityMetrics:
    """Comprehensive productivity metrics for a user"""
    overall_score: float  # 0-100 scale
    meeting_efficiency: float  # 0-100 scale  
    energy_management: float  # 0-100 scale
    time_utilization: float  # 0-100 scale
    focus_score: float  # 0-100 scale
    weekly_patterns: Dict[str, float]  # Day-wise effectiveness
    hourly_patterns: Dict[int, float]  # Hour-wise effectiveness
    duration_accuracy: float  # How well planned vs actual durations match
    meeting_outcomes: Dict[str, int]  # Count of productive/waste/neutral
    recommendations: List[str]  # AI-powered recommendations


@dataclass
class TimePattern:
    """Time-based pattern analysis"""
    peak_hours: List[int]  # Hours when user is most effective
    low_energy_periods: List[int]  # Hours when energy is low
    optimal_meeting_duration: int  # Optimal meeting length in minutes
    preferred_days: List[str]  # Days with highest effectiveness
    meeting_density_score: float  # How packed the schedule is


@dataclass
class BehaviorInsights:
    """User behavior insights from calendar patterns"""
    average_meetings_per_day: float
    average_meeting_duration: int
    most_productive_meeting_type: str
    energy_trend: str  # 'increasing', 'decreasing', 'stable'
    scheduling_pattern: str  # 'front_loaded', 'back_loaded', 'balanced'
    effectiveness_trend: str  # 'improving', 'declining', 'stable'


class AnalyticsService:
    """Advanced analytics service for calendar productivity insights"""
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_productivity_metrics(
        self, 
        user_id: UUID, 
        start_date: datetime, 
        end_date: datetime
    ) -> ProductivityMetrics:
        """
        Calculate comprehensive productivity metrics for a user within date range
        
        Args:
            user_id: User ID to analyze
            start_date: Start of analysis period
            end_date: End of analysis period
            
        Returns:
            ProductivityMetrics with all calculated scores and insights
        """
        events = self._get_user_events(user_id, start_date, end_date)
        
        if not events:
            return self._empty_metrics()
            
        # Calculate individual metric components
        meeting_efficiency = self._calculate_meeting_efficiency(events)
        energy_management = self._calculate_energy_management(events)  
        time_utilization = self._calculate_time_utilization(events)
        focus_score = self._calculate_focus_score(events)
        duration_accuracy = self._calculate_duration_accuracy(events)
        
        # Pattern analysis
        weekly_patterns = self._analyze_weekly_patterns(events)
        hourly_patterns = self._analyze_hourly_patterns(events)
        meeting_outcomes = self._count_meeting_outcomes(events)
        
        # Overall productivity score (weighted average)
        overall_score = (
            meeting_efficiency * 0.3 +
            energy_management * 0.25 +
            time_utilization * 0.25 +
            focus_score * 0.2
        )
        
        # Generate AI recommendations
        recommendations = self._generate_recommendations(
            events, meeting_efficiency, energy_management, 
            time_utilization, focus_score, weekly_patterns, hourly_patterns
        )
        
        return ProductivityMetrics(
            overall_score=round(overall_score, 1),
            meeting_efficiency=round(meeting_efficiency, 1),
            energy_management=round(energy_management, 1),
            time_utilization=round(time_utilization, 1),
            focus_score=round(focus_score, 1),
            weekly_patterns=weekly_patterns,
            hourly_patterns=hourly_patterns,
            duration_accuracy=round(duration_accuracy, 1),
            meeting_outcomes=meeting_outcomes,
            recommendations=recommendations
        )
    
    def get_time_patterns(self, user_id: UUID, start_date: datetime, end_date: datetime) -> TimePattern:
        """Analyze time-based patterns for optimal scheduling"""
        events = self._get_user_events(user_id, start_date, end_date)
        
        if not events:
            return TimePattern([], [], 60, [], 0.0)
            
        peak_hours = self._find_peak_productivity_hours(events)
        low_energy_periods = self._find_low_energy_periods(events)
        optimal_duration = self._calculate_optimal_meeting_duration(events)
        preferred_days = self._find_preferred_days(events)
        density_score = self._calculate_meeting_density_score(events, start_date, end_date)
        
        return TimePattern(
            peak_hours=peak_hours,
            low_energy_periods=low_energy_periods,
            optimal_meeting_duration=optimal_duration,
            preferred_days=preferred_days,
            meeting_density_score=round(density_score, 1)
        )
    
    def get_behavior_insights(self, user_id: UUID, start_date: datetime, end_date: datetime) -> BehaviorInsights:
        """Generate behavioral insights from calendar patterns"""
        events = self._get_user_events(user_id, start_date, end_date)
        
        if not events:
            return BehaviorInsights(0, 0, "unknown", "stable", "balanced", "stable")
            
        avg_meetings_per_day = self._calculate_average_meetings_per_day(events, start_date, end_date)
        avg_duration = self._calculate_average_meeting_duration(events)
        productive_type = self._find_most_productive_meeting_type(events)
        energy_trend = self._analyze_energy_trend(events)
        scheduling_pattern = self._analyze_scheduling_pattern(events)
        effectiveness_trend = self._analyze_effectiveness_trend(events)
        
        return BehaviorInsights(
            average_meetings_per_day=round(avg_meetings_per_day, 1),
            average_meeting_duration=avg_duration,
            most_productive_meeting_type=productive_type,
            energy_trend=energy_trend,
            scheduling_pattern=scheduling_pattern,
            effectiveness_trend=effectiveness_trend
        )
    
    def get_weekly_analytics_summary(self, user_id: UUID) -> Dict:
        """Get weekly analytics summary for dashboard"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        metrics = self.get_productivity_metrics(user_id, start_date, end_date)
        patterns = self.get_time_patterns(user_id, start_date, end_date)
        insights = self.get_behavior_insights(user_id, start_date, end_date)
        
        # Calculate week-over-week changes
        prev_start = start_date - timedelta(days=7)
        prev_metrics = self.get_productivity_metrics(user_id, prev_start, start_date)
        
        return {
            "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
            "productivity": {
                "overall_score": metrics.overall_score,
                "change": round(metrics.overall_score - prev_metrics.overall_score, 1),
                "meeting_efficiency": metrics.meeting_efficiency,
                "energy_management": metrics.energy_management,
                "time_utilization": metrics.time_utilization,
                "focus_score": metrics.focus_score
            },
            "patterns": {
                "peak_hours": patterns.peak_hours,
                "optimal_duration": patterns.optimal_meeting_duration,
                "preferred_days": patterns.preferred_days,
                "meeting_density": patterns.meeting_density_score
            },
            "insights": {
                "avg_meetings_per_day": insights.average_meetings_per_day,
                "avg_duration": insights.average_meeting_duration,
                "energy_trend": insights.energy_trend,
                "effectiveness_trend": insights.effectiveness_trend
            },
            "outcomes": metrics.meeting_outcomes,
            "recommendations": metrics.recommendations[:3]  # Top 3 recommendations
        }
    
    def generate_ai_insights(self, user_id: UUID, period_days: int = 30) -> Dict:
        """Generate AI-powered insights using ML algorithms"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=period_days)
        events = self._get_user_events(user_id, start_date, end_date)
        
        if len(events) < 10:
            return {"insights": [], "confidence": 0.0, "data_points": len(events)}
            
        insights = []
        
        # Productivity correlation analysis
        productivity_insights = self._analyze_productivity_correlations(events)
        insights.extend(productivity_insights)
        
        # Meeting pattern anomalies
        anomaly_insights = self._detect_scheduling_anomalies(events)
        insights.extend(anomaly_insights)
        
        # Energy optimization opportunities  
        energy_insights = self._identify_energy_optimization(events)
        insights.extend(energy_insights)
        
        # Time block effectiveness
        time_block_insights = self._analyze_time_block_effectiveness(events)
        insights.extend(time_block_insights)
        
        confidence = min(len(events) / 50.0, 1.0)  # Higher confidence with more data
        
        return {
            "insights": insights[:8],  # Top 8 insights
            "confidence": round(confidence, 2),
            "data_points": len(events),
            "analysis_period": f"{period_days} days"
        }
    
    # Private helper methods
    def _get_user_events(self, user_id: UUID, start_date: datetime, end_date: datetime) -> List[Event]:
        """Get all events for user within date range"""
        return self.db.query(Event).filter(
            and_(
                Event.user_id == user_id,
                Event.start_time >= start_date,
                Event.start_time <= end_date,
                Event.effectiveness_rating.isnot(None)  # Only events with analytics data
            )
        ).order_by(Event.start_time).all()
    
    def _calculate_meeting_efficiency(self, events: List[Event]) -> float:
        """Calculate meeting efficiency score based on outcomes and ratings"""
        if not events:
            return 0.0
            
        total_weight = 0
        weighted_score = 0
        
        for event in events:
            # Weight by actual duration if available, otherwise use time difference
            duration = event.actual_duration if event.actual_duration else \
                      int((event.end_time - event.start_time).total_seconds() / 60)
            
            outcome_score = {"productive": 5, "neutral": 3, "waste": 1}.get(event.meeting_outcome, 3)
            effectiveness_score = event.effectiveness_rating or 3
            
            # Combined score weighted by meeting duration
            meeting_score = (outcome_score + effectiveness_score) / 2
            weighted_score += meeting_score * duration
            total_weight += duration
            
        return (weighted_score / total_weight) * 20  # Scale to 0-100
    
    def _calculate_energy_management(self, events: List[Event]) -> float:
        """Calculate energy management score"""
        if not events:
            return 0.0
            
        energy_scores = [event.energy_level for event in events if event.energy_level]
        if not energy_scores:
            return 0.0
            
        # Calculate variance in energy levels (lower variance = better management)
        mean_energy = np.mean(energy_scores)
        energy_variance = np.var(energy_scores)
        
        # Score based on mean energy and consistency (low variance)
        base_score = (mean_energy / 5) * 60  # 60% weight for average energy
        consistency_score = max(0, 40 - (energy_variance * 10))  # 40% weight for consistency
        
        return min(100, base_score + consistency_score)
    
    def _calculate_time_utilization(self, events: List[Event]) -> float:
        """Calculate time utilization efficiency"""
        if not events:
            return 0.0
            
        productive_time = 0
        total_time = 0
        
        for event in events:
            duration = event.actual_duration if event.actual_duration else \
                      int((event.end_time - event.start_time).total_seconds() / 60)
            
            total_time += duration
            
            # Weight productive time by effectiveness and outcome
            effectiveness_weight = (event.effectiveness_rating or 3) / 5
            outcome_weight = {"productive": 1.0, "neutral": 0.6, "waste": 0.2}.get(event.meeting_outcome, 0.6)
            
            productive_time += duration * effectiveness_weight * outcome_weight
            
        return (productive_time / total_time) * 100 if total_time > 0 else 0.0
    
    def _calculate_focus_score(self, events: List[Event]) -> float:
        """Calculate focus score based on meeting density and effectiveness"""
        if not events:
            return 0.0
            
        # Group events by day
        daily_events = {}
        for event in events:
            day = event.start_time.date()
            if day not in daily_events:
                daily_events[day] = []
            daily_events[day].append(event)
        
        daily_scores = []
        for day, day_events in daily_events.items():
            if len(day_events) == 0:
                continue
                
            # Calculate time gaps between meetings
            day_events.sort(key=lambda x: x.start_time)
            gaps = []
            for i in range(1, len(day_events)):
                gap = (day_events[i].start_time - day_events[i-1].end_time).total_seconds() / 60
                gaps.append(max(0, gap))
            
            # Score based on meeting density and effectiveness
            avg_effectiveness = np.mean([e.effectiveness_rating or 3 for e in day_events])
            meeting_count = len(day_events)
            avg_gap = np.mean(gaps) if gaps else 120  # Default 2-hour gap
            
            # Optimal meeting count per day is 4-6, optimal gap is 30-60 minutes
            density_penalty = abs(meeting_count - 5) * 5  # Penalty for too many/few meetings
            gap_score = max(0, 100 - abs(avg_gap - 45) * 2)  # Optimal gap around 45 minutes
            effectiveness_score = (avg_effectiveness / 5) * 50
            
            day_score = max(0, effectiveness_score + gap_score - density_penalty)
            daily_scores.append(day_score)
        
        return np.mean(daily_scores) if daily_scores else 0.0
    
    def _calculate_duration_accuracy(self, events: List[Event]) -> float:
        """Calculate how accurately planned vs actual durations match"""
        if not events:
            return 0.0
            
        accurate_events = 0
        total_events = 0
        
        for event in events:
            if event.planned_duration and event.actual_duration:
                total_events += 1
                accuracy = 1 - abs(event.planned_duration - event.actual_duration) / event.planned_duration
                if accuracy >= 0.8:  # Within 20% is considered accurate
                    accurate_events += 1
        
        return (accurate_events / total_events) * 100 if total_events > 0 else 0.0
    
    def _analyze_weekly_patterns(self, events: List[Event]) -> Dict[str, float]:
        """Analyze effectiveness patterns by day of week"""
        day_effectiveness = {
            "Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], 
            "Friday": [], "Saturday": [], "Sunday": []
        }
        
        for event in events:
            day_name = event.start_time.strftime("%A")
            if event.effectiveness_rating:
                day_effectiveness[day_name].append(event.effectiveness_rating)
        
        return {
            day: (np.mean(ratings) * 20) if ratings else 0.0  # Scale to 0-100
            for day, ratings in day_effectiveness.items()
        }
    
    def _analyze_hourly_patterns(self, events: List[Event]) -> Dict[int, float]:
        """Analyze effectiveness patterns by hour of day"""
        hourly_effectiveness = {hour: [] for hour in range(24)}
        
        for event in events:
            hour = event.start_time.hour
            if event.effectiveness_rating:
                hourly_effectiveness[hour].append(event.effectiveness_rating)
        
        return {
            hour: (np.mean(ratings) * 20) if ratings else 0.0  # Scale to 0-100
            for hour, ratings in hourly_effectiveness.items()
        }
    
    def _count_meeting_outcomes(self, events: List[Event]) -> Dict[str, int]:
        """Count meeting outcomes"""
        outcomes = {"productive": 0, "neutral": 0, "waste": 0}
        for event in events:
            outcome = event.meeting_outcome or "neutral"
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
        return outcomes
    
    def _find_peak_productivity_hours(self, events: List[Event]) -> List[int]:
        """Find hours with highest average effectiveness"""
        hourly_patterns = self._analyze_hourly_patterns(events)
        sorted_hours = sorted(hourly_patterns.items(), key=lambda x: x[1], reverse=True)
        # Return top 3 hours with effectiveness > 60
        return [hour for hour, score in sorted_hours[:3] if score > 60]
    
    def _find_low_energy_periods(self, events: List[Event]) -> List[int]:
        """Find hours with lowest energy levels"""
        hourly_energy = {hour: [] for hour in range(24)}
        
        for event in events:
            hour = event.start_time.hour
            if event.energy_level:
                hourly_energy[hour].append(event.energy_level)
        
        hourly_avg = {
            hour: np.mean(energy) if energy else 3.0
            for hour, energy in hourly_energy.items()
        }
        
        sorted_hours = sorted(hourly_avg.items(), key=lambda x: x[1])
        # Return hours with energy < 2.5
        return [hour for hour, energy in sorted_hours if energy < 2.5]
    
    def _calculate_optimal_meeting_duration(self, events: List[Event]) -> int:
        """Calculate optimal meeting duration based on effectiveness"""
        duration_effectiveness = {}
        
        for event in events:
            duration = event.actual_duration if event.actual_duration else \
                      int((event.end_time - event.start_time).total_seconds() / 60)
            
            # Group by 15-minute buckets
            bucket = (duration // 15) * 15
            if bucket not in duration_effectiveness:
                duration_effectiveness[bucket] = []
            
            duration_effectiveness[bucket].append(event.effectiveness_rating or 3)
        
        if not duration_effectiveness:
            return 60  # Default
            
        # Find duration with highest average effectiveness
        best_duration = max(
            duration_effectiveness.items(),
            key=lambda x: np.mean(x[1])
        )[0]
        
        return best_duration
    
    def _find_preferred_days(self, events: List[Event]) -> List[str]:
        """Find days with highest effectiveness"""
        weekly_patterns = self._analyze_weekly_patterns(events)
        sorted_days = sorted(weekly_patterns.items(), key=lambda x: x[1], reverse=True)
        # Return top 3 days with effectiveness > 60
        return [day for day, score in sorted_days[:3] if score > 60]
    
    def _calculate_meeting_density_score(self, events: List[Event], start_date: datetime, end_date: datetime) -> float:
        """Calculate how densely packed the schedule is"""
        total_days = (end_date - start_date).days + 1
        meeting_days = len(set(event.start_time.date() for event in events))
        
        if meeting_days == 0:
            return 0.0
            
        avg_meetings_per_meeting_day = len(events) / meeting_days
        schedule_utilization = meeting_days / total_days
        
        # Optimal density is 3-5 meetings per day, with 60-80% schedule utilization
        density_score = max(0, 100 - abs(avg_meetings_per_meeting_day - 4) * 10)
        utilization_score = max(0, 100 - abs(schedule_utilization - 0.7) * 100)
        
        return (density_score + utilization_score) / 2
    
    def _calculate_average_meetings_per_day(self, events: List[Event], start_date: datetime, end_date: datetime) -> float:
        """Calculate average meetings per day"""
        total_days = (end_date - start_date).days + 1
        return len(events) / total_days if total_days > 0 else 0.0
    
    def _calculate_average_meeting_duration(self, events: List[Event]) -> int:
        """Calculate average meeting duration in minutes"""
        if not events:
            return 0
            
        durations = []
        for event in events:
            duration = event.actual_duration if event.actual_duration else \
                      int((event.end_time - event.start_time).total_seconds() / 60)
            durations.append(duration)
        
        return int(np.mean(durations))
    
    def _find_most_productive_meeting_type(self, events: List[Event]) -> str:
        """Find meeting type with highest productivity (simplified)"""
        # For now, return based on creation method as a proxy for meeting type
        type_scores = {}
        for event in events:
            meeting_type = event.created_via or "manual"
            if meeting_type not in type_scores:
                type_scores[meeting_type] = []
            type_scores[meeting_type].append(event.effectiveness_rating or 3)
        
        if not type_scores:
            return "unknown"
            
        return max(type_scores.items(), key=lambda x: np.mean(x[1]))[0]
    
    def _analyze_energy_trend(self, events: List[Event]) -> str:
        """Analyze if energy levels are trending up, down, or stable"""
        if len(events) < 5:
            return "stable"
            
        # Split events into first and second half
        mid = len(events) // 2
        first_half = events[:mid]
        second_half = events[mid:]
        
        first_avg = np.mean([e.energy_level for e in first_half if e.energy_level])
        second_avg = np.mean([e.energy_level for e in second_half if e.energy_level])
        
        diff = second_avg - first_avg
        if diff > 0.3:
            return "increasing"
        elif diff < -0.3:
            return "decreasing"
        else:
            return "stable"
    
    def _analyze_scheduling_pattern(self, events: List[Event]) -> str:
        """Analyze if meetings are front-loaded, back-loaded, or balanced"""
        if not events:
            return "balanced"
            
        morning_meetings = sum(1 for e in events if e.start_time.hour < 12)
        afternoon_meetings = sum(1 for e in events if 12 <= e.start_time.hour < 17)
        evening_meetings = sum(1 for e in events if e.start_time.hour >= 17)
        
        total = len(events)
        morning_pct = morning_meetings / total
        evening_pct = evening_meetings / total
        
        if morning_pct > 0.6:
            return "front_loaded"
        elif evening_pct > 0.4:
            return "back_loaded"
        else:
            return "balanced"
    
    def _analyze_effectiveness_trend(self, events: List[Event]) -> str:
        """Analyze if effectiveness is improving, declining, or stable"""
        if len(events) < 5:
            return "stable"
            
        # Split events into first and second half
        mid = len(events) // 2
        first_half = events[:mid]
        second_half = events[mid:]
        
        first_avg = np.mean([e.effectiveness_rating for e in first_half if e.effectiveness_rating])
        second_avg = np.mean([e.effectiveness_rating for e in second_half if e.effectiveness_rating])
        
        diff = second_avg - first_avg
        if diff > 0.3:
            return "improving"
        elif diff < -0.3:
            return "declining"
        else:
            return "stable"
    
    def _generate_recommendations(self, events: List[Event], meeting_efficiency: float, 
                                energy_management: float, time_utilization: float, 
                                focus_score: float, weekly_patterns: Dict, 
                                hourly_patterns: Dict) -> List[str]:
        """Generate AI-powered recommendations"""
        recommendations = []
        
        # Meeting efficiency recommendations
        if meeting_efficiency < 60:
            waste_meetings = sum(1 for e in events if e.meeting_outcome == "waste")
            if waste_meetings > len(events) * 0.2:
                recommendations.append("Consider declining or shortening meetings with low expected value - 20% of your meetings are unproductive")
        
        # Energy management recommendations  
        if energy_management < 60:
            recommendations.append("Try scheduling important meetings during your peak energy hours to improve effectiveness")
        
        # Time utilization recommendations
        if time_utilization < 50:
            recommendations.append("Focus on meeting preparation and clear agendas to improve time utilization")
        
        # Focus recommendations
        if focus_score < 60:
            recommendations.append("Add buffer time between meetings to maintain focus and reduce context switching")
        
        # Pattern-based recommendations
        best_day = max(weekly_patterns.items(), key=lambda x: x[1])[0]
        if weekly_patterns[best_day] > 70:
            recommendations.append(f"Schedule important meetings on {best_day}s when you're most effective")
        
        peak_hours = [h for h, score in hourly_patterns.items() if score > 70]
        if peak_hours:
            hour_range = f"{min(peak_hours)}-{max(peak_hours)}"
            recommendations.append(f"Block {hour_range}:00 for deep work during your peak productivity hours")
        
        # Duration recommendations
        long_meetings = [e for e in events if (e.actual_duration or 60) > 90 and (e.effectiveness_rating or 3) < 3]
        if len(long_meetings) > len(events) * 0.3:
            recommendations.append("Consider breaking long meetings into shorter focused sessions for better engagement")
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def _empty_metrics(self) -> ProductivityMetrics:
        """Return empty metrics when no data is available"""
        return ProductivityMetrics(
            overall_score=0.0,
            meeting_efficiency=0.0,
            energy_management=0.0,
            time_utilization=0.0,
            focus_score=0.0,
            weekly_patterns={day: 0.0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
            hourly_patterns={hour: 0.0 for hour in range(24)},
            duration_accuracy=0.0,
            meeting_outcomes={"productive": 0, "neutral": 0, "waste": 0},
            recommendations=["Add more events with analytics data to get insights"]
        )
    
    # Advanced ML-based analysis methods
    def _analyze_productivity_correlations(self, events: List[Event]) -> List[str]:
        """Analyze correlations between different factors and productivity"""
        insights = []
        
        # Energy vs effectiveness correlation
        energy_eff_pairs = [(e.energy_level, e.effectiveness_rating) 
                           for e in events if e.energy_level and e.effectiveness_rating]
        
        if len(energy_eff_pairs) > 10:
            energies, effectiveness = zip(*energy_eff_pairs)
            correlation = np.corrcoef(energies, effectiveness)[0, 1]
            
            if correlation > 0.5:
                insights.append(f"Strong correlation (r={correlation:.2f}) between energy levels and meeting effectiveness - prioritize energy management")
            elif correlation < -0.3:
                insights.append("Negative correlation between energy and effectiveness detected - investigate energy drains")
        
        # Duration vs effectiveness
        duration_eff_pairs = [(e.actual_duration or int((e.end_time - e.start_time).total_seconds() / 60), 
                              e.effectiveness_rating)
                             for e in events if e.effectiveness_rating]
        
        if len(duration_eff_pairs) > 10:
            durations, effectiveness = zip(*duration_eff_pairs)
            correlation = np.corrcoef(durations, effectiveness)[0, 1]
            
            if correlation < -0.3:
                insights.append(f"Longer meetings tend to be less effective - consider shorter, focused sessions")
        
        return insights
    
    def _detect_scheduling_anomalies(self, events: List[Event]) -> List[str]:
        """Detect unusual patterns in scheduling"""
        insights = []
        
        # Back-to-back meeting detection
        events.sort(key=lambda x: x.start_time)
        back_to_back_count = 0
        
        for i in range(1, len(events)):
            gap = (events[i].start_time - events[i-1].end_time).total_seconds() / 60
            if gap < 5:  # Less than 5 minutes gap
                back_to_back_count += 1
        
        if back_to_back_count > len(events) * 0.4:
            insights.append(f"High back-to-back meeting rate ({back_to_back_count}/{len(events)}) - consider adding buffer time")
        
        # Late/early meeting detection
        very_early = sum(1 for e in events if e.start_time.hour < 8)
        very_late = sum(1 for e in events if e.start_time.hour > 18)
        
        if very_early > len(events) * 0.2:
            insights.append(f"Many early meetings detected - ensure this aligns with your natural energy patterns")
        
        if very_late > len(events) * 0.2:
            insights.append(f"Many late meetings detected - monitor impact on work-life balance")
        
        return insights
    
    def _identify_energy_optimization(self, events: List[Event]) -> List[str]:
        """Identify energy optimization opportunities"""
        insights = []
        
        # Low energy high importance correlation
        low_energy_events = [e for e in events if e.energy_level and e.energy_level <= 2]
        if len(low_energy_events) > len(events) * 0.3:
            insights.append("High frequency of low-energy meetings - investigate root causes and recovery strategies")
        
        # Energy consistency
        energy_levels = [e.energy_level for e in events if e.energy_level]
        if len(energy_levels) > 10:
            energy_std = np.std(energy_levels)
            if energy_std > 1.2:
                insights.append("High energy variability detected - focus on consistency through better scheduling and preparation")
        
        return insights
    
    def _analyze_time_block_effectiveness(self, events: List[Event]) -> List[str]:
        """Analyze effectiveness of different time blocks"""
        insights = []
        
        # Morning vs afternoon effectiveness
        morning_events = [e for e in events if e.start_time.hour < 12]
        afternoon_events = [e for e in events if 12 <= e.start_time.hour < 17]
        
        if len(morning_events) > 5 and len(afternoon_events) > 5:
            morning_avg = np.mean([e.effectiveness_rating for e in morning_events if e.effectiveness_rating])
            afternoon_avg = np.mean([e.effectiveness_rating for e in afternoon_events if e.effectiveness_rating])
            
            if morning_avg > afternoon_avg + 0.5:
                insights.append("Morning meetings are significantly more effective - consider front-loading your schedule")
            elif afternoon_avg > morning_avg + 0.5:
                insights.append("Afternoon meetings are more effective for you - optimize your PM schedule")
        
        return insights
