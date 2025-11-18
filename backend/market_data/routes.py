"""
Market data API routes
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from typing import List, Optional
from backend.market_data import history, fundamentals, metadata, fx
from backend.market_data.websocket_manager import ws_manager
from backend.market_data.realtime_equities import equity_stream
from backend.market_data.realtime_crypto import crypto_stream
from backend.auth.dependencies import get_current_user
from backend.db.models import User
from backend.utils.logger import logger

router = APIRouter(prefix="/api/market", tags=["market"])

@router.get("/realtime")
async def get_realtime_info():
    """Get info about real-time streams"""
    return {
        "equity_stream": {
            "status": "running" if equity_stream.running else "stopped",
            "subscribed_symbols": list(equity_stream.subscribed_symbols)
        },
        "crypto_stream": {
            "status": "running" if crypto_stream.running else "stopped",
            "subscribed_streams": list(crypto_stream.subscribed_streams)
        }
    }

@router.websocket("/ws")
async def market_data_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time market data"""
    await ws_manager.connect(websocket)
    
    try:
        while True:
            # Receive subscription messages
            data = await websocket.receive_json()
            
            if data.get("action") == "subscribe":
                symbols = data.get("symbols", [])
                asset_type = data.get("asset_type", "equity")
                
                if asset_type == "equity":
                    await equity_stream.subscribe(symbols)
                elif asset_type == "crypto":
                    await crypto_stream.subscribe(symbols)
                
                ws_manager.subscribe(websocket, symbols)
                
                await websocket.send_json({
                    "type": "subscribed",
                    "symbols": symbols
                })
            
            elif data.get("action") == "unsubscribe":
                symbols = data.get("symbols", [])
                ws_manager.unsubscribe(websocket, symbols)
                
                await websocket.send_json({
                    "type": "unsubscribed",
                    "symbols": symbols
                })
    
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")

@router.get("/history")
async def get_history(
    symbol: str = Query(..., description="Symbol to fetch"),
    period: str = Query("1mo", description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max"),
    interval: str = Query("1d", description="Interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo")
):
    """Get historical market data"""
    data = await history.get_historical_data(symbol, period, interval)
    if not data:
        return {"error": "No data available"}
    return data

@router.get("/fundamentals")
async def get_fundamentals_data(
    symbol: str = Query(..., description="Symbol to fetch")
):
    """Get fundamental data"""
    data = await fundamentals.get_fundamentals(symbol)
    if not data:
        return {"error": "No data available"}
    return data

@router.get("/metadata")
async def get_metadata(
    symbol: str = Query(..., description="Symbol to fetch")
):
    """Get company metadata"""
    data = await metadata.get_company_metadata(symbol)
    if not data:
        return {"error": "No data available"}
    return data

@router.get("/fx/rate")
async def get_fx_rate_endpoint(
    base: str = Query("USD", description="Base currency"),
    target: str = Query("EUR", description="Target currency")
):
    """Get FX rate"""
    rate = await fx.get_fx_rate(base, target)
    if rate is None:
        return {"error": "Could not fetch FX rate"}
    return {"base": base, "target": target, "rate": rate}

@router.get("/fx/rates")
async def get_fx_rates_endpoint(
    base: str = Query("USD", description="Base currency"),
    targets: Optional[str] = Query(None, description="Comma-separated target currencies")
):
    """Get multiple FX rates"""
    target_list = targets.split(",") if targets else None
    rates = await fx.get_fx_rates(base, target_list)
    return {"base": base, "rates": rates}

@router.get("/fx/history")
async def get_fx_history_endpoint(
    base: str = Query("USD", description="Base currency"),
    target: str = Query("EUR", description="Target currency"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get historical FX rates"""
    data = await fx.get_fx_history(base, target, start_date, end_date)
    if not data:
        return {"error": "Could not fetch FX history"}
    return {"base": base, "target": target, "rates": data}
