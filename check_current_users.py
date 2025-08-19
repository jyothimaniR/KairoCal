#!/usr/bin/env python3
"""
Check current users and database state
"""
import sqlite3
import os

def check_database(db_path):
    """Check database tables and users"""
    if not os.path.exists(db_path):
        print(f"❌ Database file does not exist: {db_path}")
        return
    
    print(f"📋 Checking database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Tables found: {tables}")
        
        # If users table exists, check users
        if 'users' in tables:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"👥 Total users: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT id, email, full_name, cognito_sub FROM users LIMIT 10")
                users = cursor.fetchall()
                print(f"📝 Users:")
                for user in users:
                    print(f"  - {user[2]} ({user[1]}) - cognito_sub: {user[3]}")
        else:
            print("❌ No users table found")
            
        # If events table exists, check events
        if 'events' in tables:
            cursor.execute("SELECT COUNT(*) FROM events")
            event_count = cursor.fetchone()[0]
            print(f"📅 Total events: {event_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    # Check different database locations
    db_locations = [
        "backend/kairocal.db",
        "kairocal.db", 
        "backend/kairocal_local.db",
        "backend/calendar_ai.db"
    ]
    
    for db_path in db_locations:
        if os.path.exists(db_path):
            check_database(db_path)
            print("-" * 50)
