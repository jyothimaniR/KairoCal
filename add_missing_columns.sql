-- Add priority classification fields to events table
ALTER TABLE events ADD COLUMN IF NOT EXISTS priority_level INTEGER NOT NULL DEFAULT 3;
ALTER TABLE events ADD COLUMN IF NOT EXISTS priority_confidence REAL NOT NULL DEFAULT 0.0;
ALTER TABLE events ADD COLUMN IF NOT EXISTS classification_method VARCHAR(50) NOT NULL DEFAULT 'manual';

-- Add analytics fields that might be missing
ALTER TABLE events ADD COLUMN IF NOT EXISTS meeting_outcome VARCHAR(50) NOT NULL DEFAULT 'neutral';
ALTER TABLE events ADD COLUMN IF NOT EXISTS effectiveness_rating INTEGER NOT NULL DEFAULT 3;
ALTER TABLE events ADD COLUMN IF NOT EXISTS energy_level INTEGER NOT NULL DEFAULT 3;
ALTER TABLE events ADD COLUMN IF NOT EXISTS created_via VARCHAR(20) NOT NULL DEFAULT 'manual';
ALTER TABLE events ADD COLUMN IF NOT EXISTS actual_duration INTEGER;
ALTER TABLE events ADD COLUMN IF NOT EXISTS planned_duration INTEGER;

-- Create indexes
CREATE INDEX IF NOT EXISTS ix_events_priority_level ON events (priority_level);

-- Verify columns exist
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'events' 
ORDER BY ordinal_position;
