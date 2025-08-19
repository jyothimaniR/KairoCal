#!/usr/bin/env python3
"""
Debug script to check what dates the events have and what the MiniCalendar should be showing
"""

import requests
import json
from datetime import datetime, date

def check_event_dates():
    print("🔍 Debugging MiniCalendar date issues...")
    
    # Get events from API
    try:
        response = requests.get("http://localhost:8000/api/v1/events?cognito_sub=frontend-test-user")
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Found {len(events)} events")
            
            # Check what dates the events have
            today = date.today()
            print(f"📅 Today is: {today}")
            
            event_dates = {}
            for event in events:
                start_time = event.get('start_time')
                if start_time:
                    # Parse the datetime
                    dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    event_date = dt.date()
                    
                    if event_date not in event_dates:
                        event_dates[event_date] = []
                    event_dates[event_date].append({
                        'title': event.get('title', 'No title'),
                        'start_time': start_time,
                        'parsed_date': event_date.isoformat()
                    })
            
            print(f"\n📊 Events by date:")
            for event_date in sorted(event_dates.keys()):
                count = len(event_dates[event_date])
                print(f"  {event_date}: {count} events")
                for event in event_dates[event_date][:3]:  # Show first 3 events
                    print(f"    - {event['title']}")
                if count > 3:
                    print(f"    ... and {count - 3} more")
            
            # Check current month
            current_month = today.replace(day=1)
            events_this_month = [d for d in event_dates.keys() if d.year == today.year and d.month == today.month]
            print(f"\n📅 Events in current month ({today.year}-{today.month:02d}): {len(events_this_month)} days with events")
            
            if events_this_month:
                print("Days with events in current month:")
                for event_date in sorted(events_this_month):
                    count = len(event_dates[event_date])
                    print(f"  {event_date}: {count} events")
            
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_event_dates()
