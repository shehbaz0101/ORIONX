"""
Screener service
"""
from typing import Dict, List
from backend.market_data import fundamentals, history
from backend.screener import ta

async def run_technical_screen(symbols: List[str], filters: Dict) -> List[Dict]:
    """Run technical screening"""
    results = []
    
    for symbol in symbols:
        try:
            # Get historical data
            data = await history.get_historical_data(symbol, period="3mo", interval="1d")
            if not data or not data.get("data"):
                continue
            
            prices = [d["close"] for d in data["data"]]
            
            # Calculate indicators
            rsi = ta.calculate_rsi(prices)
            macd = ta.calculate_macd(prices)
            bb = ta.calculate_bollinger_bands(prices)
            
            # Apply filters
            passes = True
            
            if "rsi_oversold" in filters and filters["rsi_oversold"]:
                if rsi[-1] is None or rsi[-1] > 30:
                    passes = False
            
            if "rsi_overbought" in filters and filters["rsi_overbought"]:
                if rsi[-1] is None or rsi[-1] < 70:
                    passes = False
            
            if passes:
                results.append({
                    "symbol": symbol,
                    "rsi": rsi[-1],
                    "macd": macd["macd"][-1],
                    "price": prices[-1]
                })
        
        except Exception as e:
            continue
    
    return results

async def run_fundamental_screen(symbols: List[str], filters: Dict) -> List[Dict]:
    """Run fundamental screening"""
    results = []
    
    for symbol in symbols:
        try:
            fund = await fundamentals.get_fundamentals(symbol)
            if not fund:
                continue
            
            passes = True
            
            # Apply filters
            if "min_market_cap" in filters:
                if fund.get("market_cap", 0) < filters["min_market_cap"]:
                    passes = False
            
            if "max_pe_ratio" in filters:
                if fund.get("pe_ratio") and fund["pe_ratio"] > filters["max_pe_ratio"]:
                    passes = False
            
            if "min_roe" in filters:
                if fund.get("roe") and fund["roe"] < filters["min_roe"]:
                    passes = False
            
            if passes:
                results.append({
                    "symbol": symbol,
                    "market_cap": fund.get("market_cap"),
                    "pe_ratio": fund.get("pe_ratio"),
                    "roe": fund.get("roe")
                })
        
        except Exception as e:
            continue
    
    return results
