#!/usr/bin/env python3
"""
Clean up old problematic events from the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def cleanup_old_events():
    try:
        from app.core.database import get_db
        from app.models.event import Event
        from sqlalchemy.orm import Session
        
        # Get database session
        db = next(get_db())
        
        # Find the specific problematic event
        problematic_event = db.query(Event).filter(
            Event.title == 'Play Football With Friends Coming At The Anfield Stadium .'
        ).first()
        
        if problematic_event:
            print(f"🗑️ Deleting problematic event:")
            print(f"  ID: {problematic_event.id}")
            print(f"  Title: '{problematic_event.title}'")
            print(f"  Location: '{problematic_event.location}'")
            print(f"  Created: {problematic_event.created_at}")
            
            db.delete(problematic_event)
            db.commit()
            print("✅ Event deleted successfully!")
        else:
            print("ℹ️ No problematic event found to delete")
        
        # Also clean up other test events with "Coming" that were created during debugging
        other_coming_events = db.query(Event).filter(
            Event.title.ilike('%coming%'),
            Event.created_via == 'voice'
        ).all()
        
        if other_coming_events:
            print(f"\n🧹 Found {len(other_coming_events)} other test events with 'Coming' to clean up:")
            for event in other_coming_events:
                print(f"  - {event.title}")
                db.delete(event)
            
            db.commit()
            print("✅ All test events cleaned up!")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    cleanup_old_events()
