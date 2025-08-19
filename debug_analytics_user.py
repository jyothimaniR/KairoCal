#!/usr/bin/env python3
"""
Debug the analytics user lookup issue
"""

import sqlite3
import os

def debug_analytics_user_lookup():
    """Debug why analytics shows different user_id and fewer events"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'kairocal.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    print("🔍 Analytics User Lookup Debug")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check users table structure
        print("\n📋 USERS TABLE STRUCTURE:")
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Check ALL users with cognito_sub = frontend-test-user
        print("\n👥 ALL USERS WITH cognito_sub='frontend-test-user':")
        cursor.execute("SELECT id, cognito_sub, full_name, email, created_at FROM users WHERE cognito_sub = 'frontend-test-user'")
        users = cursor.fetchall()
        
        for user in users:
            print(f"  ID: {user[0]}")
            print(f"  Cognito Sub: {user[1]}")
            print(f"  Name: {user[2]}")  
            print(f"  Email: {user[3]}")
            print(f"  Created: {user[4]}")
            print("  ---")
            
        print(f"Total matching users: {len(users)}")
        
        # Check for duplicate cognito_sub values
        print("\n🔍 CHECKING FOR DUPLICATE COGNITO_SUB VALUES:")
        cursor.execute("SELECT cognito_sub, COUNT(*) as count FROM users GROUP BY cognito_sub HAVING count > 1")
        duplicates = cursor.fetchall()
        
        if duplicates:
            print("  ⚠️  Found duplicates:")
            for cognito_sub, count in duplicates:
                print(f"    {cognito_sub}: {count} users")
        else:
            print("  ✅ No duplicate cognito_sub values")
        
        # Check events for the correct user ID
        correct_user_id = "465be9a2-a553-4d81-9445-955712117b77"
        analytics_user_id = "dc5fd330-8226-4eee-9333-1a61ab3c0381"
        
        print(f"\n📅 EVENTS BY USER ID:")
        print(f"Correct User ID ({correct_user_id}):")
        cursor.execute("SELECT COUNT(*) FROM events WHERE user_id = ?", (correct_user_id,))
        correct_count = cursor.fetchone()[0]
        print(f"  Events: {correct_count}")
        
        print(f"\nAnalytics User ID ({analytics_user_id}):")
        cursor.execute("SELECT COUNT(*) FROM events WHERE user_id = ?", (analytics_user_id,))
        analytics_count = cursor.fetchone()[0]
        print(f"  Events: {analytics_count}")
        
        # Check if analytics user ID exists in users table
        print(f"\n🔍 CHECKING IF ANALYTICS USER ID EXISTS:")
        cursor.execute("SELECT id, cognito_sub, full_name FROM users WHERE id = ?", (analytics_user_id,))
        analytics_user = cursor.fetchone()
        
        if analytics_user:
            print(f"  ✅ Analytics user ID exists:")
            print(f"    ID: {analytics_user[0]}")
            print(f"    Cognito Sub: {analytics_user[1]}")
            print(f"    Name: {analytics_user[2]}")
        else:
            print(f"  ❌ Analytics user ID does not exist in users table!")
            print(f"  🤔 This indicates the analytics API is creating/finding a different user")
        
        # Check recent events for both users
        print(f"\n📋 RECENT EVENTS COMPARISON:")
        
        # Recent events for correct user
        cursor.execute("""
            SELECT title, start_time, priority_level, classification_method 
            FROM events 
            WHERE user_id = ? 
            ORDER BY start_time DESC 
            LIMIT 5
        """, (correct_user_id,))
        correct_events = cursor.fetchall()
        
        print(f"Correct User ({correct_user_id}) - Recent events:")
        for event in correct_events:
            print(f"  - {event[0]} | {event[1]} | Priority: {event[2]} | Method: {event[3]}")
        
        # Recent events for analytics user (if exists)
        cursor.execute("""
            SELECT title, start_time, priority_level, classification_method 
            FROM events 
            WHERE user_id = ? 
            ORDER BY start_time DESC 
            LIMIT 5
        """, (analytics_user_id,))
        analytics_events = cursor.fetchall()
        
        print(f"\nAnalytics User ({analytics_user_id}) - Recent events:")
        for event in analytics_events:
            print(f"  - {event[0]} | {event[1]} | Priority: {event[2]} | Method: {event[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_analytics_user_lookup()
