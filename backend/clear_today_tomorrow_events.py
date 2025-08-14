import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('kairocal.db')
cursor = conn.cursor()

# Get today and tomorrow dates
today = datetime.now().date()
tomorrow = today + timedelta(days=1)

print(f"Deleting events for:")
print(f"  Today: {today}")
print(f"  Tomorrow: {tomorrow}")

# Find events to delete first
cursor.execute('''
    SELECT id, title, start_time, created_via
    FROM events 
    WHERE DATE(start_time) = ? OR DATE(start_time) = ?
    ORDER BY start_time
''', (str(today), str(tomorrow)))

events_to_delete = cursor.fetchall()

print(f"\nFound {len(events_to_delete)} events to delete:")
for event in events_to_delete:
    print(f"  - {event[1]} ({event[2]}) [{event[3]}]")

if events_to_delete:
    # Delete the events
    cursor.execute('''
        DELETE FROM events 
        WHERE DATE(start_time) = ? OR DATE(start_time) = ?
    ''', (str(today), str(tomorrow)))
    
    deleted_count = cursor.rowcount
    conn.commit()
    print(f"\n✅ Successfully deleted {deleted_count} events")
else:
    print("\n✅ No events found to delete")

# Verify deletion
cursor.execute('''
    SELECT COUNT(*) 
    FROM events 
    WHERE DATE(start_time) = ? OR DATE(start_time) = ?
''', (str(today), str(tomorrow)))

remaining = cursor.fetchone()[0]
print(f"📊 Remaining events for today/tomorrow: {remaining}")

conn.close()
