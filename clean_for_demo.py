#!/usr/bin/env python3
"""
Clean database for demo - Remove all users and events for fresh start
"""

import sqlite3
import json
from datetime import datetime

def clean_database():
    """Clean all data from database for fresh demo"""
    try:
        conn = sqlite3.connect('kairocal.db')
        cursor = conn.cursor()
        
        print("=== CLEANING DATABASE FOR DEMO ===")
        print(f"Clean time: {datetime.now()}")
        print()
        
        # Get current counts before cleaning
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM events")
        event_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM conflicts")
        conflict_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM conflict_resolutions")
        resolution_count = cursor.fetchone()[0]
        
        print(f"📊 BEFORE CLEANING:")
        print(f"  Users: {user_count}")
        print(f"  Events: {event_count}")
        print(f"  Conflicts: {conflict_count}")
        print(f"  Resolutions: {resolution_count}")
        print()
        
        # Delete all data (in proper order due to foreign keys)
        print("🧹 CLEANING DATA...")
        
        cursor.execute("DELETE FROM conflict_resolutions")
        print("  ✅ Deleted conflict resolutions")
        
        cursor.execute("DELETE FROM conflicts")
        print("  ✅ Deleted conflicts")
        
        cursor.execute("DELETE FROM reminders")
        print("  ✅ Deleted reminders")
        
        cursor.execute("DELETE FROM events")
        print("  ✅ Deleted events")
        
        cursor.execute("DELETE FROM users")
        print("  ✅ Deleted users")
        
        conn.commit()
        
        # Verify cleanup
        cursor.execute("SELECT COUNT(*) FROM users")
        final_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM events")
        final_events = cursor.fetchone()[0]
        
        print()
        print(f"📊 AFTER CLEANING:")
        print(f"  Users: {final_users}")
        print(f"  Events: {final_events}")
        print()
        
        conn.close()
        
        print("✅ DATABASE CLEANED SUCCESSFULLY!")
        print()
        print("🎯 DEMO READY:")
        print("  - Analytics will show zero state")
        print("  - Your Google account will create fresh user")
        print("  - All metrics will start from zero")
        print("  - Perfect for clean demo presentation")
        
    except Exception as e:
        print(f"❌ Error cleaning database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("⚠️  WARNING: This will DELETE ALL data in the database!")
    print("This is intended for demo preparation only.")
    print()
    
    confirm = input("Type 'CLEAN' to proceed with cleaning: ")
    if confirm.upper() == 'CLEAN':
        clean_database()
    else:
        print("❌ Cleanup cancelled")
