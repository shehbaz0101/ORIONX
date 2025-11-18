"""
Technical analysis indicators
"""
import numpy as np
from typing import Dict, List

def calculate_sma(prices: List[float], period: int) -> List[float]:
    """Simple Moving Average"""
    sma = []
    for i in range(len(prices)):
        if i < period - 1:
            sma.append(None)
        else:
            sma.append(np.mean(prices[i - period + 1:i + 1]))
    return sma

def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Exponential Moving Average"""
    ema = []
    multiplier = 2 / (period + 1)
    
    for i, price in enumerate(prices):
        if i == 0:
            ema.append(price)
        else:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
    
    return ema

def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
    """Relative Strength Index"""
    rsi = []
    deltas = np.diff(prices)
    
    for i in range(len(prices)):
        if i < period:
            rsi.append(None)
        else:
            gains = [d for d in deltas[i - period:i] if d > 0]
            losses = [-d for d in deltas[i - period:i] if d < 0]
            
            avg_gain = np.mean(gains) if gains else 0
            avg_loss = np.mean(losses) if losses else 0
            
            if avg_loss == 0:
                rsi.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi.append(100 - (100 / (1 + rs)))
    
    return rsi

def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    """MACD indicator"""
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    
    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    signal_line = calculate_ema(macd_line, signal)
    histogram = [m - s for m, s in zip(macd_line, signal_line)]
    
    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }

def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> Dict:
    """Bollinger Bands"""
    sma = calculate_sma(prices, period)
    upper_band = []
    lower_band = []
    
    for i in range(len(prices)):
        if i < period - 1:
            upper_band.append(None)
            lower_band.append(None)
        else:
            std = np.std(prices[i - period + 1:i + 1])
            upper_band.append(sma[i] + std_dev * std)
            lower_band.append(sma[i] - std_dev * std)
    
    return {
        "upper": upper_band,
        "middle": sma,
        "lower": lower_band
    }
