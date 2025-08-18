#!/usr/bin/env python3
"""
Manual Conflict Detection Test
=============================

Based on the API data I retrieved, let me manually test the conflict detection logic
"""

from datetime import datetime

def test_conflict_detection():
    # Events from the API response (relevant ones for today - August 16, 2025)
    events = [
        {
            'id': 'standup',
            'title': 'Morning Team Standup',
            'start_time': '2025-08-16T09:00:00',
            'end_time': '2025-08-16T09:30:00',
            'all_day': False
        },
        {
            'id': 'planning',
            'title': 'Project Planning Session',
            'start_time': '2025-08-16T09:15:00',
            'end_time': '2025-08-16T10:15:00',
            'all_day': False
        },
        {
            'id': 'walk',
            'title': 'Casual Walk After Lunch . For 20 Minutes',
            'start_time': '2025-08-16T13:30:00',
            'end_time': '2025-08-16T14:30:00',
            'all_day': False
        },
        {
            'id': 'presentation',
            'title': 'Client Presentation',
            'start_time': '2025-08-16T14:00:00',
            'end_time': '2025-08-16T15:00:00',
            'all_day': False
        },
        {
            'id': 'doctor',
            'title': 'Doctor Check Up .',
            'start_time': '2025-08-16T15:00:00',
            'end_time': '2025-08-16T16:00:00',
            'all_day': False
        },
        {
            'id': 'coffee',
            'title': 'Quick Coffee Break',
            'start_time': '2025-08-16T15:45:00',
            'end_time': '2025-08-16T16:00:00',
            'all_day': False
        },
        {
            'id': 'mom',
            'title': 'Call Mom .',
            'start_time': '2025-08-16T17:00:00',
            'end_time': '2025-08-16T17:30:00',
            'all_day': False
        },
        {
            'id': 'dad',
            'title': 'Call Dad . For 15 Minutes',
            'start_time': '2025-08-16T17:00:00',
            'end_time': '2025-08-16T17:30:00',
            'all_day': False
        }
    ]
    
    print("🔍 MANUAL CONFLICT DETECTION TEST")
    print("=" * 40)
    
    conflicts = []
    
    # Check all pairs for overlaps
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            event1 = events[i]
            event2 = events[j]
            
            start1 = datetime.fromisoformat(event1['start_time'])
            end1 = datetime.fromisoformat(event1['end_time'])
            start2 = datetime.fromisoformat(event2['start_time'])
            end2 = datetime.fromisoformat(event2['end_time'])
            
            # Check for overlap: start1 < end2 AND start2 < end1
            has_overlap = start1 < end2 and start2 < end1
            
            print(f"\n🔄 Checking: {event1['title']} vs {event2['title']}")
            print(f"   Event 1: {start1.strftime('%H:%M')} - {end1.strftime('%H:%M')}")
            print(f"   Event 2: {start2.strftime('%H:%M')} - {end2.strftime('%H:%M')}")
            print(f"   Overlap: {start1} < {end2} = {start1 < end2}")
            print(f"   Overlap: {start2} < {end1} = {start2 < end1}")
            print(f"   Result: {'🚨 CONFLICT!' if has_overlap else '✅ No conflict'}")
            
            if has_overlap:
                conflicts.append({
                    'event1': event1['title'],
                    'event2': event2['title'],
                    'time1': f"{start1.strftime('%H:%M')}-{end1.strftime('%H:%M')}",
                    'time2': f"{start2.strftime('%H:%M')}-{end2.strftime('%H:%M')}"
                })
    
    print(f"\n🎯 FINAL RESULTS: Found {len(conflicts)} conflicts")
    for i, conflict in enumerate(conflicts, 1):
        print(f"   {i}. {conflict['event1']} ({conflict['time1']}) vs {conflict['event2']} ({conflict['time2']})")
    
    return conflicts

if __name__ == "__main__":
    test_conflict_detection()
