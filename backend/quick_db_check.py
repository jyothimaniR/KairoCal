#!/usr/bin/env python3
"""
Quick check for recent events
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_recent_events():
    try:
        from app.core.database import get_db
        from app.models.event import Event
        from datetime import datetime, timedelta
        
        # Get database session
        db = next(get_db())
        
        # Look for recent events 
        recent_cutoff = datetime.now() - timedelta(hours=2)
        
        recent_events = db.query(Event).filter(
            Event.created_at >= recent_cutoff
        ).order_by(Event.created_at.desc()).limit(20).all()
        
        print("🔍 RECENT EVENTS (last 2 hours)")
        print("=" * 60)
        
        if recent_events:
            for event in recent_events:
                print(f"📅 Event:")
                print(f"  ID: {event.id}")
                print(f"  Title: '{event.title}'")
                print(f"  Location: '{event.location}'")
                print(f"  Created: {event.created_at}")
                print(f"  Created via: {event.created_via}")
                print("  ---")
        else:
            print("ℹ️ No recent events found")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")

if __name__ == "__main__":
    check_recent_events()
