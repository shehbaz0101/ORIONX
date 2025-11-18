"""
News Sentiment Agent
"""
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.news.service import get_news_feed
from datetime import datetime

async def run_news_agent(db: AsyncSession, ticker: str = None) -> Dict:
    """Analyze news sentiment"""
    try:
        news = await get_news_feed(db, limit=50, ticker=ticker)
        
        # Aggregate sentiment
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for article in news:
            label = article.sentiment_label or "neutral"
            sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
        
        return {
            "date": datetime.utcnow().isoformat(),
            "ticker": ticker,
            "total_articles": len(news),
            "sentiment_breakdown": sentiment_counts,
            "overall_sentiment": max(sentiment_counts, key=sentiment_counts.get)
        }
    
    except Exception as e:
        logger.error(f"Error in news agent: {e}")
        return {"error": str(e)}
