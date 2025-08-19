#!/usr/bin/env python3
"""
Quick test to see what's happening with the API calls
"""

import requests

def test_api_calls():
    print("🔍 Testing API calls with different user IDs...")
    
    user_ids_to_test = [
        'frontend-test-user',
        'demo-user-presentation'
    ]
    
    for user_id in user_ids_to_test:
        print(f"\n📡 Testing with user_id: {user_id}")
        try:
            response = requests.get(
                f"http://127.0.0.1:8000/api/v1/events?cognito_sub={user_id}",
                timeout=5
            )
            
            if response.status_code == 200:
                events = response.json()
                print(f"   ✅ SUCCESS: {len(events)} events found")
                if events:
                    print(f"   📅 Sample event: {events[0].get('title', 'Unknown')}")
            else:
                print(f"   ❌ FAILED: HTTP {response.status_code}")
                print(f"   📄 Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   💥 ERROR: {e}")

if __name__ == "__main__":
    test_api_calls()
