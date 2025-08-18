#!/usr/bin/env python3
"""
Test Precise Timed Event Conflict
"""

import requests

def test_exact_overlap():
    print("🧪 TESTING EXACT TIME OVERLAP CONFLICT")
    print("=" * 60)
    
    # Test event that exactly overlaps with tennis match (17:00-17:30)
    payload = {
        "title": "Meeting During Tennis Time",
        "description": "Should definitely conflict with tennis",
        "start_time": "2025-08-17T17:00:00",  # Exact same start
        "end_time": "2025-08-17T17:30:00",    # Exact same end
        "is_all_day": False,
        "location": ""
    }
    
    print("📅 Testing Exact Overlap:")
    print(f"   Title: {payload['title']}")
    print(f"   Time: {payload['start_time']} - {payload['end_time']}")
    print(f"   Should conflict with: Tennis Match (17:00-17:30)")
    
    try:
        api_url = "http://127.0.0.1:8000/api/v1/conflicts/check"
        params = {"cognito_sub": "frontend-test-user"}
        
        response = requests.post(api_url, json=payload, params=params)
        
        print(f"\n📡 API Response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            conflicts_count = len(result.get("conflicts", []))
            
            print("✅ API Success!")
            print(f"   Conflicts Found: {conflicts_count}")
            
            if conflicts_count > 0:
                print("🎉 SUCCESS! Conflict detection working correctly")
                for i, conflict in enumerate(result.get("conflicts", []), 1):
                    print(f"   Conflict {i}: {conflict.get('description', 'Unknown')}")
            else:
                print("❌ FAILURE! Should detect conflict with tennis match")
                print("   Raw Response:", result)
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    test_exact_overlap()
