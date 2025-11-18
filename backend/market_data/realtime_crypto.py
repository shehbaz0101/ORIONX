"""
Real-time crypto data via Binance WebSocket
"""
import asyncio
import json
import websockets
from typing import Dict, Optional
from backend.utils.logger import logger
from backend.market_data.websocket_manager import ws_manager

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"

class BinanceCryptoStream:
    """Stream crypto data from Binance"""
    
    def __init__(self):
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.running = False
        self.subscribed_streams: set[str] = set()
    
    def _get_stream_name(self, symbol: str) -> str:
        """Convert symbol to Binance stream format (e.g., BTCUSDT -> btcusdt@ticker)"""
        symbol_lower = symbol.lower().replace("/", "")
        return f"{symbol_lower}@ticker"
    
    async def connect(self):
        """Connect to Binance WebSocket"""
        try:
            self.websocket = await websockets.connect(BINANCE_WS_URL)
            logger.info("Connected to Binance crypto stream")
            self.running = True
        except Exception as e:
            logger.error(f"Failed to connect to Binance: {e}")
            raise
    
    async def subscribe(self, symbols: list[str]):
        """Subscribe to crypto symbols"""
        if not self.websocket:
            await self.connect()
        
        streams = [self._get_stream_name(sym) for sym in symbols]
        self.subscribed_streams.update(streams)
        
        # Binance subscription format
        subscribe_msg = {
            "method": "SUBSCRIBE",
            "params": streams,
            "id": 1
        }
        
        await self.websocket.send(json.dumps(subscribe_msg))
        logger.info(f"Subscribed to {len(symbols)} crypto symbols")
    
    async def handle_message(self, message: dict):
        """Handle incoming message from Binance"""
        try:
            stream = message.get("stream", "")
            
            if "@ticker" in stream:
                data = message.get("data", {})
                symbol = data.get("s", "").replace("USDT", "/USDT")
                price = data.get("c")  # Last price
                volume = data.get("v")  # 24h volume
                change = data.get("P")  # 24h change percent
                
                market_data = {
                    "type": "ticker",
                    "symbol": symbol,
                    "price": float(price) if price else None,
                    "volume_24h": float(volume) if volume else None,
                    "change_24h": float(change) if change else None,
                    "timestamp": data.get("E")
                }
                
                await ws_manager.send_to_subscribers(symbol, market_data)
        
        except Exception as e:
            logger.error(f"Error handling Binance message: {e}")
    
    async def run(self):
        """Main loop for receiving messages"""
        while self.running:
            try:
                if not self.websocket:
                    await self.connect()
                
                message = await self.websocket.recv()
                data = json.loads(message)
                
                await self.handle_message(data)
            
            except websockets.exceptions.ConnectionClosed:
                logger.warning("Binance connection closed, reconnecting...")
                await asyncio.sleep(5)
                await self.connect()
            
            except Exception as e:
                logger.error(f"Error in Binance stream: {e}")
                await asyncio.sleep(5)
    
    async def stop(self):
        """Stop the stream"""
        self.running = False
        if self.websocket:
            await self.websocket.close()

# Global instance
crypto_stream = BinanceCryptoStream()

async def start_crypto_stream():
    """Start the crypto stream in background"""
    await crypto_stream.connect()
    asyncio.create_task(crypto_stream.run())
