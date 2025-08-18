#!/usr/bin/env python3
import sqlite3
from datetime import datetime

def delete_todays_events():
    db_file = 'backend/kairocal.db'
    today = datetime.now().strftime('%Y-%m-%d')
    
    print(f'Connecting to {db_file}...')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # First, count today's events
    cursor.execute('''
        SELECT COUNT(*) FROM events 
        WHERE date(start_time) = ? OR date(created_at) = ?
    ''', (today, today))
    
    count_before = cursor.fetchone()[0]
    print(f'Found {count_before} events for today ({today})')
    
    if count_before > 0:
        # Show some examples before deletion
        cursor.execute('''
            SELECT id, title, start_time, created_at
            FROM events 
            WHERE date(start_time) = ? OR date(created_at) = ?
            LIMIT 5
        ''', (today, today))
        
        sample_events = cursor.fetchall()
        print('\nSample events to be deleted:')
        for i, event in enumerate(sample_events, 1):
            print(f'  {i}. {event[1]} | Start: {event[2]} | Created: {event[3]}')
        
        if count_before > 5:
            print(f'  ... and {count_before - 5} more events')
        
        # Confirm deletion
        print(f'\nProceeding to delete all {count_before} events from today...')
        
        # Delete today's events
        cursor.execute('''
            DELETE FROM events 
            WHERE date(start_time) = ? OR date(created_at) = ?
        ''', (today, today))
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        # Verify deletion
        cursor.execute('SELECT COUNT(*) FROM events')
        remaining_count = cursor.fetchone()[0]
        
        print(f'\n✅ Successfully deleted {deleted_count} events from today!')
        print(f'Remaining events in database: {remaining_count}')
        
    else:
        print('No events found for today.')
    
    conn.close()

if __name__ == '__main__':
    delete_todays_events()
