import json
import sqlite3

# Direct database check
print("🔍 Direct Database Investigation")
print("=" * 50)

conn = sqlite3.connect('kairocal.db')
cursor = conn.cursor()

# Check users
print("\n👥 Users in database:")
cursor.execute("SELECT id, cognito_sub, email FROM users")
users = cursor.fetchall()
for user in users:
    print(f"  {user}")

# Check events for frontend-test-user
print("\n📅 Events for frontend-test-user:")
cursor.execute("""
    SELECT e.id, e.title, e.priority_level, e.classification_method, e.created_via, e.start_time
    FROM events e 
    JOIN users u ON e.user_id = u.id 
    WHERE u.cognito_sub = 'frontend-test-user'
    ORDER BY e.start_time
""")
events = cursor.fetchall()
print(f"Total events found: {len(events)}")
for i, event in enumerate(events[:5]):  # Show first 5
    print(f"  {i+1}. {event}")

if len(events) > 5:
    print(f"  ... and {len(events) - 5} more events")

# Check events for last 30 days (what analytics API would check)
print("\n📊 Events in last 30 days:")
cursor.execute("""
    SELECT COUNT(*) 
    FROM events e 
    JOIN users u ON e.user_id = u.id 
    WHERE u.cognito_sub = 'frontend-test-user'
    AND e.start_time >= datetime('now', '-30 days')
""")
recent_count = cursor.fetchone()[0]
print(f"Recent events (30 days): {recent_count}")

conn.close()
print("\n✅ Database check complete")
