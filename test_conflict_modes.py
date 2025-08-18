#!/usr/bin/env python3
"""
Test Conflict Detection Modes
Verifies both client-side and server-side conflict detection
"""

import requests
import json
from datetime import datetime, timedelta

def test_server_conflict_detection():
    """Test the server's conflict detection API"""
    print("🔍 TESTING SERVER CONFLICT DETECTION")
    print("="*50)
    
    base_url = "http://localhost:5001"
    
    # Get events first
    try:
        events_response = requests.get(
            f"{base_url}/api/events",
            params={"cognito_sub": "frontend-test-user"},
            timeout=5
        )
        
        if events_response.status_code != 200:
            print(f"❌ Failed to get events: {events_response.status_code}")
            return
            
        events = events_response.json()
        print(f"📊 Retrieved {len(events)} events from API")
        
        # Test conflict detection with a representative event
        if events:
            # Pick middle event as representative
            ref_event = sorted(events, key=lambda x: x['start_time'])[len(events)//2]
            
            payload = {
                "title": ref_event['title'],
                "start_time": ref_event['start_time'],
                "end_time": ref_event['end_time'],
                "description": ref_event.get('description', ''),
                "is_all_day": ref_event.get('is_all_day', False),
                "max_alternatives": 3,
                "include_event_details": True
            }
            
            print(f"🎯 Testing with reference event: {ref_event['title']}")
            
            conflicts_response = requests.post(
                f"{base_url}/api/conflicts/check",
                json=payload,
                timeout=10
            )
            
            if conflicts_response.status_code == 200:
                conflicts = conflicts_response.json()
                print(f"✅ Server conflict detection succeeded")
                print(f"📋 Found {len(conflicts.get('conflicts', []))} server conflicts:")
                
                for i, conflict in enumerate(conflicts.get('conflicts', [])):
                    print(f"   {i+1}. Severity: {conflict.get('severity', 'unknown')}")
                    print(f"      Events: {len(conflict.get('affected_events', []))} events")
                    print(f"      Recommendation: {conflict.get('recommendation', 'N/A')}")
                    
            else:
                print(f"❌ Server conflict detection failed: {conflicts_response.status_code}")
                print(f"Response: {conflicts_response.text}")
                
    except Exception as e:
        print(f"❌ Error testing server conflict detection: {e}")

def test_manual_conflict_logic():
    """Test our manual conflict detection logic"""
    print("\n🧠 TESTING MANUAL CONFLICT LOGIC")
    print("="*50)
    
    # Get events
    try:
        events_response = requests.get(
            "http://localhost:5001/api/events",
            params={"cognito_sub": "frontend-test-user"},
            timeout=5
        )
        
        if events_response.status_code != 200:
            print(f"❌ Failed to get events: {events_response.status_code}")
            return
            
        events = events_response.json()
        print(f"📊 Testing with {len(events)} events")
        
        conflicts = []
        time_events = []
        
        # Filter time-based events
        for event in events:
            if not event.get('start_time'):
                continue
            if event.get('all_day') or event.get('is_all_day'):
                continue
            time_events.append(event)
        
        print(f"⏰ Found {len(time_events)} time-based events")
        
        # Check for overlaps
        for i in range(len(time_events)):
            for j in range(i + 1, len(time_events)):
                event1 = time_events[i]
                event2 = time_events[j]
                
                start1 = datetime.fromisoformat(event1['start_time'].replace('Z', '+00:00'))
                end1 = datetime.fromisoformat((event1.get('end_time') or event1['start_time']).replace('Z', '+00:00'))
                start2 = datetime.fromisoformat(event2['start_time'].replace('Z', '+00:00'))
                end2 = datetime.fromisoformat((event2.get('end_time') or event2['start_time']).replace('Z', '+00:00'))
                
                # Default to 1 hour if no end time
                if event1.get('end_time') == event1['start_time'] or not event1.get('end_time'):
                    end1 = start1 + timedelta(hours=1)
                if event2.get('end_time') == event2['start_time'] or not event2.get('end_time'):
                    end2 = start2 + timedelta(hours=1)
                
                # Check overlap: start1 < end2 AND start2 < end1
                if start1 < end2 and start2 < end1:
                    conflicts.append({
                        'event1': event1['title'],
                        'event2': event2['title'],
                        'time1': f"{start1.strftime('%H:%M')}-{end1.strftime('%H:%M')}",
                        'time2': f"{start2.strftime('%H:%M')}-{end2.strftime('%H:%M')}"
                    })
        
        print(f"🚨 Manual logic found {len(conflicts)} conflicts:")
        for i, conflict in enumerate(conflicts):
            print(f"   {i+1}. {conflict['event1']} ({conflict['time1']}) vs {conflict['event2']} ({conflict['time2']})")
    
    except Exception as e:
        print(f"❌ Error in manual conflict logic: {e}")

if __name__ == "__main__":
    print("🧪 CONFLICT DETECTION MODE TESTING")
    print("="*50)
    print("This script tests both server and client conflict detection")
    print()
    
    test_server_conflict_detection()
    test_manual_conflict_logic()
    
    print("\n✅ Testing complete!")
