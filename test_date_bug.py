#!/usr/bin/env python3
"""
Test script to demonstrate the date scheduling bug
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime, timezone
from backend.app.nlp.temporal_resolver import TemporalResolver

def test_date_bug():
    print("=== Date Scheduling Bug Test ===")
    
    # Current times
    local_now = datetime.now()
    utc_now = datetime.now(timezone.utc)
    
    print(f"Local time: {local_now}")
    print(f"UTC time: {utc_now}")
    print(f"Local date: {local_now.date()}")
    print(f"UTC date: {utc_now.date()}")
    print()
    
    # Test TemporalResolver with default UTC behavior
    print("=== Current TemporalResolver Behavior ===")
    resolver = TemporalResolver()  # Uses UTC by default
    print(f"Resolver current_time: {resolver.current_time}")
    
    # Test "today" resolution
    today_resolved = resolver.resolve_date("today")
    print(f"Resolved 'today': {today_resolved}")
    print(f"Resolved 'today' date: {today_resolved.date()}")
    
    # Test "tomorrow" resolution
    tomorrow_resolved = resolver.resolve_date("tomorrow")
    print(f"Resolved 'tomorrow': {tomorrow_resolved}")
    print(f"Resolved 'tomorrow' date: {tomorrow_resolved.date()}")
    print()
    
    # Test with local time
    print("=== Fixed TemporalResolver Behavior (using local time) ===")
    local_resolver = TemporalResolver(current_time=local_now)
    print(f"Local resolver current_time: {local_resolver.current_time}")
    
    # Test "today" resolution with local time
    local_today_resolved = local_resolver.resolve_date("today")
    print(f"Local resolved 'today': {local_today_resolved}")
    print(f"Local resolved 'today' date: {local_today_resolved.date()}")
    
    # Test "tomorrow" resolution with local time  
    local_tomorrow_resolved = local_resolver.resolve_date("tomorrow")
    print(f"Local resolved 'tomorrow': {local_tomorrow_resolved}")
    print(f"Local resolved 'tomorrow' date: {local_tomorrow_resolved.date()}")
    print()
    
    # Show the difference
    print("=== Bug Impact ===")
    print(f"Expected 'today' date: {local_now.date()}")
    print(f"Current resolver 'today' date: {today_resolved.date()}")
    print(f"Difference: {(local_now.date() - today_resolved.date()).days} day(s)")
    
    if local_now.date() != today_resolved.date():
        print("🐛 BUG CONFIRMED: Events scheduled for 'today' are being created on the wrong date!")
    else:
        print("✅ No bug detected")

if __name__ == "__main__":
    test_date_bug()
