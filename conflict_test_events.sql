-- Simple SQL to create conflicting events for testing delete functionality
INSERT INTO events (
    id, title, description, start_time, end_time, 
    priority_level, created_via, user_id, created_at, updated_at
) VALUES 
(
    gen_random_uuid(),
    'Team Meeting - Conflict Test 1',
    'First conflicting event for testing delete functionality',
    (NOW() + INTERVAL '2 hours')::timestamp,
    (NOW() + INTERVAL '3 hours')::timestamp,
    2,
    'manual',
    '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e',
    NOW()::timestamp,
    NOW()::timestamp
),
(
    gen_random_uuid(),
    'Project Review - Conflict Test 2',
    'Second conflicting event for testing delete functionality',
    (NOW() + INTERVAL '2 hours')::timestamp,
    (NOW() + INTERVAL '3 hours')::timestamp,
    3,
    'voice',
    '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e',
    NOW()::timestamp,
    NOW()::timestamp
),
(
    gen_random_uuid(),
    'Client Call - Conflict Test 3',
    'Third conflicting event for testing delete functionality',
    (NOW() + INTERVAL '2 hours')::timestamp,
    (NOW() + INTERVAL '3 hours')::timestamp,
    1,
    'manual',
    '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e',
    NOW()::timestamp,
    NOW()::timestamp
);

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
