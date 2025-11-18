"""
Company metadata service
"""
import yfinance as yf
from typing import Optional, Dict
from backend.utils.logger import logger
from backend.utils.redis_client import cache_get, cache_set

async def get_company_metadata(symbol: str) -> Optional[Dict]:
    """Get company metadata"""
    cache_key = f"metadata:{symbol}"
    
    # Check cache
    cached = await cache_get(cache_key)
    if cached:
        return cached
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if not info:
            return None
        
        metadata = {
            "symbol": symbol,
            "company_name": info.get("longName") or info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "description": info.get("longBusinessSummary"),
            "website": info.get("website"),
            "country": info.get("country"),
            "currency": info.get("currency"),
            "exchange": info.get("exchange"),
            "employees": info.get("fullTimeEmployees"),
        }
        
        # Cache for 7 days
        await cache_set(cache_key, metadata, ttl=604800)
        return metadata
    
    except Exception as e:
        logger.error(f"Error fetching metadata for {symbol}: {e}")
        return None
