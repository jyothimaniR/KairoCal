#!/usr/bin/env python3
"""
Rule-based Priority Inference Engine for KairoCal
Provides fallback priority classification using keyword-based rules
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PriorityInferenceEngine:
    """Rule-based priority classification for events"""
    
    def __init__(self):
        self.priority_rules = self._initialize_priority_rules()
        
    def _initialize_priority_rules(self) -> Dict[int, Dict[str, List[str]]]:
        """Initialize keyword-based priority rules"""
        return {
            5: {  # Critical (Very High)
                'urgent_keywords': [
                    'urgent', 'emergency', 'critical', 'asap', 'immediately',
                    'crisis', 'fire', 'down', 'outage', 'crash', 'broken',
                    'deadline today', 'due now', 'overdue'
                ],
                'context_keywords': [
                    'server', 'production', 'system', 'client angry',
                    'board meeting', 'ceo', 'cto', 'president', 'director',
                    'lawsuit', 'compliance', 'audit', 'security breach'
                ]
            },
            4: {  # High
                'urgent_keywords': [
                    'important', 'priority', 'asap', 'soon', 'deadline',
                    'due tomorrow', 'final', 'submission', 'presentation'
                ],
                'context_keywords': [
                    'client', 'customer', 'proposal', 'contract', 'meeting',
                    'interview', 'review', 'approval', 'sign', 'deliver'
                ]
            },
            3: {  # Medium
                'urgent_keywords': [
                    'planned', 'scheduled', 'regular', 'weekly', 'monthly',
                    'routine', 'follow up', 'check in'
                ],
                'context_keywords': [
                    'team', 'standup', 'sync', 'update', 'report',
                    'doctor', 'appointment', 'meeting', 'call'
                ]
            },
            2: {  # Low
                'urgent_keywords': [
                    'optional', 'nice to have', 'when available',
                    'low priority', 'background', 'later'
                ],
                'context_keywords': [
                    'training', 'learning', 'workshop', 'seminar',
                    'social', 'fun', 'casual', 'informal'
                ]
            },
            1: {  # Very Low
                'urgent_keywords': [
                    'break', 'coffee', 'lunch', 'casual', 'optional',
                    'informal', 'social', 'fun', 'relax'
                ],
                'context_keywords': [
                    'chat', 'hang out', 'party', 'celebration',
                    'personal', 'hobby', 'entertainment'
                ]
            }
        }
    
    def _calculate_keyword_score(self, text: str, keywords: List[str]) -> float:
        """Calculate keyword match score for given text"""
        if not text or not keywords:
            return 0.0
            
        text_lower = text.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        return matches / len(keywords) if keywords else 0.0
    
    def _calculate_urgency_from_timing(self, event_data: Dict) -> float:
        """Calculate urgency based on event timing"""
        try:
            start_time_str = event_data.get('start_time')
            if not start_time_str:
                return 0.0
                
            # Parse start time
            if isinstance(start_time_str, str):
                start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            else:
                start_time = start_time_str
                
            now = datetime.now(start_time.tzinfo) if start_time.tzinfo else datetime.now()
            time_diff = start_time - now
            
            # Convert to hours
            hours_until = time_diff.total_seconds() / 3600
            
            # Urgency based on time until event
            if hours_until < 1:  # Less than 1 hour
                return 1.0
            elif hours_until < 6:  # Less than 6 hours
                return 0.8
            elif hours_until < 24:  # Less than 1 day
                return 0.6
            elif hours_until < 72:  # Less than 3 days
                return 0.4
            elif hours_until < 168:  # Less than 1 week
                return 0.2
            else:
                return 0.0
                
        except Exception as e:
            logger.warning(f"Error calculating timing urgency: {e}")
            return 0.0
    
    def infer_priority(self, title: str, description: Optional[str] = None, 
                      event_data: Optional[Dict] = None) -> int:
        """Infer event priority using rule-based approach"""
        
        # Combine text for analysis
        combined_text = title or ""
        if description:
            combined_text += " " + description
            
        if not combined_text.strip():
            return 3  # Default to medium priority
        
        # Calculate scores for each priority level
        priority_scores = {}
        
        for priority_level, rule_sets in self.priority_rules.items():
            urgent_score = self._calculate_keyword_score(combined_text, rule_sets.get('urgent_keywords', []))
            context_score = self._calculate_keyword_score(combined_text, rule_sets.get('context_keywords', []))
            
            # Weighted combination (urgent keywords have higher weight)
            combined_score = (urgent_score * 2.0) + (context_score * 1.0)
            priority_scores[priority_level] = combined_score
        
        # Add timing-based urgency if event data available
        if event_data:
            timing_urgency = self._calculate_urgency_from_timing(event_data)
            
            # Boost higher priorities based on timing urgency
            if timing_urgency > 0.8:  # Very urgent timing
                priority_scores[5] += timing_urgency
                priority_scores[4] += timing_urgency * 0.8
            elif timing_urgency > 0.5:  # Moderately urgent
                priority_scores[4] += timing_urgency
                priority_scores[3] += timing_urgency * 0.6
        
        # Find the priority level with highest score
        if not priority_scores or all(score == 0 for score in priority_scores.values()):
            return 3  # Default to medium if no matches
            
        best_priority = max(priority_scores.items(), key=lambda x: x[1])[0]
        return best_priority
    
    def get_priority_explanation(self, title: str, description: Optional[str] = None,
                               event_data: Optional[Dict] = None) -> Dict:
        """Get detailed explanation of priority inference"""
        
        combined_text = title or ""
        if description:
            combined_text += " " + description
        
        explanation = {
            'predicted_priority': self.infer_priority(title, description, event_data),
            'keyword_matches': {},
            'timing_factor': 0.0,
            'reasoning': []
        }
        
        # Analyze keyword matches
        for priority_level, rule_sets in self.priority_rules.items():
            urgent_matches = []
            context_matches = []
            
            for keyword in rule_sets.get('urgent_keywords', []):
                if keyword.lower() in combined_text.lower():
                    urgent_matches.append(keyword)
                    
            for keyword in rule_sets.get('context_keywords', []):
                if keyword.lower() in combined_text.lower():
                    context_matches.append(keyword)
            
            if urgent_matches or context_matches:
                explanation['keyword_matches'][priority_level] = {
                    'urgent': urgent_matches,
                    'context': context_matches
                }
        
        # Analyze timing
        if event_data:
            explanation['timing_factor'] = self._calculate_urgency_from_timing(event_data)
        
        # Generate reasoning
        priority = explanation['predicted_priority']
        if priority == 5:
            explanation['reasoning'].append("Critical priority due to urgent keywords or timing")
        elif priority == 4:
            explanation['reasoning'].append("High priority due to important keywords or near deadline")
        elif priority == 3:
            explanation['reasoning'].append("Medium priority - regular or routine event")
        elif priority == 2:
            explanation['reasoning'].append("Low priority - optional or training event")
        else:
            explanation['reasoning'].append("Very low priority - social or casual event")
        
        if explanation['timing_factor'] > 0.5:
            explanation['reasoning'].append(f"Timing urgency factor: {explanation['timing_factor']:.2f}")
        
        return explanation
    
    def test_sample_events(self) -> None:
        """Test the inference engine with sample events"""
        test_events = [
            {
                'title': 'URGENT: Server crashed, need immediate fix',
                'description': 'Production server down, customers can\'t access the application.',
                'expected_priority': 5
            },
            {
                'title': 'Team lunch next Friday',
                'description': 'Casual team lunch at the local restaurant.',
                'expected_priority': 1
            },
            {
                'title': 'Board meeting with CEO tomorrow',
                'description': 'Quarterly board meeting to discuss company performance.',
                'expected_priority': 5
            },
            {
                'title': 'Weekly team standup',
                'description': 'Regular weekly team standup meeting.',
                'expected_priority': 3
            }
        ]
        
        print("🧪 Testing Rule-based Priority Inference Engine")
        print("=" * 60)
        
        for event in test_events:
            predicted = self.infer_priority(event['title'], event['description'])
            status = "✅" if predicted == event['expected_priority'] else "❌"
            
            print(f"\n{status} Event: {event['title']}")
            print(f"   Expected: {event['expected_priority']}, Predicted: {predicted}")
            
            if predicted != event['expected_priority']:
                explanation = self.get_priority_explanation(event['title'], event['description'])
                print(f"   Reasoning: {', '.join(explanation['reasoning'])}")

if __name__ == "__main__":
    # Test the inference engine
    engine = PriorityInferenceEngine()
    engine.test_sample_events()
