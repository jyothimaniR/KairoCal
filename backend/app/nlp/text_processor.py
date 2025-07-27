# backend/app/nlp/text_processor.py
"""
Text preprocessing and normalization for NLP pipeline
"""

import re
import string
from typing import Dict, List, Tuple, Optional

class TextProcessor:
    """Cleans and preprocesses input text for NLP parsing"""
    
    def __init__(self):
        # Common contractions expansion
        self.contractions = {
            "i'm": "i am", "you're": "you are", "it's": "it is",
            "that's": "that is", "what's": "what is", "there's": "there is",
            "can't": "cannot", "won't": "will not", "don't": "do not",
            "doesn't": "does not", "didn't": "did not", "isn't": "is not",
            "aren't": "are not", "wasn't": "was not", "weren't": "were not",
            "haven't": "have not", "hasn't": "has not", "hadn't": "had not",
            "will's": "will", "would's": "would", "could's": "could",
            "should's": "should", "might's": "might", "must's": "must"
        }
        
        # Time format normalization patterns
        self.time_normalizations = {
            # Normalize time formats
            r"(\d{1,2})\s*:\s*(\d{2})\s*(am|pm)": r"\1:\2\3",  # "2 : 30 pm" -> "2:30pm"
            r"(\d{1,2})\s*(am|pm)": r"\1:00\2",               # "2pm" -> "2:00pm"
            r"\b(noon)\b": "12:00pm",                          # "noon" -> "12:00pm"
            r"\b(midnight)\b": "12:00am",                      # "midnight" -> "12:00am"
            r"\b(\d{1,2})\s*o\s*clock\b": r"\1:00",           # "2 o'clock" -> "2:00"
        }
        
        # Common scheduling keywords
        self.scheduling_keywords = {
            "schedule", "book", "set up", "arrange", "plan", "add",
            "create", "make", "put", "set", "organize", "calendar"
        }
        
        # Event type normalizations
        self.event_normalizations = {
            r"\b(dr|doctor)\s+(appointment|visit)\b": "doctor appointment",
            r"\b(dentist)\s+(appointment|visit)\b": "dentist appointment", 
            r"\b(team|staff)\s+(meeting|call)\b": "team meeting",
            r"\b(lunch|dinner)\s+(meeting|with)\b": "lunch meeting",
            r"\b(phone|video)\s+(call|meeting)\b": "phone call",
        }
    
    def clean_text(self, text: str) -> str:
        """
        Main text cleaning pipeline
        
        Args:
            text: Raw input text from user
            
        Returns:
            Cleaned and normalized text
        """
        if not text or not isinstance(text, str):
            return ""
            
        # Step 1: Basic cleaning
        text = text.strip()
        
        # Step 2: Convert to lowercase for processing (preserve original case for titles)
        original_text = text
        text = text.lower()
        
        # Step 3: Expand contractions
        text = self._expand_contractions(text)
        
        # Step 4: Normalize time formats
        text = self._normalize_times(text)
        
        # Step 5: Normalize event types
        text = self._normalize_event_types(text)
        
        # Step 6: Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Step 7: Remove leading scheduling words if present
        text = self._remove_scheduling_prefix(text)
        
        return text.strip()
    
    def _expand_contractions(self, text: str) -> str:
        """Expand contractions for better parsing"""
        for contraction, expansion in self.contractions.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(contraction) + r'\b'
            text = re.sub(pattern, expansion, text, flags=re.IGNORECASE)
        return text
    
    def _normalize_times(self, text: str) -> str:
        """Normalize various time formats to standard format"""
        for pattern, replacement in self.time_normalizations.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text
    
    def _normalize_event_types(self, text: str) -> str:
        """Normalize common event type phrases"""
        for pattern, replacement in self.event_normalizations.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text
    
    def _remove_scheduling_prefix(self, text: str) -> str:
        """Remove common scheduling command words from the beginning"""
        # Pattern to match scheduling verbs at the start
        pattern = r'^\s*(?:' + '|'.join(self.scheduling_keywords) + r')\s+'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text
    
    def extract_quoted_content(self, text: str) -> Tuple[str, List[str]]:
        """
        Extract content in quotes (potential event titles)
        
        Returns:
            Tuple of (text_without_quotes, list_of_quoted_strings)
        """
        # Find all quoted strings
        quoted_content = []
        
        # Handle double quotes
        double_quotes = re.findall(r'"([^"]*)"', text)
        quoted_content.extend(double_quotes)
        
        # Handle single quotes (but be careful with contractions)
        single_quotes = re.findall(r"'([^']*)'", text)
        # Filter out likely contractions (single letters or common suffixes)
        single_quotes = [q for q in single_quotes if len(q) > 2 and q not in ['t', 's', 're', 've', 'll', 'd']]
        quoted_content.extend(single_quotes)
        
        # Remove quotes from text
        text_no_quotes = re.sub(r'["\']([^"\']*)["\']', r'\1', text)
        
        return text_no_quotes.strip(), quoted_content
    
    def identify_intent_keywords(self, text: str) -> List[str]:
        """Identify keywords that suggest user intent"""
        intent_patterns = {
            "create": [r"\b(schedule|book|add|create|make|set up|arrange|plan)\b"],
            "update": [r"\b(change|modify|update|move|reschedule|edit)\b"],
            "delete": [r"\b(cancel|delete|remove|clear)\b"],
            "query": [r"\b(when|what|show|find|list|check)\b"]
        }
        
        found_intents = []
        text_lower = text.lower()
        
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    found_intents.append(intent)
                    break
        
        return found_intents
    
    def split_into_segments(self, text: str) -> Dict[str, str]:
        """
        Split text into logical segments for easier parsing
        
        Returns:
            Dictionary with segments like 'main', 'time', 'location', etc.
        """
        segments = {"main": text}
        
        # Extract time segment
        time_match = re.search(r'\b(?:at\s+)?(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b', text, re.IGNORECASE)
        if time_match:
            segments["time"] = time_match.group(1)
            segments["main"] = text.replace(time_match.group(0), "").strip()
        
        # Extract location segment
        location_match = re.search(r'\b(?:at|in)\s+([A-Za-z\s,]+(?:clinic|hospital|office|center|room|building|restaurant|cafe))\b', text, re.IGNORECASE)
        if location_match:
            segments["location"] = location_match.group(1).strip()
            segments["main"] = segments["main"].replace(location_match.group(0), "").strip()
        
        # Extract date segment  
        date_match = re.search(r'\b(tomorrow|today|yesterday|next\s+\w+|this\s+\w+|\d+/\d+(?:/\d+)?)\b', text, re.IGNORECASE)
        if date_match:
            segments["date"] = date_match.group(1)
            segments["main"] = segments["main"].replace(date_match.group(0), "").strip()
        
        # Clean up main segment
        segments["main"] = re.sub(r'\s+', ' ', segments["main"]).strip()
        
        return segments
    
    def validate_input(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Validate input text for basic requirements
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text or not isinstance(text, str):
            return False, "Input text is required"
        
        text = text.strip()
        
        if len(text) < 3:
            return False, "Input text is too short"
        
        if len(text) > 500:
            return False, "Input text is too long (max 500 characters)"
        
        # Check for obvious non-scheduling text
        spam_patterns = [
            r'^[^a-zA-Z]*$',  # Only numbers/symbols
            r'(.)\1{10,}',    # Repeated characters
        ]
        
        for pattern in spam_patterns:
            if re.search(pattern, text):
                return False, "Input text does not appear to be a scheduling request"
        
        return True, None