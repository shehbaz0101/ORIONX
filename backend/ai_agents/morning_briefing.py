"""
Morning Briefing Agent - Daily market summary
"""
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from datetime import datetime
from backend.news.service import get_news_feed
from backend.market_data.history import get_historical_data

async def run_morning_briefing(db: AsyncSession, user_id: str) -> Dict:
    """Generate morning briefing"""
    try:
        # Get top news
        news = await get_news_feed(db, limit=10)
        
        # Get market overview (simplified)
        market_data = await get_historical_data("SPY", period="1d", interval="1d")
        
        briefing = {
            "date": datetime.utcnow().isoformat(),
            "news_summary": f"Top {len(news)} news articles today",
            "market_overview": "Market data retrieved",
            "user_id": user_id
        }
        
        logger.info(f"Morning briefing generated for user {user_id}")
        return briefing
    
    except Exception as e:
        logger.error(f"Error in morning briefing: {e}")
        return {"error": str(e)}
