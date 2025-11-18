"""
News service - store and retrieve news articles
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.db.models import NewsArticle
from backend.news import rss_ingest, sentiment
from backend.utils.logger import logger
from typing import List, Optional
from datetime import datetime
import uuid

async def store_article(db: AsyncSession, article_data: dict) -> NewsArticle:
    """Store a news article in database"""
    # Check if article already exists
    result = await db.execute(
        select(NewsArticle).where(NewsArticle.url == article_data["url"])
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return existing
    
    # Analyze sentiment
    text = f"{article_data.get('title', '')} {article_data.get('content', '')}"
    sentiment_result = await sentiment.analyze_sentiment(text)
    
    # Create article
    article = NewsArticle(
        title=article_data["title"],
        content=article_data.get("content", ""),
        url=article_data["url"],
        source=article_data.get("source", "unknown"),
        published_at=datetime.fromisoformat(article_data["published_at"].replace("Z", "+00:00")),
        sentiment_score=sentiment_result.get("score", 0.0),
        sentiment_label=sentiment_result.get("label", "neutral"),
        tickers=article_data.get("tickers", [])
    )
    
    db.add(article)
    await db.commit()
    await db.refresh(article)
    
    return article

async def ingest_and_store_news(db: AsyncSession) -> int:
    """Ingest RSS feeds and store articles"""
    articles_data = await rss_ingest.ingest_all_feeds()
    stored_count = 0
    
    for article_data in articles_data:
        try:
            await store_article(db, article_data)
            stored_count += 1
        except Exception as e:
            logger.warning(f"Error storing article: {e}")
            continue
    
    logger.info(f"Stored {stored_count} new articles")
    return stored_count

async def get_news_feed(
    db: AsyncSession,
    limit: int = 50,
    offset: int = 0,
    ticker: Optional[str] = None,
    sentiment: Optional[str] = None
) -> List[NewsArticle]:
    """Get news feed with optional filters"""
    query = select(NewsArticle).order_by(desc(NewsArticle.published_at))
    
    if ticker:
        query = query.where(NewsArticle.tickers.contains([ticker]))
    
    if sentiment:
        query = query.where(NewsArticle.sentiment_label == sentiment)
    
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    return result.scalars().all()

async def search_news(
    db: AsyncSession,
    query_text: str,
    limit: int = 20
) -> List[NewsArticle]:
    """Search news articles by text"""
    from sqlalchemy import or_
    
    query = select(NewsArticle).where(
        or_(
            NewsArticle.title.ilike(f"%{query_text}%"),
            NewsArticle.content.ilike(f"%{query_text}%")
        )
    ).order_by(desc(NewsArticle.published_at)).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()
