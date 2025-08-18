#!/usr/bin/env python3
"""
Analyze the failing test cases to understand expected behavior
"""

import re

def analyze_case(text):
    print(f'\n🔍 Analyzing: "{text}"')
    
    # Check if they have explicit times
    has_explicit_time = bool(re.search(r'\b(\d{1,2}(:\d{2})?\s*(?:a\.?m\.?|p\.?m\.?|am|pm)|noon|midnight)\b', text, re.IGNORECASE))
    print(f'   Has explicit time: {has_explicit_time}')
    
    # Check if they have duration
    has_duration = bool(re.search(r'\b(for|lasting)\s+\d+\s*(minutes?|mins?|hours?|hrs?)\b', text, re.IGNORECASE))
    print(f'   Has duration: {has_duration}')
    
    # According to your logic
    if not has_explicit_time:
        print(f'   ✅ Expected behavior: ALL-DAY EVENT (no start time)')
        print(f'   ✅ Expected duration: 1439 minutes (23:59 all-day)')
        print(f'   ❌ Test expectation is WRONG - should not expect specific duration')
    else:
        print(f'   Expected behavior: TIMED EVENT with duration')

if __name__ == "__main__":
    test_cases = [
        'meeting with team for 2 hours',
        'coffee break for 15 minutes'
    ]
    
    for case in test_cases:
        analyze_case(case)
