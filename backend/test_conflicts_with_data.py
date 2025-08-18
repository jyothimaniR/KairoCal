import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def create_test_event():
    """Create a test event that will cause conflicts"""
    event_payload = {
        "title": "Existing Important Meeting",
        "description": "This is an existing meeting",
        "start_time": "2025-08-16T10:30:00",
        "end_time": "2025-08-16T11:30:00",
        "location": "Conference Room A",
        "priority_level": 4,
        "is_all_day": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/events?cognito_sub=frontend-test-user",
            headers={"Content-Type": "application/json"},
            json=event_payload,
            timeout=10
        )
        
        if response.ok:
            data = response.json()
            print(f"✅ Created test event: {data.get('title')} (ID: {data.get('id')})")
            return data
        else:
            print(f"❌ Failed to create event: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating test event: {e}")
        return None

def test_conflicts_with_existing_event():
    """Test conflicts against the created event"""
    print("🧪 TESTING CONFLICTS WITH EXISTING EVENT")
    print("=" * 50)
    
    # Create test event first
    existing_event = create_test_event()
    if not existing_event:
        return
    
    # Now test a conflicting event
    conflict_payload = {
        "title": "New Overlapping Meeting",
        "start_time": "2025-08-16T10:45:00",  # Overlaps with existing 10:30-11:30
        "end_time": "2025-08-16T11:45:00",
        "description": "This should conflict",
        "location": "Conference Room B",
        "is_all_day": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/conflicts/check?cognito_sub=frontend-test-user",
            headers={"Content-Type": "application/json"},
            json=conflict_payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.ok:
            data = response.json()
            print("✅ SUCCESS! Conflict detection response:")
            print(json.dumps(data, indent=2))
            
            conflicts = data.get('conflicts', [])
            print(f"\n📊 CONFLICT ANALYSIS:")
            print(f"   Engine Used: {data.get('engine', 'unknown')}")
            print(f"   Conflicts Found: {len(conflicts)}")
            
            for i, conflict in enumerate(conflicts):
                print(f"\n   🚨 Conflict {i+1}:")
                print(f"      ID: {conflict.get('conflict_id', 'unknown')}")
                print(f"      Type: {conflict.get('conflict_type', 'unknown')}")
                print(f"      Severity: {conflict.get('severity', 'unknown')}")
                print(f"      Description: {conflict.get('description', 'N/A')}")
                print(f"      Confidence: {conflict.get('confidence', 'N/A')}")
                print(f"      AI Confidence: {conflict.get('ai_confidence', 'N/A')}")
                print(f"      Impact Score: {conflict.get('impact_score', 'N/A')}")
                print(f"      Affected Events: {conflict.get('affected_event_ids', [])}")
                
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def cleanup_test_events():
    """Clean up test events"""
    try:
        # Get all events for the test user
        response = requests.get(
            f"{BASE_URL}/events?cognito_sub=frontend-test-user",
            timeout=10
        )
        
        if response.ok:
            events = response.json()
            print(f"\n🧹 CLEANUP: Found {len(events)} events to clean up")
            
            for event in events:
                if 'test' in event.get('title', '').lower() or 'meeting' in event.get('title', '').lower():
                    delete_response = requests.delete(
                        f"{BASE_URL}/events/{event['id']}?cognito_sub=frontend-test-user",
                        timeout=10
                    )
                    if delete_response.ok:
                        print(f"   ✅ Deleted: {event['title']}")
                    else:
                        print(f"   ❌ Failed to delete: {event['title']}")
        
    except Exception as e:
        print(f"❌ Cleanup error: {e}")

if __name__ == "__main__":
    # Clean up first
    cleanup_test_events()
    
    # Test conflicts
    test_conflicts_with_existing_event()
    
    # Clean up after
    print("\n" + "="*50)
    cleanup_test_events()
