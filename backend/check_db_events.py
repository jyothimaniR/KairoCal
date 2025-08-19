#!/usr/bin/env python3
"""
Check for existing events that might be causing confusion
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Quick database check script
def check_recent_events():
    try:
        from app.core.database import get_db
        from app.models.event import Event
        from sqlalchemy.orm import Session
        from datetime import datetime, timedelta
        
        # Get database session
        db = next(get_db())
        
        # Look for recent events with "Football" or "Anfield" in the title
        recent_cutoff = datetime.now() - timedelta(hours=24)
        
        football_events = db.query(Event).filter(
            Event.title.ilike('%football%')
        ).order_by(Event.created_at.desc()).limit(10).all()
        
        anfield_events = db.query(Event).filter(
            Event.title.ilike('%anfield%')
        ).order_by(Event.created_at.desc()).limit(10).all()
        
        coming_events = db.query(Event).filter(
            Event.title.ilike('%coming%')
        ).order_by(Event.created_at.desc()).limit(10).all()
        
        print("🔍 CHECKING DATABASE FOR EXISTING EVENTS")
        print("=" * 60)
        
        if football_events:
            print("⚽ FOOTBALL EVENTS FOUND:")
            for event in football_events:
                print(f"  ID: {event.id}")
                print(f"  Title: '{event.title}'")
                print(f"  Location: '{event.location}'")
                print(f"  Created: {event.created_at}")
                print(f"  Start: {event.start_time}")
                print("  ---")
        else:
            print("⚽ No football events found")
        
        if anfield_events:
            print("\n🏟️ ANFIELD EVENTS FOUND:")
            for event in anfield_events:
                print(f"  ID: {event.id}")
                print(f"  Title: '{event.title}'")
                print(f"  Location: '{event.location}'")
                print(f"  Created: {event.created_at}")
                print("  ---")
        else:
            print("\n🏟️ No Anfield events found")
        
        if coming_events:
            print("\n📅 EVENTS WITH 'COMING' IN TITLE:")
            for event in coming_events:
                print(f"  ID: {event.id}")
                print(f"  Title: '{event.title}'")
                print(f"  Location: '{event.location}'")
                print(f"  Created: {event.created_at}")
                print("  ---")
        else:
            print("\n📅 No events with 'coming' found")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")

if __name__ == "__main__":
    check_recent_events()
