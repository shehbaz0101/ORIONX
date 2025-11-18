-- Create embedding_vectors table with pgvector
CREATE TABLE IF NOT EXISTS embedding_vectors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filing_id UUID NOT NULL REFERENCES filing_documents(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    embedding vector(1024) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create vector similarity index using cosine distance
CREATE INDEX IF NOT EXISTS idx_embedding_vectors_embedding ON embedding_vectors 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_embedding_vectors_filing_id ON embedding_vectors(filing_id);

