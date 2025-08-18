import sqlite3
from datetime import datetime

conn = sqlite3.connect('../kairocal.db')
cursor = conn.cursor()

print('=== DATABASE CONTENTS ===')
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('Tables:', [t[0] for t in tables])

cursor.execute('SELECT COUNT(*) FROM events')
count = cursor.fetchone()[0]
print(f'Events count: {count}')

if count > 0:
    cursor.execute('SELECT id, title, start_time, end_time FROM events LIMIT 3')
    events = cursor.fetchall()
    for event in events:
        print(f'Event: {event[1]} - {event[2]} to {event[3]}')
        
        # Test parsing the times
        try:
            start_dt = datetime.fromisoformat(event[2].replace('Z', '+00:00'))
            print(f'  Parsed start: {start_dt}')
        except Exception as e:
            print(f'  Parse error: {e}')
else:
    print('No events found')

conn.close()
