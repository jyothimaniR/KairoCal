# backend/migrations/create_conflicts_table.sql
"""
Create conflicts and conflict_resolutions tables for comprehensive conflict tracking
"""

-- Create conflicts table
CREATE TABLE IF NOT EXISTS conflicts (
    id VARCHAR(36) PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id VARCHAR(36) NOT NULL,
    primary_event_id VARCHAR(36),
    conflicting_event_id VARCHAR(36),
    
    -- Conflict metadata
    conflict_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    confidence REAL NOT NULL DEFAULT 0.0,
    impact_score REAL NOT NULL DEFAULT 0.0,
    
    -- Conflict details
    description TEXT,
    conflict_start_time DATETIME,
    conflict_end_time DATETIME,
    overlap_minutes INTEGER,
    buffer_minutes INTEGER DEFAULT 15,
    
    -- BERT Analysis (JSON stored as TEXT in SQLite)
    bert_analysis TEXT,
    priority_analysis TEXT,
    
    -- Resolution tracking
    is_resolved BOOLEAN DEFAULT 0 NOT NULL,
    resolution_method VARCHAR(50),
    resolution_timestamp DATETIME,
    alternative_suggestions TEXT,
    
    -- System metadata
    detection_method VARCHAR(50) DEFAULT 'basic_v1',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (primary_event_id) REFERENCES events(id),
    FOREIGN KEY (conflicting_event_id) REFERENCES events(id)
);

-- Create conflict_resolutions table
CREATE TABLE IF NOT EXISTS conflict_resolutions (
    id VARCHAR(36) PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    conflict_id VARCHAR(36) NOT NULL,
    
    -- Resolution details
    resolution_type VARCHAR(50) NOT NULL,
    old_start_time DATETIME,
    old_end_time DATETIME,
    new_start_time DATETIME,
    new_end_time DATETIME,
    
    -- Success tracking
    was_successful BOOLEAN DEFAULT 0,
    user_accepted BOOLEAN DEFAULT 0,
    auto_applied BOOLEAN DEFAULT 0,
    
    -- Analytics
    resolution_confidence REAL,
    alternatives_offered INTEGER DEFAULT 0,
    user_choice_index INTEGER,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (conflict_id) REFERENCES conflicts(id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_conflicts_user_id ON conflicts(user_id);
CREATE INDEX IF NOT EXISTS idx_conflicts_created_at ON conflicts(created_at);
CREATE INDEX IF NOT EXISTS idx_conflicts_is_resolved ON conflicts(is_resolved);
CREATE INDEX IF NOT EXISTS idx_conflicts_severity ON conflicts(severity);
CREATE INDEX IF NOT EXISTS idx_conflict_resolutions_conflict_id ON conflict_resolutions(conflict_id);

-- Create trigger for updated_at
CREATE TRIGGER IF NOT EXISTS conflicts_updated_at 
    AFTER UPDATE ON conflicts
    FOR EACH ROW
BEGIN
    UPDATE conflicts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

COMMIT;
