"""
Enhanced NLP Service with Voice Input Support for KairoCal
Integrates with BERT priority classification and voice-specific processing
"""

import re
import logging
import time
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)

class NLPService:
    """
    Enhanced NLP Service with voice input support
    Processes voice transcriptions and natural language for event creation
    """
    
    def __init__(self):
        # Voice-specific filler words and patterns
        self.voice_fillers = [
            'um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'well', 
            'actually', 'basically', 'literally', 'totally', 'really', 
            'just', 'kinda', 'sorta', 'i mean', 'you see'
        ]
        
        # Time patterns for voice input - FIXED ORDER AND PATTERNS INCLUDING PERIODS
        self.time_patterns = {
            # Match HH:MM a.m./p.m. with periods (most specific)
            r'\b(at\s+)?(\d{1,2}):(\d{2})\s*(a\.?m\.?|p\.?m\.?)\b': self._parse_time_24h,
            # Match HH:MM am/pm without periods
            r'\b(at\s+)?(\d{1,2}):(\d{2})\s*(am|pm)\b': self._parse_time_24h,
            # Match H a.m./p.m. with periods 
            r'\b(at\s+)?(\d{1,2})\s*(a\.?m\.?|p\.?m\.?)\b': self._parse_time_12h,
            # Match H am/pm without periods
            r'\b(at\s+)?(\d{1,2})\s*(am|pm)\b': self._parse_time_12h,
            # Special times
            r'\b(at\s+)?(noon|midnight)\b': self._parse_special_time,
            # Relative times
            r'\b(at\s+)?(morning|afternoon|evening|night)\b': self._parse_relative_time,
            # 24-hour format without am/pm
            r'\b(at\s+)?(\d{1,2}):(\d{2})\b': self._parse_time_24h_no_period
        }
        
        # Date patterns for voice input
        self.date_patterns = {
            r'\b(tomorrow|tmrw)\b': lambda: datetime.now() + timedelta(days=1),
            r'\b(today|now)\b': lambda: datetime.now(),
            r'\b(next\s+week)\b': lambda: datetime.now() + timedelta(weeks=1),
            r'\b(next\s+month)\b': lambda: datetime.now() + timedelta(days=30),
            r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b': self._parse_weekday,
            r'\b(\w+)\s+(\d{1,2})(st|nd|rd|th)?\b': self._parse_month_day
        }
        
        # ENHANCED Priority Keywords with Multi-Factor Analysis
        self.priority_keywords = {
            # CRITICAL (5) - Life/Business Critical Events
            5: {
                'urgency': ['urgent', 'emergency', 'asap', 'critical', 'immediately', 'right away', 
                           'crisis', 'fire', 'drop everything', 'top priority', 'now', 'stat'],
                'people': ['ceo', 'chief executive officer', 'president', 'chairman', 'board', 
                          'director', 'vp', 'vice president', 'founder', 'owner'],
                'medical': ['surgery', 'operation', 'heart surgery', 'brain surgery', 'emergency room',
                           'ambulance', 'life threatening', 'cardiac', 'stroke', 'trauma'],
                'business': ['board meeting', 'shareholder', 'investor', 'merger', 'acquisition',
                            'lawsuit', 'court', 'compliance', 'audit', 'regulatory'],
                'time': ['deadline today', 'due now', 'overdue', 'expires today']
            },
            
            # HIGH (4) - Important Professional/Medical
            4: {
                'importance': ['important', 'high priority', 'crucial', 'vital', 'key', 'major',
                              'significant', 'deadline', 'time sensitive', 'priority'],
                'people': ['doctor', 'surgeon', 'specialist', 'manager', 'supervisor', 'client',
                          'customer', 'judge', 'lawyer', 'accountant'],
                'medical': ['doctor appointment', 'medical', 'checkup', 'consultation', 'test results',
                           'scan', 'biopsy', 'treatment', 'therapy', 'prescription'],
                'business': ['presentation', 'proposal', 'contract', 'negotiation', 'interview',
                            'performance review', 'project deadline', 'deliverable'],
                'events': ['conference', 'seminar', 'training', 'workshop', 'keynote']
            },
            
            # NORMAL (3) - Regular Work/Personal
            3: {
                'general': ['normal', 'regular', 'standard', 'typical', 'usual', 'medium'],
                'work': ['meeting', 'call', 'standup', 'sync', 'team meeting', 'review',
                        'planning', 'brainstorm', 'discussion'],
                'personal': ['appointment', 'visit', 'pickup', 'drop off', 'errand']
            },
            
            # LOW (2) - Flexible/Optional
            2: {
                'flexibility': ['low priority', 'when possible', 'sometime', 'flexible', 'optional',
                               'nice to have', 'if time allows', 'convenient'],
                'social': ['lunch', 'coffee', 'casual', 'social', 'networking', 'catch up'],
                'personal': ['shopping', 'grocery', 'banking', 'post office']
            },
            
            # VERY LOW (1) - Casual/Social
            1: {
                'casual': ['very low', 'no rush', 'whenever', 'casual', 'relaxed', 'informal',
                          'maybe', 'possibly', 'if free'],
                'social': ['hang out', 'hangout', 'friends', 'party', 'fun', 'entertainment',
                          'movie', 'game', 'hobby', 'leisure'],
                'optional': ['optional', 'if available', 'when free', 'spare time']
            }
        }
        
        # Legacy support for existing code
        self.priority_indicators = self._flatten_priority_keywords()
        
        # Event type patterns
        self.event_patterns = {
            'meeting': [r'\b(meeting|meet|sync|standup|conference|discussion)\b'],
            'appointment': [r'\b(appointment|appt|doctor|dentist|medical|checkup)\b'],
            'call': [r'\b(call|phone|ring|dial|conference call|zoom)\b'],
            'reminder': [r'\b(remind|reminder|note|remember)\b'],
            'task': [r'\b(task|todo|to do|action|work on)\b'],
            'social': [r'\b(lunch|dinner|coffee|drink|party|social|hang out)\b'],
            'travel': [r'\b(flight|train|travel|trip|vacation|journey)\b']
        }
    
    async def process_voice_input(self, voice_text: str) -> Dict[str, Any]:
        """
        Process voice input text and extract event information
        
        Args:
            voice_text: Cleaned voice input text
            
        Returns:
            Dictionary with extracted event information
        """
        start_time = time.time()
        
        try:
            logger.info(f"🎤 Processing voice input: '{voice_text}'")
            
            # Clean voice text further
            cleaned_text = self._clean_voice_text(voice_text)
            
            # Extract event components
            event_data = {
                'title': self._extract_title(cleaned_text),
                'description': self._extract_description(cleaned_text),
                'start_time': self._extract_datetime(cleaned_text),
                'end_time': None,  # Will be calculated from duration or default
                'location': self._extract_location(cleaned_text),
                'priority': self._extract_priority(cleaned_text),
                'event_type': self._extract_event_type(cleaned_text),
                'participants': self._extract_participants(cleaned_text),
                'duration': self._extract_duration(cleaned_text)
            }
            
            # Calculate end time if not explicitly provided
            if event_data['start_time'] and not event_data['end_time']:
                duration_minutes = event_data.get('duration', 60)  # Default 1 hour
                event_data['end_time'] = event_data['start_time'] + timedelta(minutes=duration_minutes)
            
            # Calculate confidence score
            confidence = self._calculate_voice_confidence(event_data, cleaned_text)
            event_data['confidence'] = confidence
            
            # Add processing metadata
            processing_time = (time.time() - start_time) * 1000
            event_data['processing_time_ms'] = processing_time
            event_data['original_voice_text'] = voice_text
            event_data['cleaned_text'] = cleaned_text
            
            logger.info(f"✅ Voice processing completed in {processing_time:.1f}ms")
            logger.info(f"📊 Extracted: {event_data['title']} at {event_data['start_time']} (confidence: {confidence:.2f})")
            
            return event_data
            
        except Exception as e:
            logger.error(f"❌ Voice processing failed: {str(e)}")
            return {
                'error': str(e),
                'confidence': 0.0,
                'original_voice_text': voice_text
            }
    
    def _clean_voice_text(self, text: str) -> str:
        """Clean voice text by removing filler words and normalizing"""
        cleaned = text.lower()
        
        # Remove filler words
        for filler in self.voice_fillers:
            pattern = r'\b' + re.escape(filler) + r'\b'
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Normalize multiple spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Fix common voice-to-text errors
        voice_corrections = {
            r'\bto\s+(\d)': r'at \1',  # "to 3" -> "at 3"
            r'\b4\s+pm\b': '4pm',      # "4 pm" -> "4pm"
            r'\bam\s+(\d)': r'at \1',  # "am 9" -> "at 9"
            r'\btomorrow\s+at\b': 'tomorrow at',
            r'\bnext\s+(\w+day)\b': r'next \1'
        }
        
        for pattern, replacement in voice_corrections.items():
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
        
        return cleaned
    
    def _extract_title(self, text: str) -> str:
        """Extract event title from voice text"""
        # First, try to identify and extract the main event content
        # Remove time/date references to get clean event title
        
        # Remove common time/date patterns from the text to isolate the title
        clean_text = text.lower().strip()
        
        # Remove ALL temporal references and scheduling words comprehensively
        temporal_stopwords = [
            # Basic time references
            r'\b(tomorrow|today|yesterday|tonight|tonite)\b',
            r'\b(now|later|soon|asap|immediately)\b',
            
            # Day references
            r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            r'\b(mon|tue|wed|thu|fri|sat|sun)\b',
            r'\b(weekday|weekend)\b',
            
            # Week/Month references  
            r'\b(this|next|last|coming|upcoming)\s+(week|month|year|weekend|morning|afternoon|evening|night)\b',
            r'\b(this|next|last|coming|upcoming)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            
            # Time of day
            r'\b(morning|afternoon|evening|night|noon|midnight|dawn|dusk)\b',
            r'\b(early|late)\s+(morning|afternoon|evening|night)\b',
            
            # Duration and timing
            r'\b(in\s+\d+\s+(minutes?|hours?|days?|weeks?|months?))\b',
            r'\b(after\s+\d+\s+(minutes?|hours?|days?))\b',
            r'\b(within\s+\d+\s+(minutes?|hours?|days?))\b',
            
            # Specific time patterns
            r'\b(at|on|for|by|until|before|after)\s+\d{1,2}(:\d{2})?\s*(am|pm|a\.?m\.?|p\.?m\.?)\b',
            r'\b(at|on|for|by|until|before|after)\s+(morning|afternoon|evening|night|noon|midnight)\b',
            
            # Date formats
            r'\b\d{1,2}/\d{1,2}(/\d{2,4})?\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b\d{1,2}(st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b',
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(st|nd|rd|th)?\b',
            
            # Relative timing
            r'\b(first|second|third|fourth|last)\s+(week|day|hour|minute)\b',
            r'\b(beginning|middle|end)\s+of\s+(week|month|year|day)\b',
            r'\b(start|end)\s+of\s+(week|month|year|day)\b',
            
            # Frequency/repetition (when used for scheduling)
            r'\b(daily|weekly|monthly|yearly|annually)\b',
            r'\b(every|each)\s+(day|week|month|year|morning|afternoon|evening)\b',
            
            # Scheduling context words
            r'\b(scheduled|planned|set|arranged|booked)\s+(for|on|at)\b',
            r'\b(due|deadline|expires?|starts?|begins?|ends?)\s+(on|at|by|in)\b'
        ]
        
        for pattern in temporal_stopwords:
            before = clean_text
            clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE).strip()
            if before != clean_text:
                logger.debug(f"🧹 Temporal removal: '{before}' -> '{clean_text}' (pattern: {pattern[:20]}...)")
        
        # Remove common scheduling verbs if they're at the beginning
        scheduling_verbs = [
            r'^\s*(schedule|set up|book|remind me to|plan|arrange)\s+(a\s+|an\s+)?',
        ]
        
        for pattern in scheduling_verbs:
            clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE).strip()
        
        # Clean up extra spaces
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # If we have a good clean title, use it
        if clean_text and len(clean_text) > 2:
            # Capitalize properly and return
            return clean_text.title()
        
        # Fallback: Extract event type
        event_type = self._extract_event_type(text)
        if event_type != 'event':
            return event_type.title()
        
        # Last resort: Use first few words
        words = text.split()[:4]
        if len(words) >= 2:
            return ' '.join(words).title()
        
        return 'Voice Event'
    
    def _extract_description(self, text: str) -> str:
        """Extract or generate event description"""
        # For voice input, the cleaned text can serve as description
        return f"Event created from voice input: {text}"
    
    def _extract_datetime(self, text: str) -> Optional[datetime]:
        """Extract date and time from voice text"""
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # First, try to extract date
        event_date = self._extract_date(text)
        if not event_date:
            event_date = base_date
        
        # Then, try to extract time
        event_time = self._extract_time(text)
        if event_time:
            # Combine date and time
            return event_date.replace(
                hour=event_time.hour,
                minute=event_time.minute,
                second=0,
                microsecond=0
            )
        else:
            # No specific time found, default to reasonable time
            current_hour = datetime.now().hour
            if current_hour < 9:
                default_hour = 9  # Morning
            elif current_hour < 17:
                default_hour = current_hour + 1  # Next hour
            else:
                default_hour = 9  # Next day morning
                event_date += timedelta(days=1)
            
            return event_date.replace(hour=default_hour, minute=0)
        
        return None
    
    def _extract_date(self, text: str) -> Optional[datetime]:
        """Extract date from voice text"""
        for pattern, parser_func in self.date_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    if callable(parser_func):
                        return parser_func()
                    else:
                        return parser_func(match)
                except Exception as e:
                    logger.warning(f"Date parsing failed for '{match.group()}': {e}")
                    continue
        
        return None
    
    def _extract_time(self, text: str) -> Optional[datetime]:
        """Extract time from voice text"""
        for pattern, parser_func in self.time_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return parser_func(match)
                except Exception as e:
                    logger.warning(f"Time parsing failed for '{match.group()}': {e}")
                    continue
        
        return None
    
    def _parse_time_12h(self, match) -> datetime:
        """Parse 12-hour format time (e.g., '3pm', '11am', '3 p.m.', '11 a.m.')"""
        hour = int(match.group(2))
        period = match.group(3).lower()
        
        # Normalize period - remove dots and spaces
        period = period.replace('.', '').replace(' ', '')
        
        # Convert to 24-hour format - FIXED LOGIC
        if 'pm' in period and hour != 12:
            hour += 12
        elif 'am' in period and hour == 12:
            hour = 0
        
        return datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
    
    def _parse_time_24h(self, match) -> datetime:
        """Parse 24-hour format time with am/pm (e.g., '2:30pm', '9:00am', '2:30 p.m.')"""
        hour = int(match.group(2))
        minute = int(match.group(3))
        period = match.group(4).lower() if match.group(4) else None
        
        # Convert to 24-hour format if period is specified
        if period:
            # Normalize period - remove dots and spaces
            period = period.replace('.', '').replace(' ', '')
            
            if 'pm' in period and hour != 12:
                hour += 12
            elif 'am' in period and hour == 12:
                hour = 0
        
        return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    def _parse_time_24h_no_period(self, match) -> datetime:
        """Parse 24-hour format time without am/pm (e.g., '15:30', '09:00')"""
        hour = int(match.group(2))
        minute = int(match.group(3))
        
        return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    def _parse_relative_time(self, match) -> datetime:
        """Parse relative time (e.g., 'morning', 'afternoon')"""
        time_map = {
            'morning': 9,
            'afternoon': 14,
            'evening': 18,
            'night': 20
        }
        
        time_ref = match.group(2).lower()
        hour = time_map.get(time_ref, 12)
        
        return datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
    
    def _parse_special_time(self, match) -> datetime:
        """Parse special time references (e.g., 'noon', 'midnight')"""
        time_map = {
            'noon': 12,
            'midnight': 0
        }
        
        time_ref = match.group(2).lower()
        hour = time_map.get(time_ref, 12)
        
        return datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
    
    def _parse_weekday(self, match) -> datetime:
        """Parse weekday references (e.g., 'monday', 'friday')"""
        weekdays = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        target_weekday = weekdays.get(match.group(1).lower())
        if target_weekday is None:
            return None
        
        today = datetime.now()
        days_ahead = target_weekday - today.weekday()
        
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        
        return today + timedelta(days=days_ahead)
    
    def _parse_month_day(self, match) -> datetime:
        """Parse month and day references (e.g., 'march 15th', 'june 3rd')"""
        try:
            month_name = match.group(1)
            day = int(match.group(2))
            
            # Use dateutil parser for month name
            date_str = f"{month_name} {day}"
            parsed_date = date_parser.parse(date_str, fuzzy=True)
            
            # Adjust year if the date has passed this year
            current_year = datetime.now().year
            parsed_date = parsed_date.replace(year=current_year)
            
            if parsed_date < datetime.now():
                parsed_date = parsed_date.replace(year=current_year + 1)
            
            return parsed_date
            
        except Exception:
            return None
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location from voice text"""
        location_patterns = [
            r'(?:at|in|@)\s+(.+?)(?:\s+at\s+\d|\s+on\s+\w|$)',
            r'location\s+(.+?)(?:\s+at\s+\d|\s+on\s+\w|$)',
            r'room\s+(\w+)',
            r'conference room\s+(\w+)',
            r'building\s+(.+?)(?:\s+at\s+\d|\s+on\s+\w|$)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                if len(location) > 2:  # Avoid single characters
                    return location.title()
        
        return None
    
    def _extract_priority(self, text: str) -> int:
        """
        Extract priority level from voice text using enhanced keyword detection
        Now properly handles CEO, surgery, and other critical events
        """
        logger.info(f"🔍 Analyzing priority for: '{text}'")
        
        # Use enhanced priority detection
        priority = self._enhanced_priority_detection(text)
        
        # Additional context-based adjustments
        text_lower = text.lower()
        
        # Medical emergency overrides
        medical_emergency_terms = ['emergency', 'urgent surgery', 'heart attack', 'stroke', 'ambulance']
        if any(term in text_lower for term in medical_emergency_terms):
            logger.info("🚨 Medical emergency detected - setting priority to 5 (CRITICAL)")
            return 5
        
        # Executive/Leadership overrides
        executive_terms = ['ceo', 'chief executive', 'president meeting', 'board meeting']
        if any(term in text_lower for term in executive_terms):
            logger.info("👔 Executive/Leadership event detected - setting priority to 5 (CRITICAL)")
            return 5
        
        # Time sensitivity adjustments
        if 'today' in text_lower or 'now' in text_lower or 'immediately' in text_lower:
            if priority < 4:
                logger.info("⏰ Time-sensitive event detected - increasing priority")
                priority = min(5, priority + 1)
        
        logger.info(f"📊 Final priority assigned: {priority}")
        return priority
    
    def _extract_event_type(self, text: str) -> str:
        """Extract event type from voice text"""
        for event_type, patterns in self.event_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return event_type
        
        return 'event'
    
    def _extract_participants(self, text: str) -> List[str]:
        """Extract participants from voice text"""
        participant_patterns = [
            r'with\s+(.+?)(?:\s+at|\s+on|\s+in|\s+for|$)',
            r'invite\s+(.+?)(?:\s+to|\s+at|\s+on|$)',
            r'including\s+(.+?)(?:\s+at|\s+on|$)'
        ]
        
        participants = []
        for pattern in participant_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                participant_text = match.group(1)
                # Split by common separators
                names = re.split(r'[,&]\s*|\s+and\s+', participant_text)
                participants.extend([name.strip() for name in names if name.strip()])
        
        return participants
    
    def _extract_duration(self, text: str) -> int:
        """Extract duration in minutes from voice text"""
        duration_patterns = [
            r'(?:for|lasting)\s+(\d+)\s*(?:hours?|hrs?)',
            r'(?:for|lasting)\s+(\d+)\s*(?:minutes?|mins?)',
            r'(\d+)\s*(?:hour|hr)\s*(?:meeting|appointment|call)',
            r'(\d+)\s*(?:minute|min)\s*(?:meeting|appointment|call)',
            r'all day',
            r'half\s+(?:an\s+)?hour',
            r'quarter\s+(?:of\s+an\s+)?hour'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if 'all day' in match.group():
                    return 480  # 8 hours
                elif 'half' in match.group():
                    return 30
                elif 'quarter' in match.group():
                    return 15
                else:
                    duration = int(match.group(1))
                    if 'hour' in pattern:
                        return duration * 60
                    else:
                        return duration
        
        # Default durations based on event type
        event_type = self._extract_event_type(text)
        default_durations = {
            'meeting': 60,
            'call': 30,
            'appointment': 30,
            'lunch': 90,
            'dinner': 120,
            'coffee': 30
        }
        
        return default_durations.get(event_type, 60)
    
    def _calculate_voice_confidence(self, event_data: Dict[str, Any], text: str) -> float:
        """Calculate confidence score for voice-extracted event"""
        confidence = 0.0
        
        # Base confidence
        confidence += 0.3
        
        # Title confidence
        if event_data.get('title') and event_data['title'] != 'Voice Event':
            confidence += 0.2
        
        # Time confidence
        if event_data.get('start_time'):
            confidence += 0.3
        
        # Location confidence
        if event_data.get('location'):
            confidence += 0.1
        
        # Event type confidence
        if event_data.get('event_type') != 'event':
            confidence += 0.1
        
        # Text quality (longer, more structured text = higher confidence)
        word_count = len(text.split())
        if word_count >= 5:
            confidence += 0.1
        if word_count >= 10:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _flatten_priority_keywords(self) -> Dict[int, List[str]]:
        """
        Convert enhanced priority keywords structure to legacy format
        for backward compatibility
        """
        flattened = {}
        for priority_level, categories in self.priority_keywords.items():
            all_keywords = []
            for category, keywords in categories.items():
                all_keywords.extend(keywords)
            flattened[priority_level] = all_keywords
        return flattened
    
    def _enhanced_priority_detection(self, text: str) -> int:
        """
        Enhanced priority detection using multi-category keyword analysis
        
        Returns:
            Priority level (1-5) with improved accuracy for CEO/medical events
        """
        text_lower = text.lower()
        priority_scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        # Check each priority level and category
        for priority_level, categories in self.priority_keywords.items():
            for category, keywords in categories.items():
                for keyword in keywords:
                    # Use word boundaries to avoid partial matches
                    import re
                    word_pattern = r'\b' + re.escape(keyword) + r'\b'
                    if re.search(word_pattern, text_lower):
                        # Give extra weight to certain categories
                        weight = 1.0
                        if category in ['medical', 'people', 'urgency']:
                            weight = 2.0  # Double weight for critical categories
                        elif category in ['business', 'importance']:
                            weight = 1.5  # Extra weight for important categories
                        
                        priority_scores[priority_level] += weight
                        logger.debug(f"Keyword '{keyword}' found in category '{category}' - Priority {priority_level} (+{weight})")
        
        # Find the priority level with highest score
        if any(score > 0 for score in priority_scores.values()):
            best_priority = max(priority_scores.keys(), key=lambda k: priority_scores[k])
            max_score = priority_scores[best_priority]
            
            logger.info(f"🎯 Enhanced priority detection: Level {best_priority} (score: {max_score})")
            return best_priority
        
        # Fallback to default priority
        logger.info("🔄 No priority keywords found, using default priority 3")
        return 3
    
    def process_text_input(self, text: str) -> Dict[str, Any]:
        """
        Process regular text input (non-voice)
        Compatible with existing NLP pipeline
        """
        # This can integrate with the existing NLP service
        # For now, use voice processing as it's more comprehensive
        return self.process_voice_input(text)
