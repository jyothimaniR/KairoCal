#!/usr/bin/env python3
"""
Check event classification methods
"""

import sqlite3
import os
from datetime import datetime, timedelta

def check_classification_methods():
    """Check what classification methods events have"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'kairocal.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    print("🔍 Checking Event Classification Methods")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE cognito_sub = 'frontend-test-user'")
        user_result = cursor.fetchone()
        
        if not user_result:
            print("❌ No user found")
            return
            
        user_id = user_result[0]
        
        # Analytics date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        print(f"📅 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Check classification methods for all events
        cursor.execute("""
            SELECT title, start_time, classification_method, priority_level
            FROM events 
            WHERE user_id = ?
            ORDER BY start_time
        """, (user_id,))
        all_events = cursor.fetchall()
        
        print(f"\n📋 ALL EVENTS CLASSIFICATION METHODS:")
        
        in_range_count = 0
        bert_in_range_count = 0
        
        for title, start_time, classification_method, priority_level in all_events:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00').replace('+00:00', ''))
            
            if start_date <= start_dt <= end_date:
                range_status = "✅ IN RANGE"
                in_range_count += 1
                
                if classification_method == 'bert':
                    bert_status = "🤖 BERT"
                    bert_in_range_count += 1
                else:
                    bert_status = f"❌ {classification_method or 'None'}"
            else:
                range_status = "❌ OUT OF RANGE"
                bert_status = f"⚪ {classification_method or 'None'}"
                
            print(f"  {range_status} | {bert_status} | Priority: {priority_level} | {title}")
        
        print(f"\n🎯 SUMMARY:")
        print(f"  Total events: {len(all_events)}")
        print(f"  Events in date range: {in_range_count}")
        print(f"  BERT events in range: {bert_in_range_count}")
        
        # Count by classification method
        cursor.execute("""
            SELECT classification_method, COUNT(*) 
            FROM events 
            WHERE user_id = ?
            GROUP BY classification_method
        """, (user_id,))
        method_counts = cursor.fetchall()
        
        print(f"\n📊 CLASSIFICATION METHOD BREAKDOWN:")
        for method, count in method_counts:
            print(f"  {method or 'None'}: {count} events")
        
        # Show what the analytics APIs should see
        print(f"\n🔍 WHAT ANALYTICS APIS SEE:")
        print(f"  Priority Trends: {in_range_count} events (all in date range)")
        print(f"  BERT Performance: {bert_in_range_count} events (BERT + in date range)")
        
        if bert_in_range_count == 0:
            print(f"\n🔧 BERT PERFORMANCE ISSUE:")
            print(f"  No BERT-classified events in the last 30 days!")
            print(f"  Solution: Either extend date range or ensure events are BERT-classified")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_classification_methods()
