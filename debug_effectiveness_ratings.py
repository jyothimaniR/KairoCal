#!/usr/bin/env python3
"""
Check which events have effectiveness_rating set
"""

import sqlite3
import os

def check_effectiveness_ratings():
    """Check how many events have effectiveness ratings"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'kairocal.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    print("🔍 Checking Event Effectiveness Ratings")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get user ID for frontend-test-user
        cursor.execute("SELECT id FROM users WHERE cognito_sub = 'frontend-test-user'")
        user_result = cursor.fetchone()
        
        if not user_result:
            print("❌ No user found with cognito_sub = 'frontend-test-user'")
            return
            
        user_id = user_result[0]
        print(f"👤 User ID: {user_id}")
        
        # Check total events
        cursor.execute("SELECT COUNT(*) FROM events WHERE user_id = ?", (user_id,))
        total_events = cursor.fetchone()[0]
        print(f"📅 Total events: {total_events}")
        
        # Check events with effectiveness_rating
        cursor.execute("""
            SELECT COUNT(*) FROM events 
            WHERE user_id = ? AND effectiveness_rating IS NOT NULL
        """, (user_id,))
        rated_events = cursor.fetchone()[0]
        print(f"⭐ Events with effectiveness_rating: {rated_events}")
        
        # Check events without effectiveness_rating
        cursor.execute("""
            SELECT COUNT(*) FROM events 
            WHERE user_id = ? AND effectiveness_rating IS NULL
        """, (user_id,))
        unrated_events = cursor.fetchone()[0]
        print(f"❌ Events without effectiveness_rating: {unrated_events}")
        
        # Show sample events with and without ratings
        print(f"\n📋 SAMPLE EVENTS WITH RATINGS:")
        cursor.execute("""
            SELECT title, effectiveness_rating, start_time 
            FROM events 
            WHERE user_id = ? AND effectiveness_rating IS NOT NULL
            LIMIT 5
        """, (user_id,))
        rated_samples = cursor.fetchall()
        
        for title, rating, start_time in rated_samples:
            print(f"  ✅ {title} | Rating: {rating} | {start_time}")
        
        print(f"\n📋 SAMPLE EVENTS WITHOUT RATINGS:")
        cursor.execute("""
            SELECT title, effectiveness_rating, start_time 
            FROM events 
            WHERE user_id = ? AND effectiveness_rating IS NULL
            LIMIT 5
        """, (user_id,))
        unrated_samples = cursor.fetchall()
        
        for title, rating, start_time in unrated_samples:
            print(f"  ❌ {title} | Rating: {rating} | {start_time}")
        
        print(f"\n🎯 CONCLUSION:")
        if rated_events == 0:
            print("  ❌ NO events have effectiveness ratings!")
            print("  🔧 This is why analytics shows 0 events")
        elif rated_events < total_events:
            print(f"  ⚠️  Only {rated_events}/{total_events} events have ratings")
            print(f"  🔧 Analytics only uses {rated_events} events")
        else:
            print("  ✅ All events have effectiveness ratings")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_effectiveness_ratings()
