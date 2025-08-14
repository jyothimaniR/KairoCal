#!/usr/bin/env python3
"""
Test script to debug temporal resolution issues
"""

from backend.app.nlp.temporal_resolver import TemporalResolver
from datetime import datetime
import pytz

# Test the temporal resolver directly
resolver = TemporalResolver()

print('=== Testing Temporal Resolver ===')
print(f'Current time: {resolver.current_time}')
print()

# Test various time parsing scenarios that users mentioned
test_cases = [
    ('', '2 pm'),        # Just "2 pm"
    ('', '2pm'),         # Just "2pm" 
    ('', '2:00 pm'),     # "2:00 pm"
    ('', '2 p.m.'),      # "2 p.m."
    ('tomorrow', '2 pm'), # "tomorrow at 2 pm"
    ('today', 'afternoon'), # "today afternoon"
    ('', 'morning'),     # Just "morning"
    ('', '6:00pm'),      # "6:00pm"
    ('', '6 PM')         # "6 PM"
]

for date_text, time_text in test_cases:
    print(f'Testing: date="{date_text}", time="{time_text}"')
    try:
        start_dt, end_dt = resolver.resolve_full_temporal(date_text, time_text, None, 'meeting')
        print(f'  Result: {start_dt} -> {end_dt}')
        if start_dt:
            print(f'  Hour: {start_dt.hour}, Minute: {start_dt.minute}')
            print(f'  Time formatted: {start_dt.strftime("%I:%M %p")}')
    except Exception as e:
        print(f'  ERROR: {e}')
    print()

# Test individual time parsing
print('\n=== Testing Individual Time Resolution ===')
time_tests = ['2pm', '2 pm', '2:00pm', '2:00 pm', '2 p.m.', '6:00pm', '6PM']

for time_str in time_tests:
    print(f'Testing time: "{time_str}"')
    try:
        time_obj = resolver.resolve_time(time_str)
        print(f'  Result: {time_obj}')
        if time_obj:
            print(f'  Hour: {time_obj.hour}, Minute: {time_obj.minute}')
            # Convert to datetime to format
            dt = datetime.combine(datetime.now().date(), time_obj)
            print(f'  Formatted: {dt.strftime("%I:%M %p")}')
    except Exception as e:
        print(f'  ERROR: {e}')
    print()
