#!/usr/bin/env python3
"""
Simple script to check current database contents
"""

import sqlite3
import json
from datetime import datetime

def check_database():
    """Check current database contents"""
    try:
        conn = sqlite3.connect('kairocal.db')
        cursor = conn.cursor()
        
        print("=== DATABASE CONTENTS CHECK ===")
        print(f"Check time: {datetime.now()}")
        print()
        
        # Check table structure first
        print("� TABLE STRUCTURES:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            print(f"\n  Table: {table_name}")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"    - {col[1]} ({col[2]})")
        print()
        
        # Check users
        print("� USERS:")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        if users:
            cursor.execute("PRAGMA table_info(users)")
            user_columns = [col[1] for col in cursor.fetchall()]
            print(f"  Columns: {user_columns}")
            for i, user in enumerate(users):
                print(f"  - User {i+1}: {dict(zip(user_columns, user))}")
        else:
            print("  No users found")
        print(f"Total users: {len(users)}")
        print()
        
        # Check events
        print("� EVENTS:")
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        if events:
            cursor.execute("PRAGMA table_info(events)")
            event_columns = [col[1] for col in cursor.fetchall()]
            print(f"  Columns: {event_columns}")
            for i, event in enumerate(events[:5]):  # Show first 5
                print(f"  - Event {i+1}: {dict(zip(event_columns, event))}")
            if len(events) > 5:
                print(f"  ... and {len(events) - 5} more events")
        else:
            print("  No events found")
        print(f"Total events: {len(events)}")
        print()
        
        conn.close()
        
        print()
        print("=== RECOMMENDATION ===")
        if len(events) > 0:
            print("🚨 Database contains demo/test data that will affect analytics")
            print("💡 For clean demo: Delete all existing users and events")
            print("✅ This will show accurate zero state for your Google account")
        else:
            print("✅ Database is clean - analytics will show correct zero state")
            
    except Exception as e:
        print(f"Error checking database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database()
