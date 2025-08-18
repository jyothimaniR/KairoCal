#!/usr/bin/env python3
"""
Test All-Day Event Conflict Fix
Verify that all-day events don't conflict with timed events
"""

import requests
import json

def test_allday_conflict_fix():
    print("🧪 TESTING ALL-DAY EVENT CONFLICT FIX")
    print("=" * 60)
    
    # Test the all-day "Project Submission" event
    payload = {
        "title": "Project Submission",
        "description": "Final project submission deadline",
        "start_time": "2025-08-17T00:00:00",
        "end_time": "2025-08-17T23:59:00",
        "is_all_day": True,
        "location": ""
    }
    
    print("📅 Testing All-Day Event:")
    print(f"   Title: {payload['title']}")
    print(f"   Is All-Day: {payload['is_all_day']}")
    print(f"   Time: {payload['start_time']} - {payload['end_time']}")
    
    try:
        api_url = "http://127.0.0.1:8000/api/v1/conflicts/check"
        params = {"cognito_sub": "frontend-test-user"}
        
        response = requests.post(api_url, json=payload, params=params)
        
        print(f"\n📡 API Response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            conflicts_count = result.get("count", 0)
            
            print("✅ API Success!")
            print(f"   Conflicts Found: {conflicts_count}")
            
            if conflicts_count == 0:
                print("🎉 SUCCESS! All-day event correctly returns NO CONFLICTS")
                debug_info = result.get("debug_info", {})
                if debug_info:
                    print(f"   Debug Message: {debug_info.get('message', '')}")
                    print(f"   Is All-Day: {debug_info.get('is_all_day', '')}")
            else:
                print(f"❌ FAILURE! All-day event still showing {conflicts_count} conflicts")
                for conflict in result.get("conflicts", []):
                    print(f"      - {conflict}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Error Details: {response.text}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")

def test_timed_event_conflict():
    """Test that timed events still detect conflicts properly"""
    print("\n🧪 TESTING TIMED EVENT CONFLICTS (Should Still Work)")
    print("=" * 60)
    
    # Test a timed event that should conflict with existing events
    payload = {
        "title": "Test Timed Event",
        "description": "Should conflict with tennis match",
        "start_time": "2025-08-17T17:15:00",  # Overlaps with tennis at 17:00-17:30
        "end_time": "2025-08-17T17:45:00",
        "is_all_day": False,
        "location": ""
    }
    
    print("📅 Testing Timed Event (should conflict with tennis):")
    print(f"   Title: {payload['title']}")
    print(f"   Is All-Day: {payload['is_all_day']}")
    print(f"   Time: {payload['start_time']} - {payload['end_time']}")
    
    try:
        api_url = "http://127.0.0.1:8000/api/v1/conflicts/check"
        params = {"cognito_sub": "frontend-test-user"}
        
        response = requests.post(api_url, json=payload, params=params)
        
        print(f"\n📡 API Response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            conflicts_count = result.get("count", 0)
            
            print("✅ API Success!")
            print(f"   Conflicts Found: {conflicts_count}")
            
            if conflicts_count > 0:
                print("🎉 SUCCESS! Timed event correctly detects conflicts with other timed events")
                for i, conflict in enumerate(result.get("conflicts", []), 1):
                    print(f"   Conflict {i}: {conflict.get('description', 'Unknown conflict')}")
            else:
                print("❌ UNEXPECTED! Timed event should have detected conflicts")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Error Details: {response.text}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    test_allday_conflict_fix()
    test_timed_event_conflict()
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY:")
    print("✅ All-day events should NOT cause conflicts")
    print("✅ Timed events should STILL detect conflicts with other timed events") 
    print("🚀 Frontend should now show no conflicts for all-day events!")
