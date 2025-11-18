"""
Scenario simulation service
"""
from typing import Dict, List
from backend.db.models import Holding
from backend.portfolio.pnl import get_current_price

async def simulate_rate_shock(holdings: List[Holding], shock_bps: int = 100) -> Dict:
    """Simulate interest rate shock"""
    # Simplified: assume rate-sensitive assets lose value
    total_value = 0.0
    shocked_value = 0.0
    
    for holding in holdings:
        price = await get_current_price(holding.symbol)
        value = holding.quantity * price
        total_value += value
        
        # Assume 10% of portfolio is rate-sensitive
        if holding.asset_type in ["bond", "reit"]:
            shocked_value += value * (1 - shock_bps / 10000 * 2)
        else:
            shocked_value += value
    
    impact = shocked_value - total_value
    impact_pct = (impact / total_value * 100) if total_value > 0 else 0
    
    return {
        "scenario": "rate_shock",
        "shock_bps": shock_bps,
        "current_value": total_value,
        "shocked_value": shocked_value,
        "impact": impact,
        "impact_pct": impact_pct
    }

async def simulate_fx_shock(holdings: List[Holding], currency: str, shock_pct: float = 10.0) -> Dict:
    """Simulate FX shock"""
    total_value = 0.0
    shocked_value = 0.0
    
    for holding in holdings:
        price = await get_current_price(holding.symbol)
        value = holding.quantity * price
        total_value += value
        
        if holding.currency == currency:
            shocked_value += value * (1 - shock_pct / 100)
        else:
            shocked_value += value
    
    impact = shocked_value - total_value
    impact_pct = (impact / total_value * 100) if total_value > 0 else 0
    
    return {
        "scenario": "fx_shock",
        "currency": currency,
        "shock_pct": shock_pct,
        "current_value": total_value,
        "shocked_value": shocked_value,
        "impact": impact,
        "impact_pct": impact_pct
    }

async def simulate_volatility_shock(holdings: List[Holding], vol_multiplier: float = 2.0) -> Dict:
    """Simulate volatility expansion"""
    # Simplified: assume higher volatility leads to lower prices
    total_value = 0.0
    shocked_value = 0.0
    
    for holding in holdings:
        price = await get_current_price(holding.symbol)
        value = holding.quantity * price
        total_value += value
        
        # Assume 5% price decline per volatility doubling
        shocked_value += value * (1 - (vol_multiplier - 1) * 0.05)
    
    impact = shocked_value - total_value
    impact_pct = (impact / total_value * 100) if total_value > 0 else 0
    
    return {
        "scenario": "volatility_shock",
        "vol_multiplier": vol_multiplier,
        "current_value": total_value,
        "shocked_value": shocked_value,
        "impact": impact,
        "impact_pct": impact_pct
    }
