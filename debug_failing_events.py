#!/usr/bin/env python3
"""
Debug script to test the specific failing cases
"""

import requests
import json
from datetime import datetime

def test_event_creation(voice_text):
    print(f'\n🧪 Testing event creation for: "{voice_text}"')
    
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
        event_data = data.get('event_data', {})
        
        print(f'✅ Event creation result:')
        print(f'   Success: {data.get("success")}')
        print(f'   Title: {event_data.get("title")}')
        print(f'   Start: {event_data.get("start_time")}')
        print(f'   End: {event_data.get("end_time")}')
        print(f'   Description: {event_data.get("description")}')
        
        # Calculate duration
        try:
            start_str = event_data.get('start_time')
            end_str = event_data.get('end_time')
            if start_str and end_str:
                start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                duration_mins = (end_dt - start_dt).total_seconds() / 60
                print(f'   Calculated Duration: {duration_mins} minutes')
            else:
                print(f'   ❌ Missing start/end times')
        except Exception as e:
            print(f'   ❌ Duration calc error: {e}')
            
    else:
        print(f'❌ Error: {response.status_code} - {response.text}')

if __name__ == "__main__":
    test_cases = [
        'meeting with team for 2 hours',
        'coffee break for 15 minutes'
    ]
    
    for test in test_cases:
        test_event_creation(test)
