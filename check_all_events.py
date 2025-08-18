#!/usr/bin/env python3
import sqlite3
from datetime import datetime
import os

def check_database(db_file):
    if os.path.exists(db_file):
        print(f'\n=== Checking {db_file} ===')
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Check if events table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
            if cursor.fetchone():
                cursor.execute('SELECT COUNT(*) FROM events')
                count = cursor.fetchone()[0]
                print(f'Total events: {count}')
                
                if count > 0:
                    # Show recent events
                    cursor.execute('''
                        SELECT id, title, start_time, created_at
                        FROM events 
                        ORDER BY created_at DESC
                        LIMIT 15
                    ''')
                    events = cursor.fetchall()
                    print('Recent events:')
                    for i, event in enumerate(events, 1):
                        created_date = event[3][:10] if event[3] else 'Unknown'
                        start_date = event[2][:10] if event[2] else 'All-day'
                        print(f'  {i}. {event[1]} | Start: {start_date} | Created: {created_date}')
            else:
                print('No events table found')
                
            conn.close()
        except Exception as e:
            print(f'Error: {e}')
    else:
        print(f'{db_file} does not exist')

# Check all possible database files
db_files = [
    'kairocal.db',
    'backend/kairocal.db',
    'backend/kairocal_local.db', 
    'backend/kairocal_fallback.db',
    'backend/calendar_ai.db'
]

for db_file in db_files:
    check_database(db_file)
