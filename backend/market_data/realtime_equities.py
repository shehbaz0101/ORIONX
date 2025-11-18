"""
Real-time equity data via Alpaca WebSocket (public feed)
"""
import asyncio
import json
import websockets
from typing import Dict, Optional
from backend.utils.logger import logger
from backend.market_data.websocket_manager import ws_manager

ALPACA_WS_URL = "wss://stream.data.alpaca.markets/v2/sip"

class AlpacaEquityStream:
    """Stream equity data from Alpaca"""
    
    def __init__(self):
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.running = False
        self.subscribed_symbols: set[str] = set()
    
    async def connect(self):
        """Connect to Alpaca WebSocket"""
        try:
            self.websocket = await websockets.connect(ALPACA_WS_URL)
            logger.info("Connected to Alpaca equity stream")
            self.running = True
        except Exception as e:
            logger.error(f"Failed to connect to Alpaca: {e}")
            raise
    
    async def subscribe(self, symbols: list[str]):
        """Subscribe to equity symbols"""
        if not self.websocket:
            await self.connect()
        
        self.subscribed_symbols.update(symbols)
        
        # Alpaca subscription message format
        subscribe_msg = {
            "action": "subscribe",
            "trades": symbols,
            "quotes": symbols
        }
        
        await self.websocket.send(json.dumps(subscribe_msg))
        logger.info(f"Subscribed to {len(symbols)} equity symbols")
    
    async def handle_message(self, message: dict):
        """Handle incoming message from Alpaca"""
        try:
            msg_type = message.get("T")  # Message type
            
            if msg_type == "t":  # Trade
                symbol = message.get("S")
                price = message.get("p")
                size = message.get("s")
                timestamp = message.get("t")
                
                data = {
                    "type": "trade",
                    "symbol": symbol,
                    "price": float(price) if price else None,
                    "size": int(size) if size else None,
                    "timestamp": timestamp
                }
                
                await ws_manager.send_to_subscribers(symbol, data)
            
            elif msg_type == "q":  # Quote
                symbol = message.get("S")
                bid = message.get("bp")
                ask = message.get("ap")
                bid_size = message.get("bs")
                ask_size = message.get("as")
                timestamp = message.get("t")
                
                data = {
                    "type": "quote",
                    "symbol": symbol,
                    "bid": float(bid) if bid else None,
                    "ask": float(ask) if ask else None,
                    "bid_size": int(bid_size) if bid_size else None,
                    "ask_size": int(ask_size) if ask_size else None,
                    "timestamp": timestamp
                }
                
                await ws_manager.send_to_subscribers(symbol, data)
        
        except Exception as e:
            logger.error(f"Error handling Alpaca message: {e}")
    
    async def run(self):
        """Main loop for receiving messages"""
        while self.running:
            try:
                if not self.websocket:
                    await self.connect()
                
                message = await self.websocket.recv()
                data = json.loads(message)
                
                # Handle array of messages
                if isinstance(data, list):
                    for msg in data:
                        await self.handle_message(msg)
                else:
                    await self.handle_message(data)
            
            except websockets.exceptions.ConnectionClosed:
                logger.warning("Alpaca connection closed, reconnecting...")
                await asyncio.sleep(5)
                await self.connect()
            
            except Exception as e:
                logger.error(f"Error in Alpaca stream: {e}")
                await asyncio.sleep(5)
    
    async def stop(self):
        """Stop the stream"""
        self.running = False
        if self.websocket:
            await self.websocket.close()

# Global instance
equity_stream = AlpacaEquityStream()

async def start_equity_stream():
    """Start the equity stream in background"""
    await equity_stream.connect()
    asyncio.create_task(equity_stream.run())
