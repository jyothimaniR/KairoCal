#!/usr/bin/env python3
"""
Debug user ID mapping between frontend and backend
"""

import sqlite3
import os

def check_user_mapping():
    """Check how frontend-test-user maps to actual database users"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'kairocal.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    print("🔍 User ID Mapping Investigation")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check all users
        print("\n👥 ALL USERS IN DATABASE:")
        cursor.execute("SELECT id, cognito_sub, full_name, email FROM users")
        users = cursor.fetchall()
        
        for user_id, cognito_sub, full_name, email in users:
            print(f"  ID: {user_id}")
            print(f"  Cognito Sub: {cognito_sub}")
            print(f"  Name: {full_name}")
            print(f"  Email: {email}")
            print(f"  ---")
        
        print(f"\nTotal users: {len(users)}")
        
        # Check events for each user
        print("\n📅 EVENTS BY USER:")
        for user_id, cognito_sub, full_name, email in users:
            cursor.execute("SELECT COUNT(*) FROM events WHERE user_id = ?", (user_id,))
            event_count = cursor.fetchone()[0]
            print(f"  {cognito_sub} ({full_name}): {event_count} events")
        
        # Check specifically for frontend-test-user
        print("\n🔍 LOOKING FOR 'frontend-test-user':")
        cursor.execute("SELECT * FROM users WHERE cognito_sub = 'frontend-test-user'")
        frontend_user = cursor.fetchone()
        
        if frontend_user:
            print("  ✅ Found frontend-test-user")
        else:
            print("  ❌ No user with cognito_sub = 'frontend-test-user'")
            print("  🤔 This explains the analytics issue!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_user_mapping()
