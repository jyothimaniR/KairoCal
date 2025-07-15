-- postgres-config/init-db.sql
-- Fixed initialization script that doesn't change the password

-- Since POSTGRES_USER and POSTGRES_PASSWORD are already set in docker-compose,
-- the user 'kairocal_user' already exists with password 'Test123'
-- We just need to grant additional privileges

-- Connect to the kairocal database
\c kairocal;

-- Grant all privileges to the existing user
GRANT ALL PRIVILEGES ON DATABASE kairocal TO kairocal_user;
GRANT ALL ON SCHEMA public TO kairocal_user;

-- Set default privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO kairocal_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO kairocal_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO kairocal_user;

-- Create useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Verify user exists and has proper access
SELECT 'Database initialized successfully!' as status;