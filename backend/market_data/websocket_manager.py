"""
WebSocket manager for broadcasting market data to connected clients
"""
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import json
from backend.utils.logger import logger

class WebSocketManager:
    """Manages WebSocket connections and broadcasts market data"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.subscriptions: Dict[WebSocket, Set[str]] = {}  # symbol subscriptions per connection
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        self.subscriptions[websocket] = set()
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.active_connections.discard(websocket)
        self.subscriptions.pop(websocket, None)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    def subscribe(self, websocket: WebSocket, symbols: list[str]):
        """Subscribe connection to symbols"""
        if websocket in self.subscriptions:
            self.subscriptions[websocket].update(symbols)
            logger.info(f"Subscribed to symbols: {symbols}")
    
    def unsubscribe(self, websocket: WebSocket, symbols: list[str]):
        """Unsubscribe connection from symbols"""
        if websocket in self.subscriptions:
            self.subscriptions[websocket].difference_update(symbols)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        message_json = json.dumps(message)
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.warning(f"Failed to send message to connection: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def send_to_subscribers(self, symbol: str, data: dict):
        """Send data only to clients subscribed to the symbol"""
        message = {
            "type": "market_data",
            "symbol": symbol,
            "data": data
        }
        
        message_json = json.dumps(message)
        disconnected = set()
        
        for connection, subscribed_symbols in self.subscriptions.items():
            if symbol in subscribed_symbols or "*" in subscribed_symbols:
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    logger.warning(f"Failed to send to subscriber: {e}")
                    disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

# Global WebSocket manager instance
ws_manager = WebSocketManager()
