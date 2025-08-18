#!/usr/bin/env python3
"""
Test script to reproduce and verify the voice duration and title issues
"""

import requests
import json
import sys
import time

def test_voice_api(voice_text, expected_duration_minutes):
    """Test voice API with specific input and verify duration"""
    print(f"\n🧪 Testing: '{voice_text}'")
    print(f"Expected duration: {expected_duration_minutes} minutes")
    
    try:
        # Test voice creation
        response = requests.post(
            'http://127.0.0.1:8000/api/v1/voice/create-event',
            json={
                'voice_text': voice_text,
                'user_id': 'frontend-test-user',
                'auto_schedule': True,
                'priority_override': None
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            event_data = data.get('event_data', {})
            
            print(f"✅ Event created successfully:")
            print(f"   Title: '{event_data.get('title')}'")
            print(f"   Description: '{event_data.get('description')}'")
            print(f"   Start: {event_data.get('start_time')}")
            print(f"   End: {event_data.get('end_time')}")
            
            # Calculate actual duration
            from datetime import datetime
            try:
                start_str = event_data.get('start_time')
                end_str = event_data.get('end_time')
                if start_str and end_str:
                    start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    actual_duration = (end_dt - start_dt).total_seconds() / 60
                    
                    print(f"   Actual Duration: {actual_duration} minutes")
                    print(f"   Expected Duration: {expected_duration_minutes} minutes")
                    
                    if actual_duration == expected_duration_minutes:
                        print(f"   ✅ DURATION CORRECT")
                    else:
                        print(f"   ❌ DURATION WRONG - Expected {expected_duration_minutes}, got {actual_duration}")
                    
                    # Check title format
                    title = event_data.get('title', '')
                    if 'for 30 minutes' in title.lower() or 'for 1 hour' in title.lower():
                        print(f"   ❌ TITLE ISSUE - Contains duration info: '{title}'")
                    else:
                        print(f"   ✅ TITLE FORMAT CORRECT: '{title}'")
                        
            except Exception as e:
                print(f"   ⚠️ Could not parse duration: {e}")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🔧 Voice API Duration & Title Test")
    print("Testing current behavior before fixes...")
    
    # Check if backend is running
    try:
        health_response = requests.get('http://127.0.0.1:8000/health', timeout=5)
        if health_response.status_code != 200:
            print("❌ Backend not running or unhealthy")
            sys.exit(1)
        print("✅ Backend is running")
    except:
        print("❌ Backend not accessible")
        sys.exit(1)
    
    # Test cases
    test_cases = [
        ("lunch with Alex today at 1:30 p.m. for 30 minutes", 30),
        ("meeting with team for 2 hours", 120),
        ("coffee break for 15 minutes", 15),
        ("doctor appointment at 3pm for 45 minutes", 45),
        ("quick call at 4pm", 30),  # Should use default for calls
    ]
    
    for voice_text, expected_duration in test_cases:
        test_voice_api(voice_text, expected_duration)
        time.sleep(1)  # Avoid overwhelming the API
    
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    main()
