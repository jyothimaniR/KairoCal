#!/usr/bin/env python3
"""
Create demo user profile via API
"""

import requests
import json

def create_demo_user_profile():
    """Create demo user profile via backend API"""
    
    print("🎭 Creating demo user profile via API...")
    
    # Demo user data
    user_data = {
        "email": "demo@kairocal.com",
        "full_name": "Demo User",
        "cognito_sub": "demo-user-presentation",
        "preferences": {
            "default_event_duration": "smart",
            "timezone": "UTC",
            "notifications_enabled": True,
            "voice_commands_enabled": True
        }
    }
    
    try:
        # Create user profile
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/users/",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Demo user profile created successfully")
            print(f"   - User ID: {result.get('id', 'Unknown')}")
            print(f"   - Email: {result.get('email', 'Unknown')}")
            print(f"   - Cognito Sub: {result.get('cognito_sub', 'Unknown')}")
            return True
        elif response.status_code == 400:
            error_detail = response.text
            if 'already' in error_detail.lower() or 'exists' in error_detail.lower():
                print("✅ Demo user profile already exists")
                return True
            else:
                print(f"❌ Failed to create user: {error_detail}")
                return False
        else:
            print(f"❌ Failed to create user: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating user profile: {e}")
        return False

def test_demo_events():
    """Test that demo events are accessible"""
    
    print("\n📅 Testing demo events access...")
    
    try:
        response = requests.get(
            "http://127.0.0.1:8000/api/v1/events?cognito_sub=demo-user-presentation",
            timeout=5
        )
        
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Demo events accessible: {len(events)} events")
            
            # Show sample events
            for event in events[:3]:
                print(f"   - {event.get('title', 'Unknown')} (Priority: {event.get('priority_level', 'N/A')})")
                
            return True
        else:
            print(f"❌ Failed to fetch events: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error fetching events: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DEMO USER SETUP")
    print("=" * 30)
    
    # Step 1: Create user profile
    if create_demo_user_profile():
        # Step 2: Test events access
        if test_demo_events():
            print("\n🎭 DEMO SETUP COMPLETE!")
            print("✅ User profile created")
            print("✅ Events accessible via API")
            print("✅ Ready for frontend demo")
        else:
            print("\n❌ Demo setup incomplete - events not accessible")
    else:
        print("\n❌ Demo setup failed - could not create user profile")
