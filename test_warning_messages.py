#!/usr/bin/env python3
"""
Test script to check the warning message for edge cases
"""

import requests
import json

def test_with_full_response(voice_text):
    print(f'\n🧪 Testing: "{voice_text}"')
    
    response = requests.post(
        'http://127.0.0.1:8000/api/v1/voice/create-event',
        json={
            'voice_text': voice_text,
            'user_id': 'frontend-test-user',
            'auto_schedule': True,
            'priority_override': None
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        
        print(f'✅ Success: {data.get("success")}')
        print(f'📝 Message: {data.get("message", "No message")}')
        
        event_data = data.get('event_data', {})
        if event_data:
            print(f'📅 Event: {event_data.get("title")} (All-day: {event_data.get("is_all_day", False)})')
    else:
        print(f'❌ Error: {response.status_code} - {response.text}')

if __name__ == "__main__":
    # Test the edge cases that should show warnings
    test_cases = [
        'meeting with team for 2 hours',  # Should show warning
        'coffee break for 15 minutes',    # Should show warning  
        'lunch with Alex at 1:30 pm for 30 minutes',  # Should NOT show warning
        'quick call at 4pm'  # Should NOT show warning
    ]
    
    for test in test_cases:
        test_with_full_response(test)
