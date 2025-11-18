-- Create price_data table for time-series data
-- Note: Supabase doesn't support TimescaleDB, so we use regular PostgreSQL with proper indexing
CREATE TABLE IF NOT EXISTS price_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    open_price DOUBLE PRECISION,
    high_price DOUBLE PRECISION,
    low_price DOUBLE PRECISION,
    close_price DOUBLE PRECISION,
    volume BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for efficient time-series queries
CREATE INDEX IF NOT EXISTS idx_price_data_symbol_timestamp ON price_data(symbol, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_price_data_timestamp ON price_data(timestamp DESC);

-- Create unique constraint to prevent duplicate entries
CREATE UNIQUE INDEX IF NOT EXISTS idx_price_data_unique ON price_data(symbol, timestamp);

