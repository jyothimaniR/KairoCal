INSERT INTO users (id, cognito_sub, email, full_name, preferences, is_active, created_at, updated_at) 
VALUES (gen_random_uuid(), 'test-user-1', 'test@example.com', 'Test User', '{"theme": "light"}', true, NOW(), NOW()) 
ON CONFLICT (email) DO NOTHING;

SELECT id, email, full_name FROM users;
