#!/usr/bin/env python3
"""
Delete All Events Script for KairoCal
Clears all scheduled events from all database files
"""

import sqlite3
import os
from datetime import datetime

def delete_events_from_db(db_path):
    """Delete all events from a specific database file"""
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if events table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='events'
            """)
            
            if not cursor.fetchone():
                print(f"⚠️ No 'events' table found in: {db_path}")
                return True
            
            # Count events before deletion
            cursor.execute("SELECT COUNT(*) FROM events")
            count_before = cursor.fetchone()[0]
            
            if count_before == 0:
                print(f"ℹ️ No events to delete in: {db_path}")
                return True
            
            # Delete all events
            cursor.execute("DELETE FROM events")
            
            # Get count after deletion (should be 0)
            cursor.execute("SELECT COUNT(*) FROM events")
            count_after = cursor.fetchone()[0]
            
            conn.commit()
            
            print(f"✅ Deleted {count_before} events from: {db_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error deleting from {db_path}: {str(e)}")
        return False

def main():
    """Delete all events from all KairoCal database files"""
    print("🗑️ Deleting all scheduled events from KairoCal databases...")
    print("=" * 60)
    
    # List of potential database files
    database_files = [
        "kairocal.db",
        "backend/kairocal.db", 
        "backend/kairocal_local.db",
        "backend/kairocal_fallback.db",
        "backend/calendar_ai.db"
    ]
    
    deleted_count = 0
    processed_count = 0
    
    for db_file in database_files:
        full_path = db_file
        if delete_events_from_db(full_path):
            processed_count += 1
    
    print("=" * 60)
    print(f"🏁 Processed {processed_count} database files")
    print("✅ All scheduled events have been deleted!")
    print(f"⏰ Deletion completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0

if __name__ == "__main__":
    exit(main())
