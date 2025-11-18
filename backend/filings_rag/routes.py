"""
Filings RAG API routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.db import get_db
from backend.filings_rag import edgar_client, chunker, embeddings, parse
from backend.db.models import FilingDocument, EmbeddingVector
from backend.auth.dependencies import get_current_user
from backend.db.models import User
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime
from backend.utils.logger import logger
import numpy as np

router = APIRouter(prefix="/api/filings", tags=["filings"])

@router.post("/sync")
async def sync_filings(
    ticker: str = Query(..., description="Ticker symbol"),
    filing_type: str = Query("10-K", description="Filing type: 10-K, 10-Q, 8-K"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Sync filings for a ticker from EDGAR"""
    # Get CIK
    cik = await edgar_client.get_cik_from_ticker(ticker)
    if not cik:
        return {"error": f"Could not find CIK for ticker {ticker}"}
    
    # Get filing index
    filings = await edgar_client.get_filing_index(cik, filing_type)
    
    synced_count = 0
    for filing_info in filings[:5]:  # Limit to 5 most recent
        try:
            # Check if already exists
            result = await db.execute(
                select(FilingDocument).where(FilingDocument.edgar_url == filing_info["url"])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                continue
            
            # Download filing
            content = await edgar_client.get_filing_content(filing_info["url"])
            if not content:
                continue
            
            # Parse content
            text = parse.parse_html_filing(content)
            if not text:
                continue
            
            # Create filing document
            filing = FilingDocument(
                ticker=ticker,
                cik=cik,
                filing_type=filing_type,
                filing_date=datetime.strptime(filing_info["filing_date"], "%Y-%m-%d"),
                edgar_url=filing_info["url"],
                raw_text=text[:10000]  # Store first 10k chars
            )
            
            db.add(filing)
            await db.flush()
            
            # Chunk and embed
            chunks = chunker.chunk_text(text, chunk_size=1024, overlap=200)
            
            for idx, chunk in enumerate(chunks[:50]):  # Limit to 50 chunks
                embedding = await embeddings.generate_embedding(chunk)
                if embedding:
                    # Convert to numpy array for pgvector
                    embedding_array = np.array(embedding, dtype=np.float32)
                    
                    vec = EmbeddingVector(
                        filing_id=filing.id,
                        chunk_text=chunk,
                        chunk_index=idx,
                        embedding=embedding_array.tolist(),
                        metadata={"ticker": ticker, "filing_type": filing_type}
                    )
                    db.add(vec)
            
            await db.commit()
            synced_count += 1
        
        except Exception as e:
            logger.error(f"Error syncing filing: {e}")
            await db.rollback()
            continue
    
    return {"message": f"Synced {synced_count} filings", "count": synced_count}

@router.get("/search")
async def search_filings(
    q: str = Query(..., description="Search query"),
    ticker: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Semantic search in filings using pgvector"""
    # Generate query embedding
    query_embedding = await embeddings.generate_embedding(q)
    if not query_embedding:
        return {"error": "Could not generate query embedding"}
    
    # Vector similarity search
    from sqlalchemy import func
    from pgvector.sqlalchemy import Vector
    
    query_embedding_array = np.array(query_embedding, dtype=np.float32)
    
    # Build query
    search_query = select(
        EmbeddingVector,
        func.cosine_distance(EmbeddingVector.embedding, query_embedding_array.tolist()).label("distance")
    )
    
    if ticker:
        search_query = search_query.join(FilingDocument).where(FilingDocument.ticker == ticker)
    
    search_query = search_query.order_by("distance").limit(limit)
    
    result = await db.execute(search_query)
    results = result.all()
    
    return {
        "results": [
            {
                "chunk_text": row[0].chunk_text,
                "ticker": row[0].metadata.get("ticker"),
                "filing_type": row[0].metadata.get("filing_type"),
                "similarity": 1 - float(row[1]),  # Convert distance to similarity
                "filing_id": str(row[0].filing_id)
            }
            for row in results
        ],
        "count": len(results)
    }
