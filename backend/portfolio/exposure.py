"""
Exposure engine - calculate portfolio exposures
"""
from typing import Dict, List
from collections import defaultdict
from backend.db.models import Holding
from backend.market_data import metadata, fundamentals
import asyncio

async def calculate_sector_exposure(holdings: List[Holding]) -> Dict:
    """Calculate sector exposure"""
    sector_values = defaultdict(float)
    total_value = 0.0
    
    for holding in holdings:
        # Get metadata
        meta = await metadata.get_company_metadata(holding.symbol)
        if not meta:
            continue
        
        sector = meta.get("sector", "Unknown")
        # Get current price (simplified)
        from backend.portfolio.pnl import get_current_price
        price = await get_current_price(holding.symbol)
        value = holding.quantity * price
        
        sector_values[sector] += value
        total_value += value
    
    # Convert to percentages
    sector_exposure = {
        sector: (value / total_value * 100) if total_value > 0 else 0
        for sector, value in sector_values.items()
    }
    
    return {
        "sector_exposure": sector_exposure,
        "total_value": total_value
    }

async def calculate_asset_class_exposure(holdings: List[Holding]) -> Dict:
    """Calculate asset class exposure"""
    asset_class_values = defaultdict(float)
    total_value = 0.0
    
    for holding in holdings:
        asset_type = holding.asset_type or "equity"
        from backend.portfolio.pnl import get_current_price
        price = await get_current_price(holding.symbol)
        value = holding.quantity * price
        
        asset_class_values[asset_type] += value
        total_value += value
    
    asset_class_exposure = {
        asset_type: (value / total_value * 100) if total_value > 0 else 0
        for asset_type, value in asset_class_values.items()
    }
    
    return {
        "asset_class_exposure": asset_class_exposure,
        "total_value": total_value
    }

async def calculate_currency_exposure(holdings: List[Holding]) -> Dict:
    """Calculate currency exposure"""
    currency_values = defaultdict(float)
    total_value = 0.0
    
    for holding in holdings:
        currency = holding.currency or "USD"
        from backend.portfolio.pnl import get_current_price
        price = await get_current_price(holding.symbol)
        value = holding.quantity * price
        
        currency_values[currency] += value
        total_value += value
    
    currency_exposure = {
        currency: (value / total_value * 100) if total_value > 0 else 0
        for currency, value in currency_values.items()
    }
    
    return {
        "currency_exposure": currency_exposure,
        "total_value": total_value
    }
