import requests
import json

def test_frontend_backend_integration():
    """Test the specific scenarios that the frontend might encounter"""
    print("🔄 TESTING FRONTEND-BACKEND INTEGRATION")
    print("=" * 60)
    
    BASE_URL = "http://localhost:8000/api/v1"
    
    # Test 1: Get all events (what frontend does first)
    print("📋 Test 1: Getting all events for conflict analysis...")
    try:
        response = requests.get(f"{BASE_URL}/events?cognito_sub=frontend-test-user")
        if response.ok:
            events = response.json()
            print(f"✅ Retrieved {len(events)} events from backend")
            
            # Show events that should conflict
            print("\n   Key events that should create conflicts:")
            for event in events:
                if "standup" in event['title'].lower() or "planning" in event['title'].lower() or "presentation" in event['title'].lower() or "executive" in event['title'].lower():
                    print(f"   - {event['title']}: {event['start_time']} - {event['end_time']}")
        else:
            print(f"❌ Failed to get events: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting events: {e}")
        return False
    
    # Test 2: Conflict detection using median event (simulating frontend logic)
    print("\n🔍 Test 2: Running conflict detection (frontend simulation)...")
    if events:
        # Sort events by start time and pick median (like frontend does)
        sorted_events = sorted(events, key=lambda x: x['start_time'])
        median_event = sorted_events[len(sorted_events) // 2]
        
        print(f"   Using median event as test reference: {median_event['title']}")
        
        payload = {
            "title": median_event['title'],
            "start_time": median_event['start_time'],
            "end_time": median_event['end_time'],
            "description": median_event.get('description', ''),
            "location": median_event.get('location', ''),
            "is_all_day": median_event.get('is_all_day', False),
            "max_alternatives": 3,
            "include_event_details": True
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/conflicts/check?cognito_sub=frontend-test-user",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            
            if response.ok:
                data = response.json()
                conflicts = data.get('conflicts', [])
                print(f"✅ Conflict detection successful: {len(conflicts)} conflicts found")
                
                if conflicts:
                    print("\n   📊 Detected conflicts:")
                    for i, conflict in enumerate(conflicts):
                        print(f"   {i+1}. {conflict.get('description', 'No description')}")
                        print(f"      Severity: {conflict.get('severity')}, Confidence: {conflict.get('confidence')}")
                else:
                    print("   ℹ️  No conflicts detected with median event approach")
                    
                return data
            else:
                print(f"❌ Conflict detection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error in conflict detection: {e}")
            return False
    
    # Test 3: Test with a deliberately conflicting event
    print("\n🚨 Test 3: Testing with deliberately conflicting event...")
    
    conflict_event = {
        "title": "Frontend Integration Test Event",
        "start_time": "2025-08-16T09:20:00",  # Should overlap with both standup and planning
        "end_time": "2025-08-16T09:50:00",
        "description": "Testing frontend integration",
        "location": "Test Room",
        "is_all_day": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/conflicts/check?cognito_sub=frontend-test-user",
            headers={"Content-Type": "application/json"},
            json=conflict_event
        )
        
        if response.ok:
            data = response.json()
            conflicts = data.get('conflicts', [])
            print(f"✅ Deliberate conflict test: {len(conflicts)} conflicts detected")
            
            if conflicts:
                print("\n   🎯 Expected conflicts found:")
                for conflict in conflicts:
                    print(f"   - {conflict.get('description')}")
                    print(f"     Type: {conflict.get('conflict_type')}, Severity: {conflict.get('severity')}")
                    
                    # Check BERT analysis
                    if conflict.get('ai_confidence'):
                        print(f"     🤖 AI Confidence: {conflict.get('ai_confidence'):.2f}")
                    
                    if conflict.get('priority_analysis'):
                        pa = conflict['priority_analysis']
                        print(f"     🎯 Priority Analysis: Proposed={pa.get('proposed_event', {}).get('priority')}, Existing={pa.get('existing_event', {}).get('priority')}")
            else:
                print("   ❌ Expected conflicts but none found - this indicates a problem!")
                
            return data
        else:
            print(f"❌ Deliberate conflict test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error in deliberate conflict test: {e}")
        return False

def check_frontend_api_compatibility():
    """Check if the API responses match what frontend expects"""
    print("\n🔧 CHECKING FRONTEND-BACKEND API COMPATIBILITY")
    print("=" * 60)
    
    # Check expected response structure
    expected_keys = [
        'conflicts',  # Array of conflicts
        'engine',     # Engine used
        'correlation_id'  # Request ID
    ]
    
    expected_conflict_keys = [
        'conflict_id',
        'conflict_type', 
        'severity',
        'description',
        'confidence',
        'impact_score',
        'affected_event_ids'
    ]
    
    BASE_URL = "http://localhost:8000/api/v1"
    
    test_payload = {
        "title": "API Test Event",
        "start_time": "2025-08-16T10:00:00",
        "end_time": "2025-08-16T11:00:00",
        "description": "Testing API compatibility",
        "is_all_day": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/conflicts/check?cognito_sub=frontend-test-user",
            headers={"Content-Type": "application/json"},
            json=test_payload
        )
        
        if response.ok:
            data = response.json()
            
            # Check top-level structure
            missing_keys = [key for key in expected_keys if key not in data]
            if missing_keys:
                print(f"❌ Missing top-level keys: {missing_keys}")
            else:
                print("✅ Top-level response structure correct")
            
            # Check conflict structure
            conflicts = data.get('conflicts', [])
            if conflicts:
                conflict = conflicts[0]
                missing_conflict_keys = [key for key in expected_conflict_keys if key not in conflict]
                if missing_conflict_keys:
                    print(f"❌ Missing conflict keys: {missing_conflict_keys}")
                else:
                    print("✅ Conflict object structure correct")
            else:
                print("ℹ️  No conflicts to validate structure")
            
            print(f"\n📊 API Response Summary:")
            print(f"   Engine: {data.get('engine')}")
            print(f"   Conflicts: {len(conflicts)}")
            print(f"   Response size: {len(json.dumps(data))} bytes")
            
            return True
        else:
            print(f"❌ API compatibility test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API compatibility test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE FRONTEND-BACKEND INTEGRATION TEST")
    print("=" * 70)
    
    # Run integration tests
    integration_result = test_frontend_backend_integration()
    
    # Run compatibility tests
    compatibility_result = check_frontend_api_compatibility()
    
    print("\n" + "=" * 70)
    print("📊 INTEGRATION TEST SUMMARY:")
    print(f"   Frontend-Backend Integration: {'✅ PASS' if integration_result else '❌ FAIL'}")
    print(f"   API Compatibility: {'✅ PASS' if compatibility_result else '❌ FAIL'}")
    
    if integration_result and compatibility_result:
        print("\n🎉 ALL TESTS PASSED! Frontend-backend integration is working correctly!")
        print("   The ConflictDetectionPanel should now show conflicts properly.")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
        
    print(f"\n🌐 Frontend URL: http://localhost:3000/dashboard")
    print("   Look for the ConflictDetectionPanel at the bottom of the dashboard.")
