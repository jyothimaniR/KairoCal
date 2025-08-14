# backend/app/nlp/temporal_resolver.py
"""
Temporal resolution - converts relative dates/times to absolute datetime objects
"""

import re
from datetime import datetime, timedelta, time, timezone
from typing import Optional, Tuple, Dict

class TemporalResolver:
    """Converts human temporal expressions to datetime objects"""
    
    def __init__(self, current_time: Optional[datetime] = None, tz: str = "UTC"):
        self.current_time = current_time or datetime.now(timezone.utc)
        self.timezone = timezone.utc  # Simplified to UTC for now
        
        # Default durations for different event types (in minutes)
        self.default_durations = {
            "appointment": 60,
            "doctor appointment": 30,
            "dentist appointment": 45,
            "meeting": 60,
            "lunch": 90,
            "dinner": 120,
            "coffee": 30,
            "call": 30,
            "interview": 60,
            "default": 60
        }
        
        # Default times for different periods
        self.period_defaults = {
            "morning": time(9, 0),      # 9:00 AM
            "afternoon": time(14, 0),   # 2:00 PM
            "evening": time(18, 0),     # 6:00 PM
            "night": time(20, 0),       # 8:00 PM
        }
    
    def resolve_date(self, date_text: str) -> Optional[datetime]:
        """
        Convert date text to datetime object
        
        Args:
            date_text: Raw date text like "tomorrow", "next friday", "7/27"
            
        Returns:
            datetime object or None if can't parse
        """
        if not date_text:
            return None
        
        date_text = date_text.lower().strip()
        current_date = self.current_time.date()
        
        # Relative day names
        if date_text == "today":
            return self.current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_text == "tomorrow":
            return self.current_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif date_text == "yesterday":
            return self.current_time.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        # Next/this + weekday
        next_weekday_match = re.match(r"(next|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", date_text)
        if next_weekday_match:
            modifier, weekday = next_weekday_match.groups()
            return self._get_next_weekday(weekday, modifier == "next")
        
        # Standalone weekday (assume next occurrence)
        weekday_match = re.match(r"^(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$", date_text)
        if weekday_match:
            weekday = weekday_match.group(1)
            return self._get_next_weekday(weekday, next_week=False)
        
        # Numeric dates
        try:
            # Try common date formats
            for fmt in ["%m/%d/%Y", "%m/%d", "%Y-%m-%d", "%d/%m/%Y"]:
                try:
                    parsed_date = datetime.strptime(date_text, fmt)
                    # If year not specified, assume current year
                    if parsed_date.year == 1900:
                        parsed_date = parsed_date.replace(year=self.current_time.year)
                    return parsed_date.replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
            
        except Exception:
            pass
        
        # Relative periods
        if "next week" in date_text:
            return self.current_time + timedelta(weeks=1)
        elif "next month" in date_text:
            # Simple month calculation (add 30 days)
            return self.current_time + timedelta(days=30)
        
        return None
    
    def resolve_time(self, time_text: str) -> Optional[time]:
        """
        Convert time text to time object
        
        Args:
            time_text: Raw time text like "2:00pm", "noon", "morning"
            
        Returns:
            time object or None if can't parse
        """
        if not time_text:
            return None
        
        time_text = time_text.lower().strip()
        
        # Special time words
        if time_text == "noon":
            return time(12, 0)
        elif time_text == "midnight":
            return time(0, 0)
        
        # Period defaults
        if time_text in self.period_defaults:
            return self.period_defaults[time_text]
        
        # 12-hour format with AM/PM - FIXED VERSION
        twelve_hour_match = re.match(r"(\d{1,2}):?(\d{2})?\s*(am|pm|a\.?m\.?|p\.?m\.?)", time_text)
        if twelve_hour_match:
            hour, minute, period = twelve_hour_match.groups()
            hour = int(hour)
            minute = int(minute) if minute else 0
            
            # Normalize period
            period = period.lower().replace('.', '')
            
            # Convert to 24-hour format - CRITICAL FIX
            if 'pm' in period and hour != 12:
                hour += 12
            elif 'am' in period and hour == 12:
                hour = 0
            
            try:
                return time(hour, minute)
            except ValueError:
                return None
        
        # Just number followed by pm/am (like "2pm", "2 pm")  
        simple_hour_match = re.match(r"(\d{1,2})\s*(am|pm|a\.?m\.?|p\.?m\.?)", time_text)
        if simple_hour_match:
            hour, period = simple_hour_match.groups()
            hour = int(hour)
            
            # Normalize period
            period = period.lower().replace('.', '')
            
            # Convert to 24-hour format - CRITICAL FIX
            if 'pm' in period and hour != 12:
                hour += 12
            elif 'am' in period and hour == 12:
                hour = 0
            
            try:
                return time(hour, 0)  # Assume :00 minutes
            except ValueError:
                return None
        
        # 24-hour format
        twenty_four_hour_match = re.match(r"(\d{1,2}):(\d{2})", time_text)
        if twenty_four_hour_match:
            hour, minute = twenty_four_hour_match.groups()
            try:
                return time(int(hour), int(minute))
            except ValueError:
                return None
        
        return None
    
    def resolve_duration(self, duration_text: str, event_type: str = "default") -> int:
        """
        Convert duration text to minutes
        
        Args:
            duration_text: Raw duration text like "2 hours", "30 minutes"
            event_type: Type of event for default duration
            
        Returns:
            Duration in minutes
        """
        if not duration_text:
            return self.default_durations.get(event_type, self.default_durations["default"])
        
        duration_text = duration_text.lower().strip()
        
        # All day events
        if "all day" in duration_text or "full day" in duration_text:
            return 24 * 60  # 24 hours
        
        # Hours
        hours_match = re.search(r"(\d+)\s*(?:hours?|hrs?)", duration_text)
        if hours_match:
            return int(hours_match.group(1)) * 60
        
        # Minutes
        minutes_match = re.search(r"(\d+)\s*(?:minutes?|mins?)", duration_text)
        if minutes_match:
            return int(minutes_match.group(1))
        
        # Special durations
        if "half hour" in duration_text or "30 min" in duration_text:
            return 30
        elif "quick" in duration_text or "brief" in duration_text:
            return 15
        elif "long" in duration_text:
            return 120
        
        # Default duration based on event type
        return self.default_durations.get(event_type, self.default_durations["default"])
    
    def combine_date_time(self, date_obj: Optional[datetime], time_obj: Optional[time]) -> Optional[datetime]:
        """
        Combine date and time objects into a single datetime
        
        Args:
            date_obj: Date component
            time_obj: Time component
            
        Returns:
            Combined datetime object
        """
        if not date_obj and not time_obj:
            return None
        
        # Use current date if no date specified
        if not date_obj:
            date_obj = self.current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Use default time if no time specified
        if not time_obj:
            time_obj = time(9, 0)  # Default to 9 AM
        
        # Combine date and time
        combined = datetime.combine(date_obj.date(), time_obj)
        
        # Ensure timezone awareness
        if combined.tzinfo is None:
            combined = combined.replace(tzinfo=timezone.utc)
        
        return combined
    
    def resolve_full_temporal(self, date_text: str, time_text: str, 
                            duration_text: str = None, event_type: str = "default") -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Resolve complete temporal information for an event
        
        Args:
            date_text: Raw date text
            time_text: Raw time text  
            duration_text: Raw duration text
            event_type: Type of event for defaults
            
        Returns:
            Tuple of (start_datetime, end_datetime)
        """
        # Resolve components
        date_obj = self.resolve_date(date_text)
        time_obj = self.resolve_time(time_text)
        duration_minutes = self.resolve_duration(duration_text, event_type)
        
        # Combine date and time
        start_datetime = self.combine_date_time(date_obj, time_obj)
        
        if not start_datetime:
            return None, None
        
        # Calculate end time
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        
        return start_datetime, end_datetime
    
    def _get_next_weekday(self, weekday: str, next_week: bool = False) -> datetime:
        """Get the next occurrence of a specific weekday"""
        weekdays = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        
        target_weekday = weekdays[weekday.lower()]
        current_weekday = self.current_time.weekday()
        
        days_ahead = target_weekday - current_weekday
        
        if next_week or days_ahead <= 0:
            days_ahead += 7
        
        target_date = self.current_time + timedelta(days=days_ahead)
        return target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def is_in_past(self, dt: datetime) -> bool:
        """Check if a datetime is in the past"""
        return dt < self.current_time
    
    def format_relative_time(self, dt: datetime) -> str:
        """Format datetime as relative time (e.g., 'tomorrow at 2:00 PM')"""
        if not dt:
            return "unknown time"
        
        # Calculate days difference
        days_diff = (dt.date() - self.current_time.date()).days
        
        # Format date part
        if days_diff == 0:
            date_part = "today"
        elif days_diff == 1:
            date_part = "tomorrow"
        elif days_diff == -1:
            date_part = "yesterday"
        elif 1 < days_diff <= 7:
            date_part = dt.strftime("%A")  # Weekday name
        else:
            date_part = dt.strftime("%B %d")  # Month and day
        
        # Format time part
        time_part = dt.strftime("%I:%M %p").lstrip("0")
        
        return f"{date_part} at {time_part}"