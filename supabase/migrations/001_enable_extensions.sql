-- Enable required PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS vector;
-- Note: TimescaleDB is not available in Supabase free tier
-- If needed, use regular PostgreSQL tables with proper indexing

