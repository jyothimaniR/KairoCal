#!/usr/bin/env python3
"""
Test voice event creation with date scheduling to verify the fix
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
import requests
import json
from datetime import datetime

async def test_voice_event_creation():
    print("=== Testing Voice Event Creation Date Fix ===")
    print(f"Current local date: {datetime.now().date()}")
    print(f"Current UTC date: {datetime.utcnow().date()}")
    print()
    
    # Test cases
    test_cases = [
        "Schedule a meeting today at 2pm",
        "Coffee meeting tomorrow at 10am", 
        "Team standup today at 9am"
    ]
    
    base_url = "http://127.0.0.1:8000/api/v1/voice"
    
    for i, voice_text in enumerate(test_cases, 1):
        print(f"=== Test Case {i}: '{voice_text}' ===")
        
        try:
            # Call the voice event creation API
            response = requests.post(
                f"{base_url}/create-event",
                json={
                    "voice_text": voice_text,
                    "user_id": "frontend-test-user",
                    "auto_schedule": True
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    event_data = data.get("event_data", {})
                    start_time = event_data.get("start_time")
                    if start_time:
                        # Parse the date from the start_time
                        event_date = datetime.fromisoformat(start_time.replace('Z', '+00:00')).date()
                        print(f"✅ Event created successfully")
                        print(f"   Title: {event_data.get('title')}")
                        print(f"   Start time: {start_time}")
                        print(f"   Event date: {event_date}")
                        
                        # Check if the date is correct
                        expected_date = datetime.now().date()
                        if "tomorrow" in voice_text.lower():
                            expected_date = expected_date.replace(day=expected_date.day + 1)
                        
                        if event_date == expected_date:
                            print(f"   ✅ Date is correct!")
                        else:
                            print(f"   ❌ Date is wrong! Expected {expected_date}, got {event_date}")
                    else:
                        print(f"❌ No start_time in response")
                else:
                    print(f"❌ Event creation failed: {data}")
            else:
                print(f"❌ API call failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to backend server. Make sure it's running at {base_url}")
        except Exception as e:
            print(f"❌ Test failed: {e}")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_voice_event_creation())
