-- Create filing_documents table
CREATE TABLE IF NOT EXISTS filing_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker VARCHAR(20) NOT NULL,
    cik VARCHAR(10) NOT NULL,
    filing_type VARCHAR(10) NOT NULL,
    filing_date TIMESTAMPTZ NOT NULL,
    edgar_url VARCHAR(1000) UNIQUE NOT NULL,
    raw_text TEXT,
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_filing_documents_ticker ON filing_documents(ticker);
CREATE INDEX IF NOT EXISTS idx_filing_documents_filing_date ON filing_documents(filing_date);

