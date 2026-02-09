-- This script runs when PostgreSQL starts for the FIRST TIME
-- Sets up additional configuration

-- Create extensions (PostgreSQL superpowers!)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- For UUIDs
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- For better text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";  -- For better indexing

-- Create additional database roles if needed
-- DO $$
-- BEGIN
--     IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'readonly_user') THEN
--         CREATE ROLE readonly_user WITH LOGIN PASSWORD 'readonly_pass';
--     END IF;
-- END $$;

-- Set database parameters for better performance
ALTER DATABASE workoutdb SET timezone TO 'UTC';
ALTER DATABASE workoutdb SET datestyle TO 'ISO, DMY';