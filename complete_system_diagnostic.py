#!/usr/bin/env python3
"""
Complete KairoCal System Diagnostic
Tests all components and identifies root causes of issues
"""

import requests
import json
import sys
from datetime import datetime, timedelta

def test_backend_health():
    """Test basic backend health"""
    print("\n🏥 Testing Backend Health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend Health: {json.dumps(health_data, indent=2)}")
            return True, health_data
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False, {}
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False, {}

def test_voice_api():
    """Test voice API endpoints"""
    print("\n🎤 Testing Voice API...")
    
    # Test voice health endpoint
    try:
        response = requests.get("http://localhost:8000/api/v1/voice/health", timeout=10)
        if response.status_code == 200:
            voice_health = response.json()
            print(f"✅ Voice Health: {json.dumps(voice_health, indent=2)}")
        else:
            print(f"❌ Voice health endpoint failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Voice health endpoint failed: {e}")
        return False
    
    # Test voice analysis endpoint
    try:
        analysis_data = {
            "voice_text": "Create urgent meeting with CEO tomorrow at 2:00 PM",
            "user_id": "18209d0d-62c7-48a6-8b49-7fb4e5d3f28e",
            "include_bert": True,
            "detailed_analysis": True
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/voice/analyze-voice", 
            json=analysis_data,
            timeout=15
        )
        
        if response.status_code == 200:
            analysis_result = response.json()
            print(f"✅ Voice Analysis: {json.dumps(analysis_result, indent=2)}")
        else:
            print(f"❌ Voice analysis endpoint failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Voice analysis endpoint failed: {e}")
        return False
    
    return True

def test_time_parsing():
    """Test time parsing specifically"""
    print("\n⏰ Testing Time Parsing...")
    
    test_cases = [
        "Create meeting tomorrow at 2:00 PM",
        "Schedule lunch at 2 pm",
        "Set up call at 2:30 PM",
        "Meeting at 14:00",
        "Appointment at noon"
    ]
    
    for test_case in test_cases:
        try:
            analysis_data = {
                "voice_text": test_case,
                "user_id": "18209d0d-62c7-48a6-8b49-7fb4e5d3f28e",
                "include_bert": True,
                "detailed_analysis": True
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/voice/analyze-voice", 
                json=analysis_data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"🧪 Test: '{test_case}'")
                print(f"   📊 Analysis: {json.dumps(result, indent=6)}")
            else:
                print(f"❌ Time parsing test failed for '{test_case}': {response.status_code}")
                
        except Exception as e:
            print(f"❌ Time parsing test failed for '{test_case}': {e}")

def test_user_creation():
    """Test creating a test user for event creation"""
    print("\n👤 Testing User Creation...")
    
    user_data = {
        "cognito_sub": "18209d0d-62c7-48a6-8b49-7fb4e5d3f28e",
        "email": "test@kairocal.com",
        "first_name": "Test",
        "last_name": "User",
        "timezone": "UTC"
    }
    
    try:
        # First try to get user
        response = requests.get(
            f"http://localhost:8000/api/v1/users?cognito_sub={user_data['cognito_sub']}"
        )
        
        if response.status_code == 200:
            print("✅ Test user already exists")
            return True
        
        # Create user
        response = requests.post(
            "http://localhost:8000/api/v1/users/",
            json=user_data
        )
        
        if response.status_code == 201:
            user_result = response.json()
            print(f"✅ Test user created: {json.dumps(user_result, indent=2)}")
            return True
        else:
            print(f"❌ User creation failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return False

def test_voice_event_creation():
    """Test voice event creation with specific time"""
    print("\n📅 Testing Voice Event Creation...")
    
    # Test with 2:00 PM to verify time parsing
    event_data = {
        "voice_text": "Create urgent meeting with CEO tomorrow at 2:00 PM",
        "user_id": "18209d0d-62c7-48a6-8b49-7fb4e5d3f28e",
        "auto_schedule": True
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/voice/create-event",
            json=event_data,
            timeout=20
        )
        
        if response.status_code == 200:
            event_result = response.json()
            print(f"✅ Voice event created: {json.dumps(event_result, indent=2)}")
            
            # Check if time was parsed correctly
            if 'event_data' in event_result and 'start_time' in event_result['event_data']:
                start_time = event_result['event_data']['start_time']
                parsed_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                print(f"🕐 Parsed start time: {parsed_time}")
                print(f"🕐 Hour: {parsed_time.hour}, Should be: 14 (2 PM)")
                
                if parsed_time.hour == 14:
                    print("✅ Time parsing is CORRECT!")
                else:
                    print("❌ Time parsing is WRONG - this is the scheduling issue!")
            
            return True
        else:
            print(f"❌ Voice event creation failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Voice event creation failed: {e}")
        return False

def test_analytics_health():
    """Test analytics API health"""
    print("\n📊 Testing Analytics Health...")
    try:
        response = requests.get("http://localhost:8000/api/v1/analytics/health", timeout=10)
        if response.status_code == 200:
            analytics_health = response.json()
            print(f"✅ Analytics Health: {json.dumps(analytics_health, indent=2)}")
            return True
        else:
            print(f"❌ Analytics health endpoint failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Analytics health endpoint failed: {e}")
        return False

def run_complete_diagnostic():
    """Run complete system diagnostic"""
    print("🔍 KairoCal Complete System Diagnostic")
    print("=" * 50)
    
    results = {}
    
    # Test backend health
    backend_healthy, health_data = test_backend_health()
    results['backend_health'] = backend_healthy
    
    # Test user creation (required for events)
    user_created = test_user_creation()
    results['user_creation'] = user_created
    
    # Test voice API
    voice_working = test_voice_api()
    results['voice_api'] = voice_working
    
    # Test analytics health
    analytics_working = test_analytics_health()
    results['analytics_health'] = analytics_working
    
    # Test time parsing
    if voice_working:
        test_time_parsing()
    
    # Test voice event creation
    if voice_working and user_created:
        event_created = test_voice_event_creation()
        results['voice_event_creation'] = event_created
    
    # Summary
    print("\n📋 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    # Root cause analysis
    print("\n🔍 ROOT CAUSE ANALYSIS")
    print("=" * 50)
    
    if not results.get('backend_health'):
        print("🚨 CRITICAL: Backend is not running or unhealthy")
        print("   → Start backend with: docker compose up -d")
    
    if not results.get('voice_api'):
        print("🚨 CRITICAL: Voice API endpoints are not working")
        print("   → Check if voice router is properly registered")
        print("   → Check backend logs for import errors")
    
    if not results.get('user_creation'):
        print("🚨 CRITICAL: Cannot create test user")
        print("   → Database connection or user model issues")
    
    if results.get('voice_api') and results.get('user_creation') and not results.get('voice_event_creation'):
        print("🚨 CRITICAL: Voice event creation failing")
        print("   → This is likely the time parsing issue")
    
    all_passing = all(results.values())
    if all_passing:
        print("\n🎉 ALL TESTS PASSING - SYSTEM IS READY FOR ACADEMIC DEMONSTRATION!")
    else:
        print("\n⚠️ ISSUES FOUND - SYSTEM NEEDS FIXES BEFORE DEMONSTRATION")
    
    return results

if __name__ == "__main__":
    run_complete_diagnostic()
