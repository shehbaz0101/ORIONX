"""
News API routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.db import get_db
from backend.news import service
from backend.auth.dependencies import get_current_user
from backend.db.models import User
from typing import Optional
from backend.utils.logger import logger

router = APIRouter(prefix="/api/news", tags=["news"])

@router.post("/sync")
async def sync_news(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually trigger news ingestion"""
    count = await service.ingest_and_store_news(db)
    return {"message": f"Synced {count} articles", "count": count}

@router.get("/feed")
async def get_news_feed(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    ticker: Optional[str] = Query(None),
    sentiment: Optional[str] = Query(None, regex="^(positive|negative|neutral)$"),
    db: AsyncSession = Depends(get_db)
):
    """Get news feed"""
    articles = await service.get_news_feed(db, limit, offset, ticker, sentiment)
    
    return {
        "articles": [
            {
                "id": str(article.id),
                "title": article.title,
                "content": article.content,
                "url": article.url,
                "source": article.source,
                "published_at": article.published_at.isoformat(),
                "sentiment_score": article.sentiment_score,
                "sentiment_label": article.sentiment_label,
                "tickers": article.tickers
            }
            for article in articles
        ],
        "count": len(articles)
    }

@router.get("/search")
async def search_news(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Search news articles"""
    articles = await service.search_news(db, q, limit)
    
    return {
        "articles": [
            {
                "id": str(article.id),
                "title": article.title,
                "content": article.content,
                "url": article.url,
                "source": article.source,
                "published_at": article.published_at.isoformat(),
                "sentiment_score": article.sentiment_score,
                "sentiment_label": article.sentiment_label,
                "tickers": article.tickers
            }
            for article in articles
        ],
        "count": len(articles)
    }
