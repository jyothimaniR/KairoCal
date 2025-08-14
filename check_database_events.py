#!/usr/bin/env python3
"""
Check database storage for events to see if is_all_day is stored correctly
"""

import sys
import os
from datetime import datetime

# Add the backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.core.database import get_db, get_engine
from backend.app.models.event import Event
from sqlalchemy.orm import Session

def check_database_events():
    print('=== Checking Database Events ===')
    print(f'Current time: {datetime.now()}')
    print()
    
    # Get database session
    engine = get_engine()
    db = Session(engine)
    
    try:
        # Query recent events
        events = db.query(Event).order_by(Event.created_at.desc()).limit(10).all()
        
        print(f"Found {len(events)} recent events:")
        print()
        
        for event in events:
            print(f"Event ID: {event.id}")
            print(f"  Title: {event.title}")
            print(f"  Start: {event.start_time}")
            print(f"  End: {event.end_time}")
            print(f"  is_all_day: {event.is_all_day}")
            print(f"  Created via: {event.created_via}")
            print(f"  Priority: {event.priority_level}")
            
            # Check time details
            if event.start_time:
                hour = event.start_time.hour
                minute = event.start_time.minute
                print(f"  Time details: {hour:02d}:{minute:02d}")
                
                # Check for inconsistencies
                if event.is_all_day and (hour != 0 or minute != 0):
                    print(f"  ⚠️  INCONSISTENCY: Marked all-day but has time {hour:02d}:{minute:02d}")
                elif not event.is_all_day and hour == 0 and minute == 0:
                    print(f"  ⚠️  POTENTIAL ISSUE: Not all-day but time is 00:00")
                else:
                    print(f"  ✅ Consistent: all_day={event.is_all_day}, time={hour:02d}:{minute:02d}")
            
            print(f"  Created: {event.created_at}")
            print()
    
    except Exception as e:
        print(f"Database error: {e}")
    
    finally:
        db.close()

if __name__ == '__main__':
    check_database_events()
