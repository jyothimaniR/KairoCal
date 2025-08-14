#!/usr/bin/env python3
"""
Create conflicting events directly in PostgreSQL database
"""
import psycopg2
from datetime import datetime, timedelta
import uuid

def create_conflicting_events():
    """Create conflicting events directly in PostgreSQL database"""
    
    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'kairocal',
        'user': 'kairocal_user',
        'password': 'Test123'
    }
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Get the test user ID
        test_user_id = "18209d0d-62c7-48a6-8b49-7fb4e5d3f28e"
        
        # Create conflicting events at the same time (2 hours from now)
        now = datetime.now()
        test_time = now + timedelta(hours=2)
        start_time = test_time.isoformat()
        end_time = (test_time + timedelta(hours=1)).isoformat()
        
        conflicting_events = [
            {
                "id": str(uuid.uuid4()),
                "title": "Team Meeting - Conflict Test 1",
                "description": "First conflicting event for testing delete functionality",
                "start_time": start_time,
                "end_time": end_time,
                "priority_level": 2,
                "created_via": "manual",
                "user_id": test_user_id
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Project Review - Conflict Test 2", 
                "description": "Second conflicting event for testing delete functionality",
                "start_time": start_time,  # Same time as first event
                "end_time": end_time,
                "priority_level": 3,
                "created_via": "voice",
                "user_id": test_user_id
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Client Call - Conflict Test 3",
                "description": "Third conflicting event for testing delete functionality", 
                "start_time": start_time,  # Same time as other events
                "end_time": end_time,
                "priority_level": 1,
                "created_via": "manual",
                "user_id": test_user_id
            }
        ]
        
        print(f"🔧 Creating {len(conflicting_events)} conflicting events...")
        print(f"📅 Event time: {test_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check table structure first
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'events';")
        columns = [row[0] for row in cursor.fetchall()]
        print(f"📊 Available columns: {columns}")
        
        # Insert each event
        for i, event in enumerate(conflicting_events):
            try:
                cursor.execute("""
                    INSERT INTO events (
                        id, title, description, start_time, end_time, 
                        priority_level, created_via, user_id,
                        created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    event["id"],
                    event["title"],
                    event["description"], 
                    event["start_time"],
                    event["end_time"],
                    event["priority_level"],
                    event["created_via"],
                    event["user_id"],
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                
                print(f"✅ Created event {i+1}: {event['title']}")
                
            except psycopg2.Error as e:
                print(f"❌ Error creating event {i+1}: {e}")
        
        # Commit changes
        conn.commit()
        print("\n🎉 All conflicting events created successfully!")
        print("💡 Refresh your dashboard to see the conflicts and test delete functionality")
        
        # Verify events were created
        cursor.execute("""
            SELECT id, title, start_time FROM events 
            WHERE title LIKE %s 
            ORDER BY created_at DESC
        """, ('%Conflict Test%',))
        
        created_events = cursor.fetchall()
        print(f"\n📋 Verification: Found {len(created_events)} test events in database:")
        for event in created_events:
            print(f"   - {event[1]} (ID: {event[0][:8]}...)")
            
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

def cleanup_test_events():
    """Remove all test events from database"""
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'kairocal',
        'user': 'kairocal_user',
        'password': 'Test123'
    }
    
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Find test events
        cursor.execute("SELECT id, title FROM events WHERE title LIKE %s", ('%Conflict Test%',))
        test_events = cursor.fetchall()
        
        print(f"🧹 Found {len(test_events)} test events to cleanup:")
        for event in test_events:
            print(f"   - {event[1]}")
        
        # Delete test events
        cursor.execute("DELETE FROM events WHERE title LIKE %s", ('%Conflict Test%',))
        deleted_count = cursor.rowcount
        
        conn.commit()
        print(f"✅ Deleted {deleted_count} test events")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        cleanup_test_events()
    else:
        create_conflicting_events()
