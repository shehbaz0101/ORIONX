"""
Historical market data via yfinance
"""
import yfinance as yf
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from backend.utils.logger import logger
from backend.utils.redis_client import cache_get, cache_set

async def get_historical_data(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d"
) -> Optional[Dict]:
    """Get historical OHLCV data"""
    cache_key = f"history:{symbol}:{period}:{interval}"
    
    # Check cache
    cached = await cache_get(cache_key)
    if cached:
        return cached
    
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            return None
        
        # Convert to dict format
        data = {
            "symbol": symbol,
            "period": period,
            "interval": interval,
            "data": []
        }
        
        for idx, row in df.iterrows():
            data["data"].append({
                "timestamp": idx.isoformat(),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"])
            })
        
        # Cache for 1 hour
        await cache_set(cache_key, data, ttl=3600)
        return data
    
    except Exception as e:
        logger.error(f"Error fetching historical data for {symbol}: {e}")
        return None

async def get_splits_dividends(symbol: str) -> Dict:
    """Get splits and dividends history"""
    try:
        ticker = yf.Ticker(symbol)
        splits = ticker.splits
        dividends = ticker.dividends
        
        return {
            "symbol": symbol,
            "splits": [
                {"date": idx.isoformat(), "ratio": float(val)}
                for idx, val in splits.items()
            ],
            "dividends": [
                {"date": idx.isoformat(), "amount": float(val)}
                for idx, val in dividends.items()
            ]
        }
    
    except Exception as e:
        logger.error(f"Error fetching splits/dividends for {symbol}: {e}")
        return {"symbol": symbol, "splits": [], "dividends": []}
