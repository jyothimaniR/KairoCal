#!/usr/bin/env python3
"""
Comprehensive All-Day Event Fix Test
Test all scenarios to ensure the fix is complete
"""

import requests
import json

def test_allday_no_conflicts():
    """Test that all-day events return no conflicts"""
    print("🧪 TEST 1: All-Day Event (Should Return No Conflicts)")
    print("-" * 50)
    
    payload = {
        "title": "Project Submission",
        "start_time": "2025-08-17T00:00:00",
        "end_time": "2025-08-17T23:59:00",
        "is_all_day": True,
        "description": "All-day event test"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/conflicts/check",
        json=payload,
        params={"cognito_sub": "test-user"}
    )
    
    result = response.json()
    conflicts = len(result.get("conflicts", []))
    
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Conflicts: {conflicts} (Expected: 0)")
    
    return conflicts == 0

def test_timed_event_conflicts():
    """Test that timed events still detect conflicts"""
    print("\n🧪 TEST 2: Timed Event Conflict (Should Detect Conflicts)")
    print("-" * 50)
    
    payload = {
        "title": "Overlapping Meeting",
        "start_time": "2025-08-17T17:15:00",  # Overlaps tennis at 17:00-17:30
        "end_time": "2025-08-17T17:45:00",
        "is_all_day": False,
        "description": "Should conflict with tennis"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/conflicts/check",
        json=payload,
        params={"cognito_sub": "test-user"}
    )
    
    result = response.json()
    conflicts = len(result.get("conflicts", []))
    
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Conflicts: {conflicts} (Expected: 1+)")
    
    if conflicts > 0:
        for conflict in result.get("conflicts", []):
            print(f"   📝 {conflict.get('description', 'Unknown conflict')}")
    
    return conflicts > 0

def test_multiple_allday_events():
    """Test that multiple all-day events don't conflict with each other"""
    print("\n🧪 TEST 3: Another All-Day Event (Should Not Conflict)")
    print("-" * 50)
    
    payload = {
        "title": "Holiday - Independence Day",
        "start_time": "2025-08-17T00:00:00",
        "end_time": "2025-08-17T23:59:00",
        "is_all_day": True,
        "description": "Another all-day event"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/conflicts/check",
        json=payload,
        params={"cognito_sub": "test-user"}
    )
    
    result = response.json()
    conflicts = len(result.get("conflicts", []))
    
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Conflicts: {conflicts} (Expected: 0)")
    
    return conflicts == 0

def test_no_conflicts_scenario():
    """Test a timed event that genuinely has no conflicts"""
    print("\n🧪 TEST 4: Timed Event No Conflict (Should Return No Conflicts)")
    print("-" * 50)
    
    payload = {
        "title": "Morning Coffee",
        "start_time": "2025-08-17T08:00:00",  # No conflicts at this time
        "end_time": "2025-08-17T08:30:00",
        "is_all_day": False,
        "description": "Should have no conflicts"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/conflicts/check",
        json=payload,
        params={"cognito_sub": "test-user"}
    )
    
    result = response.json()
    conflicts = len(result.get("conflicts", []))
    
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Conflicts: {conflicts} (Expected: 0)")
    
    return conflicts == 0

if __name__ == "__main__":
    print("🔧 COMPREHENSIVE ALL-DAY EVENT CONFLICT FIX TEST")
    print("=" * 70)
    
    results = []
    
    # Run all tests
    results.append(("All-day events return no conflicts", test_allday_no_conflicts()))
    results.append(("Timed events detect conflicts", test_timed_event_conflicts()))
    results.append(("Multiple all-day events don't conflict", test_multiple_allday_events()))
    results.append(("Non-conflicting timed events work", test_no_conflicts_scenario()))
    
    # Summary
    print("\n" + "=" * 70)
    print("🎯 TEST RESULTS SUMMARY:")
    print("-" * 30)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! All-day event conflict fix is working correctly!")
        print("🚀 The conflicts page should now work properly:")
        print("   ✅ All-day events will not show any conflicts")
        print("   ✅ Timed events will still detect real conflicts")  
        print("   ✅ Users can change priorities in the conflicts page")
    else:
        print("❌ SOME TESTS FAILED - Further investigation needed")
    print("=" * 70)
