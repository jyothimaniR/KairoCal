#!/usr/bin/env python3
"""
Test the voice API endpoint directly to verify the time parsing fix
"""

import requests
import json
from datetime import datetime

def test_voice_api_endpoint():
    print('=== Testing Voice API Endpoint ===')
    print(f'Current time: {datetime.now()}')
    print()
    
    base_url = "http://localhost:8000/api/v1"
    
    test_cases = [
        "Schedule meeting with CEO tomorrow at 2 pm",
        "Call mom at 6pm today", 
        "Doctor appointment at 2:00 pm tomorrow",
        "Meeting at 2 PM",
        "Lunch at 12:30pm tomorrow"
    ]
    
    for voice_text in test_cases:
        print(f'Testing: "{voice_text}"')
        
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
                print(f"  📋 Full response: {json.dumps(data, indent=2)}")
                
                # Try both event_data and direct access patterns
                event_data = data.get('event_data', data)
                
                print(f"  ✅ Success: {data.get('message', 'Created')}")
                print(f"  📅 Title: {event_data.get('title')}")
                print(f"  🕐 Start: {event_data.get('start_time')}")
                print(f"  🏁 End: {event_data.get('end_time')}")
                print(f"  ⭐ Priority: {event_data.get('priority_level')}")
                print(f"  📍 All Day: {event_data.get('is_all_day', False)}")
                
                # Parse and display the hour for verification
                if event_data.get('start_time'):
                    try:
                        dt = datetime.fromisoformat(event_data['start_time'].replace('Z', '+00:00'))
                        print(f"  🕐 Hour: {dt.hour} (24-hour format)")
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
    test_voice_api_endpoint()
