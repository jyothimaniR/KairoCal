-- Create conflicting test events directly in PostgreSQL
-- Run this with: docker exec -i kairocal_postgres psql -U kairocal_user -d kairocal < create_conflict_events.sql

-- Generate UUIDs and timestamps for the test events
DO $$
DECLARE
    test_user_id UUID := '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e';
    conflict_time TIMESTAMP := (NOW() + INTERVAL '2 hours')::timestamp;
    event_id_1 UUID := gen_random_uuid();
    event_id_2 UUID := gen_random_uuid();
    event_id_3 UUID := gen_random_uuid();
    current_time TIMESTAMP := NOW()::timestamp;
BEGIN
    -- Insert first conflicting event
    INSERT INTO events (
        id, title, description, start_time, end_time, 
        priority_level, created_via, user_id, created_at, updated_at
    ) VALUES (
        event_id_1,
        'Team Meeting - Conflict Test 1',
        'First conflicting event for testing delete functionality',
        conflict_time,
        (conflict_time + INTERVAL '1 hour')::timestamp,
        2,
        'manual',
        test_user_id,
        current_time,
        current_time
    );
    
    -- Insert second conflicting event (same time)
    INSERT INTO events (
        id, title, description, start_time, end_time, 
        priority_level, created_via, user_id, created_at, updated_at
    ) VALUES (
        event_id_2,
        'Project Review - Conflict Test 2',
        'Second conflicting event for testing delete functionality',
        conflict_time,
        (conflict_time + INTERVAL '1 hour')::timestamp,
        3,
        'voice',
        test_user_id,
        current_time,
        current_time
    );
    
    -- Insert third conflicting event (same time)
    INSERT INTO events (
        id, title, description, start_time, end_time, 
        priority_level, created_via, user_id, created_at, updated_at
    ) VALUES (
        event_id_3,
        'Client Call - Conflict Test 3',
        'Third conflicting event for testing delete functionality',
        conflict_time,
        (conflict_time + INTERVAL '1 hour')::timestamp,
        1,
        'manual',
        test_user_id,
        current_time,
        current_time
    );
    
    -- Show created events
    RAISE NOTICE 'Created 3 conflicting events at time: %', conflict_time;
END $$;

-- Verify the events were created
SELECT 
    id,
    title,
    start_time,
    priority_level,
    created_via
FROM events 
WHERE title LIKE '%Conflict Test%' 
ORDER BY created_at DESC;
