import sqlite3
import os

db_path = os.path.join('..', 'kairocal.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if conflicts table exists
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="conflicts"')
result = cursor.fetchone()

if result:
    print('✅ Conflicts table exists')
    # Get table schema
    cursor.execute('PRAGMA table_info(conflicts)')
    columns = cursor.fetchall()
    print('Conflicts table columns:')
    for col in columns:
        print(f'  - {col[1]} ({col[2]})')
else:
    print('❌ Conflicts table does not exist')

# Check conflict_resolutions table
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="conflict_resolutions"')
result = cursor.fetchone()

if result:
    print('✅ Conflict_resolutions table exists')
else:
    print('❌ Conflict_resolutions table does not exist')

conn.close()
