# backend/app/nlp/pattern_matcher.py
"""
Regex-based pattern matching for entity extraction from natural language
"""

import re
from typing import Dict, List, Optional, Set
from .entities import ExtractedEntity

class PatternMatcher:
    """Regex-based pattern matching for entity extraction"""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self._compiled_patterns = self._compile_patterns()
    
    def _initialize_patterns(self) -> Dict[str, List[Dict]]:
        """Initialize all regex patterns with confidence scores"""
        return {
            "time": [
                # 12-hour format with minutes
                {"pattern": r"\b(\d{1,2}):(\d{2})\s*(am|pm)\b", "confidence": 0.95, "group": "12h_full"},
                # 12-hour format without minutes
                {"pattern": r"\b(\d{1,2})\s*(am|pm)\b", "confidence": 0.90, "group": "12h_simple"},
                # Special time words
                {"pattern": r"\b(noon|midnight)\b", "confidence": 0.85, "group": "special"},
                # 24-hour format
                {"pattern": r"\b(\d{1,2}):(\d{2})\b", "confidence": 0.70, "group": "24h"},
                # Relative time
                {"pattern": r"\b(morning|afternoon|evening|night)\b", "confidence": 0.60, "group": "relative"},
                # Approximate time
                {"pattern": r"\b(around|about|roughly)\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\b", "confidence": 0.75, "group": "approximate"},
            ],
            
            "date": [
                # Relative dates (high confidence)
                {"pattern": r"\b(tomorrow)\b", "confidence": 0.95, "group": "relative_day"},
                {"pattern": r"\b(today)\b", "confidence": 0.95, "group": "relative_day"},
                {"pattern": r"\b(yesterday)\b", "confidence": 0.90, "group": "relative_day"},
                
                # Next/this + weekday
                {"pattern": r"\b(next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", "confidence": 0.90, "group": "next_weekday"},
                
                # Standalone weekdays
                {"pattern": r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", "confidence": 0.80, "group": "weekday"},
                
                # Numeric dates
                {"pattern": r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", "confidence": 0.95, "group": "full_date"},
                {"pattern": r"\b(\d{1,2})/(\d{1,2})\b", "confidence": 0.85, "group": "month_day"},
                
                # Month + day
                {"pattern": r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})\b", "confidence": 0.90, "group": "month_day_text"},
                
                # Relative periods
                {"pattern": r"\b(next\s+week|this\s+week|next\s+month|this\s+month)\b", "confidence": 0.70, "group": "relative_period"},
            ],
            
            "duration": [
                # Specific duration
                {"pattern": r"\b(\d+)\s*hours?\b", "confidence": 0.90, "group": "hours"},
                {"pattern": r"\b(\d+)\s*minutes?\b", "confidence": 0.90, "group": "minutes"},
                {"pattern": r"\b(\d+)\s*hrs?\b", "confidence": 0.85, "group": "hours_short"},
                {"pattern": r"\b(\d+)\s*mins?\b", "confidence": 0.85, "group": "minutes_short"},
                
                # All day indicator
                {"pattern": r"\b(all\s*day|full\s*day|entire\s*day)\b", "confidence": 0.95, "group": "all_day"},
                
                # Common duration patterns
                {"pattern": r"\b(half\s*hour|30\s*minutes?)\b", "confidence": 0.80, "group": "half_hour"},
                {"pattern": r"\b(quick|brief|short)\b", "confidence": 0.60, "group": "short"},
                {"pattern": r"\b(long|extended)\b", "confidence": 0.60, "group": "long"},
            ],
            
            "location": [
                # Medical locations
                {"pattern": r"\bat\s+([A-Za-z\s]+(?:clinic|hospital|medical\s*center))\b", "confidence": 0.90, "group": "medical"},
                
                # Office/business locations  
                {"pattern": r"\bat\s+([A-Za-z\s]+(?:office|building|center|headquarters))\b", "confidence": 0.85, "group": "business"},
                
                # Room/venue locations
                {"pattern": r"\bin\s+([A-Za-z\s]+(?:room|hall|auditorium|conference\s*room))\b", "confidence": 0.85, "group": "room"},
                
                # Restaurant/social locations
                {"pattern": r"\bat\s+([A-Za-z\s]+(?:restaurant|cafe|bar|pub))\b", "confidence": 0.80, "group": "social"},
                
                # Generic location with preposition
                {"pattern": r"\b(?:at|in)\s+([A-Z][A-Za-z\s,'-]+)\b", "confidence": 0.70, "group": "generic"},
                
                # Address-like patterns
                {"pattern": r"\b(\d+\s+[A-Za-z\s]+(?:street|road|avenue|drive|lane|way))\b", "confidence": 0.85, "group": "address"},
            ],
            
            "event_type": [
                # Medical appointments
                {"pattern": r"\b(doctor|dr|physician|medical)\s+(appointment|visit|checkup)\b", "confidence": 0.95, "group": "medical"},
                {"pattern": r"\b(dentist|dental)\s+(appointment|visit|cleaning)\b", "confidence": 0.95, "group": "dental"},
                
                # Business meetings
                {"pattern": r"\b(meeting|call|conference|discussion)\b", "confidence": 0.85, "group": "meeting"},
                {"pattern": r"\b(team|staff|board|client)\s+(meeting|call)\b", "confidence": 0.90, "group": "business_meeting"},
                
                # Social events
                {"pattern": r"\b(lunch|dinner|breakfast|coffee)\b", "confidence": 0.80, "group": "meal"},
                {"pattern": r"\b(party|celebration|birthday|anniversary)\b", "confidence": 0.80, "group": "social"},
                
                # Work/professional
                {"pattern": r"\b(interview|presentation|training|workshop|seminar)\b", "confidence": 0.85, "group": "professional"},
                
                # Personal
                {"pattern": r"\b(appointment|visit|trip|vacation|holiday)\b", "confidence": 0.75, "group": "personal"},
            ],
            
            "participants": [
                # With specific people
                {"pattern": r"\bwith\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", "confidence": 0.85, "group": "person"},
                
                # With groups
                {"pattern": r"\bwith\s+(team|staff|colleagues|friends|family)\b", "confidence": 0.80, "group": "group"},
                
                # Meeting participants
                {"pattern": r"\b(attendees?|participants?)\s*:\s*([A-Za-z\s,]+)\b", "confidence": 0.90, "group": "attendee_list"},
            ]
        }
    
    def _compile_patterns(self) -> Dict[str, List[Dict]]:
        """Pre-compile regex patterns for better performance"""
        compiled = {}
        for entity_type, patterns in self.patterns.items():
            compiled[entity_type] = []
            for pattern_info in patterns:
                compiled_pattern = {
                    "regex": re.compile(pattern_info["pattern"], re.IGNORECASE),
                    "confidence": pattern_info["confidence"],
                    "group": pattern_info["group"],
                    "original": pattern_info["pattern"]
                }
                compiled[entity_type].append(compiled_pattern)
        return compiled
    
    def extract_entities(self, text: str) -> List[ExtractedEntity]:
        """
        Extract all entities from text using regex patterns
        
        Args:
            text: Preprocessed text to extract entities from
            
        Returns:
            List of extracted entities sorted by confidence
        """
        if not text:
            return []
        
        entities = []
        
        for entity_type, patterns in self._compiled_patterns.items():
            for pattern_info in patterns:
                regex = pattern_info["regex"]
                confidence = pattern_info["confidence"]
                group = pattern_info["group"]
                
                matches = regex.finditer(text)
                for match in matches:
                    # Create entity object
                    entity = ExtractedEntity(
                        type=entity_type,
                        value=match.group().strip(),
                        confidence=confidence,
                        start_pos=match.start(),
                        end_pos=match.end(),
                        normalized_value=self._normalize_entity_value(entity_type, match.group().strip(), group)
                    )
                    entities.append(entity)
        
        # Remove overlapping entities (keep higher confidence ones)
        entities = self._deduplicate_entities(entities)
        
        # Sort by position in text
        entities.sort(key=lambda x: x.start_pos)
        
        return entities
    
    def _normalize_entity_value(self, entity_type: str, value: str, group: str) -> str:
        """Normalize extracted entity values"""
        value = value.strip().lower()
        
        if entity_type == "time":
            if group == "12h_simple":
                # Add :00 to simple hour format
                return re.sub(r'(\d+)\s*(am|pm)', r'\1:00\2', value)
            elif group == "special":
                return "12:00pm" if value == "noon" else "12:00am"
            elif group == "relative":
                # Map relative times to approximate hours
                mapping = {
                    "morning": "09:00", "afternoon": "14:00", 
                    "evening": "18:00", "night": "20:00"
                }
                return mapping.get(value, value)
        
        elif entity_type == "date":
            if group == "relative_day":
                return value  # Keep as-is for temporal resolver
            elif group == "weekday":
                return value
        
        elif entity_type == "location":
            # Remove prepositions and clean up
            value = re.sub(r'^(at|in)\s+', '', value, flags=re.IGNORECASE)
            # Capitalize properly
            return ' '.join(word.capitalize() for word in value.split())
        
        elif entity_type == "event_type":
            # Normalize event types
            if "doctor" in value or "medical" in value:
                return "doctor appointment"
            elif "dentist" in value:
                return "dentist appointment"
            elif "meeting" in value:
                return "meeting"
            elif any(meal in value for meal in ["lunch", "dinner", "breakfast"]):
                return next(meal for meal in ["lunch", "dinner", "breakfast"] if meal in value)
        
        return value
    
    def _deduplicate_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """
        Remove overlapping entities, keeping higher confidence ones
        
        Args:
            entities: List of extracted entities
            
        Returns:
            Filtered list without overlaps
        """
        if not entities:
            return []
        
        # Sort by confidence (descending) then by length (descending)
        entities.sort(key=lambda x: (-x.confidence, -(x.end_pos - x.start_pos)))
        
        filtered = []
        used_positions = set()
        
        for entity in entities:
            # Check if this entity overlaps with any already selected entity
            entity_positions = set(range(entity.start_pos, entity.end_pos))
            
            if not entity_positions.intersection(used_positions):
                # No overlap, add this entity
                filtered.append(entity)
                used_positions.update(entity_positions)
        
        return filtered
    
    def extract_entities_by_type(self, text: str, entity_type: str) -> List[ExtractedEntity]:
        """Extract only entities of a specific type"""
        if entity_type not in self._compiled_patterns:
            return []
        
        entities = []
        patterns = self._compiled_patterns[entity_type]
        
        for pattern_info in patterns:
            regex = pattern_info["regex"]
            confidence = pattern_info["confidence"]
            group = pattern_info["group"]
            
            matches = regex.finditer(text)
            for match in matches:
                entity = ExtractedEntity(
                    type=entity_type,
                    value=match.group().strip(),
                    confidence=confidence,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    normalized_value=self._normalize_entity_value(entity_type, match.group().strip(), group)
                )
                entities.append(entity)
        
        return self._deduplicate_entities(entities)
    
    def get_pattern_stats(self) -> Dict[str, int]:
        """Get statistics about available patterns"""
        return {
            entity_type: len(patterns) 
            for entity_type, patterns in self.patterns.items()
        }
    
    def test_pattern(self, pattern: str, text: str) -> List[str]:
        """Test a specific regex pattern against text (for debugging)"""
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            matches = regex.findall(text)
            return matches
        except re.error as e:
            return [f"Regex error: {str(e)}"]