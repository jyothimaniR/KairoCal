#!/usr/bin/env python3
"""
Test the analytics API get_user_from_cognito function directly
"""

import requests
import json

def test_analytics_directly():
    """Test the analytics API to see what user it returns"""
    
    print("🔍 Testing Analytics API User Lookup")
    print("=" * 50)
    
    # Test priority trends endpoint
    print("\n📈 Testing Priority Trends Endpoint:")
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/analytics/priority/trends?cognito_sub=frontend-test-user",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success - User ID returned: {data.get('user_id', 'N/A')}")
            print(f"  📊 Total events analyzed: {data.get('insights', {}).get('total_events_analyzed', 'N/A')}")
        else:
            print(f"  ❌ Failed: HTTP {response.status_code}")
            print(f"  Response: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test BERT performance endpoint  
    print("\n🤖 Testing BERT Performance Endpoint:")
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/analytics/bert/performance?cognito_sub=frontend-test-user",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success - User ID returned: {data.get('user_id', 'N/A')}")
            print(f"  📊 Total events: {data.get('classification_overview', {}).get('total_events', 'N/A')}")
            print(f"  🔍 BERT classified: {data.get('classification_overview', {}).get('bert_classified', 'N/A')}")
        else:
            print(f"  ❌ Failed: HTTP {response.status_code}")
            print(f"  Response: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Compare with events API
    print("\n📅 Testing Events API for Comparison:")
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/events?cognito_sub=frontend-test-user",
            timeout=10
        )
        
        if response.status_code == 200:
            events = response.json()
            print(f"  ✅ Success - Found {len(events)} events")
            if events:
                print(f"  📝 Sample event user_id: {events[0].get('user_id', 'N/A')}")
        else:
            print(f"  ❌ Failed: HTTP {response.status_code}")
            print(f"  Response: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    test_analytics_directly()
