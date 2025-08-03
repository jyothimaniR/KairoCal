-- Simple Analytics Demo Data
-- Users

INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
VALUES ('77ed786d-c179-4325-aec8-9a45b8f2c19e', 'demo_user_001', 'sarah.chen@company.com', 'Sarah Chen', 
        '{"demo": true}', true, now(), now())
ON CONFLICT (cognito_sub) DO UPDATE SET 
    email = EXCLUDED.email, full_name = EXCLUDED.full_name, updated_at = now();


INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
VALUES ('72ce59cc-7ce3-4639-9733-70624cf90ab1', 'demo_user_002', 'marcus.rodriguez@company.com', 'Marcus Rodriguez', 
        '{"demo": true}', true, now(), now())
ON CONFLICT (cognito_sub) DO UPDATE SET 
    email = EXCLUDED.email, full_name = EXCLUDED.full_name, updated_at = now();


INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
VALUES ('f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'demo_user_003', 'emily.watson@company.com', 'Emily Watson', 
        '{"demo": true}', true, now(), now())
ON CONFLICT (cognito_sub) DO UPDATE SET 
    email = EXCLUDED.email, full_name = EXCLUDED.full_name, updated_at = now();


-- Events

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '08a07f50-3c97-41bb-9e28-15c2a4cc51b0', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-06-09T12:30:00', '2025-06-09T14:30:00', 'Conference Room',
    false, null, 'neutral', 3, 3, 'text',
    119, 110, '2025-06-09T12:30:00', '2025-06-09T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e3054a53-7b39-44ca-b2bc-70722ffbd50f', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-06-08T16:15:00', '2025-06-08T17:15:00', 'Conference Room',
    false, null, 'productive', 5, 4, 'imported',
    76, 51, '2025-06-08T16:15:00', '2025-06-08T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8fed8807-7020-4606-9120-7c1456bcffce', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-06-11T13:45:00', '2025-06-11T14:30:00', 'Conference Room',
    false, null, 'neutral', 3, 5, 'text',
    55, 36, '2025-06-11T13:45:00', '2025-06-11T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd0be0d2e-bf55-48f0-9329-7cc73934a861', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'All Hands', 'Demo analytics data',
    '2025-06-08T16:00:00', '2025-06-08T16:30:00', 'Conference Room',
    false, null, 'waste', 2, 3, 'manual',
    38, 37, '2025-06-08T16:00:00', '2025-06-08T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2b6138bb-3de5-4769-a566-dff8e9c38c35', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-06-09T12:45:00', '2025-06-09T13:45:00', 'Conference Room',
    false, null, 'neutral', 4, 4, 'imported',
    75, 57, '2025-06-09T12:45:00', '2025-06-09T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '894b5582-d8aa-4de8-86d8-c91e1183b668', '77ed786d-c179-4325-aec8-9a45b8f2c19e', '1:1 Check-in', 'Demo analytics data',
    '2025-06-08T14:30:00', '2025-06-08T16:00:00', 'Conference Room',
    false, null, 'waste', 2, 2, 'manual',
    106, 98, '2025-06-08T14:30:00', '2025-06-08T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f4c7fcae-4a7f-4ca8-813f-e6b76506d25f', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Team Meeting', 'Demo analytics data',
    '2025-06-07T14:00:00', '2025-06-07T14:30:00', 'Conference Room',
    false, null, 'neutral', 1, 3, 'manual',
    45, 15, '2025-06-07T14:00:00', '2025-06-07T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '51b8a557-0e8f-4c14-8d34-757c77ecddc2', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-06-07T16:00:00', '2025-06-07T17:00:00', 'Conference Room',
    false, null, 'neutral', 4, 2, 'manual',
    62, 51, '2025-06-07T16:00:00', '2025-06-07T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '55af8137-852f-4621-a057-f9e940d0c7d7', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-06-13T13:00:00', '2025-06-13T13:30:00', 'Conference Room',
    false, null, 'waste', 1, 1, 'imported',
    31, 17, '2025-06-13T13:00:00', '2025-06-13T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e700dcf8-def8-4998-b068-4e5049f9712b', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-06-08T14:15:00', '2025-06-08T14:45:00', 'Conference Room',
    false, null, 'productive', 5, 1, 'text',
    34, 18, '2025-06-08T14:15:00', '2025-06-08T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7fecf6cd-1d51-4340-af73-97e0fc414a03', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Client Call', 'Demo analytics data',
    '2025-06-15T17:30:00', '2025-06-15T18:15:00', 'Conference Room',
    false, null, 'waste', 4, 5, 'manual',
    45, 49, '2025-06-15T17:30:00', '2025-06-15T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e9d180e4-30a9-4713-869a-1eb99cedd875', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-06-19T16:15:00', '2025-06-19T17:00:00', 'Conference Room',
    false, null, 'productive', 4, 5, 'voice',
    45, 32, '2025-06-19T16:15:00', '2025-06-19T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '73f41078-ac92-4508-bd68-bf13936084b9', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'All Hands', 'Demo analytics data',
    '2025-06-17T11:30:00', '2025-06-17T13:00:00', 'Conference Room',
    false, null, 'neutral', 5, 3, 'text',
    91, 85, '2025-06-17T11:30:00', '2025-06-17T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0e6f1dd9-6e3c-4e58-8500-5ee92ef597f9', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-06-19T14:00:00', '2025-06-19T15:00:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'imported',
    71, 75, '2025-06-19T14:00:00', '2025-06-19T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ea53e250-2416-40a4-85bd-36fe4e022d6c', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-06-18T14:45:00', '2025-06-18T16:15:00', 'Conference Room',
    false, null, 'productive', 1, 2, 'manual',
    95, 103, '2025-06-18T14:45:00', '2025-06-18T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ee9235c9-2c7d-4712-a35e-67f6989c9385', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-06-15T17:00:00', '2025-06-15T18:30:00', 'Conference Room',
    false, null, 'neutral', 3, 4, 'text',
    95, 89, '2025-06-15T17:00:00', '2025-06-15T17:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b55327f2-ab63-495c-a631-56bbb30bac94', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-06-16T17:15:00', '2025-06-16T18:00:00', 'Conference Room',
    false, null, 'waste', 1, 3, 'manual',
    41, 36, '2025-06-16T17:15:00', '2025-06-16T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b2ff6fa8-e517-4ca9-974e-6f8e79541958', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-06-16T11:15:00', '2025-06-16T12:45:00', 'Conference Room',
    false, null, 'waste', 4, 4, 'manual',
    100, 78, '2025-06-16T11:15:00', '2025-06-16T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ca7a3aa2-bd4b-43e5-88da-0ba1ce099877', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Team Meeting', 'Demo analytics data',
    '2025-06-15T09:30:00', '2025-06-15T10:00:00', 'Conference Room',
    false, null, 'waste', 5, 1, 'manual',
    36, 23, '2025-06-15T09:30:00', '2025-06-15T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0e29e459-f322-422d-b5a9-1a5c6c9535b3', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-06-16T12:30:00', '2025-06-16T14:00:00', 'Conference Room',
    false, null, 'neutral', 2, 3, 'voice',
    102, 98, '2025-06-16T12:30:00', '2025-06-16T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6379c6cb-4098-4925-a3a8-e0707cab4816', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-06-21T14:00:00', '2025-06-21T15:30:00', 'Conference Room',
    false, null, 'neutral', 1, 4, 'manual',
    100, 84, '2025-06-21T14:00:00', '2025-06-21T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'bdbd33d4-59c5-4610-8da3-3671f2208ab4', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-06-24T08:30:00', '2025-06-24T10:30:00', 'Conference Room',
    false, null, 'waste', 5, 1, 'text',
    133, 108, '2025-06-24T08:30:00', '2025-06-24T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7c64e952-7b2a-45cb-9b58-68cbc23c4d3b', '77ed786d-c179-4325-aec8-9a45b8f2c19e', '1:1 Check-in', 'Demo analytics data',
    '2025-06-26T08:15:00', '2025-06-26T09:00:00', 'Conference Room',
    false, null, 'waste', 2, 3, 'voice',
    43, 51, '2025-06-26T08:15:00', '2025-06-26T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8978a909-cc14-4ee5-ae37-fb5b4c21e81b', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-06-26T08:45:00', '2025-06-26T09:15:00', 'Conference Room',
    false, null, 'productive', 1, 5, 'text',
    21, 33, '2025-06-26T08:45:00', '2025-06-26T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '36bf6f2f-fca6-4a06-98a5-600408918fdc', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'All Hands', 'Demo analytics data',
    '2025-06-26T16:30:00', '2025-06-26T17:00:00', 'Conference Room',
    false, null, 'productive', 4, 1, 'manual',
    46, 29, '2025-06-26T16:30:00', '2025-06-26T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5301b192-6f1b-4f17-98b5-c890b4704506', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-06-25T16:15:00', '2025-06-25T18:15:00', 'Conference Room',
    false, null, 'neutral', 3, 4, 'voice',
    121, 113, '2025-06-25T16:15:00', '2025-06-25T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1bba2aee-fcf5-4879-9c5b-a43981a70c3d', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-06-21T13:45:00', '2025-06-21T14:15:00', 'Conference Room',
    false, null, 'productive', 5, 5, 'text',
    31, 32, '2025-06-21T13:45:00', '2025-06-21T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '80771846-3b01-4263-ae4f-e3a8eaf8d931', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-06-21T08:45:00', '2025-06-21T09:15:00', 'Conference Room',
    false, null, 'productive', 3, 2, 'imported',
    45, 41, '2025-06-21T08:45:00', '2025-06-21T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3b8b2a71-5138-4843-82eb-dd5d82ab56da', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Team Meeting', 'Demo analytics data',
    '2025-06-22T10:45:00', '2025-06-22T11:30:00', 'Conference Room',
    false, null, 'neutral', 1, 4, 'voice',
    59, 52, '2025-06-22T10:45:00', '2025-06-22T10:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2584b898-a732-41dc-b290-6ab8bfdc8958', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-06-22T16:15:00', '2025-06-22T17:15:00', 'Conference Room',
    false, null, 'neutral', 4, 2, 'manual',
    53, 64, '2025-06-22T16:15:00', '2025-06-22T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e6156fd2-e07c-4c8a-90ea-12a12d73742e', '77ed786d-c179-4325-aec8-9a45b8f2c19e', '1:1 Check-in', 'Demo analytics data',
    '2025-06-25T11:45:00', '2025-06-25T12:45:00', 'Conference Room',
    false, null, 'neutral', 1, 5, 'imported',
    57, 57, '2025-06-25T11:45:00', '2025-06-25T11:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '00fd377f-ce6b-4678-8c9e-9f73f446457f', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-06-21T13:45:00', '2025-06-21T15:15:00', 'Conference Room',
    false, null, 'neutral', 5, 3, 'voice',
    87, 90, '2025-06-21T13:45:00', '2025-06-21T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a5153c8d-c397-41f5-9fed-9f3719036dd5', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Client Call', 'Demo analytics data',
    '2025-06-29T13:15:00', '2025-06-29T13:45:00', 'Conference Room',
    false, null, 'productive', 4, 3, 'manual',
    39, 18, '2025-06-29T13:15:00', '2025-06-29T13:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7472b1c2-9f00-46b6-b10c-f3c3cabb67e6', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-07-01T16:15:00', '2025-07-01T18:15:00', 'Conference Room',
    false, null, 'waste', 1, 3, 'manual',
    119, 120, '2025-07-01T16:15:00', '2025-07-01T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '47890e70-6696-490b-a1c5-4508ecafb9e9', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'All Hands', 'Demo analytics data',
    '2025-06-30T14:00:00', '2025-06-30T14:45:00', 'Conference Room',
    false, null, 'waste', 2, 1, 'imported',
    44, 57, '2025-06-30T14:00:00', '2025-06-30T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2bb74ab3-d5f6-4b97-8edc-44d16ac31da7', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-06-28T10:15:00', '2025-06-28T11:15:00', 'Conference Room',
    false, null, 'neutral', 2, 1, 'manual',
    76, 72, '2025-06-28T10:15:00', '2025-06-28T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e65ae846-80ac-41c6-a815-af11d577b676', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-06-28T10:00:00', '2025-06-28T11:30:00', 'Conference Room',
    false, null, 'waste', 3, 4, 'manual',
    93, 97, '2025-06-28T10:00:00', '2025-06-28T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '770a6dde-814e-447c-8ec2-3c233dec0e49', '77ed786d-c179-4325-aec8-9a45b8f2c19e', '1:1 Check-in', 'Demo analytics data',
    '2025-07-01T15:15:00', '2025-07-01T16:15:00', 'Conference Room',
    false, null, 'neutral', 3, 2, 'imported',
    71, 72, '2025-07-01T15:15:00', '2025-07-01T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '14d50709-3810-427d-9dbf-728f358343c7', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-07-02T10:00:00', '2025-07-02T11:30:00', 'Conference Room',
    false, null, 'waste', 2, 2, 'voice',
    80, 87, '2025-07-02T10:00:00', '2025-07-02T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '745b2d0d-2b2f-4987-ab4f-31ab2ca0ba56', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-02T15:30:00', '2025-07-02T17:00:00', 'Conference Room',
    false, null, 'neutral', 3, 3, 'voice',
    94, 80, '2025-07-02T15:30:00', '2025-07-02T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7fd786f7-113b-46ef-b708-1173866e81a4', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-07-08T09:45:00', '2025-07-08T10:45:00', 'Conference Room',
    false, null, 'waste', 4, 5, 'text',
    66, 66, '2025-07-08T09:45:00', '2025-07-08T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2400017e-9db1-4934-a472-babc5c282d6d', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-07-11T10:30:00', '2025-07-11T11:00:00', 'Conference Room',
    false, null, 'productive', 1, 4, 'manual',
    28, 33, '2025-07-11T10:30:00', '2025-07-11T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'df7ede03-0476-463b-902b-d4f4c15402aa', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-07-08T11:30:00', '2025-07-08T12:15:00', 'Conference Room',
    false, null, 'neutral', 5, 5, 'imported',
    39, 60, '2025-07-08T11:30:00', '2025-07-08T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '00ffdccb-f231-4630-832c-9307293f220d', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-07-05T12:30:00', '2025-07-05T13:00:00', 'Conference Room',
    false, null, 'productive', 5, 4, 'voice',
    23, 31, '2025-07-05T12:30:00', '2025-07-05T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '81112590-c0ce-4efb-bb7f-06a43bfb769f', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Client Call', 'Demo analytics data',
    '2025-07-09T16:00:00', '2025-07-09T16:45:00', 'Conference Room',
    false, null, 'waste', 2, 1, 'text',
    62, 57, '2025-07-09T16:00:00', '2025-07-09T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a73fde31-4858-49ad-9eb4-2b7650a94ed3', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Client Call', 'Demo analytics data',
    '2025-07-07T08:45:00', '2025-07-07T10:45:00', 'Conference Room',
    false, null, 'neutral', 2, 2, 'voice',
    123, 114, '2025-07-07T08:45:00', '2025-07-07T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '13269dee-5b12-4855-80cb-8892e80fc2cd', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Team Meeting', 'Demo analytics data',
    '2025-07-08T12:45:00', '2025-07-08T13:30:00', 'Conference Room',
    false, null, 'neutral', 1, 2, 'imported',
    38, 54, '2025-07-08T12:45:00', '2025-07-08T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '4c7695d2-be3c-4584-ab06-47dde9aefd68', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Team Meeting', 'Demo analytics data',
    '2025-07-06T11:30:00', '2025-07-06T12:15:00', 'Conference Room',
    false, null, 'neutral', 5, 1, 'voice',
    45, 41, '2025-07-06T11:30:00', '2025-07-06T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'aa87b809-2d09-42ac-b204-809c41d86222', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Client Call', 'Demo analytics data',
    '2025-07-16T16:45:00', '2025-07-16T17:45:00', 'Conference Room',
    false, null, 'neutral', 4, 2, 'imported',
    76, 51, '2025-07-16T16:45:00', '2025-07-16T16:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '114769ec-bd08-49b7-a442-b110fa06b098', '77ed786d-c179-4325-aec8-9a45b8f2c19e', '1:1 Check-in', 'Demo analytics data',
    '2025-07-17T15:45:00', '2025-07-17T16:30:00', 'Conference Room',
    false, null, 'neutral', 1, 4, 'manual',
    51, 46, '2025-07-17T15:45:00', '2025-07-17T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f6207199-d521-4ab9-96ee-084f49bd7554', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'All Hands', 'Demo analytics data',
    '2025-07-15T12:30:00', '2025-07-15T14:00:00', 'Conference Room',
    false, null, 'productive', 2, 5, 'voice',
    103, 103, '2025-07-15T12:30:00', '2025-07-15T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f35eaf44-ca65-43f7-b310-ad3fbae51fde', '77ed786d-c179-4325-aec8-9a45b8f2c19e', '1:1 Check-in', 'Demo analytics data',
    '2025-07-12T09:00:00', '2025-07-12T10:30:00', 'Conference Room',
    false, null, 'neutral', 4, 4, 'imported',
    101, 80, '2025-07-12T09:00:00', '2025-07-12T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '57364563-ca0a-48f3-b1e6-277bfb03add2', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-07-12T14:30:00', '2025-07-12T16:30:00', 'Conference Room',
    false, null, 'waste', 4, 1, 'imported',
    115, 122, '2025-07-12T14:30:00', '2025-07-12T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c2e9a034-0b0a-4d9e-b448-0f5191c5dd46', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-13T14:45:00', '2025-07-13T16:45:00', 'Conference Room',
    false, null, 'productive', 4, 3, 'imported',
    124, 132, '2025-07-13T14:45:00', '2025-07-13T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2e52038a-9f64-47e3-8ee8-6c38599ba97d', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-07-16T15:30:00', '2025-07-16T17:30:00', 'Conference Room',
    false, null, 'waste', 3, 3, 'imported',
    130, 121, '2025-07-16T15:30:00', '2025-07-16T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '470e7ed7-795a-4ce9-b939-c85b5d592fdf', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Team Meeting', 'Demo analytics data',
    '2025-07-12T11:30:00', '2025-07-12T12:15:00', 'Conference Room',
    false, null, 'neutral', 2, 1, 'text',
    53, 60, '2025-07-12T11:30:00', '2025-07-12T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f251a6bd-94ac-4b8e-89a6-cf6126000a24', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'All Hands', 'Demo analytics data',
    '2025-07-12T14:45:00', '2025-07-12T16:45:00', 'Conference Room',
    false, null, 'productive', 4, 2, 'imported',
    125, 118, '2025-07-12T14:45:00', '2025-07-12T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '011afeb8-fdb7-4513-96ae-bf40366f9ccb', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-14T09:45:00', '2025-07-14T10:15:00', 'Conference Room',
    false, null, 'productive', 4, 5, 'imported',
    49, 16, '2025-07-14T09:45:00', '2025-07-14T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9ca0634b-c4dd-4916-bda2-a7649047fb35', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Client Call', 'Demo analytics data',
    '2025-07-24T11:45:00', '2025-07-24T12:30:00', 'Conference Room',
    false, null, 'productive', 2, 1, 'text',
    43, 36, '2025-07-24T11:45:00', '2025-07-24T11:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a76b2f1f-b110-4cc9-ae8a-6798ed17cbca', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'All Hands', 'Demo analytics data',
    '2025-07-22T14:15:00', '2025-07-22T14:45:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'manual',
    31, 29, '2025-07-22T14:15:00', '2025-07-22T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b508c0be-b179-413d-acf2-b470d9f46613', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-07-19T12:00:00', '2025-07-19T12:30:00', 'Conference Room',
    false, null, 'neutral', 4, 5, 'voice',
    20, 20, '2025-07-19T12:00:00', '2025-07-19T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'befa47ec-278c-4f56-b4e2-3ceb703ee338', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-21T09:15:00', '2025-07-21T10:00:00', 'Conference Room',
    false, null, 'neutral', 4, 3, 'voice',
    40, 38, '2025-07-21T09:15:00', '2025-07-21T09:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e397aaee-86bb-4ab2-9255-9d9de7b38e20', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Brainstorm', 'Demo analytics data',
    '2025-07-21T08:15:00', '2025-07-21T09:15:00', 'Conference Room',
    false, null, 'productive', 1, 5, 'imported',
    65, 53, '2025-07-21T08:15:00', '2025-07-21T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '311c0550-511d-4735-bc97-27dfbdaeabae', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-07-23T13:45:00', '2025-07-23T14:15:00', 'Conference Room',
    false, null, 'productive', 5, 1, 'manual',
    40, 15, '2025-07-23T13:45:00', '2025-07-23T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9f1b0c2a-c90f-4f27-a5d9-5bd37ce4a7f3', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-22T12:30:00', '2025-07-22T14:30:00', 'Conference Room',
    false, null, 'productive', 5, 3, 'manual',
    118, 129, '2025-07-22T12:30:00', '2025-07-22T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c0c97748-2f3d-499a-bc18-e39bd0bff33b', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-21T15:15:00', '2025-07-21T16:15:00', 'Conference Room',
    false, null, 'neutral', 3, 4, 'manual',
    77, 71, '2025-07-21T15:15:00', '2025-07-21T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '03e12195-46d2-4e90-996c-ad1e5770611c', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-19T12:15:00', '2025-07-19T13:45:00', 'Conference Room',
    false, null, 'neutral', 4, 3, 'imported',
    99, 105, '2025-07-19T12:15:00', '2025-07-19T12:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ad513ebb-4334-44d6-a79b-e3cd31684808', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Client Call', 'Demo analytics data',
    '2025-07-26T08:15:00', '2025-07-26T09:00:00', 'Conference Room',
    false, null, 'waste', 4, 2, 'voice',
    62, 41, '2025-07-26T08:15:00', '2025-07-26T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a3dd99c6-87a3-4e7f-9c12-0d65ef6b1522', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-30T17:45:00', '2025-07-30T19:15:00', 'Conference Room',
    false, null, 'waste', 2, 1, 'text',
    94, 98, '2025-07-30T17:45:00', '2025-07-30T17:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '77109aca-be14-470b-a6d5-bc5015c07c53', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Project Review', 'Demo analytics data',
    '2025-07-26T17:30:00', '2025-07-26T19:00:00', 'Conference Room',
    false, null, 'waste', 5, 5, 'manual',
    81, 80, '2025-07-26T17:30:00', '2025-07-26T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '55ef06e7-cb75-4704-a435-8245497e3db7', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-07-26T16:15:00', '2025-07-26T17:45:00', 'Conference Room',
    false, null, 'neutral', 4, 2, 'voice',
    90, 76, '2025-07-26T16:15:00', '2025-07-26T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1c11b2fd-6855-44af-9391-ff5e8c4fc5df', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-07-26T08:00:00', '2025-07-26T08:30:00', 'Conference Room',
    false, null, 'productive', 4, 3, 'voice',
    27, 29, '2025-07-26T08:00:00', '2025-07-26T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '18a27f17-0b45-48cc-aa0d-567da2de4e3d', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Training', 'Demo analytics data',
    '2025-07-26T16:45:00', '2025-07-26T18:45:00', 'Conference Room',
    false, null, 'productive', 4, 2, 'voice',
    122, 119, '2025-07-26T16:45:00', '2025-07-26T16:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '81c4d6e3-3a2f-4459-8e3c-aea5d13b0079', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Team Meeting', 'Demo analytics data',
    '2025-07-27T09:30:00', '2025-07-27T10:30:00', 'Conference Room',
    false, null, 'productive', 3, 5, 'voice',
    72, 68, '2025-07-27T09:30:00', '2025-07-27T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a7d3c660-84e0-406f-9d43-6632f296da7e', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Client Call', 'Demo analytics data',
    '2025-07-27T15:45:00', '2025-07-27T17:15:00', 'Conference Room',
    false, null, 'waste', 2, 1, 'manual',
    89, 104, '2025-07-27T15:45:00', '2025-07-27T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '724bb103-fff8-4204-9d24-7590c24166f8', '77ed786d-c179-4325-aec8-9a45b8f2c19e', 'Planning Session', 'Demo analytics data',
    '2025-07-30T12:15:00', '2025-07-30T13:15:00', 'Conference Room',
    false, null, 'waste', 5, 4, 'voice',
    59, 51, '2025-07-30T12:15:00', '2025-07-30T12:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd641d99f-63f7-4821-a8c0-6eb637c5df02', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-06-09T15:00:00', '2025-06-09T15:30:00', 'Conference Room',
    false, null, 'productive', 1, 4, 'manual',
    23, 41, '2025-06-09T15:00:00', '2025-06-09T15:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6163399a-6a02-4916-bef6-e041b140c061', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-06-10T10:15:00', '2025-06-10T12:15:00', 'Conference Room',
    false, null, 'waste', 4, 5, 'voice',
    137, 133, '2025-06-10T10:15:00', '2025-06-10T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1229b8e6-307d-4ce4-a6f6-7fb611aa51b3', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-06-11T13:30:00', '2025-06-11T15:00:00', 'Conference Room',
    false, null, 'neutral', 3, 2, 'text',
    80, 103, '2025-06-11T13:30:00', '2025-06-11T13:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b2bbd925-f2ae-4062-ab5d-952cff86ba9c', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-06-08T16:00:00', '2025-06-08T18:00:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'manual',
    119, 116, '2025-06-08T16:00:00', '2025-06-08T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6f93e232-b343-459d-8558-2773d5f53b83', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-06-11T09:30:00', '2025-06-11T11:30:00', 'Conference Room',
    false, null, 'waste', 3, 1, 'manual',
    127, 128, '2025-06-11T09:30:00', '2025-06-11T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '58dbeda5-c57a-4bcf-9741-fceb9bc35226', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-06-12T09:00:00', '2025-06-12T10:30:00', 'Conference Room',
    false, null, 'waste', 1, 5, 'text',
    93, 99, '2025-06-12T09:00:00', '2025-06-12T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '691ff11f-8f1b-458f-b78e-356788ade01c', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-06-08T14:45:00', '2025-06-08T16:15:00', 'Conference Room',
    false, null, 'waste', 4, 1, 'text',
    85, 100, '2025-06-08T14:45:00', '2025-06-08T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd0012310-4326-4260-afd6-dff372f4509a', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-06-11T14:15:00', '2025-06-11T15:00:00', 'Conference Room',
    false, null, 'waste', 2, 2, 'imported',
    63, 43, '2025-06-11T14:15:00', '2025-06-11T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '198d0a2e-882a-4a4b-91f2-0386498ed04e', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-06-11T14:45:00', '2025-06-11T16:45:00', 'Conference Room',
    false, null, 'neutral', 5, 4, 'text',
    127, 114, '2025-06-11T14:45:00', '2025-06-11T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '64bde3a6-cba6-461d-8b69-7087f9830ea2', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Project Review', 'Demo analytics data',
    '2025-06-15T16:15:00', '2025-06-15T17:15:00', 'Conference Room',
    false, null, 'neutral', 4, 4, 'text',
    55, 52, '2025-06-15T16:15:00', '2025-06-15T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a09e1ee1-2392-4303-970f-0f54eb16bbfc', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-06-15T13:45:00', '2025-06-15T15:15:00', 'Conference Room',
    false, null, 'productive', 5, 5, 'text',
    91, 92, '2025-06-15T13:45:00', '2025-06-15T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fba8f597-6007-4907-9188-18117cfcfe67', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Project Review', 'Demo analytics data',
    '2025-06-14T09:15:00', '2025-06-14T11:15:00', 'Conference Room',
    false, null, 'neutral', 2, 1, 'text',
    132, 116, '2025-06-14T09:15:00', '2025-06-14T09:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6cb69b1a-07d4-4d05-9b30-8767847cc4c9', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Project Review', 'Demo analytics data',
    '2025-06-17T10:30:00', '2025-06-17T11:15:00', 'Conference Room',
    false, null, 'productive', 2, 4, 'text',
    65, 60, '2025-06-17T10:30:00', '2025-06-17T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '46fc33c2-352c-4e11-ab35-31c6125dabf6', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-06-17T12:45:00', '2025-06-17T14:45:00', 'Conference Room',
    false, null, 'neutral', 1, 5, 'voice',
    120, 133, '2025-06-17T12:45:00', '2025-06-17T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8e354385-6571-4226-aa83-a34d8efb15f8', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-06-14T11:00:00', '2025-06-14T13:00:00', 'Conference Room',
    false, null, 'productive', 2, 1, 'manual',
    123, 119, '2025-06-14T11:00:00', '2025-06-14T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0c8033a4-4ba1-4a68-a4fa-2b4e3ee8d732', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-06-15T10:45:00', '2025-06-15T11:15:00', 'Conference Room',
    false, null, 'neutral', 2, 5, 'text',
    33, 22, '2025-06-15T10:45:00', '2025-06-15T10:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9f167108-f4dd-4aea-a272-f1af3cc389a9', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-06-14T17:45:00', '2025-06-14T18:30:00', 'Conference Room',
    false, null, 'waste', 1, 1, 'manual',
    41, 30, '2025-06-14T17:45:00', '2025-06-14T17:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f5e265c9-c668-4d2f-afcc-fa6725108e70', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-06-18T09:00:00', '2025-06-18T11:00:00', 'Conference Room',
    false, null, 'waste', 1, 1, 'voice',
    122, 130, '2025-06-18T09:00:00', '2025-06-18T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'cca2c47b-7737-43a6-be3a-e274f0c990ec', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-06-15T10:30:00', '2025-06-15T11:00:00', 'Conference Room',
    false, null, 'waste', 5, 2, 'voice',
    45, 22, '2025-06-15T10:30:00', '2025-06-15T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7b5b4ce2-2404-42e5-8821-44eaf39bfce3', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-06-19T16:00:00', '2025-06-19T17:30:00', 'Conference Room',
    false, null, 'waste', 2, 3, 'voice',
    85, 87, '2025-06-19T16:00:00', '2025-06-19T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fe661d4c-934c-479b-9e1b-5def402c041b', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-06-23T13:00:00', '2025-06-23T14:00:00', 'Conference Room',
    false, null, 'waste', 3, 5, 'imported',
    53, 49, '2025-06-23T13:00:00', '2025-06-23T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'bf2537e9-79a5-4b4c-ae91-e8d312c203df', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-06-23T13:45:00', '2025-06-23T15:45:00', 'Conference Room',
    false, null, 'waste', 1, 3, 'voice',
    137, 107, '2025-06-23T13:45:00', '2025-06-23T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '59f65f7a-f0bf-4474-b64c-9647c2fbacee', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-06-22T08:30:00', '2025-06-22T10:00:00', 'Conference Room',
    false, null, 'neutral', 4, 1, 'manual',
    94, 88, '2025-06-22T08:30:00', '2025-06-22T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '130a1b5d-7ee4-4061-9b00-557d1f2a69ae', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-06-27T11:15:00', '2025-06-27T12:15:00', 'Conference Room',
    false, null, 'waste', 4, 4, 'voice',
    62, 51, '2025-06-27T11:15:00', '2025-06-27T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b7486a98-3aad-4c83-9d88-4ff9e7c057d2', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-06-23T09:00:00', '2025-06-23T10:30:00', 'Conference Room',
    false, null, 'productive', 1, 3, 'imported',
    83, 87, '2025-06-23T09:00:00', '2025-06-23T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '95432420-7f56-4c40-9921-802036f4a530', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-06-27T16:15:00', '2025-06-27T18:15:00', 'Conference Room',
    false, null, 'neutral', 3, 2, 'voice',
    138, 119, '2025-06-27T16:15:00', '2025-06-27T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '187f8bb8-00ac-4404-b917-371a8709675e', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Project Review', 'Demo analytics data',
    '2025-06-26T15:30:00', '2025-06-26T16:30:00', 'Conference Room',
    false, null, 'neutral', 4, 1, 'voice',
    80, 72, '2025-06-26T15:30:00', '2025-06-26T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'eff8cdea-61c8-46bd-99b3-a53c8b5154e8', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-06-25T10:00:00', '2025-06-25T12:00:00', 'Conference Room',
    false, null, 'neutral', 1, 3, 'imported',
    139, 129, '2025-06-25T10:00:00', '2025-06-25T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8542d45a-5e16-46c9-93ad-a032f6300e6d', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-06-21T13:45:00', '2025-06-21T15:15:00', 'Conference Room',
    false, null, 'waste', 3, 3, 'voice',
    106, 81, '2025-06-21T13:45:00', '2025-06-21T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9ca20cf2-4e8a-476b-9b60-a8371982f746', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-06-21T12:30:00', '2025-06-21T14:00:00', 'Conference Room',
    false, null, 'waste', 5, 4, 'text',
    99, 93, '2025-06-21T12:30:00', '2025-06-21T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3031de2e-9826-43a3-be5c-9e855fa4d1a4', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-06-21T17:30:00', '2025-06-21T18:00:00', 'Conference Room',
    false, null, 'waste', 1, 1, 'text',
    27, 40, '2025-06-21T17:30:00', '2025-06-21T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '73d12f7a-47c3-4eec-a2b1-45bf30bcf5bb', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-06-29T11:45:00', '2025-06-29T12:15:00', 'Conference Room',
    false, null, 'waste', 4, 5, 'text',
    46, 33, '2025-06-29T11:45:00', '2025-06-29T11:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '4d2161a4-0ea3-4c62-8148-97b914bba259', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-06-30T10:30:00', '2025-06-30T12:30:00', 'Conference Room',
    false, null, 'productive', 2, 1, 'voice',
    119, 123, '2025-06-30T10:30:00', '2025-06-30T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f3485cb6-9968-403b-a79a-3fe4b5540dd3', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-07-03T17:00:00', '2025-07-03T18:30:00', 'Conference Room',
    false, null, 'productive', 3, 1, 'voice',
    87, 100, '2025-07-03T17:00:00', '2025-07-03T17:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5c2868df-b342-4011-bd6a-399f40b8491c', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-07-02T15:15:00', '2025-07-02T17:15:00', 'Conference Room',
    false, null, 'neutral', 1, 5, 'voice',
    133, 125, '2025-07-02T15:15:00', '2025-07-02T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd5965a0b-ae45-4ae5-89e4-b6cab6156b9a', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-07-01T15:15:00', '2025-07-01T16:15:00', 'Conference Room',
    false, null, 'productive', 1, 1, 'manual',
    74, 62, '2025-07-01T15:15:00', '2025-07-01T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '975e9039-6968-48c9-8b20-ddddf2420bf9', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-06-29T08:00:00', '2025-06-29T09:00:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'manual',
    53, 61, '2025-06-29T08:00:00', '2025-06-29T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'bcbeafa0-760f-453d-98f4-629ccd3701a2', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-07-03T15:15:00', '2025-07-03T16:15:00', 'Conference Room',
    false, null, 'productive', 4, 5, 'voice',
    65, 52, '2025-07-03T15:15:00', '2025-07-03T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '90365601-715f-4bec-a193-3ed8f9deffad', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-07-01T10:15:00', '2025-07-01T11:45:00', 'Conference Room',
    false, null, 'neutral', 3, 5, 'manual',
    88, 105, '2025-07-01T10:15:00', '2025-07-01T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3804c37e-360b-4dbb-861e-d664bf1928e9', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Project Review', 'Demo analytics data',
    '2025-07-06T14:45:00', '2025-07-06T15:45:00', 'Conference Room',
    false, null, 'waste', 3, 3, 'voice',
    76, 63, '2025-07-06T14:45:00', '2025-07-06T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b826ab51-56ae-4794-9ebf-65ec311b60bd', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-05T13:15:00', '2025-07-05T14:15:00', 'Conference Room',
    false, null, 'neutral', 3, 2, 'voice',
    63, 61, '2025-07-05T13:15:00', '2025-07-05T13:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0459bf5e-6128-418b-8e93-02f6673cd9c1', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-07-09T14:00:00', '2025-07-09T14:45:00', 'Conference Room',
    false, null, 'productive', 2, 4, 'imported',
    42, 60, '2025-07-09T14:00:00', '2025-07-09T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ccd6d418-c325-4b2b-a19a-e0b4fe522a00', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-07-05T11:45:00', '2025-07-05T13:15:00', 'Conference Room',
    false, null, 'neutral', 3, 2, 'manual',
    102, 85, '2025-07-05T11:45:00', '2025-07-05T11:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ebe0ded7-c432-4331-9dcd-3ceef5f31343', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-07-06T15:30:00', '2025-07-06T17:00:00', 'Conference Room',
    false, null, 'productive', 1, 4, 'manual',
    106, 92, '2025-07-06T15:30:00', '2025-07-06T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd79c712b-55db-427e-a2fa-3028206be26d', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-07-09T08:15:00', '2025-07-09T10:15:00', 'Conference Room',
    false, null, 'waste', 4, 3, 'imported',
    119, 110, '2025-07-09T08:15:00', '2025-07-09T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7c1ab737-cdb9-42f6-8562-803c63d94fe0', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-07-09T15:45:00', '2025-07-09T16:30:00', 'Conference Room',
    false, null, 'productive', 3, 5, 'imported',
    46, 51, '2025-07-09T15:45:00', '2025-07-09T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3f027301-bcb8-4c4d-bc52-d5ba4c1ccb23', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-07-06T13:30:00', '2025-07-06T15:00:00', 'Conference Room',
    false, null, 'neutral', 5, 1, 'voice',
    94, 96, '2025-07-06T13:30:00', '2025-07-06T13:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '288fed41-5467-4c84-8fc4-b85404c1362e', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-09T11:15:00', '2025-07-09T13:15:00', 'Conference Room',
    false, null, 'waste', 2, 5, 'manual',
    122, 117, '2025-07-09T11:15:00', '2025-07-09T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b66633cd-0d42-48b4-bd52-fe3f9fff3f05', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-08T15:30:00', '2025-07-08T16:15:00', 'Conference Room',
    false, null, 'waste', 5, 5, 'voice',
    61, 30, '2025-07-08T15:30:00', '2025-07-08T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3b4e2d06-0848-4f29-8ad8-78d280e7f0de', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Project Review', 'Demo analytics data',
    '2025-07-06T17:15:00', '2025-07-06T18:00:00', 'Conference Room',
    false, null, 'productive', 4, 5, 'voice',
    49, 38, '2025-07-06T17:15:00', '2025-07-06T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '03a1d7ad-ae45-4b30-b0e7-f25ce5435552', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-07-08T17:30:00', '2025-07-08T18:30:00', 'Conference Room',
    false, null, 'productive', 1, 4, 'text',
    63, 57, '2025-07-08T17:30:00', '2025-07-08T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fd42f87c-3205-4adf-96de-5dd72433a616', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-07-18T10:15:00', '2025-07-18T11:00:00', 'Conference Room',
    false, null, 'waste', 3, 4, 'imported',
    57, 45, '2025-07-18T10:15:00', '2025-07-18T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8805a192-acb0-4b10-ac1e-d3c0f202842c', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-07-14T17:15:00', '2025-07-14T18:15:00', 'Conference Room',
    false, null, 'productive', 1, 1, 'text',
    68, 73, '2025-07-14T17:15:00', '2025-07-14T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '05bf2cae-b89b-4642-90ab-2ac8ffa66aae', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-15T10:00:00', '2025-07-15T10:45:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'voice',
    40, 54, '2025-07-15T10:00:00', '2025-07-15T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9748b6e3-c836-42ba-b164-48d7b8b31ded', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-07-16T14:45:00', '2025-07-16T15:45:00', 'Conference Room',
    false, null, 'waste', 1, 1, 'text',
    55, 56, '2025-07-16T14:45:00', '2025-07-16T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c17be2a0-5e99-4359-afc5-68bac5606d60', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-07-17T16:00:00', '2025-07-17T18:00:00', 'Conference Room',
    false, null, 'productive', 5, 4, 'imported',
    130, 106, '2025-07-17T16:00:00', '2025-07-17T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7e526f48-1d75-4092-a165-b605750ed644', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-07-14T14:15:00', '2025-07-14T14:45:00', 'Conference Room',
    false, null, 'productive', 4, 4, 'text',
    31, 27, '2025-07-14T14:15:00', '2025-07-14T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ae4a515f-3a39-46e1-8295-5cde29d3c06d', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Training', 'Demo analytics data',
    '2025-07-16T08:30:00', '2025-07-16T10:30:00', 'Conference Room',
    false, null, 'productive', 2, 4, 'imported',
    111, 122, '2025-07-16T08:30:00', '2025-07-16T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd7c8edce-942a-46cf-a1f4-68b8e9434cf4', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-12T10:15:00', '2025-07-12T11:00:00', 'Conference Room',
    false, null, 'productive', 5, 4, 'voice',
    59, 39, '2025-07-12T10:15:00', '2025-07-12T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c585ce25-0665-4e44-a288-72a0be3349e6', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-07-12T12:30:00', '2025-07-12T13:15:00', 'Conference Room',
    false, null, 'waste', 5, 5, 'voice',
    50, 35, '2025-07-12T12:30:00', '2025-07-12T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6540cce4-d925-48ed-9d50-0a1e31d59a21', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-07-13T11:30:00', '2025-07-13T12:00:00', 'Conference Room',
    false, null, 'productive', 1, 1, 'voice',
    33, 18, '2025-07-13T11:30:00', '2025-07-13T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'aa317c84-d6bb-419a-b83f-a0084283c7a5', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Project Review', 'Demo analytics data',
    '2025-07-16T16:15:00', '2025-07-16T17:45:00', 'Conference Room',
    false, null, 'waste', 1, 1, 'text',
    84, 103, '2025-07-16T16:15:00', '2025-07-16T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7eba043d-df3e-43b8-9772-210621ecca85', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-07-18T12:30:00', '2025-07-18T14:00:00', 'Conference Room',
    false, null, 'waste', 4, 4, 'imported',
    94, 79, '2025-07-18T12:30:00', '2025-07-18T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '188213db-5e35-4dc5-8ad2-5f6a98007c2b', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-07-19T11:30:00', '2025-07-19T12:00:00', 'Conference Room',
    false, null, 'waste', 2, 5, 'imported',
    36, 40, '2025-07-19T11:30:00', '2025-07-19T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c550d129-ae6c-41b4-bcaf-0b00468acea7', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-07-23T09:00:00', '2025-07-23T10:00:00', 'Conference Room',
    false, null, 'neutral', 4, 5, 'voice',
    67, 69, '2025-07-23T09:00:00', '2025-07-23T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7ebe6768-5489-4b7c-8ab5-ba139b8c9ae1', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-07-22T10:15:00', '2025-07-22T11:45:00', 'Conference Room',
    false, null, 'waste', 4, 2, 'manual',
    94, 104, '2025-07-22T10:15:00', '2025-07-22T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '50297ddc-bbe4-458a-b927-d44f90e4bf0f', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-07-20T12:45:00', '2025-07-20T14:15:00', 'Conference Room',
    false, null, 'neutral', 3, 4, 'imported',
    90, 88, '2025-07-20T12:45:00', '2025-07-20T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3abffab4-fb9f-49a9-bfda-deb8f2da4063', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-23T09:00:00', '2025-07-23T09:45:00', 'Conference Room',
    false, null, 'neutral', 4, 1, 'voice',
    61, 50, '2025-07-23T09:00:00', '2025-07-23T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a33ba902-be14-46e6-805e-2b51f41a6610', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-07-22T16:00:00', '2025-07-22T18:00:00', 'Conference Room',
    false, null, 'neutral', 4, 4, 'manual',
    120, 107, '2025-07-22T16:00:00', '2025-07-22T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8b130bf3-bbd5-414a-8976-7fb8b17fae6f', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-07-25T09:00:00', '2025-07-25T11:00:00', 'Conference Room',
    false, null, 'waste', 4, 2, 'text',
    139, 111, '2025-07-25T09:00:00', '2025-07-25T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a9c3cd27-425f-455e-bed2-7ee1320832fb', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-07-25T14:45:00', '2025-07-25T16:15:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'manual',
    98, 76, '2025-07-25T14:45:00', '2025-07-25T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5b41c21d-9ec8-4a37-80a0-e2b6a56a613e', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-07-25T10:30:00', '2025-07-25T11:15:00', 'Conference Room',
    false, null, 'productive', 2, 5, 'text',
    44, 58, '2025-07-25T10:30:00', '2025-07-25T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1ab72355-68de-472c-943d-638c09066a51', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Brainstorm', 'Demo analytics data',
    '2025-07-23T17:00:00', '2025-07-23T18:30:00', 'Conference Room',
    false, null, 'productive', 1, 1, 'manual',
    100, 89, '2025-07-23T17:00:00', '2025-07-23T17:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '20af04eb-89dd-45c2-aab7-41a01451843d', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Project Review', 'Demo analytics data',
    '2025-07-20T08:00:00', '2025-07-20T08:30:00', 'Conference Room',
    false, null, 'productive', 1, 3, 'manual',
    38, 36, '2025-07-20T08:00:00', '2025-07-20T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f851ecec-9181-406e-906f-d89d9e02bfb1', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-26T08:00:00', '2025-07-26T08:45:00', 'Conference Room',
    false, null, 'waste', 4, 3, 'imported',
    37, 41, '2025-07-26T08:00:00', '2025-07-26T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9cae1bb7-832e-4b68-9606-b7a75fea81ff', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-07-30T14:15:00', '2025-07-30T14:45:00', 'Conference Room',
    false, null, 'neutral', 4, 4, 'text',
    33, 37, '2025-07-30T14:15:00', '2025-07-30T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'afbd6fd5-349a-49fd-a956-52de4604c2eb', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-07-31T08:45:00', '2025-07-31T09:30:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'imported',
    64, 49, '2025-07-31T08:45:00', '2025-07-31T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '704a1c0c-0a12-48d9-982e-263014342b8c', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Client Call', 'Demo analytics data',
    '2025-07-28T11:00:00', '2025-07-28T12:00:00', 'Conference Room',
    false, null, 'neutral', 4, 4, 'manual',
    74, 63, '2025-07-28T11:00:00', '2025-07-28T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '059a7c97-bf9e-48ff-b3a9-52bd0d5578d9', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-30T14:15:00', '2025-07-30T16:15:00', 'Conference Room',
    false, null, 'productive', 3, 4, 'imported',
    126, 133, '2025-07-30T14:15:00', '2025-07-30T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '019cf5fb-60b9-4054-af0d-6a5cb3951b71', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'All Hands', 'Demo analytics data',
    '2025-07-30T16:00:00', '2025-07-30T18:00:00', 'Conference Room',
    false, null, 'waste', 1, 2, 'imported',
    126, 117, '2025-07-30T16:00:00', '2025-07-30T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '96e402ce-41b4-44b2-8396-84cdd5220f59', '72ce59cc-7ce3-4639-9733-70624cf90ab1', '1:1 Check-in', 'Demo analytics data',
    '2025-07-29T11:00:00', '2025-07-29T12:00:00', 'Conference Room',
    false, null, 'neutral', 4, 2, 'imported',
    50, 50, '2025-07-29T11:00:00', '2025-07-29T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '82526a74-a9e5-497b-a475-2c9003380130', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Planning Session', 'Demo analytics data',
    '2025-07-30T17:30:00', '2025-07-30T19:30:00', 'Conference Room',
    false, null, 'neutral', 1, 4, 'imported',
    135, 120, '2025-07-30T17:30:00', '2025-07-30T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '08c9058a-16fb-40f2-9933-7ae1b03e6fbe', '72ce59cc-7ce3-4639-9733-70624cf90ab1', 'Team Meeting', 'Demo analytics data',
    '2025-07-28T17:45:00', '2025-07-28T18:30:00', 'Conference Room',
    false, null, 'productive', 4, 1, 'manual',
    57, 39, '2025-07-28T17:45:00', '2025-07-28T17:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a4e16daa-b6c0-42bc-a548-55ba8aeefe82', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-06-11T15:15:00', '2025-06-11T17:15:00', 'Conference Room',
    false, null, 'neutral', 2, 1, 'text',
    134, 127, '2025-06-11T15:15:00', '2025-06-11T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a484c46f-d296-4d58-95fb-1a23a9c1722c', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-06-12T09:15:00', '2025-06-12T11:15:00', 'Conference Room',
    false, null, 'productive', 4, 3, 'manual',
    121, 110, '2025-06-12T09:15:00', '2025-06-12T09:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9b7e29c1-7a52-4994-9876-9735261f98b1', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-06-09T11:15:00', '2025-06-09T12:15:00', 'Conference Room',
    false, null, 'neutral', 3, 5, 'manual',
    67, 45, '2025-06-09T11:15:00', '2025-06-09T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '01cf17cf-ac09-4f5b-bba7-a12481c3797b', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-06-13T13:15:00', '2025-06-13T14:45:00', 'Conference Room',
    false, null, 'productive', 3, 5, 'imported',
    98, 96, '2025-06-13T13:15:00', '2025-06-13T13:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ee2950cb-01da-4398-8314-3dac5dc19bf9', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-06-07T17:30:00', '2025-06-07T19:30:00', 'Conference Room',
    false, null, 'neutral', 4, 5, 'text',
    121, 132, '2025-06-07T17:30:00', '2025-06-07T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '89ca4357-141d-4989-91e4-5ff1838d523a', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-06-13T14:00:00', '2025-06-13T14:45:00', 'Conference Room',
    false, null, 'neutral', 5, 2, 'imported',
    62, 38, '2025-06-13T14:00:00', '2025-06-13T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f5f65e06-e9bb-42f7-8c9e-ba5c9a65ecdc', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-06-08T14:00:00', '2025-06-08T15:00:00', 'Conference Room',
    false, null, 'waste', 2, 1, 'text',
    56, 67, '2025-06-08T14:00:00', '2025-06-08T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '479d4349-22f2-4452-91ec-3a194666f591', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-06-09T11:00:00', '2025-06-09T12:30:00', 'Conference Room',
    false, null, 'neutral', 3, 2, 'manual',
    98, 87, '2025-06-09T11:00:00', '2025-06-09T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ddcfde15-ad51-4c61-9ef7-5f811d3046e0', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-06-11T14:45:00', '2025-06-11T15:15:00', 'Conference Room',
    false, null, 'waste', 4, 1, 'voice',
    34, 41, '2025-06-11T14:45:00', '2025-06-11T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6047a5d0-33da-433c-8131-599246957e2f', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-06-11T09:45:00', '2025-06-11T10:15:00', 'Conference Room',
    false, null, 'productive', 4, 5, 'text',
    44, 25, '2025-06-11T09:45:00', '2025-06-11T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c25d6ca6-f9b0-4fb6-87e2-92a45d55d6d5', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', '1:1 Check-in', 'Demo analytics data',
    '2025-06-07T17:15:00', '2025-06-07T18:15:00', 'Conference Room',
    false, null, 'productive', 4, 4, 'text',
    62, 65, '2025-06-07T17:15:00', '2025-06-07T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '47a43967-25ac-44ba-b1d7-d167e3d766dd', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-06-15T12:15:00', '2025-06-15T12:45:00', 'Conference Room',
    false, null, 'productive', 2, 5, 'voice',
    39, 39, '2025-06-15T12:15:00', '2025-06-15T12:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a7965ead-b5ad-46f8-95ca-4dc138e5017a', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-06-17T09:15:00', '2025-06-17T11:15:00', 'Conference Room',
    false, null, 'neutral', 4, 1, 'manual',
    111, 123, '2025-06-17T09:15:00', '2025-06-17T09:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2fa00302-0567-4a5c-ad96-d43437c77b27', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-06-17T09:15:00', '2025-06-17T10:15:00', 'Conference Room',
    false, null, 'neutral', 1, 5, 'manual',
    59, 50, '2025-06-17T09:15:00', '2025-06-17T09:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '4f324641-1afc-4f5f-933b-861a91166778', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-06-17T14:15:00', '2025-06-17T15:15:00', 'Conference Room',
    false, null, 'neutral', 1, 1, 'manual',
    71, 57, '2025-06-17T14:15:00', '2025-06-17T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'abbb6702-3591-414c-8082-268ceb4669e1', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-06-18T12:15:00', '2025-06-18T13:00:00', 'Conference Room',
    false, null, 'productive', 2, 4, 'voice',
    47, 32, '2025-06-18T12:15:00', '2025-06-18T12:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'dd393dd0-a675-4999-bdf1-08a6428bc4bf', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-06-18T14:30:00', '2025-06-18T15:30:00', 'Conference Room',
    false, null, 'neutral', 3, 4, 'manual',
    71, 55, '2025-06-18T14:30:00', '2025-06-18T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '4cc85a9c-4357-405b-b6ff-b83f72c9f536', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-06-16T11:15:00', '2025-06-16T12:45:00', 'Conference Room',
    false, null, 'productive', 2, 5, 'imported',
    110, 105, '2025-06-16T11:15:00', '2025-06-16T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '997b5020-9087-4e0d-91f4-a01691b9e11d', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-06-16T08:45:00', '2025-06-16T09:15:00', 'Conference Room',
    false, null, 'waste', 3, 3, 'voice',
    31, 41, '2025-06-16T08:45:00', '2025-06-16T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a171b717-67d5-41f8-9327-229ca40a3451', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-06-15T08:45:00', '2025-06-15T09:30:00', 'Conference Room',
    false, null, 'waste', 4, 4, 'manual',
    50, 60, '2025-06-15T08:45:00', '2025-06-15T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8690a86e-3d5a-47b1-abe0-4ac1f3be9124', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-06-14T10:15:00', '2025-06-14T11:15:00', 'Conference Room',
    false, null, 'neutral', 5, 1, 'imported',
    66, 73, '2025-06-14T10:15:00', '2025-06-14T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '376d3548-fe6f-4490-8651-1cb98b89148d', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-06-14T15:15:00', '2025-06-14T16:45:00', 'Conference Room',
    false, null, 'waste', 5, 2, 'text',
    107, 93, '2025-06-14T15:15:00', '2025-06-14T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '28dae0c7-e5b1-4db0-9ddc-9483c362018f', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-06-15T12:00:00', '2025-06-15T14:00:00', 'Conference Room',
    false, null, 'productive', 2, 2, 'voice',
    124, 135, '2025-06-15T12:00:00', '2025-06-15T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '68c5cdd5-775f-448f-9589-d62fbdb44009', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-06-24T14:30:00', '2025-06-24T16:00:00', 'Conference Room',
    false, null, 'neutral', 5, 1, 'manual',
    97, 77, '2025-06-24T14:30:00', '2025-06-24T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '255accdb-a883-4e1f-8b50-5c6117a69cb8', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-06-24T13:00:00', '2025-06-24T14:00:00', 'Conference Room',
    false, null, 'productive', 1, 3, 'imported',
    65, 70, '2025-06-24T13:00:00', '2025-06-24T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1cd5e25c-a81e-415a-bcb1-568430a93d3e', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Planning Session', 'Demo analytics data',
    '2025-06-24T11:00:00', '2025-06-24T12:30:00', 'Conference Room',
    false, null, 'productive', 4, 3, 'text',
    89, 102, '2025-06-24T11:00:00', '2025-06-24T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '19bc4ac4-9dc1-414a-ad4d-8140932d0132', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-06-25T13:45:00', '2025-06-25T15:15:00', 'Conference Room',
    false, null, 'waste', 2, 4, 'text',
    83, 101, '2025-06-25T13:45:00', '2025-06-25T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '74f64fc0-b668-419d-9576-9ee54bfa562e', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-06-23T13:15:00', '2025-06-23T14:15:00', 'Conference Room',
    false, null, 'waste', 1, 1, 'text',
    58, 62, '2025-06-23T13:15:00', '2025-06-23T13:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ee6e1b8f-210e-4e26-911b-ba0b5e9f20ea', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-06-22T12:45:00', '2025-06-22T13:30:00', 'Conference Room',
    false, null, 'productive', 2, 3, 'imported',
    44, 50, '2025-06-22T12:45:00', '2025-06-22T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9d18fbff-e99d-42b5-bba9-456e72c95e04', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-06-23T08:45:00', '2025-06-23T09:45:00', 'Conference Room',
    false, null, 'neutral', 1, 5, 'imported',
    50, 58, '2025-06-23T08:45:00', '2025-06-23T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c21d2877-8f29-4ffc-990b-25f17e4f14e4', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', '1:1 Check-in', 'Demo analytics data',
    '2025-06-25T08:30:00', '2025-06-25T09:00:00', 'Conference Room',
    false, null, 'waste', 2, 4, 'text',
    25, 37, '2025-06-25T08:30:00', '2025-06-25T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'bc312714-2f6a-498d-9ddb-23926d7471a7', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-06-24T17:30:00', '2025-06-24T19:00:00', 'Conference Room',
    false, null, 'waste', 5, 2, 'manual',
    86, 96, '2025-06-24T17:30:00', '2025-06-24T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '18f489b6-3515-4c8c-b43c-f58f401c4b81', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-06-27T14:00:00', '2025-06-27T15:00:00', 'Conference Room',
    false, null, 'productive', 3, 5, 'text',
    79, 72, '2025-06-27T14:00:00', '2025-06-27T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c08d415d-142f-4966-8cdd-86f0dc009cc7', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-06-29T12:00:00', '2025-06-29T13:30:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'imported',
    81, 103, '2025-06-29T12:00:00', '2025-06-29T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c32c76e9-f00d-4a19-a369-802859c5523b', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-06-29T11:15:00', '2025-06-29T12:00:00', 'Conference Room',
    false, null, 'waste', 1, 3, 'imported',
    35, 52, '2025-06-29T11:15:00', '2025-06-29T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a172fbbf-b772-41fc-b118-6987a6bae8fc', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Planning Session', 'Demo analytics data',
    '2025-07-01T11:15:00', '2025-07-01T12:15:00', 'Conference Room',
    false, null, 'productive', 1, 1, 'voice',
    69, 58, '2025-07-01T11:15:00', '2025-07-01T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0fb6c5cf-de2d-448f-8a37-420e0303d8b4', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-07-01T16:00:00', '2025-07-01T17:00:00', 'Conference Room',
    false, null, 'waste', 3, 3, 'imported',
    56, 66, '2025-07-01T16:00:00', '2025-07-01T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b987ebd6-3430-4fa0-9ce7-b7611e891156', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', '1:1 Check-in', 'Demo analytics data',
    '2025-07-02T10:15:00', '2025-07-02T11:15:00', 'Conference Room',
    false, null, 'neutral', 1, 3, 'voice',
    71, 68, '2025-07-02T10:15:00', '2025-07-02T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '782c06a1-db50-417e-8eeb-3f9543743406', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-06-30T14:30:00', '2025-06-30T15:30:00', 'Conference Room',
    false, null, 'waste', 3, 5, 'text',
    58, 55, '2025-06-30T14:30:00', '2025-06-30T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8852da77-7e57-4b9c-813d-2487023c0fa6', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-06-29T13:45:00', '2025-06-29T14:45:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'text',
    73, 51, '2025-06-29T13:45:00', '2025-06-29T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2078b435-f860-4d22-988c-db37fa395548', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-06-30T14:30:00', '2025-06-30T15:30:00', 'Conference Room',
    false, null, 'neutral', 3, 1, 'text',
    61, 47, '2025-06-30T14:30:00', '2025-06-30T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3af465ab-dfe8-4b31-87cb-f1beaeefedf1', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-06-28T09:45:00', '2025-06-28T11:15:00', 'Conference Room',
    false, null, 'productive', 4, 2, 'manual',
    96, 86, '2025-06-28T09:45:00', '2025-06-28T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '568846bb-6ce0-4dc0-bac1-a58d5db121da', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-07-01T15:30:00', '2025-07-01T16:15:00', 'Conference Room',
    false, null, 'productive', 3, 5, 'voice',
    54, 57, '2025-07-01T15:30:00', '2025-07-01T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c2bdeb7b-14c5-49b9-bff9-42b94b9626b6', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Planning Session', 'Demo analytics data',
    '2025-07-09T15:15:00', '2025-07-09T16:45:00', 'Conference Room',
    false, null, 'productive', 2, 2, 'voice',
    100, 100, '2025-07-09T15:15:00', '2025-07-09T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ef62706d-880a-4905-8aed-ba78318b8364', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-07-08T09:15:00', '2025-07-08T10:45:00', 'Conference Room',
    false, null, 'waste', 1, 5, 'imported',
    83, 86, '2025-07-08T09:15:00', '2025-07-08T09:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd32eccc3-86a1-418b-ab53-e4b2553720b2', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-07-06T12:30:00', '2025-07-06T13:00:00', 'Conference Room',
    false, null, 'productive', 4, 4, 'manual',
    25, 26, '2025-07-06T12:30:00', '2025-07-06T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5d7de0ea-7bee-4aac-b767-d2dd7fd55237', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-07-06T14:00:00', '2025-07-06T16:00:00', 'Conference Room',
    false, null, 'waste', 3, 2, 'imported',
    122, 119, '2025-07-06T14:00:00', '2025-07-06T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6e44fcc5-e16d-470e-a1b3-b0752ac7a1f2', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-07-07T16:15:00', '2025-07-07T17:15:00', 'Conference Room',
    false, null, 'productive', 4, 4, 'text',
    74, 51, '2025-07-07T16:15:00', '2025-07-07T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '98d98ac5-df4c-451d-a932-991841d82ec6', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-07-07T10:30:00', '2025-07-07T11:00:00', 'Conference Room',
    false, null, 'productive', 2, 5, 'voice',
    44, 27, '2025-07-07T10:30:00', '2025-07-07T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9a4e3e8b-8a2e-4e08-a436-32fc395ce391', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-07-09T12:45:00', '2025-07-09T13:30:00', 'Conference Room',
    false, null, 'neutral', 2, 3, 'voice',
    61, 53, '2025-07-09T12:45:00', '2025-07-09T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0aa265e8-51de-4d7b-abc4-c2571aee0054', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-07-07T12:30:00', '2025-07-07T14:30:00', 'Conference Room',
    false, null, 'waste', 5, 1, 'voice',
    125, 130, '2025-07-07T12:30:00', '2025-07-07T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '01b0960a-656f-4cb8-9f76-50cf2565e5da', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Planning Session', 'Demo analytics data',
    '2025-07-14T08:30:00', '2025-07-14T10:00:00', 'Conference Room',
    false, null, 'neutral', 1, 4, 'voice',
    99, 101, '2025-07-14T08:30:00', '2025-07-14T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'da4d922b-304a-455e-9c1f-714e8c4f8860', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-07-12T13:30:00', '2025-07-12T14:30:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'text',
    62, 75, '2025-07-12T13:30:00', '2025-07-12T13:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6ae1c47f-1bf8-409a-9632-b6c380256ed2', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-07-12T13:30:00', '2025-07-12T14:00:00', 'Conference Room',
    false, null, 'productive', 3, 3, 'imported',
    47, 44, '2025-07-12T13:30:00', '2025-07-12T13:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '20dc9269-2d3d-47cf-8857-b93283023cf8', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-07-12T12:15:00', '2025-07-12T12:45:00', 'Conference Room',
    false, null, 'neutral', 1, 2, 'text',
    50, 41, '2025-07-12T12:15:00', '2025-07-12T12:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5b0617a6-fa1d-4512-8d6b-ce1076619927', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-07-13T14:00:00', '2025-07-13T15:30:00', 'Conference Room',
    false, null, 'waste', 1, 2, 'text',
    103, 100, '2025-07-13T14:00:00', '2025-07-13T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '37fda9e4-9359-4292-98d8-f6cd1f954d7d', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-07-16T09:30:00', '2025-07-16T10:15:00', 'Conference Room',
    false, null, 'waste', 4, 5, 'text',
    51, 46, '2025-07-16T09:30:00', '2025-07-16T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6915ae6d-5c6b-4cb0-9bea-d79b8a8578f9', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-07-15T15:15:00', '2025-07-15T17:15:00', 'Conference Room',
    false, null, 'waste', 4, 1, 'voice',
    126, 133, '2025-07-15T15:15:00', '2025-07-15T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e384d6c5-ad0d-4aee-a60c-d742e1d5fa46', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-07-12T17:30:00', '2025-07-12T19:30:00', 'Conference Room',
    false, null, 'neutral', 1, 5, 'text',
    122, 118, '2025-07-12T17:30:00', '2025-07-12T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '927c5bd5-db5e-498c-a784-28255090543f', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', '1:1 Check-in', 'Demo analytics data',
    '2025-07-16T14:45:00', '2025-07-16T15:15:00', 'Conference Room',
    false, null, 'neutral', 4, 2, 'imported',
    29, 38, '2025-07-16T14:45:00', '2025-07-16T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '77c17fb7-25f6-4dcd-a374-30a1a5f46a7c', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-07-15T14:45:00', '2025-07-15T15:30:00', 'Conference Room',
    false, null, 'neutral', 1, 3, 'imported',
    42, 56, '2025-07-15T14:45:00', '2025-07-15T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6de2c5c2-1b83-40a5-b345-5c8d7a0c724a', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Brainstorm', 'Demo analytics data',
    '2025-07-22T12:30:00', '2025-07-22T14:00:00', 'Conference Room',
    false, null, 'waste', 4, 2, 'voice',
    108, 95, '2025-07-22T12:30:00', '2025-07-22T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1037186e-af55-4af5-b638-d3296ddbb8e7', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-07-22T16:30:00', '2025-07-22T18:30:00', 'Conference Room',
    false, null, 'productive', 2, 4, 'text',
    140, 134, '2025-07-22T16:30:00', '2025-07-22T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd8e8c867-3459-4dba-a81e-3ab19fdf1f9a', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-07-21T09:00:00', '2025-07-21T11:00:00', 'Conference Room',
    false, null, 'neutral', 4, 4, 'voice',
    139, 105, '2025-07-21T09:00:00', '2025-07-21T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '970ea950-ac98-44ca-9ac6-1c549caa4346', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', '1:1 Check-in', 'Demo analytics data',
    '2025-07-19T15:45:00', '2025-07-19T16:15:00', 'Conference Room',
    false, null, 'productive', 3, 2, 'voice',
    42, 44, '2025-07-19T15:45:00', '2025-07-19T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8eb7b3a3-b39d-44e9-9f50-f19e90a71f58', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', '1:1 Check-in', 'Demo analytics data',
    '2025-07-23T12:45:00', '2025-07-23T13:45:00', 'Conference Room',
    false, null, 'waste', 1, 5, 'imported',
    61, 48, '2025-07-23T12:45:00', '2025-07-23T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'eea07549-6877-494a-8c81-6fa643488e5e', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Planning Session', 'Demo analytics data',
    '2025-07-22T12:45:00', '2025-07-22T14:45:00', 'Conference Room',
    false, null, 'neutral', 3, 1, 'text',
    130, 123, '2025-07-22T12:45:00', '2025-07-22T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3e7c8e2c-5dd6-4282-b92e-a364c5bacd23', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-07-19T09:30:00', '2025-07-19T10:00:00', 'Conference Room',
    false, null, 'waste', 4, 2, 'text',
    26, 31, '2025-07-19T09:30:00', '2025-07-19T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e628cff7-8a47-49dd-b44e-d77c2e9c5593', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Planning Session', 'Demo analytics data',
    '2025-07-23T17:15:00', '2025-07-23T18:45:00', 'Conference Room',
    false, null, 'productive', 1, 3, 'text',
    110, 95, '2025-07-23T17:15:00', '2025-07-23T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '73948692-c716-447d-9202-48de5e69a7d1', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Client Call', 'Demo analytics data',
    '2025-07-24T09:30:00', '2025-07-24T10:00:00', 'Conference Room',
    false, null, 'waste', 3, 4, 'text',
    22, 33, '2025-07-24T09:30:00', '2025-07-24T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'caae62a2-bbcf-411f-a977-a8b3802aba9b', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Training', 'Demo analytics data',
    '2025-07-21T12:00:00', '2025-07-21T14:00:00', 'Conference Room',
    false, null, 'waste', 1, 1, 'imported',
    119, 106, '2025-07-21T12:00:00', '2025-07-21T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '654fb32a-55f4-4d40-b75c-d23770fbfc7a', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-07-25T12:30:00', '2025-07-25T14:00:00', 'Conference Room',
    false, null, 'waste', 5, 4, 'manual',
    87, 96, '2025-07-25T12:30:00', '2025-07-25T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a4c6d6b6-2817-4f7e-8413-84d1ecc44b2b', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-07-26T10:00:00', '2025-07-26T11:00:00', 'Conference Room',
    false, null, 'neutral', 3, 5, 'imported',
    64, 46, '2025-07-26T10:00:00', '2025-07-26T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fb369db4-d87c-472a-a035-4215038c9335', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-07-28T14:45:00', '2025-07-28T16:15:00', 'Conference Room',
    false, null, 'waste', 3, 2, 'voice',
    80, 82, '2025-07-28T14:45:00', '2025-07-28T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2eeba9b5-6f4f-47c5-a39f-12881efae489', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-07-26T09:45:00', '2025-07-26T11:45:00', 'Conference Room',
    false, null, 'neutral', 1, 2, 'imported',
    128, 133, '2025-07-26T09:45:00', '2025-07-26T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6ae6b75d-f6cc-4150-aafc-126dec9d6faf', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-07-30T10:30:00', '2025-07-30T11:00:00', 'Conference Room',
    false, null, 'neutral', 5, 2, 'voice',
    34, 22, '2025-07-30T10:30:00', '2025-07-30T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '21a350e9-da01-4526-980f-3296f7c8a121', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-07-30T08:15:00', '2025-07-30T09:45:00', 'Conference Room',
    false, null, 'waste', 5, 3, 'voice',
    98, 78, '2025-07-30T08:15:00', '2025-07-30T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '55f6313e-2725-42c3-9350-3bc68a5b477b', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-07-26T15:30:00', '2025-07-26T16:15:00', 'Conference Room',
    false, null, 'waste', 2, 4, 'manual',
    48, 42, '2025-07-26T15:30:00', '2025-07-26T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a0fbaf16-6dad-4e64-ba82-3e29a384eb4d', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-07-27T09:30:00', '2025-07-27T10:30:00', 'Conference Room',
    false, null, 'productive', 4, 3, 'voice',
    67, 54, '2025-07-27T09:30:00', '2025-07-27T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8c8e8da7-85ef-43ce-98fd-f200ba59639b', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Project Review', 'Demo analytics data',
    '2025-07-27T11:30:00', '2025-07-27T13:00:00', 'Conference Room',
    false, null, 'productive', 2, 2, 'manual',
    92, 86, '2025-07-27T11:30:00', '2025-07-27T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0f379197-113e-47ae-b106-952d892c22ef', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'Team Meeting', 'Demo analytics data',
    '2025-07-26T14:00:00', '2025-07-26T14:45:00', 'Conference Room',
    false, null, 'neutral', 3, 4, 'manual',
    59, 54, '2025-07-26T14:00:00', '2025-07-26T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, meeting_outcome, effectiveness_rating, energy_level, 
    created_via, actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '32cc8e56-5076-4ed8-a86a-ceb4a3febdcf', 'f1c6a8a1-6cc4-4c8b-922a-900a04c74946', 'All Hands', 'Demo analytics data',
    '2025-07-27T12:30:00', '2025-07-27T14:00:00', 'Conference Room',
    false, null, 'waste', 4, 3, 'voice',
    90, 88, '2025-07-27T12:30:00', '2025-07-27T12:30:00'
);