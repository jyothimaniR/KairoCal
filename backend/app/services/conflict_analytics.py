# backend/app/services/conflict_analytics.py
"""
Conflict Analytics Service for comprehensive conflict analysis and reporting
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
import json
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

@dataclass
class ConflictPattern:
    """Represents a detected conflict pattern"""
    pattern_type: str
    frequency: int
    severity: str
    description: str
    suggestions: List[str]
    confidence: float

@dataclass
class ConflictAnalyticsReport:
    """Comprehensive conflict analytics report"""
    total_conflicts: int
    resolved_conflicts: int
    unresolved_conflicts: int
    conflict_types: Dict[str, int]
    severity_breakdown: Dict[str, int]
    patterns: List[ConflictPattern]
    recommendations: List[str]
    performance_metrics: Dict[str, float]
    report_timestamp: datetime

class ConflictAnalytics:
    """
    Advanced conflict analytics service for pattern recognition and insights
    """
    
    def __init__(self, db_session=None):
        self.db = db_session
        self.logger = logger
        
    def analyze_user_conflict_patterns(self, user_id: str, days_back: int = 30) -> ConflictAnalyticsReport:
        """
        Analyze conflict patterns for a specific user
        
        Args:
            user_id: User identifier
            days_back: Number of days to analyze
            
        Returns:
            Comprehensive analytics report
        """
        try:
            # Get user's conflict history
            conflicts = self._get_user_conflicts(user_id, days_back)
            
            # Analyze patterns
            patterns = self._detect_conflict_patterns(conflicts)
            
            # Calculate metrics
            metrics = self._calculate_performance_metrics(conflicts)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(patterns, metrics)
            
            # Create report
            report = ConflictAnalyticsReport(
                total_conflicts=len(conflicts),
                resolved_conflicts=len([c for c in conflicts if c.get('is_resolved', False)]),
                unresolved_conflicts=len([c for c in conflicts if not c.get('is_resolved', False)]),
                conflict_types=self._count_conflict_types(conflicts),
                severity_breakdown=self._count_severity_levels(conflicts),
                patterns=patterns,
                recommendations=recommendations,
                performance_metrics=metrics,
                report_timestamp=datetime.now()
            )
            
            self.logger.info(f"Generated conflict analytics report for user {user_id}: {len(conflicts)} conflicts analyzed")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to analyze conflict patterns for user {user_id}: {e}")
            # Return empty report on error
            return ConflictAnalyticsReport(
                total_conflicts=0,
                resolved_conflicts=0,
                unresolved_conflicts=0,
                conflict_types={},
                severity_breakdown={},
                patterns=[],
                recommendations=[],
                performance_metrics={},
                report_timestamp=datetime.now()
            )
    
    def analyze_system_wide_conflicts(self, days_back: int = 7) -> Dict[str, Any]:
        """
        Analyze system-wide conflict patterns and performance
        
        Args:
            days_back: Number of days to analyze
            
        Returns:
            System-wide analytics report
        """
        try:
            # Get all conflicts in timeframe
            all_conflicts = self._get_all_conflicts(days_back)
            
            # System-wide metrics
            metrics = {
                'total_conflicts': len(all_conflicts),
                'conflicts_per_day': len(all_conflicts) / days_back if days_back > 0 else 0,
                'resolution_rate': self._calculate_resolution_rate(all_conflicts),
                'average_severity': self._calculate_average_severity(all_conflicts),
                'most_common_types': self._get_most_common_conflict_types(all_conflicts),
                'peak_conflict_times': self._analyze_peak_conflict_times(all_conflicts),
                'bert_performance': self._analyze_bert_performance(all_conflicts)
            }
            
            # Performance indicators
            performance = {
                'detection_accuracy': self._calculate_detection_accuracy(all_conflicts),
                'resolution_success_rate': self._calculate_resolution_success_rate(all_conflicts),
                'user_satisfaction_score': self._estimate_user_satisfaction(all_conflicts),
                'system_efficiency': self._calculate_system_efficiency(all_conflicts)
            }
            
            return {
                'system_metrics': metrics,
                'performance_indicators': performance,
                'trends': self._analyze_trends(all_conflicts, days_back),
                'recommendations': self._generate_system_recommendations(metrics, performance),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"System-wide conflict analysis failed: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _get_user_conflicts(self, user_id: str, days_back: int) -> List[Dict[str, Any]]:
        """Get user's conflict history from database"""
        # Mock data for now - replace with actual database query
        if not self.db:
            return self._generate_mock_conflicts(days_back)
            
        try:
            # This would be the actual database query
            # conflicts = self.db.query(Conflict).filter(
            #     Conflict.user_id == user_id,
            #     Conflict.created_at >= datetime.now() - timedelta(days=days_back)
            # ).all()
            # return [c.to_dict() for c in conflicts]
            
            # For now, return mock data
            return self._generate_mock_conflicts(days_back)
            
        except Exception as e:
            self.logger.error(f"Database query failed: {e}")
            return []
    
    def _get_all_conflicts(self, days_back: int) -> List[Dict[str, Any]]:
        """Get all conflicts from database"""
        # Mock data for now - replace with actual database query
        return self._generate_mock_conflicts(days_back * 5)  # Simulate multiple users
    
    def _generate_mock_conflicts(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock conflict data for testing"""
        import random
        
        conflict_types = ['time_overlap', 'location_conflict', 'priority_conflict', 'buffer_violation']
        severities = ['low', 'medium', 'high', 'critical']
        
        conflicts = []
        for i in range(count):
            conflicts.append({
                'id': f'conflict_{i}',
                'conflict_type': random.choice(conflict_types),
                'severity': random.choice(severities),
                'is_resolved': random.choice([True, False]),
                'confidence': random.uniform(0.3, 0.9),
                'impact_score': random.uniform(0.2, 1.0),
                'created_at': datetime.now() - timedelta(days=random.randint(0, 30)),
                'resolution_method': random.choice(['manual', 'auto_reschedule', 'ignored', None]),
                'detection_method': random.choice(['basic_v1', 'bert_enhanced'])
            })
        
        return conflicts
    
    def _detect_conflict_patterns(self, conflicts: List[Dict[str, Any]]) -> List[ConflictPattern]:
        """Detect recurring conflict patterns"""
        patterns = []
        
        # Time-based patterns
        time_patterns = self._analyze_time_patterns(conflicts)
        patterns.extend(time_patterns)
        
        # Type-based patterns
        type_patterns = self._analyze_type_patterns(conflicts)
        patterns.extend(type_patterns)
        
        # Severity patterns
        severity_patterns = self._analyze_severity_patterns(conflicts)
        patterns.extend(severity_patterns)
        
        return patterns
    
    def _analyze_time_patterns(self, conflicts: List[Dict[str, Any]]) -> List[ConflictPattern]:
        """Analyze time-based conflict patterns"""
        patterns = []
        
        # Group conflicts by hour of day
        hour_conflicts = defaultdict(int)
        for conflict in conflicts:
            if conflict.get('created_at'):
                hour = conflict['created_at'].hour
                hour_conflicts[hour] += 1
        
        # Find peak conflict hours
        if hour_conflicts:
            peak_hour = max(hour_conflicts, key=hour_conflicts.get)
            peak_count = hour_conflicts[peak_hour]
            
            if peak_count >= 3:  # Significant pattern
                patterns.append(ConflictPattern(
                    pattern_type='peak_hour_conflicts',
                    frequency=peak_count,
                    severity='medium',
                    description=f'High conflict frequency at {peak_hour}:00 ({peak_count} conflicts)',
                    suggestions=[
                        f'Consider avoiding scheduling at {peak_hour}:00',
                        'Implement buffer time around peak conflict hours',
                        'Analyze user scheduling preferences for this time slot'
                    ],
                    confidence=0.8
                ))
        
        return patterns
    
    def _analyze_type_patterns(self, conflicts: List[Dict[str, Any]]) -> List[ConflictPattern]:
        """Analyze conflict type patterns"""
        patterns = []
        
        type_counts = Counter(c.get('conflict_type', 'unknown') for c in conflicts)
        total_conflicts = len(conflicts)
        
        for conflict_type, count in type_counts.items():
            if count >= 3 and count / total_conflicts >= 0.3:  # 30% or more
                patterns.append(ConflictPattern(
                    pattern_type=f'frequent_{conflict_type}',
                    frequency=count,
                    severity='high' if count / total_conflicts >= 0.5 else 'medium',
                    description=f'Frequent {conflict_type} conflicts ({count}/{total_conflicts})',
                    suggestions=self._get_type_specific_suggestions(conflict_type),
                    confidence=0.7 + (count / total_conflicts * 0.3)
                ))
        
        return patterns
    
    def _analyze_severity_patterns(self, conflicts: List[Dict[str, Any]]) -> List[ConflictPattern]:
        """Analyze severity level patterns"""
        patterns = []
        
        severity_counts = Counter(c.get('severity', 'unknown') for c in conflicts)
        total_conflicts = len(conflicts)
        
        # Check for high severity pattern
        high_severity = severity_counts.get('high', 0) + severity_counts.get('critical', 0)
        if high_severity / total_conflicts >= 0.4:  # 40% or more high/critical
            patterns.append(ConflictPattern(
                pattern_type='high_severity_trend',
                frequency=high_severity,
                severity='critical',
                description=f'High severity conflicts are frequent ({high_severity}/{total_conflicts})',
                suggestions=[
                    'Review scheduling practices to prevent high-impact conflicts',
                    'Implement stricter conflict prevention rules',
                    'Consider priority-based scheduling assistance'
                ],
                confidence=0.8
            ))
        
        return patterns
    
    def _get_type_specific_suggestions(self, conflict_type: str) -> List[str]:
        """Get specific suggestions based on conflict type"""
        suggestions = {
            'time_overlap': [
                'Implement mandatory buffer time between events',
                'Use automatic conflict detection before scheduling',
                'Consider shorter default event durations'
            ],
            'location_conflict': [
                'Add travel time calculations between locations',
                'Group events by location when possible',
                'Implement location-aware scheduling'
            ],
            'priority_conflict': [
                'Improve priority classification training',
                'Add priority-based scheduling rules',
                'Implement better priority conflict resolution'
            ],
            'buffer_violation': [
                'Increase default buffer times',
                'Implement context-aware buffer requirements',
                'Add buffer time preferences per event type'
            ]
        }
        
        return suggestions.get(conflict_type, [
            'Review conflict detection rules',
            'Improve event scheduling practices'
        ])
    
    def _calculate_performance_metrics(self, conflicts: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate performance metrics"""
        if not conflicts:
            return {}
        
        total_conflicts = len(conflicts)
        resolved_conflicts = len([c for c in conflicts if c.get('is_resolved', False)])
        auto_resolved = len([c for c in conflicts if c.get('resolution_method') == 'auto_reschedule'])
        
        return {
            'resolution_rate': resolved_conflicts / total_conflicts if total_conflicts > 0 else 0.0,
            'auto_resolution_rate': auto_resolved / total_conflicts if total_conflicts > 0 else 0.0,
            'average_confidence': sum(c.get('confidence', 0.0) for c in conflicts) / total_conflicts,
            'average_impact': sum(c.get('impact_score', 0.0) for c in conflicts) / total_conflicts
        }
    
    def _generate_recommendations(self, patterns: List[ConflictPattern], metrics: Dict[str, float]) -> List[str]:
        """Generate recommendations based on patterns and metrics"""
        recommendations = []
        
        # Resolution rate recommendations
        resolution_rate = metrics.get('resolution_rate', 0.0)
        if resolution_rate < 0.6:
            recommendations.append('Improve conflict resolution strategies - current rate is below 60%')
        
        # Auto-resolution recommendations
        auto_resolution_rate = metrics.get('auto_resolution_rate', 0.0)
        if auto_resolution_rate < 0.3:
            recommendations.append('Consider implementing more automated conflict resolution options')
        
        # Pattern-based recommendations
        for pattern in patterns:
            if pattern.severity in ['high', 'critical']:
                recommendations.extend(pattern.suggestions[:2])  # Top 2 suggestions
        
        # Confidence recommendations
        avg_confidence = metrics.get('average_confidence', 0.0)
        if avg_confidence < 0.6:
            recommendations.append('Improve conflict detection confidence through better training data')
        
        return list(set(recommendations))  # Remove duplicates
    
    def _count_conflict_types(self, conflicts: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count conflicts by type"""
        return dict(Counter(c.get('conflict_type', 'unknown') for c in conflicts))
    
    def _count_severity_levels(self, conflicts: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count conflicts by severity"""
        return dict(Counter(c.get('severity', 'unknown') for c in conflicts))
    
    def _calculate_resolution_rate(self, conflicts: List[Dict[str, Any]]) -> float:
        """Calculate overall resolution rate"""
        if not conflicts:
            return 0.0
        resolved = len([c for c in conflicts if c.get('is_resolved', False)])
        return resolved / len(conflicts)
    
    def _calculate_average_severity(self, conflicts: List[Dict[str, Any]]) -> float:
        """Calculate average severity score"""
        severity_scores = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        if not conflicts:
            return 0.0
        
        total_score = sum(severity_scores.get(c.get('severity', 'low'), 1) for c in conflicts)
        return total_score / len(conflicts)
    
    def _get_most_common_conflict_types(self, conflicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get most common conflict types"""
        type_counts = Counter(c.get('conflict_type', 'unknown') for c in conflicts)
        return [{'type': t, 'count': c} for t, c in type_counts.most_common(5)]
    
    def _analyze_peak_conflict_times(self, conflicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze peak conflict times"""
        hour_counts = defaultdict(int)
        for conflict in conflicts:
            if conflict.get('created_at'):
                hour = conflict['created_at'].hour
                hour_counts[hour] += 1
        
        peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        return [{'hour': h, 'conflicts': c} for h, c in peak_hours]
    
    def _analyze_bert_performance(self, conflicts: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze BERT performance metrics"""
        bert_conflicts = [c for c in conflicts if c.get('detection_method') == 'bert_enhanced']
        basic_conflicts = [c for c in conflicts if c.get('detection_method') == 'basic_v1']
        
        if not bert_conflicts and not basic_conflicts:
            return {}
        
        bert_avg_confidence = sum(c.get('confidence', 0.0) for c in bert_conflicts) / len(bert_conflicts) if bert_conflicts else 0.0
        basic_avg_confidence = sum(c.get('confidence', 0.0) for c in basic_conflicts) / len(basic_conflicts) if basic_conflicts else 0.0
        
        return {
            'bert_usage_rate': len(bert_conflicts) / len(conflicts) if conflicts else 0.0,
            'bert_confidence': bert_avg_confidence,
            'basic_confidence': basic_avg_confidence,
            'bert_performance_boost': bert_avg_confidence - basic_avg_confidence
        }
    
    def _calculate_detection_accuracy(self, conflicts: List[Dict[str, Any]]) -> float:
        """Calculate detection accuracy score"""
        if not conflicts:
            return 0.0
        
        # Mock calculation - in reality, this would compare with ground truth
        avg_confidence = sum(c.get('confidence', 0.0) for c in conflicts) / len(conflicts)
        return avg_confidence * 0.9  # Approximate accuracy based on confidence
    
    def _calculate_resolution_success_rate(self, conflicts: List[Dict[str, Any]]) -> float:
        """Calculate resolution success rate"""
        resolved_conflicts = [c for c in conflicts if c.get('is_resolved', False)]
        if not resolved_conflicts:
            return 0.0
        
        # Mock calculation - success rate based on resolution methods
        successful_resolutions = len([c for c in resolved_conflicts 
                                    if c.get('resolution_method') in ['manual', 'auto_reschedule']])
        return successful_resolutions / len(resolved_conflicts)
    
    def _estimate_user_satisfaction(self, conflicts: List[Dict[str, Any]]) -> float:
        """Estimate user satisfaction score"""
        if not conflicts:
            return 5.0
        
        # Mock calculation based on resolution rate and conflict severity
        resolution_rate = self._calculate_resolution_rate(conflicts)
        avg_severity = self._calculate_average_severity(conflicts)
        
        # Higher resolution rate = higher satisfaction
        # Lower average severity = higher satisfaction
        satisfaction = (resolution_rate * 4) + (1 - (avg_severity - 1) / 3) * 1
        return max(1.0, min(5.0, satisfaction))
    
    def _calculate_system_efficiency(self, conflicts: List[Dict[str, Any]]) -> float:
        """Calculate overall system efficiency score"""
        if not conflicts:
            return 1.0
        
        auto_resolution_rate = len([c for c in conflicts if c.get('resolution_method') == 'auto_reschedule']) / len(conflicts)
        avg_confidence = sum(c.get('confidence', 0.0) for c in conflicts) / len(conflicts)
        
        # Efficiency based on automation and confidence
        efficiency = (auto_resolution_rate * 0.6) + (avg_confidence * 0.4)
        return efficiency
    
    def _analyze_trends(self, conflicts: List[Dict[str, Any]], days_back: int) -> Dict[str, Any]:
        """Analyze conflict trends over time"""
        if not conflicts or days_back <= 1:
            return {}
        
        # Group conflicts by day
        daily_conflicts = defaultdict(int)
        for conflict in conflicts:
            if conflict.get('created_at'):
                day = conflict['created_at'].date()
                daily_conflicts[day] += 1
        
        # Calculate trend
        sorted_days = sorted(daily_conflicts.keys())
        if len(sorted_days) >= 2:
            first_half = sorted_days[:len(sorted_days)//2]
            second_half = sorted_days[len(sorted_days)//2:]
            
            first_half_avg = sum(daily_conflicts[day] for day in first_half) / len(first_half)
            second_half_avg = sum(daily_conflicts[day] for day in second_half) / len(second_half)
            
            trend = 'increasing' if second_half_avg > first_half_avg else 'decreasing' if second_half_avg < first_half_avg else 'stable'
            
            return {
                'trend': trend,
                'first_period_avg': first_half_avg,
                'second_period_avg': second_half_avg,
                'trend_percentage': ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0
            }
        
        return {'trend': 'insufficient_data'}
    
    @staticmethod
    def generate_conflict_report(conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a quick conflict report from a list of conflict objects
        
        Args:
            conflicts: List of ConflictDetection objects or dictionaries
            
        Returns:
            Dictionary with conflict summary and analysis
        """
        if not conflicts:
            return {
                'total_conflicts': 0,
                'types': {},
                'severities': {},
                'summary': 'No conflicts detected'
            }
        
        # Convert ConflictDetection objects to dictionaries if needed
        conflict_data = []
        for conflict in conflicts:
            if hasattr(conflict, 'conflict_type'):
                # ConflictDetection object
                conflict_data.append({
                    'conflict_type': conflict.conflict_type.value if hasattr(conflict.conflict_type, 'value') else str(conflict.conflict_type),
                    'severity': conflict.severity.value if hasattr(conflict.severity, 'value') else str(conflict.severity),
                    'confidence': getattr(conflict, 'confidence', 0.0),
                    'description': getattr(conflict, 'description', ''),
                    'impact_score': getattr(conflict, 'impact_score', 0.0)
                })
            else:
                # Already a dictionary
                conflict_data.append(conflict)
        
        # Count types and severities
        types_count = {}
        severities_count = {}
        
        for conflict in conflict_data:
            conflict_type = conflict.get('conflict_type', 'unknown')
            severity = conflict.get('severity', 'unknown')
            
            types_count[conflict_type] = types_count.get(conflict_type, 0) + 1
            severities_count[severity] = severities_count.get(severity, 0) + 1
        
        # Calculate averages
        avg_confidence = sum(c.get('confidence', 0.0) for c in conflict_data) / len(conflict_data)
        avg_impact = sum(c.get('impact_score', 0.0) for c in conflict_data) / len(conflict_data)
        
        return {
            'total_conflicts': len(conflicts),
            'types': types_count,
            'severities': severities_count,
            'severity_breakdown': severities_count,  # Add alias for compatibility
            'average_confidence': avg_confidence,
            'average_impact_score': avg_impact,
            'summary': f'Detected {len(conflicts)} conflicts with {avg_confidence:.1%} average confidence',
            'recommendations': [
                'Review conflicts by severity level',
                'Consider rescheduling for high-impact conflicts',
                'Implement buffer time between events'
            ]
        }

    def _generate_system_recommendations(self, metrics: Dict[str, Any], performance: Dict[str, float]) -> List[str]:
        """Generate system-wide recommendations"""
        recommendations = []
        
        # Conflict frequency recommendations
        conflicts_per_day = metrics.get('conflicts_per_day', 0)
        if conflicts_per_day > 10:
            recommendations.append('High conflict frequency detected - consider implementing stricter scheduling rules')
        
        # Resolution rate recommendations
        resolution_rate = metrics.get('resolution_rate', 0.0)
        if resolution_rate < 0.7:
            recommendations.append('Improve conflict resolution mechanisms - current rate below 70%')
        
        # BERT performance recommendations
        bert_perf = metrics.get('bert_performance', {})
        if bert_perf.get('bert_usage_rate', 0) < 0.5:
            recommendations.append('Increase BERT model usage for better conflict detection accuracy')
        
        # User satisfaction recommendations
        satisfaction = performance.get('user_satisfaction_score', 5.0)
        if satisfaction < 3.5:
            recommendations.append('User satisfaction is low - review conflict handling user experience')
        
        return recommendations
