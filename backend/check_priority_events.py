import sqlite3

conn = sqlite3.connect('kairocal.db')
cursor = conn.cursor()

# Find events with CEO or emergency 
cursor.execute('''
    SELECT title, priority_level, start_time, created_via
    FROM events 
    WHERE title LIKE '%CEO%' OR title LIKE '%emergency%' OR title LIKE '%Emergency%'
    ORDER BY created_at DESC
''')
events = cursor.fetchall()

print('CEO/Emergency events:')
for event in events:
    print(f'Title: "{event[0]}" | Priority: {event[1]} | Time: {event[2]} | Via: {event[3]}')

conn.close()
