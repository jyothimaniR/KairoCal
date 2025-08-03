-- Analytics Demo Data
-- Users

INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
VALUES ('27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'demo_user_001', 'sarah.chen@company.com', 'Sarah Chen', 
        '{"pattern": "high_performer"}', true, now(), now())
ON CONFLICT (cognito_sub) DO UPDATE SET 
    email = EXCLUDED.email, full_name = EXCLUDED.full_name, updated_at = now();


INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
VALUES ('ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'demo_user_002', 'marcus.rodriguez@company.com', 'Marcus Rodriguez', 
        '{"pattern": "morning_person"}', true, now(), now())
ON CONFLICT (cognito_sub) DO UPDATE SET 
    email = EXCLUDED.email, full_name = EXCLUDED.full_name, updated_at = now();


INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at)
VALUES ('b017910f-479e-4871-a343-d375f5505403', 'demo_user_003', 'emily.watson@company.com', 'Emily Watson', 
        '{"pattern": "afternoon_focus"}', true, now(), now())
ON CONFLICT (cognito_sub) DO UPDATE SET 
    email = EXCLUDED.email, full_name = EXCLUDED.full_name, updated_at = now();


-- Events

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0c119e99-96cb-4142-a07e-c728ddc796c1', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-11T14:15:00', '2025-06-11T16:15:00', 'Conference Room',
    false, null, 1, 0.688, 'manual',
    'productive', 4, 3, 'voice',
    125, 128, '2025-06-11T14:15:00', '2025-06-11T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f03ebf45-5995-4196-b8d4-73a8d2cca088', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-06-10T08:15:00', '2025-06-10T10:15:00', 'Conference Room',
    false, null, 3, 0.638, 'bert',
    'productive', 4, 5, 'voice',
    120, 114, '2025-06-10T08:15:00', '2025-06-10T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '771ecb71-b345-4797-8a9f-8d53b4b45dcc', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-09T10:15:00', '2025-06-09T11:00:00', 'Conference Room',
    false, null, 4, 0.678, 'rule_based',
    'neutral', 3, 4, 'voice',
    43, 54, '2025-06-09T10:15:00', '2025-06-09T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '63e8eb32-c654-433f-92ca-431534af1c5e', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-06-10T16:45:00', '2025-06-10T18:15:00', 'Conference Room',
    false, null, 4, 0.845, 'manual',
    'productive', 5, 5, 'manual',
    108, 92, '2025-06-10T16:45:00', '2025-06-10T16:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3e37b0a1-19f5-4a2c-9d07-5e7195ed16a3', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-06-12T12:30:00', '2025-06-12T14:30:00', 'Conference Room',
    false, null, 5, 0.919, 'rule_based',
    'productive', 4, 3, 'manual',
    138, 135, '2025-06-12T12:30:00', '2025-06-12T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2b2e0e4d-0ca1-4bc5-9eb5-81fbbd7ab798', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-13T15:45:00', '2025-06-13T16:45:00', 'Conference Room',
    false, null, 5, 0.923, 'rule_based',
    'productive', 5, 4, 'text',
    80, 75, '2025-06-13T15:45:00', '2025-06-13T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '265b5158-8099-4d9a-9cdc-fc4bc0ced2ca', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-09T10:00:00', '2025-06-09T10:45:00', 'Conference Room',
    false, null, 3, 0.704, 'rule_based',
    'productive', 5, 3, 'manual',
    52, 48, '2025-06-09T10:00:00', '2025-06-09T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '803c2f20-33d2-48ff-8604-8361a11385bb', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-06-13T11:30:00', '2025-06-13T12:15:00', 'Conference Room',
    false, null, 2, 0.724, 'rule_based',
    'productive', 5, 5, 'text',
    43, 43, '2025-06-13T11:30:00', '2025-06-13T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3b7b96e1-ee85-4e69-8957-6b0801eb1aa5', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-12T08:30:00', '2025-06-12T09:15:00', 'Conference Room',
    false, null, 3, 0.648, 'rule_based',
    'productive', 5, 3, 'voice',
    54, 41, '2025-06-12T08:30:00', '2025-06-12T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'acf58d00-95cc-448f-be12-780431262cf6', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-06-10T16:30:00', '2025-06-10T17:30:00', 'Conference Room',
    false, null, 2, 0.701, 'rule_based',
    'productive', 5, 5, 'manual',
    53, 57, '2025-06-10T16:30:00', '2025-06-10T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0e44e8ba-add5-4864-b9cb-982a37ad563e', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-09T09:45:00', '2025-06-09T10:30:00', 'Conference Room',
    false, null, 2, 0.824, 'manual',
    'neutral', 3, 5, 'voice',
    57, 48, '2025-06-09T09:45:00', '2025-06-09T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2b87d085-84eb-440e-988e-32e8edbb0c57', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-06-20T15:45:00', '2025-06-20T16:45:00', 'Conference Room',
    false, null, 4, 0.933, 'rule_based',
    'productive', 3, 4, 'voice',
    50, 69, '2025-06-20T15:45:00', '2025-06-20T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6a94a287-7f71-4dbc-a7ab-4021d269bbbd', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-06-17T14:30:00', '2025-06-17T15:30:00', 'Conference Room',
    false, null, 3, 0.724, 'bert',
    'neutral', 3, 5, 'imported',
    74, 70, '2025-06-17T14:30:00', '2025-06-17T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7cbccc55-291e-4596-af69-21c0f33eb4a4', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-14T11:00:00', '2025-06-14T12:30:00', 'Conference Room',
    false, null, 4, 0.810, 'rule_based',
    'productive', 5, 4, 'text',
    95, 75, '2025-06-14T11:00:00', '2025-06-14T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3671fa01-be3d-452a-a57d-edf2f5adf3b2', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-06-18T16:30:00', '2025-06-18T17:15:00', 'Conference Room',
    false, null, 4, 0.674, 'manual',
    'productive', 4, 5, 'manual',
    41, 51, '2025-06-18T16:30:00', '2025-06-18T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1682eda7-e0bc-4697-8f99-7da4c38f55de', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-06-20T13:00:00', '2025-06-20T13:30:00', 'Conference Room',
    false, null, 4, 0.900, 'manual',
    'productive', 5, 5, 'text',
    38, 44, '2025-06-20T13:00:00', '2025-06-20T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'bb096417-bc12-48fa-9d79-083c2c6be19c', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-06-18T12:00:00', '2025-06-18T12:30:00', 'Conference Room',
    false, null, 4, 0.829, 'bert',
    'productive', 4, 3, 'text',
    25, 28, '2025-06-18T12:00:00', '2025-06-18T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0d299fd4-2295-47e8-914b-69f84c3a56a5', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-06-16T17:15:00', '2025-06-16T17:45:00', 'Conference Room',
    false, null, 2, 0.765, 'manual',
    'productive', 4, 4, 'imported',
    43, 18, '2025-06-16T17:15:00', '2025-06-16T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '596bea6c-6b92-4810-99d6-c8e675866922', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-06-19T12:00:00', '2025-06-19T13:30:00', 'Conference Room',
    false, null, 2, 0.684, 'manual',
    'productive', 3, 4, 'voice',
    85, 81, '2025-06-19T12:00:00', '2025-06-19T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0b46a1a7-4047-4be3-b13e-54e24fd106cb', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-06-17T16:00:00', '2025-06-17T18:00:00', 'Conference Room',
    false, null, 1, 0.847, 'rule_based',
    'waste', 4, 5, 'manual',
    112, 108, '2025-06-17T16:00:00', '2025-06-17T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b3461d19-345a-4a32-bb81-36326e35362d', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-06-17T13:45:00', '2025-06-17T15:15:00', 'Conference Room',
    false, null, 1, 0.897, 'manual',
    'productive', 5, 4, 'voice',
    101, 91, '2025-06-17T13:45:00', '2025-06-17T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '83be831a-ccf0-43a8-8d82-ce275daa1ee1', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-06-20T15:00:00', '2025-06-20T17:00:00', 'Conference Room',
    false, null, 3, 0.819, 'rule_based',
    'neutral', 4, 4, 'voice',
    122, 133, '2025-06-20T15:00:00', '2025-06-20T15:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5a4486f1-74c6-4e19-b4ce-ab3b73e3c339', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-06-14T08:00:00', '2025-06-14T09:00:00', 'Conference Room',
    false, null, 5, 0.854, 'rule_based',
    'productive', 5, 4, 'text',
    50, 53, '2025-06-14T08:00:00', '2025-06-14T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd1cb67a4-a0df-4697-b6b2-d9cdd91489c5', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-06-24T16:45:00', '2025-06-24T17:45:00', 'Conference Room',
    false, null, 3, 0.913, 'bert',
    'productive', 5, 5, 'voice',
    57, 70, '2025-06-24T16:45:00', '2025-06-24T16:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e6a69729-27a3-4f60-8682-6901fb5d4d2d', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-06-26T16:00:00', '2025-06-26T17:00:00', 'Conference Room',
    false, null, 2, 0.846, 'manual',
    'productive', 3, 4, 'voice',
    75, 67, '2025-06-26T16:00:00', '2025-06-26T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '232140dc-f66c-4074-88e6-6936e4183fac', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-06-26T09:30:00', '2025-06-26T11:30:00', 'Conference Room',
    false, null, 5, 0.638, 'manual',
    'productive', 4, 4, 'voice',
    120, 124, '2025-06-26T09:30:00', '2025-06-26T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'bc1ffa5c-ac42-461d-b40b-c7af407409f6', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-27T09:00:00', '2025-06-27T10:30:00', 'Conference Room',
    false, null, 3, 0.741, 'manual',
    'neutral', 5, 3, 'text',
    90, 94, '2025-06-27T09:00:00', '2025-06-27T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '19578737-654d-42f8-ac33-05a28663d8d0', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-23T13:30:00', '2025-06-23T14:00:00', 'Conference Room',
    false, null, 3, 0.885, 'rule_based',
    'waste', 3, 4, 'text',
    49, 26, '2025-06-23T13:30:00', '2025-06-23T13:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0aafb4ef-97a9-4d36-8448-7c57b401165d', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-06-23T09:30:00', '2025-06-23T11:30:00', 'Conference Room',
    false, null, 4, 0.662, 'manual',
    'productive', 5, 5, 'text',
    125, 112, '2025-06-23T09:30:00', '2025-06-23T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '566085f9-705b-479f-badf-57cf876c3229', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-06-22T12:15:00', '2025-06-22T13:15:00', 'Conference Room',
    false, null, 4, 0.688, 'rule_based',
    'waste', 5, 4, 'manual',
    62, 66, '2025-06-22T12:15:00', '2025-06-22T12:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd7958687-8f57-49ae-9092-b930723704f5', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-23T14:00:00', '2025-06-23T16:00:00', 'Conference Room',
    false, null, 2, 0.916, 'bert',
    'waste', 3, 3, 'imported',
    110, 126, '2025-06-23T14:00:00', '2025-06-23T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '79061516-7d82-4b47-8641-8232c83c9b7b', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-27T11:30:00', '2025-06-27T12:15:00', 'Conference Room',
    false, null, 2, 0.761, 'manual',
    'neutral', 5, 4, 'manual',
    57, 35, '2025-06-27T11:30:00', '2025-06-27T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '454da3b7-da7a-4f99-87f0-c7212acb35c7', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-06-27T10:00:00', '2025-06-27T11:30:00', 'Conference Room',
    false, null, 2, 0.636, 'bert',
    'productive', 3, 3, 'voice',
    81, 87, '2025-06-27T10:00:00', '2025-06-27T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'dd9fa7c3-f84e-4c62-bbd6-dc45e07a7ce8', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-03T11:30:00', '2025-07-03T13:30:00', 'Conference Room',
    false, null, 4, 0.838, 'manual',
    'neutral', 3, 3, 'voice',
    110, 130, '2025-07-03T11:30:00', '2025-07-03T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0491265f-3ba9-4c65-9f63-9cb60cbabfcd', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-02T13:30:00', '2025-07-02T14:15:00', 'Conference Room',
    false, null, 5, 0.940, 'manual',
    'productive', 5, 5, 'text',
    59, 43, '2025-07-02T13:30:00', '2025-07-02T13:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '46e450c5-4f79-4c04-8044-a48541db642d', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-28T14:00:00', '2025-06-28T15:00:00', 'Conference Room',
    false, null, 5, 0.874, 'manual',
    'productive', 4, 5, 'voice',
    57, 50, '2025-06-28T14:00:00', '2025-06-28T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fd0f3481-ea99-4050-9cf1-d2625da9ddb2', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-02T08:45:00', '2025-07-02T09:30:00', 'Conference Room',
    false, null, 2, 0.938, 'rule_based',
    'waste', 4, 5, 'voice',
    62, 59, '2025-07-02T08:45:00', '2025-07-02T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1f20ffd5-7cfd-4fb3-9a39-31422d593bbf', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-07-01T09:45:00', '2025-07-01T10:30:00', 'Conference Room',
    false, null, 1, 0.739, 'manual',
    'productive', 5, 3, 'voice',
    61, 44, '2025-07-01T09:45:00', '2025-07-01T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3096d98a-e39c-469f-9c50-e2f065561433', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-03T09:00:00', '2025-07-03T09:45:00', 'Conference Room',
    false, null, 2, 0.800, 'rule_based',
    'productive', 3, 4, 'voice',
    55, 48, '2025-07-03T09:00:00', '2025-07-03T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '4a6bb199-fa16-4380-b1b1-a0e760c13882', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-03T13:45:00', '2025-07-03T14:45:00', 'Conference Room',
    false, null, 5, 0.754, 'bert',
    'productive', 5, 3, 'text',
    56, 65, '2025-07-03T13:45:00', '2025-07-03T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '03ff4701-9efd-4160-b458-2420885fa298', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-06-30T09:00:00', '2025-06-30T09:30:00', 'Conference Room',
    false, null, 1, 0.887, 'bert',
    'waste', 4, 5, 'manual',
    26, 29, '2025-06-30T09:00:00', '2025-06-30T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '392aa95e-862f-48e6-8e73-5a7d54546d28', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-03T15:30:00', '2025-07-03T16:00:00', 'Conference Room',
    false, null, 4, 0.902, 'bert',
    'neutral', 4, 5, 'text',
    32, 26, '2025-07-03T15:30:00', '2025-07-03T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '73b77436-9b54-4b6d-b205-24101b976373', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-07-02T08:00:00', '2025-07-02T08:30:00', 'Conference Room',
    false, null, 4, 0.756, 'rule_based',
    'waste', 3, 4, 'voice',
    29, 17, '2025-07-02T08:00:00', '2025-07-02T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2c6cd885-4769-4c79-9d34-87b4ee9280f8', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-07-03T17:00:00', '2025-07-03T17:30:00', 'Conference Room',
    false, null, 3, 0.850, 'rule_based',
    'productive', 4, 3, 'voice',
    48, 19, '2025-07-03T17:00:00', '2025-07-03T17:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '569969e9-d6bc-49d3-9fcf-033dfbde35ad', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-07-07T14:45:00', '2025-07-07T16:15:00', 'Conference Room',
    false, null, 4, 0.694, 'rule_based',
    'waste', 4, 3, 'imported',
    95, 81, '2025-07-07T14:45:00', '2025-07-07T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e5bb648a-9c57-409d-b2d5-a78dfe76564a', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-11T13:00:00', '2025-07-11T14:30:00', 'Conference Room',
    false, null, 2, 0.873, 'rule_based',
    'productive', 5, 3, 'voice',
    108, 104, '2025-07-11T13:00:00', '2025-07-11T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd765f85f-bdfb-49ac-a2dd-546213a786de', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-07-11T11:15:00', '2025-07-11T12:45:00', 'Conference Room',
    false, null, 3, 0.822, 'manual',
    'productive', 4, 4, 'manual',
    90, 93, '2025-07-11T11:15:00', '2025-07-11T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fc3c13f2-e459-4985-99b9-61fea3402241', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-09T15:30:00', '2025-07-09T16:15:00', 'Conference Room',
    false, null, 3, 0.880, 'bert',
    'productive', 4, 5, 'text',
    35, 45, '2025-07-09T15:30:00', '2025-07-09T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3c9bc8b2-f854-441a-bfa4-09aa57b73c3c', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-07T10:45:00', '2025-07-07T12:45:00', 'Conference Room',
    false, null, 4, 0.909, 'bert',
    'productive', 4, 4, 'text',
    129, 125, '2025-07-07T10:45:00', '2025-07-07T10:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e62ff5c1-c97e-405d-86cc-6edfc9459007', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-07-06T11:30:00', '2025-07-06T13:00:00', 'Conference Room',
    false, null, 2, 0.717, 'manual',
    'productive', 3, 4, 'voice',
    92, 84, '2025-07-06T11:30:00', '2025-07-06T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9d7a5862-1300-4c12-9614-9037c18f1c28', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-08T14:30:00', '2025-07-08T16:30:00', 'Conference Room',
    false, null, 3, 0.910, 'manual',
    'neutral', 4, 4, 'text',
    129, 122, '2025-07-08T14:30:00', '2025-07-08T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '81d86a7b-0ed6-4518-851c-db28c0287d71', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-07T11:30:00', '2025-07-07T12:00:00', 'Conference Room',
    false, null, 4, 0.829, 'rule_based',
    'productive', 3, 3, 'text',
    38, 29, '2025-07-07T11:30:00', '2025-07-07T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f585666c-bca0-4255-b5fb-a23f165e1e8c', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-07-11T09:45:00', '2025-07-11T11:15:00', 'Conference Room',
    false, null, 5, 0.934, 'bert',
    'productive', 5, 3, 'imported',
    90, 83, '2025-07-11T09:45:00', '2025-07-11T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ee8bf136-fc19-4c1e-9bfb-2031ece089cc', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-07-09T08:00:00', '2025-07-09T08:30:00', 'Conference Room',
    false, null, 5, 0.716, 'rule_based',
    'productive', 5, 3, 'imported',
    48, 21, '2025-07-09T08:00:00', '2025-07-09T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c1ce894c-af44-432f-926e-0a74254e92ce', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-07-17T08:30:00', '2025-07-17T09:30:00', 'Conference Room',
    false, null, 2, 0.639, 'manual',
    'productive', 3, 4, 'manual',
    68, 45, '2025-07-17T08:30:00', '2025-07-17T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f067a71f-4f7d-4cf6-b041-7bcda565aa0a', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-17T12:00:00', '2025-07-17T14:00:00', 'Conference Room',
    false, null, 4, 0.728, 'rule_based',
    'waste', 4, 3, 'voice',
    121, 117, '2025-07-17T12:00:00', '2025-07-17T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2e285f75-d6ea-4e5b-821e-f76acf35086f', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-16T09:45:00', '2025-07-16T10:30:00', 'Conference Room',
    false, null, 4, 0.855, 'bert',
    'neutral', 4, 3, 'imported',
    38, 58, '2025-07-16T09:45:00', '2025-07-16T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c11894d2-0a9e-4c97-825a-edeeaae882a8', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-07-17T11:15:00', '2025-07-17T12:00:00', 'Conference Room',
    false, null, 3, 0.659, 'rule_based',
    'productive', 5, 5, 'voice',
    36, 47, '2025-07-17T11:15:00', '2025-07-17T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '33307b16-9cd9-4213-85f7-d3c6fd888035', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-07-16T09:00:00', '2025-07-16T11:00:00', 'Conference Room',
    false, null, 1, 0.701, 'bert',
    'neutral', 4, 5, 'imported',
    130, 122, '2025-07-16T09:00:00', '2025-07-16T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3cafa489-d6b0-4de4-b1b5-8053963bf479', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-14T16:00:00', '2025-07-14T18:00:00', 'Conference Room',
    false, null, 5, 0.917, 'rule_based',
    'productive', 3, 3, 'imported',
    120, 127, '2025-07-14T16:00:00', '2025-07-14T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd17bd416-dc8a-4a2b-b4d8-0db9c42750bc', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-07-20T08:00:00', '2025-07-20T09:00:00', 'Conference Room',
    false, null, 4, 0.771, 'manual',
    'productive', 5, 3, 'manual',
    67, 72, '2025-07-20T08:00:00', '2025-07-20T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd200bbab-b31a-4698-9a64-53a9f655c9f6', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-23T13:30:00', '2025-07-23T14:30:00', 'Conference Room',
    false, null, 3, 0.923, 'bert',
    'neutral', 3, 3, 'text',
    77, 59, '2025-07-23T13:30:00', '2025-07-23T13:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'db0800f4-8afc-4eb2-897d-769088703a8c', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-25T09:45:00', '2025-07-25T11:15:00', 'Conference Room',
    false, null, 5, 0.708, 'rule_based',
    'waste', 5, 5, 'text',
    91, 89, '2025-07-25T09:45:00', '2025-07-25T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '756c06d2-504b-4996-8d4b-3f59fa8c7ebd', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-20T17:15:00', '2025-07-20T18:45:00', 'Conference Room',
    false, null, 4, 0.671, 'manual',
    'productive', 4, 4, 'manual',
    96, 97, '2025-07-20T17:15:00', '2025-07-20T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '49b29ce1-aee3-4fcd-b993-fc0564f82470', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-22T13:45:00', '2025-07-22T15:45:00', 'Conference Room',
    false, null, 3, 0.626, 'rule_based',
    'neutral', 4, 4, 'imported',
    119, 125, '2025-07-22T13:45:00', '2025-07-22T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '20a0e3ea-53e0-48f6-81a1-2c54d0f1f512', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-22T08:45:00', '2025-07-22T09:45:00', 'Conference Room',
    false, null, 4, 0.635, 'rule_based',
    'neutral', 4, 3, 'text',
    52, 65, '2025-07-22T08:45:00', '2025-07-22T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6dcdf44e-e7b5-4986-9500-58167d054ee8', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-23T16:30:00', '2025-07-23T18:30:00', 'Conference Room',
    false, null, 3, 0.870, 'manual',
    'productive', 5, 3, 'text',
    118, 122, '2025-07-23T16:30:00', '2025-07-23T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e0fbbcbf-4651-4011-97e3-57fdd6e03048', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Client Call', 'Demo analytics data',
    '2025-07-24T08:45:00', '2025-07-24T09:45:00', 'Conference Room',
    false, null, 3, 0.716, 'manual',
    'neutral', 3, 5, 'voice',
    64, 60, '2025-07-24T08:45:00', '2025-07-24T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f651dafc-798f-4e6f-ab0f-c7b23e1a09b8', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-07-25T16:30:00', '2025-07-25T18:30:00', 'Conference Room',
    false, null, 4, 0.890, 'rule_based',
    'productive', 5, 3, 'manual',
    117, 111, '2025-07-25T16:30:00', '2025-07-25T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5e871047-7db3-4bd7-983a-18ebbddbc5fe', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-07-21T15:00:00', '2025-07-21T16:30:00', 'Conference Room',
    false, null, 1, 0.677, 'rule_based',
    'productive', 5, 4, 'imported',
    94, 102, '2025-07-21T15:00:00', '2025-07-21T15:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f924067d-6383-4658-bf02-b36307cc151f', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-07-24T12:00:00', '2025-07-24T14:00:00', 'Conference Room',
    false, null, 5, 0.745, 'manual',
    'neutral', 5, 5, 'manual',
    115, 109, '2025-07-24T12:00:00', '2025-07-24T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a1c48732-e4ec-41f7-8816-b2aa64908027', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-29T14:15:00', '2025-07-29T15:15:00', 'Conference Room',
    false, null, 4, 0.649, 'manual',
    'productive', 3, 4, 'manual',
    71, 49, '2025-07-29T14:15:00', '2025-07-29T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '06f28a32-2e2a-417f-8255-792e9f5a5f25', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Planning Session', 'Demo analytics data',
    '2025-08-01T13:45:00', '2025-08-01T14:30:00', 'Conference Room',
    false, null, 4, 0.769, 'manual',
    'productive', 5, 4, 'manual',
    63, 58, '2025-08-01T13:45:00', '2025-08-01T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'de773e5b-776c-4429-a0f3-13816747b1b7', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Team Meeting', 'Demo analytics data',
    '2025-07-30T10:15:00', '2025-07-30T11:00:00', 'Conference Room',
    false, null, 1, 0.918, 'bert',
    'productive', 4, 4, 'manual',
    58, 35, '2025-07-30T10:15:00', '2025-07-30T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '07b5b5c0-62b0-4d33-a098-bab0f15861f6', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', 'Project Review', 'Demo analytics data',
    '2025-07-28T16:30:00', '2025-07-28T18:00:00', 'Conference Room',
    false, null, 5, 0.814, 'manual',
    'productive', 5, 4, 'imported',
    105, 77, '2025-07-28T16:30:00', '2025-07-28T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f4ee2b6f-755e-474e-b5fe-e177923b0b77', '27f70f71-d6f9-4d92-80e8-00da1a3a7297', '1:1 Check-in', 'Demo analytics data',
    '2025-07-30T09:45:00', '2025-07-30T11:15:00', 'Conference Room',
    false, null, 5, 0.909, 'bert',
    'productive', 4, 5, 'manual',
    90, 86, '2025-07-30T09:45:00', '2025-07-30T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0f7c9271-8ca1-4f0b-a5c8-cb1873a81187', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-06-10T10:15:00', '2025-06-10T11:00:00', 'Conference Room',
    false, null, 4, 0.648, 'bert',
    'neutral', 4, 4, 'voice',
    39, 30, '2025-06-10T10:15:00', '2025-06-10T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c1f0c6f8-0367-4062-b1bc-754cce491f7c', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-11T12:30:00', '2025-06-11T13:00:00', 'Conference Room',
    false, null, 4, 0.865, 'rule_based',
    'productive', 4, 4, 'imported',
    31, 26, '2025-06-11T12:30:00', '2025-06-11T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2a43c4dc-2850-4b6e-9bc1-d3ef07d9eb53', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-06-11T08:30:00', '2025-06-11T10:00:00', 'Conference Room',
    false, null, 1, 0.683, 'rule_based',
    'productive', 4, 5, 'manual',
    85, 85, '2025-06-11T08:30:00', '2025-06-11T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b37224c6-0532-4cd1-a0da-ff2cc9a1fe80', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-09T10:15:00', '2025-06-09T12:15:00', 'Conference Room',
    false, null, 5, 0.802, 'rule_based',
    'productive', 5, 5, 'text',
    120, 119, '2025-06-09T10:15:00', '2025-06-09T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9f0e4ad9-4c36-405a-be95-578323534e3c', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-11T17:00:00', '2025-06-11T18:30:00', 'Conference Room',
    false, null, 3, 0.774, 'bert',
    'productive', 3, 2, 'voice',
    108, 83, '2025-06-11T17:00:00', '2025-06-11T17:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e6ea47bb-32cc-4ecd-9bfa-2f6ec336bd82', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-12T09:45:00', '2025-06-12T10:30:00', 'Conference Room',
    false, null, 5, 0.631, 'rule_based',
    'neutral', 4, 4, 'imported',
    57, 50, '2025-06-12T09:45:00', '2025-06-12T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '41fc6c4e-0a06-4238-a813-04ef6d97340c', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-06-10T13:15:00', '2025-06-10T15:15:00', 'Conference Room',
    false, null, 4, 0.689, 'manual',
    'neutral', 3, 4, 'voice',
    134, 110, '2025-06-10T13:15:00', '2025-06-10T13:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '33237347-c37b-4e36-be81-3c5cbd19246d', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-11T16:30:00', '2025-06-11T17:30:00', 'Conference Room',
    false, null, 3, 0.697, 'rule_based',
    'neutral', 2, 4, 'imported',
    57, 60, '2025-06-11T16:30:00', '2025-06-11T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6f71e43c-d653-4fd0-9636-5c32e659d780', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-06-11T16:00:00', '2025-06-11T18:00:00', 'Conference Room',
    false, null, 1, 0.934, 'manual',
    'productive', 3, 4, 'imported',
    111, 132, '2025-06-11T16:00:00', '2025-06-11T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7768b552-f432-4851-829c-4580e9a71427', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-06-13T09:00:00', '2025-06-13T09:45:00', 'Conference Room',
    false, null, 5, 0.824, 'rule_based',
    'productive', 5, 5, 'manual',
    60, 35, '2025-06-13T09:00:00', '2025-06-13T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0182416f-e6d6-4034-ac7f-1d201abd6c83', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-06-11T14:45:00', '2025-06-11T16:45:00', 'Conference Room',
    false, null, 3, 0.704, 'rule_based',
    'productive', 3, 2, 'text',
    132, 117, '2025-06-11T14:45:00', '2025-06-11T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1e6d92e9-1b3d-49f8-8785-fc7b5916cc66', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-06-13T14:00:00', '2025-06-13T15:00:00', 'Conference Room',
    false, null, 4, 0.612, 'manual',
    'waste', 2, 3, 'text',
    80, 46, '2025-06-13T14:00:00', '2025-06-13T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7d64d000-0687-42d7-b998-e0730df22083', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-20T15:30:00', '2025-06-20T17:00:00', 'Conference Room',
    false, null, 3, 0.901, 'rule_based',
    'productive', 4, 3, 'voice',
    102, 84, '2025-06-20T15:30:00', '2025-06-20T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '789de1a7-3561-4ccb-b20f-de2afca54e54', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-06-20T09:00:00', '2025-06-20T10:30:00', 'Conference Room',
    false, null, 4, 0.697, 'bert',
    'waste', 4, 4, 'imported',
    82, 93, '2025-06-20T09:00:00', '2025-06-20T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8beaf33e-dd77-489f-bafe-b3ae4216df0a', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-06-20T15:15:00', '2025-06-20T16:00:00', 'Conference Room',
    false, null, 2, 0.802, 'rule_based',
    'productive', 4, 4, 'text',
    62, 55, '2025-06-20T15:15:00', '2025-06-20T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ae945264-2fcc-4f85-a8a4-9af862c21855', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-06-14T09:30:00', '2025-06-14T11:00:00', 'Conference Room',
    false, null, 5, 0.908, 'bert',
    'productive', 5, 5, 'manual',
    110, 94, '2025-06-14T09:30:00', '2025-06-14T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '77b7cd87-6c06-4079-9256-e30c97c99b3a', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-06-19T08:45:00', '2025-06-19T09:15:00', 'Conference Room',
    false, null, 5, 0.785, 'manual',
    'neutral', 5, 5, 'voice',
    29, 42, '2025-06-19T08:45:00', '2025-06-19T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'dbc99196-7eed-4c88-beb3-01f0d186b88c', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-19T09:45:00', '2025-06-19T10:15:00', 'Conference Room',
    false, null, 1, 0.736, 'rule_based',
    'neutral', 4, 5, 'manual',
    31, 15, '2025-06-19T09:45:00', '2025-06-19T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7c503a76-2e73-41c0-9e2f-c77e95d6dc39', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-06-18T14:15:00', '2025-06-18T14:45:00', 'Conference Room',
    false, null, 2, 0.619, 'bert',
    'productive', 3, 2, 'imported',
    20, 44, '2025-06-18T14:15:00', '2025-06-18T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '01ee4fa2-7f27-4b8d-898c-25b6ac6b70fb', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-06-20T10:30:00', '2025-06-20T12:00:00', 'Conference Room',
    false, null, 3, 0.822, 'rule_based',
    'productive', 5, 4, 'manual',
    109, 90, '2025-06-20T10:30:00', '2025-06-20T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1b567790-77ac-4ee8-84d9-25c7a23cd234', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-15T12:15:00', '2025-06-15T13:45:00', 'Conference Room',
    false, null, 3, 0.939, 'manual',
    'productive', 4, 5, 'manual',
    87, 105, '2025-06-15T12:15:00', '2025-06-15T12:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ccf5766d-6b99-47c2-af57-ee5792669cda', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-06-19T12:45:00', '2025-06-19T13:15:00', 'Conference Room',
    false, null, 4, 0.890, 'rule_based',
    'productive', 4, 4, 'manual',
    48, 15, '2025-06-19T12:45:00', '2025-06-19T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '89f7150c-d6f3-4781-9ed0-795aa97a18ba', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-06-19T14:15:00', '2025-06-19T15:45:00', 'Conference Room',
    false, null, 3, 0.732, 'bert',
    'waste', 3, 3, 'voice',
    96, 78, '2025-06-19T14:15:00', '2025-06-19T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0e2d24c6-e852-4cb4-87c8-99a4f325940f', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-19T11:30:00', '2025-06-19T13:00:00', 'Conference Room',
    false, null, 4, 0.814, 'manual',
    'productive', 4, 4, 'imported',
    108, 104, '2025-06-19T11:30:00', '2025-06-19T11:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e0674bb4-a397-484c-bcf9-fad3dad43f4a', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-06-20T13:00:00', '2025-06-20T15:00:00', 'Conference Room',
    false, null, 3, 0.689, 'rule_based',
    'neutral', 3, 2, 'imported',
    118, 105, '2025-06-20T13:00:00', '2025-06-20T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1b817780-14fe-4559-b910-8899f5102485', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-06-27T08:15:00', '2025-06-27T08:45:00', 'Conference Room',
    false, null, 5, 0.732, 'bert',
    'productive', 4, 4, 'manual',
    36, 37, '2025-06-27T08:15:00', '2025-06-27T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'eab3f113-b93b-4f78-90d6-5419e8fdcacb', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-06-26T10:15:00', '2025-06-26T11:00:00', 'Conference Room',
    false, null, 5, 0.933, 'bert',
    'productive', 4, 4, 'voice',
    64, 59, '2025-06-26T10:15:00', '2025-06-26T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '34223305-59b5-4d80-aa8d-5bf5b956b958', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-27T12:30:00', '2025-06-27T14:00:00', 'Conference Room',
    false, null, 5, 0.887, 'bert',
    'productive', 4, 4, 'voice',
    84, 83, '2025-06-27T12:30:00', '2025-06-27T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '62f124d4-b910-4edc-bc2a-9f671df81b32', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-06-27T10:30:00', '2025-06-27T11:15:00', 'Conference Room',
    false, null, 1, 0.940, 'rule_based',
    'waste', 5, 5, 'voice',
    35, 58, '2025-06-27T10:30:00', '2025-06-27T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6f61e723-1515-4b98-a7c9-28b19b9557e0', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-26T11:15:00', '2025-06-26T11:45:00', 'Conference Room',
    false, null, 5, 0.786, 'rule_based',
    'productive', 4, 5, 'text',
    47, 22, '2025-06-26T11:15:00', '2025-06-26T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f69fc85e-3008-41a6-9f86-f58c6bf7824d', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-06-27T15:15:00', '2025-06-27T16:00:00', 'Conference Room',
    false, null, 3, 0.729, 'rule_based',
    'neutral', 3, 3, 'text',
    59, 51, '2025-06-27T15:15:00', '2025-06-27T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a4ec55b1-321a-4880-a86f-66b5f4dd2b3d', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-06-26T08:15:00', '2025-06-26T09:15:00', 'Conference Room',
    false, null, 5, 0.861, 'manual',
    'productive', 5, 4, 'imported',
    67, 75, '2025-06-26T08:15:00', '2025-06-26T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fec9fe38-8c89-48bd-9612-e9852419ea50', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-06-25T15:30:00', '2025-06-25T17:00:00', 'Conference Room',
    false, null, 1, 0.797, 'bert',
    'productive', 3, 3, 'manual',
    92, 99, '2025-06-25T15:30:00', '2025-06-25T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5b464871-af21-441e-a4d7-7755b42aaf3e', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-02T08:45:00', '2025-07-02T09:30:00', 'Conference Room',
    false, null, 5, 0.774, 'manual',
    'productive', 4, 4, 'text',
    39, 55, '2025-07-02T08:45:00', '2025-07-02T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6d8b8e2e-c64b-49e3-a513-a163c180e539', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-01T14:45:00', '2025-07-01T15:45:00', 'Conference Room',
    false, null, 2, 0.882, 'bert',
    'productive', 4, 2, 'voice',
    56, 57, '2025-07-01T14:45:00', '2025-07-01T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3e151e13-e548-4025-99b8-7a425c5d4588', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-06-30T08:15:00', '2025-06-30T09:00:00', 'Conference Room',
    false, null, 4, 0.679, 'bert',
    'neutral', 4, 4, 'text',
    61, 36, '2025-06-30T08:15:00', '2025-06-30T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6a347ffd-ccc7-4c42-b8af-5c7604036498', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-04T08:00:00', '2025-07-04T09:30:00', 'Conference Room',
    false, null, 1, 0.733, 'bert',
    'neutral', 5, 4, 'voice',
    96, 100, '2025-07-04T08:00:00', '2025-07-04T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0648c4d7-dc69-4b89-b84e-f5065c22b1d0', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-03T09:30:00', '2025-07-03T10:15:00', 'Conference Room',
    false, null, 3, 0.697, 'manual',
    'productive', 4, 4, 'manual',
    63, 39, '2025-07-03T09:30:00', '2025-07-03T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a0b3fc6b-0e1e-40c0-ab59-be572a8fa79a', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-06-30T17:00:00', '2025-06-30T19:00:00', 'Conference Room',
    false, null, 4, 0.860, 'rule_based',
    'productive', 4, 2, 'imported',
    118, 130, '2025-06-30T17:00:00', '2025-06-30T17:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e9c6a9fe-54ed-4748-a6d8-4e93da745795', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-07-03T08:15:00', '2025-07-03T10:15:00', 'Conference Room',
    false, null, 3, 0.676, 'bert',
    'waste', 5, 4, 'manual',
    112, 106, '2025-07-03T08:15:00', '2025-07-03T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1b8db75a-af65-4a54-b36d-bf8034ada81f', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-02T11:00:00', '2025-07-02T11:45:00', 'Conference Room',
    false, null, 2, 0.767, 'manual',
    'productive', 4, 5, 'manual',
    39, 44, '2025-07-02T11:00:00', '2025-07-02T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5d371ad2-3f8f-4a7b-9e7e-594954d671ac', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-07-04T15:15:00', '2025-07-04T16:15:00', 'Conference Room',
    false, null, 2, 0.940, 'bert',
    'neutral', 2, 2, 'voice',
    60, 61, '2025-07-04T15:15:00', '2025-07-04T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f59b1db3-6a18-4aa2-b4a0-18d60a24a403', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-08T16:00:00', '2025-07-08T18:00:00', 'Conference Room',
    false, null, 1, 0.868, 'rule_based',
    'neutral', 3, 3, 'manual',
    134, 110, '2025-07-08T16:00:00', '2025-07-08T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fa33a392-ee76-4334-9f5c-11a6b5ed80a7', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-07T16:15:00', '2025-07-07T17:45:00', 'Conference Room',
    false, null, 3, 0.905, 'manual',
    'productive', 2, 3, 'imported',
    80, 89, '2025-07-07T16:15:00', '2025-07-07T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '36df1c96-aa3f-42bb-9f90-3a5578079ef4', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-09T17:45:00', '2025-07-09T19:15:00', 'Conference Room',
    false, null, 4, 0.605, 'rule_based',
    'productive', 3, 3, 'voice',
    80, 78, '2025-07-09T17:45:00', '2025-07-09T17:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'bb22f55c-082d-408c-88dd-da1d77a8eb1f', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-09T14:30:00', '2025-07-09T16:30:00', 'Conference Room',
    false, null, 5, 0.684, 'manual',
    'productive', 3, 4, 'manual',
    122, 119, '2025-07-09T14:30:00', '2025-07-09T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'eb0c66ed-ebd9-436e-a2dd-54f95f9190d7', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-11T10:15:00', '2025-07-11T11:45:00', 'Conference Room',
    false, null, 4, 0.911, 'manual',
    'productive', 5, 5, 'imported',
    102, 82, '2025-07-11T10:15:00', '2025-07-11T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd4290e0d-7e3e-4901-800a-1fff2c5a614f', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-11T17:00:00', '2025-07-11T18:30:00', 'Conference Room',
    false, null, 2, 0.881, 'manual',
    'productive', 3, 2, 'manual',
    107, 85, '2025-07-11T17:00:00', '2025-07-11T17:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '702c57a7-83e5-445a-8435-0d681c16b47f', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-07-10T09:30:00', '2025-07-10T11:00:00', 'Conference Room',
    false, null, 2, 0.900, 'manual',
    'productive', 5, 4, 'text',
    82, 100, '2025-07-10T09:30:00', '2025-07-10T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ec68721c-9a90-4ff8-bbc1-ed48ce7b3db3', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-07-11T10:00:00', '2025-07-11T12:00:00', 'Conference Room',
    false, null, 4, 0.656, 'rule_based',
    'neutral', 5, 4, 'manual',
    118, 105, '2025-07-11T10:00:00', '2025-07-11T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '626467ee-5d0f-495b-ad75-e88ed65c01fd', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-10T12:45:00', '2025-07-10T13:15:00', 'Conference Room',
    false, null, 2, 0.823, 'rule_based',
    'productive', 4, 5, 'voice',
    45, 27, '2025-07-10T12:45:00', '2025-07-10T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd405e9c9-e8c5-465f-80f3-2fd82088a22b', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-16T16:45:00', '2025-07-16T18:15:00', 'Conference Room',
    false, null, 3, 0.772, 'manual',
    'waste', 2, 4, 'imported',
    92, 78, '2025-07-16T16:45:00', '2025-07-16T16:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c6544fc3-54e8-4ec5-abf2-584374ef385e', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-07-14T16:45:00', '2025-07-14T17:30:00', 'Conference Room',
    false, null, 2, 0.795, 'bert',
    'productive', 3, 4, 'voice',
    40, 51, '2025-07-14T16:45:00', '2025-07-14T16:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e318c528-5008-4e9c-ba38-b61a5f132813', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-13T14:45:00', '2025-07-13T16:15:00', 'Conference Room',
    false, null, 4, 0.749, 'bert',
    'waste', 2, 2, 'text',
    108, 80, '2025-07-13T14:45:00', '2025-07-13T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c4e18027-f858-41f1-b491-4241808afb4f', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-07-15T10:30:00', '2025-07-15T11:15:00', 'Conference Room',
    false, null, 4, 0.902, 'manual',
    'productive', 5, 5, 'voice',
    53, 49, '2025-07-15T10:30:00', '2025-07-15T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'aa4135d7-2745-4732-b66e-f7fbfcd94058', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-14T16:15:00', '2025-07-14T17:45:00', 'Conference Room',
    false, null, 3, 0.811, 'bert',
    'productive', 4, 2, 'manual',
    101, 88, '2025-07-14T16:15:00', '2025-07-14T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '496a867a-d59f-42a7-a99d-b8fc483c39db', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-16T15:45:00', '2025-07-16T17:45:00', 'Conference Room',
    false, null, 3, 0.755, 'manual',
    'neutral', 4, 2, 'imported',
    112, 112, '2025-07-16T15:45:00', '2025-07-16T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f7e1fbdd-88e7-44d0-969c-8848c857ceb5', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-14T12:00:00', '2025-07-14T13:00:00', 'Conference Room',
    false, null, 5, 0.790, 'rule_based',
    'productive', 5, 5, 'voice',
    69, 61, '2025-07-14T12:00:00', '2025-07-14T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9c30970f-a57a-4569-8eea-beec0b074d04', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-16T09:30:00', '2025-07-16T11:30:00', 'Conference Room',
    false, null, 4, 0.799, 'bert',
    'neutral', 4, 4, 'manual',
    121, 122, '2025-07-16T09:30:00', '2025-07-16T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8b0b8411-8419-4721-b387-b283bf338e9a', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-15T10:00:00', '2025-07-15T12:00:00', 'Conference Room',
    false, null, 4, 0.710, 'manual',
    'neutral', 5, 4, 'text',
    140, 129, '2025-07-15T10:00:00', '2025-07-15T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a6a15215-c669-4200-a595-a8eae89536f3', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-23T12:00:00', '2025-07-23T13:30:00', 'Conference Room',
    false, null, 1, 0.634, 'bert',
    'neutral', 4, 4, 'voice',
    99, 87, '2025-07-23T12:00:00', '2025-07-23T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'cff24db6-67b0-462d-80e9-8dadd747554c', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-25T16:15:00', '2025-07-25T17:15:00', 'Conference Room',
    false, null, 2, 0.871, 'rule_based',
    'neutral', 3, 4, 'voice',
    54, 53, '2025-07-25T16:15:00', '2025-07-25T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a67c0a4f-a9c9-44d6-85c0-14e67802b50e', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-22T10:45:00', '2025-07-22T11:15:00', 'Conference Room',
    false, null, 3, 0.758, 'rule_based',
    'productive', 5, 4, 'text',
    40, 37, '2025-07-22T10:45:00', '2025-07-22T10:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '94fcfc85-0276-4ab5-ae59-3bac78b82368', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-19T13:45:00', '2025-07-19T14:45:00', 'Conference Room',
    false, null, 1, 0.931, 'rule_based',
    'neutral', 4, 2, 'voice',
    62, 62, '2025-07-19T13:45:00', '2025-07-19T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c6b59ac9-1b4c-44a2-a239-82ece2233412', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-24T08:15:00', '2025-07-24T10:15:00', 'Conference Room',
    false, null, 5, 0.817, 'rule_based',
    'productive', 4, 4, 'text',
    114, 105, '2025-07-24T08:15:00', '2025-07-24T08:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '788d6e83-9a1f-40db-ad5c-81031e3be283', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-07-22T09:30:00', '2025-07-22T11:00:00', 'Conference Room',
    false, null, 1, 0.725, 'rule_based',
    'productive', 5, 5, 'voice',
    90, 104, '2025-07-22T09:30:00', '2025-07-22T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '45b97202-5808-453b-a2dd-27096382f537', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-07-24T11:45:00', '2025-07-24T12:45:00', 'Conference Room',
    false, null, 3, 0.833, 'manual',
    'productive', 5, 5, 'manual',
    78, 65, '2025-07-24T11:45:00', '2025-07-24T11:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0dec452d-ad9d-4300-8690-f5990d539edf', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-08-01T17:15:00', '2025-08-01T17:45:00', 'Conference Room',
    false, null, 4, 0.734, 'bert',
    'neutral', 3, 3, 'text',
    47, 20, '2025-08-01T17:15:00', '2025-08-01T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e6798930-050e-49d1-9752-1e743e9c64c8', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-08-01T13:00:00', '2025-08-01T15:00:00', 'Conference Room',
    false, null, 5, 0.700, 'rule_based',
    'waste', 2, 4, 'text',
    140, 106, '2025-08-01T13:00:00', '2025-08-01T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c806387b-5101-4da2-86de-f8a0aa219831', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Client Call', 'Demo analytics data',
    '2025-07-30T17:45:00', '2025-07-30T18:15:00', 'Conference Room',
    false, null, 1, 0.801, 'bert',
    'productive', 2, 2, 'voice',
    49, 42, '2025-07-30T17:45:00', '2025-07-30T17:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '78b6cf4e-9610-4b02-a606-87db88d99f86', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-08-01T16:15:00', '2025-08-01T16:45:00', 'Conference Room',
    false, null, 5, 0.865, 'bert',
    'waste', 2, 2, 'text',
    30, 40, '2025-08-01T16:15:00', '2025-08-01T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '393afbca-8548-47e9-82ff-38d8c7fa249e', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', '1:1 Check-in', 'Demo analytics data',
    '2025-07-31T12:30:00', '2025-07-31T14:00:00', 'Conference Room',
    false, null, 3, 0.754, 'bert',
    'neutral', 5, 4, 'imported',
    101, 87, '2025-07-31T12:30:00', '2025-07-31T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd21296f3-3524-4ad5-89e8-b51c60491b8b', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Planning Session', 'Demo analytics data',
    '2025-07-27T14:15:00', '2025-07-27T14:45:00', 'Conference Room',
    false, null, 5, 0.629, 'manual',
    'neutral', 3, 4, 'voice',
    50, 16, '2025-07-27T14:15:00', '2025-07-27T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '47c88087-d120-4f48-8569-2ed83658f3da', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-07-27T08:30:00', '2025-07-27T09:15:00', 'Conference Room',
    false, null, 5, 0.816, 'manual',
    'neutral', 4, 4, 'manual',
    38, 50, '2025-07-27T08:30:00', '2025-07-27T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '13d20fc6-ac8c-4255-b017-b4f118c1caa2', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Team Meeting', 'Demo analytics data',
    '2025-07-29T13:00:00', '2025-07-29T13:45:00', 'Conference Room',
    false, null, 5, 0.758, 'rule_based',
    'neutral', 2, 2, 'voice',
    37, 37, '2025-07-29T13:00:00', '2025-07-29T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '06465aad-fcdd-48fe-b5bf-0469469ad210', 'ac88fcb8-3e34-4d96-8410-ff2459dbd37f', 'Project Review', 'Demo analytics data',
    '2025-07-29T10:15:00', '2025-07-29T11:15:00', 'Conference Room',
    false, null, 4, 0.710, 'rule_based',
    'productive', 5, 4, 'manual',
    64, 55, '2025-07-29T10:15:00', '2025-07-29T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fed14c46-b2a0-486a-98c9-90b90bfbaa05', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-06-08T12:30:00', '2025-06-08T14:30:00', 'Conference Room',
    false, null, 2, 0.932, 'bert',
    'productive', 2, 2, 'text',
    130, 127, '2025-06-08T12:30:00', '2025-06-08T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f1854c7c-8d28-4752-8264-d0d4abbde905', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-06-09T08:30:00', '2025-06-09T10:00:00', 'Conference Room',
    false, null, 5, 0.819, 'rule_based',
    'productive', 3, 2, 'imported',
    109, 103, '2025-06-09T08:30:00', '2025-06-09T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5487fb23-c7c8-4fa3-9677-ba6f893bc427', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-06-09T15:00:00', '2025-06-09T17:00:00', 'Conference Room',
    false, null, 2, 0.691, 'bert',
    'productive', 4, 5, 'voice',
    136, 118, '2025-06-09T15:00:00', '2025-06-09T15:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '6315287c-eb8c-4b8f-9362-688dca124402', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-10T12:45:00', '2025-06-10T14:45:00', 'Conference Room',
    false, null, 4, 0.779, 'rule_based',
    'productive', 3, 3, 'voice',
    133, 125, '2025-06-10T12:45:00', '2025-06-10T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '74b55c2f-df25-4415-a709-81ed88b82dbc', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-06-08T15:15:00', '2025-06-08T15:45:00', 'Conference Room',
    false, null, 5, 0.812, 'manual',
    'neutral', 4, 4, 'voice',
    29, 20, '2025-06-08T15:15:00', '2025-06-08T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2d89d022-6125-4f3f-ac56-f9f5fd2c5848', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-10T10:30:00', '2025-06-10T11:00:00', 'Conference Room',
    false, null, 2, 0.769, 'bert',
    'neutral', 3, 2, 'voice',
    46, 16, '2025-06-10T10:30:00', '2025-06-10T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '4d2c8782-f0c9-4bda-9c1f-80532cdffd9f', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-13T08:00:00', '2025-06-13T09:00:00', 'Conference Room',
    false, null, 3, 0.786, 'manual',
    'neutral', 3, 2, 'manual',
    57, 71, '2025-06-13T08:00:00', '2025-06-13T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f44a4e8f-8d82-4b5a-85a9-9e0899f92a56', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-06-13T14:00:00', '2025-06-13T16:00:00', 'Conference Room',
    false, null, 3, 0.739, 'bert',
    'productive', 4, 5, 'imported',
    130, 134, '2025-06-13T14:00:00', '2025-06-13T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a6aad08a-b98e-46f9-892b-4f579f080b07', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-09T15:45:00', '2025-06-09T16:30:00', 'Conference Room',
    false, null, 3, 0.733, 'bert',
    'neutral', 4, 3, 'text',
    54, 36, '2025-06-09T15:45:00', '2025-06-09T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b8dbdd08-42b9-4fea-8696-bba37157c249', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-12T13:15:00', '2025-06-12T15:15:00', 'Conference Room',
    false, null, 4, 0.703, 'rule_based',
    'productive', 5, 3, 'imported',
    130, 110, '2025-06-12T13:15:00', '2025-06-12T13:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f2933c23-52ef-4de4-b340-6bb21bab0f87', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-06-11T09:30:00', '2025-06-11T10:30:00', 'Conference Room',
    false, null, 3, 0.799, 'manual',
    'waste', 2, 3, 'voice',
    56, 47, '2025-06-11T09:30:00', '2025-06-11T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c6022c01-fba3-4539-9126-fba6ecb2e268', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-16T15:15:00', '2025-06-16T15:45:00', 'Conference Room',
    false, null, 2, 0.917, 'bert',
    'productive', 4, 5, 'imported',
    32, 20, '2025-06-16T15:15:00', '2025-06-16T15:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9dba0192-6acc-4548-9f3a-3e142096d163', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-06-17T14:15:00', '2025-06-17T15:00:00', 'Conference Room',
    false, null, 2, 0.896, 'manual',
    'productive', 4, 5, 'voice',
    36, 34, '2025-06-17T14:15:00', '2025-06-17T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '50bfc75a-c67b-4600-8b82-b1ebdb089757', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-19T11:45:00', '2025-06-19T12:15:00', 'Conference Room',
    false, null, 5, 0.900, 'manual',
    'neutral', 3, 2, 'manual',
    25, 24, '2025-06-19T11:45:00', '2025-06-19T11:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '122db7c8-6f3f-4295-8ec7-9197bee74374', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-18T10:45:00', '2025-06-18T11:30:00', 'Conference Room',
    false, null, 1, 0.819, 'rule_based',
    'productive', 2, 3, 'imported',
    55, 35, '2025-06-18T10:45:00', '2025-06-18T10:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '51a9538e-76b8-442b-bf2f-6caac745cd41', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-06-18T13:00:00', '2025-06-18T13:45:00', 'Conference Room',
    false, null, 2, 0.835, 'bert',
    'productive', 4, 3, 'imported',
    63, 39, '2025-06-18T13:00:00', '2025-06-18T13:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'fc260b3b-65fd-4918-8a43-ec402898d7a8', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-20T11:00:00', '2025-06-20T11:45:00', 'Conference Room',
    false, null, 2, 0.781, 'bert',
    'waste', 2, 3, 'imported',
    44, 57, '2025-06-20T11:00:00', '2025-06-20T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1025931b-4b1e-47de-bff5-54b59c557cca', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-15T14:30:00', '2025-06-15T16:30:00', 'Conference Room',
    false, null, 2, 0.741, 'rule_based',
    'neutral', 5, 5, 'manual',
    120, 105, '2025-06-15T14:30:00', '2025-06-15T14:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '24439c09-7505-4e33-9035-212780d912bb', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-06-20T10:00:00', '2025-06-20T11:00:00', 'Conference Room',
    false, null, 4, 0.824, 'bert',
    'waste', 2, 3, 'imported',
    59, 56, '2025-06-20T10:00:00', '2025-06-20T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '89a6f9eb-598d-45be-9bd7-9eac47bb9763', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-18T14:45:00', '2025-06-18T15:30:00', 'Conference Room',
    false, null, 3, 0.950, 'bert',
    'productive', 4, 4, 'voice',
    52, 41, '2025-06-18T14:45:00', '2025-06-18T14:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0691c2fa-efeb-457b-b314-c7f66312fed3', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-23T15:45:00', '2025-06-23T17:45:00', 'Conference Room',
    false, null, 1, 0.660, 'manual',
    'productive', 4, 4, 'text',
    116, 118, '2025-06-23T15:45:00', '2025-06-23T15:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '738b1222-a54a-4c28-8fc9-98694e463df4', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-23T17:30:00', '2025-06-23T19:00:00', 'Conference Room',
    false, null, 4, 0.641, 'manual',
    'neutral', 4, 3, 'voice',
    103, 102, '2025-06-23T17:30:00', '2025-06-23T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'da3ea3f7-2a23-4fde-93c6-b7a64c650723', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-06-26T17:30:00', '2025-06-26T18:15:00', 'Conference Room',
    false, null, 5, 0.679, 'manual',
    'productive', 4, 4, 'text',
    49, 45, '2025-06-26T17:30:00', '2025-06-26T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '27c2aac7-f359-4633-ab0c-8dc5f75229d9', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-06-25T15:30:00', '2025-06-25T16:00:00', 'Conference Room',
    false, null, 3, 0.633, 'manual',
    'productive', 5, 3, 'voice',
    30, 37, '2025-06-25T15:30:00', '2025-06-25T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '4837f7ff-3b85-4ead-b75b-bc9a4fe03a17', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-06-24T16:00:00', '2025-06-24T16:45:00', 'Conference Room',
    false, null, 3, 0.705, 'bert',
    'productive', 4, 3, 'imported',
    48, 32, '2025-06-24T16:00:00', '2025-06-24T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9d97c53f-33c4-4b56-a947-28dbfefcb1bc', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-06-26T12:00:00', '2025-06-26T14:00:00', 'Conference Room',
    false, null, 4, 0.853, 'rule_based',
    'waste', 3, 3, 'voice',
    116, 113, '2025-06-26T12:00:00', '2025-06-26T12:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ed39b77a-2e5c-48ec-8f86-82169f2f3bed', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-23T09:30:00', '2025-06-23T11:00:00', 'Conference Room',
    false, null, 5, 0.789, 'rule_based',
    'neutral', 3, 2, 'text',
    105, 86, '2025-06-23T09:30:00', '2025-06-23T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ce0647f2-81c6-4705-a89d-ffd0bd0b3175', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-23T12:30:00', '2025-06-23T13:15:00', 'Conference Room',
    false, null, 1, 0.664, 'manual',
    'neutral', 3, 2, 'manual',
    60, 56, '2025-06-23T12:30:00', '2025-06-23T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2922bb26-bd3b-41fb-9859-f05d84a712dc', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-06-24T15:30:00', '2025-06-24T16:30:00', 'Conference Room',
    false, null, 3, 0.802, 'manual',
    'productive', 4, 3, 'text',
    53, 52, '2025-06-24T15:30:00', '2025-06-24T15:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '0afc692b-24be-4b00-8bc9-87c1f7bb1dbb', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-06-23T12:45:00', '2025-06-23T14:15:00', 'Conference Room',
    false, null, 4, 0.941, 'bert',
    'waste', 2, 3, 'imported',
    99, 89, '2025-06-23T12:45:00', '2025-06-23T12:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3d847e20-ffae-4cd5-b9e5-a4e10b0839de', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-27T09:30:00', '2025-06-27T10:30:00', 'Conference Room',
    false, null, 4, 0.856, 'rule_based',
    'neutral', 3, 3, 'manual',
    77, 52, '2025-06-27T09:30:00', '2025-06-27T09:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '88e4cb6a-5daa-4f1f-a504-71201a40c2dd', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-06-23T09:45:00', '2025-06-23T11:15:00', 'Conference Room',
    false, null, 2, 0.928, 'bert',
    'neutral', 3, 2, 'text',
    97, 89, '2025-06-23T09:45:00', '2025-06-23T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2d4fda43-d3bc-47b0-9a7f-dec9259edb13', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-04T10:15:00', '2025-07-04T12:15:00', 'Conference Room',
    false, null, 5, 0.873, 'manual',
    'productive', 3, 3, 'manual',
    113, 133, '2025-07-04T10:15:00', '2025-07-04T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'bfda7289-2119-4b59-8678-0a1ce8ce83a7', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-07-04T10:30:00', '2025-07-04T11:15:00', 'Conference Room',
    false, null, 3, 0.729, 'bert',
    'neutral', 3, 3, 'voice',
    36, 50, '2025-07-04T10:30:00', '2025-07-04T10:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f3f85172-2a1f-48c2-95a1-6d707a068037', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-06-30T16:15:00', '2025-06-30T17:15:00', 'Conference Room',
    false, null, 3, 0.730, 'bert',
    'neutral', 4, 5, 'voice',
    61, 48, '2025-06-30T16:15:00', '2025-06-30T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '604463ee-699b-4c0a-9a3c-6bd98a1caa31', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-02T09:15:00', '2025-07-02T09:45:00', 'Conference Room',
    false, null, 3, 0.855, 'bert',
    'neutral', 3, 3, 'voice',
    38, 20, '2025-07-02T09:15:00', '2025-07-02T09:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'a3810d3b-f68e-4040-9037-b6408db9e11a', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-07-04T11:00:00', '2025-07-04T13:00:00', 'Conference Room',
    false, null, 3, 0.885, 'rule_based',
    'productive', 3, 2, 'text',
    117, 111, '2025-07-04T11:00:00', '2025-07-04T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '4b9bd367-f94f-4e12-93a9-eb5082203ec4', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-03T13:30:00', '2025-07-03T14:30:00', 'Conference Room',
    false, null, 4, 0.823, 'bert',
    'neutral', 4, 3, 'voice',
    63, 50, '2025-07-03T13:30:00', '2025-07-03T13:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8671805b-bd11-4816-828d-8ac28ba4bc36', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-03T10:45:00', '2025-07-03T12:45:00', 'Conference Room',
    false, null, 5, 0.941, 'manual',
    'productive', 3, 3, 'voice',
    127, 119, '2025-07-03T10:45:00', '2025-07-03T10:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '1ec3493a-33f3-49c0-8195-e3f27f05d2b9', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-02T13:45:00', '2025-07-02T14:30:00', 'Conference Room',
    false, null, 5, 0.934, 'manual',
    'productive', 4, 5, 'imported',
    48, 38, '2025-07-02T13:45:00', '2025-07-02T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '82598e22-0ac5-4599-827a-be71b05190a9', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-10T11:45:00', '2025-07-10T12:30:00', 'Conference Room',
    false, null, 2, 0.627, 'rule_based',
    'productive', 3, 2, 'voice',
    49, 33, '2025-07-10T11:45:00', '2025-07-10T11:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '2dd526d3-0d88-437a-bf4c-a0f403a6e34e', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-08T16:15:00', '2025-07-08T17:45:00', 'Conference Room',
    false, null, 2, 0.699, 'bert',
    'neutral', 4, 4, 'text',
    85, 99, '2025-07-08T16:15:00', '2025-07-08T16:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'd4941db4-b83c-4f6e-a3ca-7114ebd638eb', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-07-07T17:45:00', '2025-07-07T19:45:00', 'Conference Room',
    false, null, 1, 0.645, 'rule_based',
    'neutral', 5, 3, 'manual',
    128, 110, '2025-07-07T17:45:00', '2025-07-07T17:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '896a124e-2285-4fdb-bfd6-6723ceb7095d', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-07-11T17:45:00', '2025-07-11T18:45:00', 'Conference Room',
    false, null, 5, 0.681, 'manual',
    'waste', 5, 5, 'voice',
    56, 68, '2025-07-11T17:45:00', '2025-07-11T17:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8ff13b27-edc0-4cab-9200-967bcea85fef', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-05T09:45:00', '2025-07-05T11:45:00', 'Conference Room',
    false, null, 3, 0.834, 'bert',
    'waste', 2, 3, 'voice',
    120, 112, '2025-07-05T09:45:00', '2025-07-05T09:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '46e811a7-3171-4d1b-985d-6f0aa1d12b4e', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-06T10:15:00', '2025-07-06T11:45:00', 'Conference Room',
    false, null, 1, 0.876, 'manual',
    'productive', 3, 2, 'manual',
    88, 89, '2025-07-06T10:15:00', '2025-07-06T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8338a9ef-af86-4f6d-acc3-7403975aaab0', 'b017910f-479e-4871-a343-d375f5505403', 'Team Meeting', 'Demo analytics data',
    '2025-07-08T17:30:00', '2025-07-08T18:15:00', 'Conference Room',
    false, null, 5, 0.788, 'rule_based',
    'productive', 4, 5, 'text',
    65, 37, '2025-07-08T17:30:00', '2025-07-08T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f3b9424f-854b-4890-92dd-3b8ae5b26fb5', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-07-09T08:45:00', '2025-07-09T10:45:00', 'Conference Room',
    false, null, 4, 0.824, 'bert',
    'neutral', 3, 3, 'manual',
    112, 114, '2025-07-09T08:45:00', '2025-07-09T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ca15a350-9b26-4f4e-a5af-e2722e27fa06', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-10T15:00:00', '2025-07-10T16:00:00', 'Conference Room',
    false, null, 4, 0.905, 'rule_based',
    'neutral', 5, 5, 'voice',
    63, 64, '2025-07-10T15:00:00', '2025-07-10T15:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8c720c24-4f17-4530-b0c8-31eb96b75288', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-07T13:45:00', '2025-07-07T14:45:00', 'Conference Room',
    false, null, 4, 0.828, 'bert',
    'productive', 4, 3, 'manual',
    78, 50, '2025-07-07T13:45:00', '2025-07-07T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '63da8b78-cd05-46c6-a659-ff4122843d34', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-07-17T11:00:00', '2025-07-17T11:45:00', 'Conference Room',
    false, null, 2, 0.879, 'rule_based',
    'neutral', 2, 2, 'text',
    61, 53, '2025-07-17T11:00:00', '2025-07-17T11:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'b653fc94-17bd-4a89-9de7-c186edb8d7d5', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-16T08:45:00', '2025-07-16T09:30:00', 'Conference Room',
    false, null, 3, 0.896, 'manual',
    'neutral', 3, 2, 'voice',
    36, 45, '2025-07-16T08:45:00', '2025-07-16T08:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f49bb611-7462-4518-9bc6-b2d2979cb4df', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-07-15T14:00:00', '2025-07-15T16:00:00', 'Conference Room',
    false, null, 5, 0.633, 'manual',
    'waste', 4, 4, 'voice',
    111, 132, '2025-07-15T14:00:00', '2025-07-15T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '12cf03fe-afe0-42a0-adaa-2822537f49dd', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-07-15T10:15:00', '2025-07-15T11:45:00', 'Conference Room',
    false, null, 3, 0.847, 'rule_based',
    'productive', 2, 3, 'text',
    95, 92, '2025-07-15T10:15:00', '2025-07-15T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e05fe18e-8194-491d-b60e-ac13ef525718', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-15T14:15:00', '2025-07-15T14:45:00', 'Conference Room',
    false, null, 4, 0.886, 'bert',
    'productive', 4, 4, 'voice',
    24, 44, '2025-07-15T14:15:00', '2025-07-15T14:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '818bb4ab-041a-48fe-8176-2bd37dcbac59', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-17T11:15:00', '2025-07-17T11:45:00', 'Conference Room',
    false, null, 5, 0.816, 'rule_based',
    'productive', 3, 2, 'text',
    24, 32, '2025-07-17T11:15:00', '2025-07-17T11:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5b67fa1f-7194-44af-8060-eb0f11789324', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-23T17:00:00', '2025-07-23T17:45:00', 'Conference Room',
    false, null, 5, 0.742, 'manual',
    'productive', 4, 3, 'manual',
    38, 38, '2025-07-23T17:00:00', '2025-07-23T17:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '66d69954-0036-478b-ae0e-e493b185ad5b', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-07-22T17:30:00', '2025-07-22T18:15:00', 'Conference Room',
    false, null, 2, 0.808, 'rule_based',
    'productive', 4, 5, 'manual',
    45, 60, '2025-07-22T17:30:00', '2025-07-22T17:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9768d550-071e-4841-992a-37b5d8f3968e', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-21T09:00:00', '2025-07-21T10:30:00', 'Conference Room',
    false, null, 4, 0.726, 'manual',
    'neutral', 3, 3, 'voice',
    107, 98, '2025-07-21T09:00:00', '2025-07-21T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '071edbb9-0891-49bf-be4b-f0c95703be85', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-22T09:00:00', '2025-07-22T10:00:00', 'Conference Room',
    false, null, 4, 0.942, 'manual',
    'productive', 3, 2, 'voice',
    78, 49, '2025-07-22T09:00:00', '2025-07-22T09:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '7e815574-aa25-45a1-99b7-dc0e130593bc', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-25T16:00:00', '2025-07-25T16:45:00', 'Conference Room',
    false, null, 1, 0.818, 'manual',
    'neutral', 4, 4, 'text',
    65, 42, '2025-07-25T16:00:00', '2025-07-25T16:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '3a49bb5d-8eae-499b-a556-88d1a2c1e30d', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-07-25T10:00:00', '2025-07-25T12:00:00', 'Conference Room',
    false, null, 1, 0.862, 'rule_based',
    'waste', 3, 3, 'text',
    139, 135, '2025-07-25T10:00:00', '2025-07-25T10:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '04bc91e9-7856-495b-9b59-19635538bf7c', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-07-24T17:15:00', '2025-07-24T17:45:00', 'Conference Room',
    false, null, 5, 0.621, 'bert',
    'productive', 4, 4, 'text',
    25, 34, '2025-07-24T17:15:00', '2025-07-24T17:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '8497f285-c44f-4d30-88b2-eb4b321e18e9', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-22T16:30:00', '2025-07-22T18:00:00', 'Conference Room',
    false, null, 3, 0.936, 'bert',
    'productive', 5, 3, 'imported',
    92, 103, '2025-07-22T16:30:00', '2025-07-22T16:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'af445e6a-7749-424a-a98d-d0d0470b07c7', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-08-01T12:15:00', '2025-08-01T13:45:00', 'Conference Room',
    false, null, 5, 0.946, 'rule_based',
    'neutral', 2, 3, 'imported',
    81, 90, '2025-08-01T12:15:00', '2025-08-01T12:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '9fca3afc-7889-4079-99ae-59dbd2286890', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-08-01T13:45:00', '2025-08-01T15:15:00', 'Conference Room',
    false, null, 1, 0.734, 'manual',
    'productive', 4, 4, 'voice',
    80, 93, '2025-08-01T13:45:00', '2025-08-01T13:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'ac0397c7-713e-46ed-b843-3ba754a614ce', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-29T10:15:00', '2025-07-29T12:15:00', 'Conference Room',
    false, null, 1, 0.849, 'bert',
    'waste', 2, 3, 'voice',
    135, 117, '2025-07-29T10:15:00', '2025-07-29T10:15:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '5107cae8-d28e-4777-89b8-5944211ceb07', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-31T16:45:00', '2025-07-31T18:15:00', 'Conference Room',
    false, null, 3, 0.913, 'rule_based',
    'waste', 5, 5, 'imported',
    82, 102, '2025-07-31T16:45:00', '2025-07-31T16:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'f14a3101-73a6-4b81-94a4-8b42e5887501', 'b017910f-479e-4871-a343-d375f5505403', '1:1 Check-in', 'Demo analytics data',
    '2025-07-30T08:30:00', '2025-07-30T09:00:00', 'Conference Room',
    false, null, 1, 0.815, 'bert',
    'productive', 3, 2, 'manual',
    44, 44, '2025-07-30T08:30:00', '2025-07-30T08:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'cb5b6727-5439-44df-bdca-29b4832a5b81', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-07-27T17:45:00', '2025-07-27T19:15:00', 'Conference Room',
    false, null, 4, 0.697, 'bert',
    'productive', 5, 5, 'manual',
    108, 76, '2025-07-27T17:45:00', '2025-07-27T17:45:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '94b75ac2-68a1-47ca-bc89-132445d05d3b', 'b017910f-479e-4871-a343-d375f5505403', 'Client Call', 'Demo analytics data',
    '2025-07-29T08:00:00', '2025-07-29T10:00:00', 'Conference Room',
    false, null, 5, 0.743, 'rule_based',
    'productive', 2, 3, 'voice',
    114, 131, '2025-07-29T08:00:00', '2025-07-29T08:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    '020ed166-f647-42f0-8b15-8ff901b4d488', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-30T12:30:00', '2025-07-30T14:30:00', 'Conference Room',
    false, null, 5, 0.852, 'bert',
    'waste', 2, 2, 'voice',
    112, 125, '2025-07-30T12:30:00', '2025-07-30T12:30:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'e07f2cd9-cedb-4b98-bf91-f9a0db6ba918', 'b017910f-479e-4871-a343-d375f5505403', 'Project Review', 'Demo analytics data',
    '2025-07-29T14:00:00', '2025-07-29T16:00:00', 'Conference Room',
    false, null, 5, 0.914, 'manual',
    'productive', 4, 5, 'voice',
    111, 118, '2025-07-29T14:00:00', '2025-07-29T14:00:00'
);

INSERT INTO events (
    id, user_id, title, description, start_time, end_time, location, is_all_day,
    recurrence_rule, priority_level, priority_confidence, classification_method,
    meeting_outcome, effectiveness_rating, energy_level, created_via,
    actual_duration, planned_duration, created_at, updated_at
) VALUES (
    'c89e903b-7437-4145-9ee6-3b3fa32fabfd', 'b017910f-479e-4871-a343-d375f5505403', 'Planning Session', 'Demo analytics data',
    '2025-07-30T12:45:00', '2025-07-30T13:15:00', 'Conference Room',
    false, null, 1, 0.647, 'bert',
    'waste', 2, 3, 'voice',
    23, 21, '2025-07-30T12:45:00', '2025-07-30T12:45:00'
);