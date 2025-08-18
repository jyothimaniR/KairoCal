import sqlite3
import os

db_path = os.path.join('..', 'kairocal.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create conflicts table manually
create_conflicts_sql = '''
CREATE TABLE IF NOT EXISTS conflicts (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    primary_event_id VARCHAR(36),
    conflicting_event_id VARCHAR(36),
    conflict_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    confidence REAL NOT NULL DEFAULT 0.0,
    impact_score REAL NOT NULL DEFAULT 0.0,
    description TEXT,
    conflict_start_time DATETIME,
    conflict_end_time DATETIME,
    overlap_minutes INTEGER,
    buffer_minutes INTEGER DEFAULT 15,
    bert_analysis TEXT,
    priority_analysis TEXT,
    is_resolved BOOLEAN DEFAULT 0 NOT NULL,
    resolution_method VARCHAR(50),
    resolution_timestamp DATETIME,
    alternative_suggestions TEXT,
    detection_method VARCHAR(50) DEFAULT 'basic_v1',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
'''

try:
    cursor.execute(create_conflicts_sql)
    print('✅ Created conflicts table')
    
    # Create indexes
    indexes = [
        'CREATE INDEX IF NOT EXISTS idx_conflicts_user_id ON conflicts(user_id)',
        'CREATE INDEX IF NOT EXISTS idx_conflicts_created_at ON conflicts(created_at)',
        'CREATE INDEX IF NOT EXISTS idx_conflicts_is_resolved ON conflicts(is_resolved)',
        'CREATE INDEX IF NOT EXISTS idx_conflicts_severity ON conflicts(severity)'
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
        print(f'✅ Created index: {index_sql.split()[-1]}')
    
    conn.commit()
    print('✅ All changes committed')
    
except Exception as e:
    print(f'❌ Error: {e}')
    
finally:
    conn.close()
