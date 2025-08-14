#!/usr/bin/env python3
"""
Debug script to investigate the is_all_day flag issue
"""

import requests
import json
from datetime import datetime

def debug_voice_api_all_day():
    print('=== Debugging is_all_day Flag Issue ===')
    print(f'Current time: {datetime.now()}')
    print()
    
    base_url = "http://localhost:8000/api/v1"
    
    test_cases = [
        {
            "voice_text": "Schedule lunch tomorrow at 2 PM",
            "expected_all_day": False,
            "reason": "Explicit time specified"
        },
        {
            "voice_text": "Schedule meeting on Friday", 
            "expected_all_day": True,
            "reason": "No time specified, date-only"
        },
        {
            "voice_text": "Doctor appointment at 2:00 pm tomorrow",
            "expected_all_day": False,
            "reason": "Explicit time with minutes"
        },
        {
            "voice_text": "Meeting tomorrow morning",
            "expected_all_day": False,  # Should be timed to 9:00 AM
            "reason": "Morning is a time reference"
        }
    ]
    
    for test_case in test_cases:
        voice_text = test_case["voice_text"]
        expected_all_day = test_case["expected_all_day"]
        reason = test_case["reason"]
        
        print(f'Testing: "{voice_text}"')
        print(f'Expected all_day: {expected_all_day} ({reason})')
        
        payload = {
            "voice_text": voice_text,
            "user_id": "test-user-1",
            "auto_schedule": True
        }
        
        try:
            response = requests.post(
                f"{base_url}/voice/create-event",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                event_data = data.get('event_data', {})
                
                actual_all_day = event_data.get('is_all_day', False)
                start_time = event_data.get('start_time')
                
                print(f"  📅 Title: {event_data.get('title')}")
                print(f"  🕐 Start: {start_time}")
                print(f"  📍 is_all_day: {actual_all_day}")
                print(f"  ✅ Expected: {expected_all_day}")
                
                # Check if result matches expectation
                if actual_all_day == expected_all_day:
                    print(f"  ✅ CORRECT: is_all_day flag matches expected value")
                else:
                    print(f"  ❌ BUG: Expected is_all_day={expected_all_day}, got {actual_all_day}")
                
                # Parse and display the time details
                if start_time:
                    try:
                        dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                        print(f"  🕐 Hour: {dt.hour}, Minute: {dt.minute}")
                        
                        if dt.hour == 0 and dt.minute == 0:
                            print(f"  ⚠️  Time is midnight (00:00) - possible all-day anchor")
                        else:
                            print(f"  🕐 Formatted: {dt.strftime('%I:%M %p')}")
                    except Exception as e:
                        print(f"  ⚠️ Time parsing error: {e}")
                
            else:
                print(f"  ❌ Error: {response.status_code}")
                print(f"  📝 Response: {response.text}")
        
        except Exception as e:
            print(f"  ❌ Request failed: {e}")
        
        print()

if __name__ == '__main__':
    debug_voice_api_all_day()
