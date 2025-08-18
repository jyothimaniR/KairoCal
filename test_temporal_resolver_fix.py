#!/usr/bin/env python3
"""
Test the TemporalResolver directly to ensure the fix is working
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from backend.app.nlp.temporal_resolver import TemporalResolver

def test_temporal_resolver_fix():
    print("=== Testing TemporalResolver Fix ===")
    print(f"Local date: {datetime.now().date()}")
    print(f"UTC date: {datetime.utcnow().date()}")
    print()
    
    # Create a fresh resolver (this should use the fixed code)
    resolver = TemporalResolver()
    print(f"Resolver current_time: {resolver.current_time}")
    print(f"Resolver current_time type: {type(resolver.current_time)}")
    print()
    
    # Test today resolution
    today_resolved = resolver.resolve_date("today")
    print(f"Resolved 'today': {today_resolved}")
    print(f"Resolved 'today' date: {today_resolved.date()}")
    
    # Test tomorrow resolution
    tomorrow_resolved = resolver.resolve_date("tomorrow")
    print(f"Resolved 'tomorrow': {tomorrow_resolved}")
    print(f"Resolved 'tomorrow' date: {tomorrow_resolved.date()}")
    print()
    
    # Test full temporal resolution
    start_time, end_time = resolver.resolve_full_temporal(
        date_text="today",
        time_text="2pm", 
        duration_text="60 minutes"
    )
    print(f"Full temporal 'today at 2pm for 60 minutes':")
    print(f"  Start: {start_time}")
    print(f"  End: {end_time}")
    print(f"  Start date: {start_time.date() if start_time else None}")
    print()
    
    # Check if dates are correct
    expected_today = datetime.now().date()
    expected_tomorrow = datetime.now().date().replace(day=expected_today.day + 1)
    
    print("=== Validation ===")
    today_correct = today_resolved.date() == expected_today
    tomorrow_correct = tomorrow_resolved.date() == expected_tomorrow
    
    print(f"Today resolution correct: {today_correct}")
    print(f"Tomorrow resolution correct: {tomorrow_correct}")
    
    if today_correct and tomorrow_correct:
        print("✅ TemporalResolver fix is working correctly!")
    else:
        print("❌ TemporalResolver fix has issues")
        print(f"Expected today: {expected_today}, got: {today_resolved.date()}")
        print(f"Expected tomorrow: {expected_tomorrow}, got: {tomorrow_resolved.date()}")

if __name__ == "__main__":
    test_temporal_resolver_fix()
