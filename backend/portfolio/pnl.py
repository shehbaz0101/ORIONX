"""
PnL engine - calculate profit and loss
"""
from typing import Dict, List
from datetime import datetime, timedelta
from backend.db.models import Holding
from backend.market_data.history import get_historical_data
import asyncio

async def get_current_price(symbol: str) -> float:
    """Get current price for symbol (placeholder - would use real-time data)"""
    # In production, this would fetch from real-time stream
    # For now, use latest close from historical data
    data = await get_historical_data(symbol, period="1d", interval="1d")
    if data and data.get("data"):
        return data["data"][-1]["close"]
    return 0.0

async def calculate_position_pnl(holding: Holding, current_price: float) -> Dict:
    """Calculate PnL for a single position"""
    market_value = holding.quantity * current_price
    cost_basis_total = holding.cost_basis
    unrealized_pnl = market_value - cost_basis_total
    unrealized_pnl_pct = (unrealized_pnl / cost_basis_total * 100) if cost_basis_total > 0 else 0
    
    return {
        "symbol": holding.symbol,
        "quantity": holding.quantity,
        "cost_basis": cost_basis_total,
        "current_price": current_price,
        "market_value": market_value,
        "unrealized_pnl": unrealized_pnl,
        "unrealized_pnl_pct": unrealized_pnl_pct
    }

async def calculate_portfolio_pnl(holdings: List[Holding]) -> Dict:
    """Calculate total portfolio PnL"""
    positions = []
    total_cost_basis = 0.0
    total_market_value = 0.0
    
    # Get prices for all symbols
    symbols = [h.symbol for h in holdings]
    prices = {}
    
    for symbol in symbols:
        price = await get_current_price(symbol)
        prices[symbol] = price
    
    # Calculate PnL for each position
    for holding in holdings:
        current_price = prices.get(holding.symbol, 0.0)
        position_pnl = await calculate_position_pnl(holding, current_price)
        positions.append(position_pnl)
        
        total_cost_basis += position_pnl["cost_basis"]
        total_market_value += position_pnl["market_value"]
    
    total_pnl = total_market_value - total_cost_basis
    total_pnl_pct = (total_pnl / total_cost_basis * 100) if total_cost_basis > 0 else 0
    
    # Calculate daily PnL (simplified - would need historical prices)
    today = datetime.utcnow().date()
    daily_pnl = 0.0  # Placeholder
    
    return {
        "total_cost_basis": total_cost_basis,
        "total_market_value": total_market_value,
        "total_pnl": total_pnl,
        "total_pnl_pct": total_pnl_pct,
        "daily_pnl": daily_pnl,
        "positions": positions
    }
