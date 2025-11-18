"""
Risk service - calculate risk metrics
"""
from typing import Dict, List
import numpy as np
from backend.db.models import Holding
from backend.market_data.history import get_historical_data
from backend.portfolio.pnl import get_current_price

async def calculate_volatility(symbol: str, days: int = 30) -> float:
    """Calculate rolling volatility"""
    data = await get_historical_data(symbol, period=f"{days}d", interval="1d")
    if not data or not data.get("data"):
        return 0.0
    
    prices = [d["close"] for d in data["data"]]
    returns = np.diff(np.log(prices))
    volatility = np.std(returns) * np.sqrt(252)  # Annualized
    return float(volatility)

async def calculate_correlation_matrix(symbols: List[str], days: int = 90) -> Dict:
    """Calculate correlation matrix"""
    returns_data = {}
    
    for symbol in symbols:
        data = await get_historical_data(symbol, period=f"{days}d", interval="1d")
        if data and data.get("data"):
            prices = [d["close"] for d in data["data"]]
            returns = np.diff(np.log(prices))
            returns_data[symbol] = returns
    
    if len(returns_data) < 2:
        return {"correlations": {}}
    
    # Align returns by length
    min_len = min(len(r) for r in returns_data.values())
    aligned_returns = {sym: r[-min_len:] for sym, r in returns_data.items()}
    
    # Calculate correlation
    correlation_matrix = {}
    symbols_list = list(aligned_returns.keys())
    
    for i, sym1 in enumerate(symbols_list):
        for sym2 in symbols_list[i:]:
            corr = np.corrcoef(aligned_returns[sym1], aligned_returns[sym2])[0, 1]
            correlation_matrix[f"{sym1}-{sym2}"] = float(corr)
    
    return {"correlations": correlation_matrix}

async def calculate_var(holdings: List[Holding], confidence: float = 0.95) -> Dict:
    """Calculate Value at Risk (simplified)"""
    # Simplified VaR calculation
    total_value = 0.0
    
    for holding in holdings:
        price = await get_current_price(holding.symbol)
        total_value += holding.quantity * price
    
    # Assume 2% daily volatility
    daily_vol = 0.02
    var_95 = total_value * daily_vol * 1.645  # 95% VaR
    
    return {
        "var_95": var_95,
        "var_95_pct": (var_95 / total_value * 100) if total_value > 0 else 0,
        "confidence": confidence
    }

async def calculate_portfolio_risk(holdings: List[Holding]) -> Dict:
    """Calculate comprehensive portfolio risk metrics"""
    symbols = [h.symbol for h in holdings]
    
    # Calculate volatilities
    volatilities = {}
    for symbol in symbols:
        vol = await calculate_volatility(symbol)
        volatilities[symbol] = vol
    
    # Calculate correlation matrix
    correlation = await calculate_correlation_matrix(symbols)
    
    # Calculate VaR
    var_data = await calculate_var(holdings)
    
    # Concentration risk
    total_value = sum(h.quantity * await get_current_price(h.symbol) for h in holdings)
    position_weights = {}
    for holding in holdings:
        price = await get_current_price(holding.symbol)
        value = holding.quantity * price
        weight = (value / total_value * 100) if total_value > 0 else 0
        position_weights[holding.symbol] = weight
    
    max_concentration = max(position_weights.values()) if position_weights else 0
    
    return {
        "volatilities": volatilities,
        "correlation_matrix": correlation,
        "var": var_data,
        "concentration": {
            "position_weights": position_weights,
            "max_concentration": max_concentration
        },
        "warnings": generate_risk_warnings(volatilities, max_concentration, var_data)
    }

def generate_risk_warnings(volatilities: Dict, max_concentration: float, var_data: Dict) -> List[str]:
    """Generate risk warnings"""
    warnings = []
    
    # High volatility warning
    high_vol_symbols = [sym for sym, vol in volatilities.items() if vol > 0.4]
    if high_vol_symbols:
        warnings.append(f"High volatility detected in: {', '.join(high_vol_symbols)}")
    
    # Concentration warning
    if max_concentration > 20:
        warnings.append(f"High concentration risk: {max_concentration:.1f}% in single position")
    
    # VaR warning
    if var_data.get("var_95_pct", 0) > 5:
        warnings.append(f"High VaR: {var_data['var_95_pct']:.1f}% of portfolio value at risk")
    
    return warnings
