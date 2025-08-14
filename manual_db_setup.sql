-- Manual database setup based on Alembic migrations
-- Create proper schema for KairoCal

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cognito_sub VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    preferences JSON,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_users_id ON users(id);

-- Create events table
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    location VARCHAR(255),
    is_all_day BOOLEAN DEFAULT false,
    recurrence_rule VARCHAR(255),
    priority VARCHAR(20), -- For BERT classification
    priority_confidence FLOAT, -- BERT confidence score
    priority_reasoning TEXT, -- BERT explanation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_events_id ON events(id);
CREATE INDEX ix_events_user_id ON events(user_id);
CREATE INDEX ix_events_start_time ON events(start_time);

-- Create reminders table
CREATE TABLE reminders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    minutes_before INTEGER NOT NULL,
    notification_type VARCHAR(50) DEFAULT 'email',
    is_sent BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_reminders_id ON reminders(id);
CREATE INDEX ix_reminders_event_id ON reminders(event_id);

-- Create conflicts table
CREATE TABLE conflicts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event1_id UUID REFERENCES events(id) ON DELETE CASCADE,
    event2_id UUID REFERENCES events(id) ON DELETE CASCADE,
    conflict_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium',
    resolution_suggestion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create alembic version table to indicate migrations are up to date
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

-- Insert the latest migration version
INSERT INTO alembic_version (version_num) VALUES ('20250810_merge_finalize_lineage') ON CONFLICT DO NOTHING;

-- Create a test user for development
INSERT INTO users (email, full_name, cognito_sub) VALUES 
('test@kairocal.com', 'Test User', 'test-user-123') ON CONFLICT DO NOTHING;

SELECT 'Database setup complete!' as status;
