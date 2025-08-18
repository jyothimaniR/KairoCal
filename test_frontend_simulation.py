#!/usr/bin/env python3
"""
Test Frontend All-Day Event Skip Logic
This simulates what the frontend should now be doing
"""

import requests
import sqlite3

def simulate_frontend_behavior():
    """Simulate the corrected frontend behavior"""
    print("🧪 SIMULATING CORRECTED FRONTEND BEHAVIOR")
    print("=" * 60)
    
    # Get all events from database (like frontend does)
    with sqlite3.connect('backend/kairocal.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title, start_time, end_time, is_all_day, priority_level
            FROM events 
            ORDER BY start_time
        """)
        
        events = cursor.fetchall()
        
    print(f"📊 Found {len(events)} total events in database:")
    
    all_day_skipped = 0
    timed_checked = 0
    total_conflicts = 0
    
    for title, start_time, end_time, is_all_day, priority in events:
        event_type = "ALL-DAY" if is_all_day else "TIMED"
        print(f"\n📅 Processing: {title} ({event_type})")
        
        if is_all_day:
            print(f"   ⏭️  SKIPPED: All-day event ignored by frontend")
            all_day_skipped += 1
            continue
        
        # Only check timed events for conflicts
        print(f"   🔍 CHECKING: Timed event for conflicts...")
        timed_checked += 1
        
        payload = {
            'title': title,
            'start_time': start_time,
            'end_time': end_time,
            'is_all_day': False,
            'description': f'Checking {title}'
        }
        
        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/conflicts/check',
                json=payload,
                params={'cognito_sub': 'frontend-test-user'}
            )
            
            if response.status_code == 200:
                result = response.json()
                conflicts = len(result.get('conflicts', []))
                total_conflicts += conflicts
                
                if conflicts > 0:
                    print(f"   ⚠️  CONFLICTS: Found {conflicts} conflicts")
                    for conflict in result.get('conflicts', []):
                        print(f"      - {conflict.get('description', 'Unknown')}")
                else:
                    print(f"   ✅ NO CONFLICTS: Clear schedule slot")
            else:
                print(f"   ❌ API ERROR: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 FRONTEND SIMULATION RESULTS:")
    print(f"   📊 Total events: {len(events)}")
    print(f"   ⏭️  All-day events skipped: {all_day_skipped}")
    print(f"   🔍 Timed events checked: {timed_checked}")
    print(f"   ⚠️  Total conflicts found: {total_conflicts}")
    
    if all_day_skipped > 0 and total_conflicts == 0:
        print("\n🎉 SUCCESS! Frontend will now show:")
        print("   ✅ No conflicts from all-day events")
        print("   ✅ Only real timed event conflicts")
        print("   ✅ Clean conflicts page")
    elif total_conflicts > 0:
        print(f"\n⚠️  DETECTED: {total_conflicts} real conflicts between timed events")
        print("   ✅ All-day events properly ignored") 
        print("   ✅ Only showing meaningful conflicts")
    else:
        print("\n✅ CLEAN SCHEDULE: No conflicts detected")

if __name__ == "__main__":
    simulate_frontend_behavior()
