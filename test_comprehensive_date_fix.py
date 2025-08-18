#!/usr/bin/env python3
"""
Comprehensive test for the "day rollover drift" fix near midnight
Based on Backend_Unused_Features_Inventory_2025-08-08.md documentation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime, timedelta, timezone
from backend.app.nlp.temporal_resolver import TemporalResolver

def test_midnight_edge_cases():
    """Test the documented edge case: parsing times near midnight incorrectly shifting dates"""
    print("=== Testing Day Rollover Drift Near Midnight ===")
    
    # Simulate different times around midnight to test edge cases
    test_times = [
        datetime(2025, 8, 18, 0, 0, 0),    # Exactly midnight
        datetime(2025, 8, 18, 0, 15, 0),   # 15 minutes past midnight
        datetime(2025, 8, 18, 23, 45, 0),  # 15 minutes before midnight
        datetime(2025, 8, 17, 23, 59, 0),  # 1 minute before midnight (previous day)
    ]
    
    for test_time in test_times:
        print(f"\n--- Testing at {test_time} (Local) ---")
        
        # Create resolver with specific time
        resolver = TemporalResolver(current_time=test_time)
        
        # Test "today" resolution
        today_resolved = resolver.resolve_date("today")
        expected_date = test_time.date()
        
        print(f"  Local time: {test_time}")
        print(f"  Expected 'today': {expected_date}")
        print(f"  Resolved 'today': {today_resolved.date()}")
        
        if today_resolved.date() == expected_date:
            print(f"  ✅ 'Today' correct at {test_time.strftime('%H:%M')}")
        else:
            print(f"  ❌ 'Today' WRONG at {test_time.strftime('%H:%M')} - Expected {expected_date}, got {today_resolved.date()}")
        
        # Test "tomorrow" resolution
        tomorrow_resolved = resolver.resolve_date("tomorrow")
        expected_tomorrow = expected_date + timedelta(days=1)
        
        print(f"  Expected 'tomorrow': {expected_tomorrow}")
        print(f"  Resolved 'tomorrow': {tomorrow_resolved.date()}")
        
        if tomorrow_resolved.date() == expected_tomorrow:
            print(f"  ✅ 'Tomorrow' correct at {test_time.strftime('%H:%M')}")
        else:
            print(f"  ❌ 'Tomorrow' WRONG at {test_time.strftime('%H:%M')} - Expected {expected_tomorrow}, got {tomorrow_resolved.date()}")

def test_timezone_consistency():
    """Test that the fix maintains consistency with database timezone requirements"""
    print("\n=== Testing Timezone Consistency ===")
    
    local_now = datetime.now()
    utc_now = datetime.now(timezone.utc)
    
    print(f"Local time: {local_now}")
    print(f"UTC time: {utc_now}")
    
    # Test with default (current time)
    resolver = TemporalResolver()
    
    # Test full temporal resolution
    start_time, end_time = resolver.resolve_full_temporal(
        date_text="today",
        time_text="2pm",
        duration_text="60 minutes"
    )
    
    print(f"\nFull temporal resolution:")
    print(f"  Start time: {start_time}")
    print(f"  End time: {end_time}")
    print(f"  Start date: {start_time.date()}")
    print(f"  Timezone info: {start_time.tzinfo}")
    
    # Verify the result is timezone-naive (as required by the existing system)
    if start_time.tzinfo is None:
        print("  ✅ Returns timezone-naive datetime (correct for SQLAlchemy)")
    else:
        print("  ⚠️ Returns timezone-aware datetime (may cause issues)")
    
    # Verify the date is correct
    expected_date = local_now.date()
    if start_time.date() == expected_date:
        print(f"  ✅ Date is correct: {expected_date}")
    else:
        print(f"  ❌ Date is wrong: Expected {expected_date}, got {start_time.date()}")

def test_documented_scenarios():
    """Test specific scenarios mentioned in the documentation"""
    print("\n=== Testing Documented Scenarios ===")
    
    # Test the edge case: user creates event near midnight
    midnight_time = datetime(2025, 8, 18, 0, 5, 0)  # 5 minutes past midnight
    resolver = TemporalResolver(current_time=midnight_time)
    
    print(f"Scenario: User creates event at {midnight_time}")
    
    # Test various date/time combinations
    test_cases = [
        ("today", "2pm", "Should be August 18th at 2pm"),
        ("tomorrow", "10am", "Should be August 19th at 10am"),
        ("today", None, "Should be August 18th at default time"),
    ]
    
    for date_text, time_text, description in test_cases:
        start_time, end_time = resolver.resolve_full_temporal(
            date_text=date_text,
            time_text=time_text or "",
            duration_text="60 minutes"
        )
        
        print(f"\n  Test: '{date_text}' + '{time_text}' ({description})")
        print(f"    Result: {start_time}")
        print(f"    Date: {start_time.date()}")
        
        # Validate based on expectation
        if date_text == "today":
            expected_date = midnight_time.date()  # Should be Aug 18
        elif date_text == "tomorrow":
            expected_date = midnight_time.date() + timedelta(days=1)  # Should be Aug 19
            
        if start_time.date() == expected_date:
            print(f"    ✅ Correct date: {expected_date}")
        else:
            print(f"    ❌ Wrong date: Expected {expected_date}, got {start_time.date()}")

if __name__ == "__main__":
    test_midnight_edge_cases()
    test_timezone_consistency()
    test_documented_scenarios()
    
    print("\n" + "="*60)
    print("🎯 SUMMARY")
    print("This fix addresses the documented issue:")
    print("'Anchored time parsing prevents day rollover drift'")
    print("'parsing times near midnight incorrectly shifting dates'")
    print("="*60)
