#!/usr/bin/env python3
"""
Direct test of analytics endpoints to debug dashboard issue
"""

import requests
import json

def test_analytics_endpoints():
    base_url = "http://127.0.0.1:8000"
    user_id = "frontend-test-user"
    
    print("🔬 Testing Analytics Endpoints Directly")
    print("=" * 50)
    
    endpoints = [
        f"/api/v1/analytics/priority/trends?cognito_sub={user_id}",
        f"/api/v1/analytics/bert/performance?cognito_sub={user_id}",
        f"/api/v1/analytics/productivity/metrics?cognito_sub={user_id}"
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\n📡 Testing: {endpoint}")
        print("-" * 30)
        
        try:
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response keys: {list(data.keys())}")
                
                # Show relevant data structure
                if "trends" in data:
                    print(f"Trends count: {len(data['trends'])}")
                    if data['trends']:
                        print(f"First trend: {data['trends'][0]}")
                
                if "classification_overview" in data:
                    print(f"Classification overview: {data['classification_overview']}")
                
                if "insights" in data:
                    print(f"Insights: {data['insights']}")
                    
                if "metrics" in data:
                    print(f"Metrics keys: {list(data['metrics'].keys()) if isinstance(data['metrics'], dict) else data['metrics']}")
                    
            else:
                print(f"Error response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_analytics_endpoints()
