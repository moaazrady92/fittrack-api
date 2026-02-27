-- This script runs when PostgreSQL starts for the FIRST TIME
-- Sets up additional configuration

-- Create extensions (PostgreSQL superpowers!)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- For UUIDs
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- For better text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";  -- For better indexing

-- Set database parameters for better performance
ALTER DATABASE workoutdb SET timezone TO 'UTC';  -- fixes timezone bugs and incorrect dates
ALTER DATABASE workoutdb SET datestyle TO 'ISO, DMY'; -- sets dates to yyyy-mm--dd format