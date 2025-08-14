-- Create conflicting test events
INSERT INTO events (
    id, 
    user_id, 
    title, 
    description, 
    start_time, 
    end_time, 
    priority_level, 
    created_via
) VALUES 
-- 3 conflicting events at 3:00 PM
('c0000000-0000-0000-0000-000000000001', '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e', 'Team Meeting', 'Weekly sync meeting', '2025-08-07 15:00:00', '2025-08-07 16:00:00', 2, 'manual'),
('c0000000-0000-0000-0000-000000000002', '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e', 'Client Call', 'Important client discussion', '2025-08-07 15:00:00', '2025-08-07 16:00:00', 1, 'voice'),
('c0000000-0000-0000-0000-000000000003', '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e', 'Code Review', 'Review pull requests', '2025-08-07 15:00:00', '2025-08-07 16:00:00', 3, 'manual'),

-- 2 conflicting events at 12:00 PM
('c0000000-0000-0000-0000-000000000004', '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e', 'Lunch Break', 'Take a break', '2025-08-07 12:00:00', '2025-08-07 13:00:00', 4, 'manual'),
('c0000000-0000-0000-0000-000000000005', '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e', 'Project Planning', 'Plan next sprint', '2025-08-07 12:00:00', '2025-08-07 13:00:00', 2, 'voice'),

-- Some events for busy slots at different times
('c0000000-0000-0000-0000-000000000006', '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e', 'Morning Standup', 'Daily standup', '2025-08-07 09:00:00', '2025-08-07 10:00:00', 3, 'manual'),
('c0000000-0000-0000-0000-000000000007', '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e', 'Afternoon Workshop', 'Training session', '2025-08-07 14:00:00', '2025-08-07 15:00:00', 2, 'manual');
