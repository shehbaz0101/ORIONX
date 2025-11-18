"""
FX data fetcher using exchangerate.host
"""
import httpx
from typing import Dict, Optional
from backend.utils.logger import logger
from backend.utils.redis_client import cache_get, cache_set
import os

EXCHANGERATE_API = "https://api.exchangerate.host"

async def get_fx_rate(base: str = "USD", target: str = "EUR") -> Optional[float]:
    """Get current FX rate"""
    cache_key = f"fx:{base}:{target}"
    
    # Check cache first
    cached = await cache_get(cache_key)
    if cached:
        return cached
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"{EXCHANGERATE_API}/latest"
            params = {"base": base, "symbols": target}
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                rate = data["rates"].get(target)
                if rate:
                    # Cache for 1 hour
                    await cache_set(cache_key, rate, ttl=3600)
                    return float(rate)
    
    except Exception as e:
        logger.error(f"Error fetching FX rate {base}/{target}: {e}")
    
    return None

async def get_fx_rates(base: str = "USD", targets: list[str] = None) -> Dict[str, float]:
    """Get multiple FX rates"""
    if targets is None:
        targets = ["EUR", "GBP", "JPY", "CNY", "AUD", "CAD"]
    
    rates = {}
    for target in targets:
        rate = await get_fx_rate(base, target)
        if rate:
            rates[target] = rate
    
    return rates

async def get_fx_history(
    base: str = "USD",
    target: str = "EUR",
    start_date: str = None,
    end_date: str = None
) -> Optional[Dict]:
    """Get historical FX rates"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{EXCHANGERATE_API}/timeseries"
            params = {
                "base": base,
                "symbols": target,
            }
            
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                return data.get("rates", {})
    
    except Exception as e:
        logger.error(f"Error fetching FX history: {e}")
    
    return None
