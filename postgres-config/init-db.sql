-- create-user.sql
-- Create user with encrypted password for external connections

-- Drop user if exists (for clean setup)
DROP USER IF EXISTS kairocal_user;

-- Create user with encrypted password
CREATE USER kairocal_user WITH 
    ENCRYPTED PASSWORD 'kairocal_password'
    CREATEDB 
    CREATEROLE 
    LOGIN;

-- Grant superuser privileges (for development)
ALTER USER kairocal_user WITH SUPERUSER;

-- Connect to kairocal database
\c kairocal;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE kairocal TO kairocal_user;
GRANT ALL ON SCHEMA public TO kairocal_user;

-- Set default privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO kairocal_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO kairocal_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO kairocal_user;

-- Create useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Verify user creation
SELECT rolname, rolcanlogin, rolpassword IS NOT NULL as has_encrypted_password 
FROM pg_roles WHERE rolname = 'kairocal_user';

SELECT 'KairoCal user created with encrypted password!' as status;