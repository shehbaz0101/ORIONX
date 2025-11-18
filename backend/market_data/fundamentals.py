"""
Fundamentals data via yfinance
"""
import yfinance as yf
from typing import Optional, Dict
from backend.utils.logger import logger
from backend.utils.redis_client import cache_get, cache_set

async def get_fundamentals(symbol: str) -> Optional[Dict]:
    """Get fundamental data for a symbol"""
    cache_key = f"fundamentals:{symbol}"
    
    # Check cache (cache for 24 hours)
    cached = await cache_get(cache_key)
    if cached:
        return cached
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if not info:
            return None
        
        fundamentals = {
            "symbol": symbol,
            "company_name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "enterprise_value": info.get("enterpriseValue"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_book": info.get("priceToBook"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "dividend_yield": info.get("dividendYield"),
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "revenue": info.get("totalRevenue"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "beta": info.get("beta"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "avg_volume": info.get("averageVolume"),
            "shares_outstanding": info.get("sharesOutstanding"),
            "float_shares": info.get("floatShares"),
        }
        
        # Cache for 24 hours
        await cache_set(cache_key, fundamentals, ttl=86400)
        return fundamentals
    
    except Exception as e:
        logger.error(f"Error fetching fundamentals for {symbol}: {e}")
        return None
