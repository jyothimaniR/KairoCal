#!/usr/bin/env python3
"""
Test Duration Flow - Verify voice API respects user duration preferences
"""

import json
import requests
import time

# API endpoint
BASE_URL = "http://localhost:8000/api/v1"

def test_duration_preferences():
    """Test different duration preferences with the same voice input"""
    
    test_cases = [
        {
            "name": "Smart Duration (Movie should be ~150 min)",
            "voice_text": "Movie With My Girlfriend tomorrow at 7pm",
            "duration_preference": "smart",
            "expected_duration_range": (140, 160)  # Around 150 minutes
        },
        {
            "name": "Fixed 2 hour preference",
            "voice_text": "Movie With My Girlfriend tomorrow at 7pm", 
            "duration_preference": 120,
            "expected_duration_range": (115, 125)  # Around 120 minutes
        },
        {
            "name": "Fixed 30 min preference",
            "voice_text": "Movie With My Girlfriend tomorrow at 7pm",
            "duration_preference": 30,
            "expected_duration_range": (25, 35)  # Around 30 minutes
        },
        {
            "name": "Smart Duration (Coffee should be ~30 min)",
            "voice_text": "Coffee meeting with John tomorrow at 2pm",
            "duration_preference": "smart", 
            "expected_duration_range": (25, 35)  # Around 30 minutes
        },
        {
            "name": "Fixed 2 hour preference for coffee",
            "voice_text": "Coffee meeting with John tomorrow at 2pm",
            "duration_preference": 120,
            "expected_duration_range": (115, 125)  # Should override smart to 120 minutes
        }
    ]
    
    print("🧪 Testing Duration Preference Flow")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   Voice Text: '{test['voice_text']}'")
        print(f"   Duration Preference: {test['duration_preference']}")
        
        # Test the voice API
        payload = {
            "voice_text": test["voice_text"],
            "user_id": "test-user-123",
            "auto_schedule": True,
            "duration_preference": test["duration_preference"]
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/voice/create-event",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                event_data = data.get("event_data", {})
                
                # Calculate duration from start/end times
                start_time = event_data.get("start_time")
                end_time = event_data.get("end_time") 
                
                if start_time and end_time:
                    from datetime import datetime
                    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                    duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
                    
                    expected_min, expected_max = test["expected_duration_range"]
                    is_correct = expected_min <= duration_minutes <= expected_max
                    
                    status = "✅ PASS" if is_correct else "❌ FAIL"
                    print(f"   Result: {status}")
                    print(f"   Duration: {duration_minutes} minutes (expected {expected_min}-{expected_max})")
                    
                    if not is_correct:
                        print(f"   🔍 Event data: {json.dumps(event_data, indent=2)}")
                        print(f"   🔍 NLP Analysis: {json.dumps(data.get('nlp_analysis', {}), indent=2)}")
                else:
                    print("   ❌ FAIL - No start/end time in response")
                    print(f"   🔍 Full response: {json.dumps(data, indent=2)}")
                    
            else:
                print(f"   ❌ FAIL - HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ FAIL - Exception: {str(e)}")
        
        time.sleep(0.5)  # Small delay between tests

def test_nlp_duration_extraction():
    """Test the NLP service duration extraction directly"""
    
    print("\n" + "=" * 60)
    print("🧪 Testing NLP Duration Extraction Directly")
    print("=" * 60)
    
    # Import NLP service
    import sys
    sys.path.append('c:/Github/KairoCal')
    
    try:
        from backend.app.services.nlp_service import NLPService
        nlp = NLPService()
        
        test_texts = [
            ("Movie With My Girlfriend", "smart", "Should detect 'movie' -> 150 min"),
            ("Movie With My Girlfriend", 120, "Should use fixed 120 min"),
            ("Coffee meeting with John", "smart", "Should detect 'coffee meeting' -> 45 min"),
            ("Coffee meeting with John", 30, "Should use fixed 30 min"),
            ("Random text", "smart", "Should fallback to 60 min"),
            ("Random text", 90, "Should use fixed 90 min")
        ]
        
        for text, preference, description in test_texts:
            duration = nlp._extract_duration(text, preference)
            print(f"\n   Text: '{text}'")
            print(f"   Preference: {preference}")
            print(f"   Result: {duration} minutes")
            print(f"   Expected: {description}")
            
    except Exception as e:
        print(f"❌ Failed to test NLP directly: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Duration Flow Tests")
    
    # Test if backend is running
    try:
        response = requests.get(f"{BASE_URL}/voice/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"⚠️ Backend health check returned {response.status_code}")
    except Exception as e:
        print(f"❌ Backend is not running: {str(e)}")
        print("Please start the backend first: python -m backend.app.main")
        exit(1)
    
    # Run tests
    test_duration_preferences()
    test_nlp_duration_extraction()
    
    print("\n" + "=" * 60)
    print("🏁 Tests completed!")
