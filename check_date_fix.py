#!/usr/bin/env python3
"""
Simple test to create events and check dates using the existing API test script
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import sqlite3
from datetime import datetime

def check_recent_events():
    """Check recently created events to see their dates"""
    print("=== Checking Recent Events in Database ===")
    print(f"Current local date: {datetime.now().date()}")
    print(f"Current UTC date: {datetime.utcnow().date()}")
    print()
    
    try:
        # Connect to the database
        db_path = os.path.join(os.path.dirname(__file__), 'backend', 'kairocal.db')
        if not os.path.exists(db_path):
            db_path = os.path.join(os.path.dirname(__file__), 'kairocal.db')
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get the most recent events from today
        cursor.execute('''
            SELECT id, title, start_time, end_time, created_via, created_at
            FROM events 
            WHERE DATE(created_at) >= DATE('now', '-1 day')
            ORDER BY created_at DESC
            LIMIT 10
        ''')
        
        events = cursor.fetchall()
        
        if events:
            print(f"Found {len(events)} recent events:")
            for event in events:
                event_id, title, start_time, end_time, created_via, created_at = event
                
                # Parse the start_time to get the date
                try:
                    if start_time:
                        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                        event_date = start_dt.date()
                    else:
                        event_date = "No start time"
                        
                    created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    
                    print(f"  - {title}")
                    print(f"    Event Date: {event_date}")
                    print(f"    Start Time: {start_time}")
                    print(f"    Created: {created_dt}")
                    print(f"    Via: {created_via}")
                    print()
                except Exception as e:
                    print(f"  - {title} (Error parsing date: {e})")
        else:
            print("No recent events found")
            
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}")

def instructions():
    print("=== Manual Test Instructions ===")
    print("1. Open the KairoCal frontend in your browser")
    print("2. Try creating a voice event with 'Schedule meeting today at 2pm'")
    print("3. Check that the event is created for August 18th (today)")
    print("4. Try creating 'Schedule call tomorrow at 10am'") 
    print("5. Check that the event is created for August 19th (tomorrow)")
    print("6. Run this script again to check the database results")
    print()

if __name__ == "__main__":
    instructions()
    check_recent_events()
