import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def create_frontend_integration_test_data():
    """Create test events that will trigger conflicts for frontend testing"""
    print("🎯 CREATING FRONTEND INTEGRATION TEST DATA")
    print("=" * 60)
    
    # Create overlapping events that should be detected by frontend
    test_events = [
        {
            "title": "Morning Team Standup",
            "description": "Daily team standup meeting",
            "start_time": "2025-08-16T09:00:00",
            "end_time": "2025-08-16T09:30:00",
            "location": "Conference Room A",
            "priority_level": 3,
            "is_all_day": False
        },
        {
            "title": "Project Planning Session",
            "description": "Important project planning",
            "start_time": "2025-08-16T09:15:00",  # Overlaps with standup
            "end_time": "2025-08-16T10:15:00",
            "location": "Conference Room B",
            "priority_level": 4,
            "is_all_day": False
        },
        {
            "title": "Client Presentation",
            "description": "Critical client presentation",
            "start_time": "2025-08-16T14:00:00",
            "end_time": "2025-08-16T15:00:00",
            "location": "Main Hall",
            "priority_level": 5,
            "is_all_day": False
        },
        {
            "title": "Executive Review Meeting",
            "description": "Review with executives",
            "start_time": "2025-08-16T14:30:00",  # Overlaps with presentation
            "end_time": "2025-08-16T15:30:00",
            "location": "Executive Board Room",
            "priority_level": 5,
            "is_all_day": False
        },
        {
            "title": "Quick Coffee Break",
            "description": "Informal coffee with team",
            "start_time": "2025-08-16T15:45:00",
            "end_time": "2025-08-16T16:00:00",
            "location": "Kitchen",
            "priority_level": 1,
            "is_all_day": False
        }
    ]
    
    created_events = []
    
    for event in test_events:
        try:
            response = requests.post(
                f"{BASE_URL}/events?cognito_sub=frontend-test-user",
                headers={"Content-Type": "application/json"},
                json=event,
                timeout=10
            )
            
            if response.ok:
                data = response.json()
                created_events.append(data)
                print(f"✅ Created: {event['title']} ({event['start_time']} - {event['end_time']})")
            else:
                print(f"❌ Failed to create {event['title']}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error creating {event['title']}: {e}")
    
    print(f"\n📊 CREATED {len(created_events)} TEST EVENTS")
    return created_events

def test_conflicts_detection_for_frontend():
    """Test how the frontend will see these conflicts"""
    print("\n🔍 TESTING CONFLICTS DETECTION FOR FRONTEND")
    print("=" * 60)
    
    # Test a new event that conflicts with multiple existing events
    new_conflicting_event = {
        "title": "New Urgent Meeting",
        "start_time": "2025-08-16T09:10:00",  # Conflicts with both standup and planning
        "end_time": "2025-08-16T09:40:00",
        "description": "This should conflict with multiple events",
        "location": "Conference Room C",
        "is_all_day": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/conflicts/check?cognito_sub=frontend-test-user",
            headers={"Content-Type": "application/json"},
            json=new_conflicting_event,
            timeout=10
        )
        
        if response.ok:
            data = response.json()
            conflicts = data.get('conflicts', [])
            
            print(f"🚨 CONFLICTS DETECTED: {len(conflicts)}")
            print(f"Engine: {data.get('engine')}")
            print(f"Correlation ID: {data.get('correlation_id')}")
            
            for i, conflict in enumerate(conflicts):
                print(f"\n   Conflict {i+1}:")
                print(f"   📋 Type: {conflict.get('conflict_type')}")
                print(f"   🔥 Severity: {conflict.get('severity')}")
                print(f"   📝 Description: {conflict.get('description')}")
                print(f"   🎯 Confidence: {conflict.get('confidence')}")
                print(f"   🤖 AI Confidence: {conflict.get('ai_confidence', 'N/A')}")
                print(f"   📊 Impact Score: {conflict.get('impact_score')}")
                
                # Show BERT analysis if available
                priority_analysis = conflict.get('priority_analysis')
                if priority_analysis:
                    proposed = priority_analysis.get('proposed_event', {})
                    existing = priority_analysis.get('existing_event', {})
                    print(f"   🧠 BERT Analysis:")
                    print(f"      Proposed Priority: {proposed.get('priority')} (confidence: {proposed.get('confidence', 0):.2f})")
                    print(f"      Existing Event: {existing.get('title', 'Unknown')} (Priority: {existing.get('priority', 'N/A')})")
            
            return data
        else:
            print(f"❌ Conflicts check failed: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error testing conflicts: {e}")
        return None

def list_all_events():
    """List all events to see what the frontend will see"""
    print("\n📋 CURRENT EVENTS IN DATABASE")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/events?cognito_sub=frontend-test-user",
            timeout=10
        )
        
        if response.ok:
            events = response.json()
            print(f"Total Events: {len(events)}")
            
            for i, event in enumerate(events):
                print(f"\n   Event {i+1}:")
                print(f"   📝 Title: {event.get('title')}")
                print(f"   🕐 Time: {event.get('start_time')} - {event.get('end_time')}")
                print(f"   📍 Location: {event.get('location', 'No location')}")
                print(f"   🎯 Priority: {event.get('priority_level', 'N/A')}")
                print(f"   🆔 ID: {event.get('id')}")
            
            return events
        else:
            print(f"❌ Failed to get events: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error getting events: {e}")
        return []

if __name__ == "__main__":
    # Create test data
    created_events = create_frontend_integration_test_data()
    
    # List all events
    all_events = list_all_events()
    
    # Test conflict detection
    conflicts = test_conflicts_detection_for_frontend()
    
    print(f"\n🎉 FRONTEND INTEGRATION TEST DATA READY!")
    print(f"   📊 Events Created: {len(created_events)}")
    print(f"   📋 Total Events: {len(all_events)}")
    print(f"   🚨 Test Conflicts: {len(conflicts.get('conflicts', [])) if conflicts else 0}")
    print(f"\n🌐 Frontend URL: http://localhost:3000")
    print(f"🔧 Go to ConflictDetectionPanel to see the conflicts!")
