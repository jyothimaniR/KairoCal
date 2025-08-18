import requests
import json
from datetime import datetime, timedelta

# Test the /conflicts/check endpoint
BASE_URL = "http://localhost:8000/api/v1"

def test_conflicts_check():
    print("🧪 TESTING BACKEND CONFLICTS/CHECK ENDPOINT")
    print("=" * 50)
    
    # Test payload (simulating frontend request)
    payload = {
        "title": "New Team Meeting",
        "start_time": "2025-08-16T10:00:00",
        "end_time": "2025-08-16T11:00:00",
        "description": "Important project discussion",
        "location": "Conference Room A",
        "is_all_day": False
    }
    
    try:
        # Call conflicts check endpoint
        response = requests.post(
            f"{BASE_URL}/conflicts/check?cognito_sub=frontend-test-user",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.ok:
            data = response.json()
            print("✅ SUCCESS! Backend response:")
            print(json.dumps(data, indent=2))
            
            # Analyze the response
            conflicts = data.get('conflicts', [])
            engine = data.get('engine', 'unknown')
            
            print(f"\n📊 ANALYSIS:")
            print(f"   Engine Used: {engine}")
            print(f"   Conflicts Found: {len(conflicts)}")
            
            for i, conflict in enumerate(conflicts):
                print(f"   Conflict {i+1}:")
                print(f"      Type: {conflict.get('conflict_type', 'unknown')}")
                print(f"      Severity: {conflict.get('severity', 'unknown')}")
                print(f"      Description: {conflict.get('description', 'N/A')}")
                print(f"      Confidence: {conflict.get('confidence', 'N/A')}")
                print(f"      AI Confidence: {conflict.get('ai_confidence', 'N/A')}")
                
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Backend server is not running")
        print("   Please start the backend server first:")
        print("   cd c:\\Github\\KairoCal\\backend && python -m uvicorn main:app --reload")
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    test_conflicts_check()
