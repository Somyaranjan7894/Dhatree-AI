-- =============================================================================
-- Dhatree AI PostgreSQL Initialization Script
-- Executed on container startup if database cluster is empty
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis"; -- For future spatial farm mapping & coordinates
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fast text search indexing across crop/disease names

-- Set standard timezone to UTC
ALTER DATABASE dhatree_ai_db SET timezone TO 'UTC';
