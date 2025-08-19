#!/usr/bin/env python3
"""
Check event dates vs analytics date filtering
"""

import sqlite3
import os
from datetime import datetime, timedelta

def check_event_dates():
    """Check event dates vs analytics filtering"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'kairocal.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    print("🔍 Checking Event Dates vs Analytics Filtering")
    print("=" * 55)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE cognito_sub = 'frontend-test-user'")
        user_result = cursor.fetchone()
        
        if not user_result:
            print("❌ No user found")
            return
            
        user_id = user_result[0]
        print(f"👤 User ID: {user_id}")
        
        # Analytics date range (default 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        print(f"\n📅 ANALYTICS DATE RANGE:")
        print(f"  Start: {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  End:   {end_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check all events
        cursor.execute("""
            SELECT title, start_time, end_time 
            FROM events 
            WHERE user_id = ?
            ORDER BY start_time
        """, (user_id,))
        all_events = cursor.fetchall()
        
        print(f"\n📋 ALL EVENTS ({len(all_events)}):")
        events_in_range = 0
        events_out_of_range = 0
        
        for title, start_time, end_time in all_events:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00').replace('+00:00', ''))
            
            if start_date <= start_dt <= end_date:
                status = "✅ IN RANGE"
                events_in_range += 1
            else:
                status = "❌ OUT OF RANGE"
                events_out_of_range += 1
                
            print(f"  {status} | {title} | {start_time}")
        
        print(f"\n🎯 SUMMARY:")
        print(f"  Events in analytics range: {events_in_range}")
        print(f"  Events outside range: {events_out_of_range}")
        
        if events_in_range == 0:
            print(f"\n🔧 SOLUTION: All events are outside the 30-day analytics window!")
            print(f"  Analytics needs to use a wider date range or events need current dates")
        elif events_in_range < len(all_events):
            print(f"\n⚠️  Some events are outside the analytics window")
            print(f"  Consider extending the date range in analytics")
        
        # Check what range would include all events
        if all_events:
            oldest_event = min(all_events, key=lambda x: x[1])
            newest_event = max(all_events, key=lambda x: x[1])
            
            oldest_dt = datetime.fromisoformat(oldest_event[1].replace('Z', '+00:00').replace('+00:00', ''))
            newest_dt = datetime.fromisoformat(newest_event[1].replace('Z', '+00:00').replace('+00:00', ''))
            
            days_needed = (end_date - oldest_dt).days
            
            print(f"\n📊 OPTIMAL DATE RANGE:")
            print(f"  Oldest event: {oldest_event[1]} ({oldest_event[0]})")
            print(f"  Newest event: {newest_event[1]} ({newest_event[0]})")
            print(f"  Days needed: {days_needed} days back from now")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_event_dates()
