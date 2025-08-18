#!/usr/bin/env python3
"""
Database Priority Check Script
Check actual priority values stored in the database
"""

import sqlite3
import os
from datetime import datetime

def check_database_priorities():
    """Check priority values in all database files"""
    print("🔍 CHECKING DATABASE PRIORITY VALUES")
    print("=" * 50)
    
    # Database files to check
    db_files = [
        "kairocal.db",
        "backend/kairocal.db",
        "backend/calendar_ai.db"
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"\n📁 Database: {db_file}")
            try:
                with sqlite3.connect(db_file) as conn:
                    cursor = conn.cursor()
                    
                    # Check if events table exists
                    cursor.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name='events'
                    """)
                    
                    if not cursor.fetchone():
                        print("   ⚠️ No events table found")
                        continue
                    
                    # Get recent events with priority info
                    cursor.execute("""
                        SELECT 
                            title,
                            priority_level,
                            priority_confidence,
                            classification_method,
                            created_via,
                            created_at
                        FROM events 
                        ORDER BY created_at DESC 
                        LIMIT 10
                    """)
                    
                    events = cursor.fetchall()
                    
                    if not events:
                        print("   ℹ️ No events found")
                        continue
                    
                    print(f"   📊 Found {len(events)} events:")
                    for i, event in enumerate(events, 1):
                        title, priority, confidence, method, created_via, created_at = event
                        print(f"   {i}. '{title[:40]}{'...' if len(title) > 40 else ''}'")
                        print(f"      Priority: {priority} | Confidence: {confidence:.3f} | Method: {method}")
                        print(f"      Created via: {created_via} | At: {created_at}")
                        print()
                    
                    # Check priority distribution
                    cursor.execute("""
                        SELECT 
                            priority_level,
                            COUNT(*) as count,
                            AVG(priority_confidence) as avg_confidence
                        FROM events 
                        GROUP BY priority_level 
                        ORDER BY priority_level
                    """)
                    
                    distribution = cursor.fetchall()
                    
                    print("   📈 Priority Distribution:")
                    priority_labels = {
                        1: "VERY LOW",
                        2: "LOW", 
                        3: "MEDIUM",
                        4: "HIGH",
                        5: "CRITICAL"
                    }
                    
                    for priority, count, avg_conf in distribution:
                        label = priority_labels.get(priority, f"UNKNOWN({priority})")
                        print(f"      {priority} ({label}): {count} events (avg confidence: {avg_conf:.3f})")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"\n📁 Database: {db_file} - NOT FOUND")

def check_tennis_event():
    """Specifically look for the tennis event from the screenshot"""
    print("\n🎾 LOOKING FOR TENNIS EVENT")
    print("=" * 30)
    
    db_files = ["kairocal.db", "backend/kairocal.db"]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                with sqlite3.connect(db_file) as conn:
                    cursor = conn.cursor()
                    
                    # Look for tennis-related events
                    cursor.execute("""
                        SELECT 
                            title,
                            priority_level,
                            priority_confidence,
                            classification_method,
                            start_time,
                            end_time,
                            created_at
                        FROM events 
                        WHERE title LIKE '%tennis%' 
                           OR description LIKE '%tennis%'
                           OR title LIKE '%friend%'
                        ORDER BY created_at DESC
                    """)
                    
                    tennis_events = cursor.fetchall()
                    
                    if tennis_events:
                        print(f"🎾 Found {len(tennis_events)} tennis/friend events in {db_file}:")
                        for event in tennis_events:
                            title, priority, confidence, method, start_time, end_time, created_at = event
                            print(f"   📅 Event: '{title}'")
                            print(f"      💾 Stored Priority: {priority}")
                            print(f"      🎯 Confidence: {confidence}")
                            print(f"      🔧 Method: {method}")
                            print(f"      ⏰ Time: {start_time} - {end_time}")
                            print(f"      📝 Created: {created_at}")
                            print()
                    else:
                        print(f"   No tennis events found in {db_file}")
                        
            except Exception as e:
                print(f"   ❌ Error checking {db_file}: {e}")

def main():
    check_database_priorities()
    check_tennis_event()
    
    print("\n" + "=" * 50)
    print("🔍 KEY FINDINGS TO LOOK FOR:")
    print("1. Are events stored with BERT scale (1=VERY LOW, 5=CRITICAL)?")
    print("2. What priority was stored for the tennis event?")
    print("3. Is there a mismatch between stored vs displayed values?")

if __name__ == "__main__":
    main()
