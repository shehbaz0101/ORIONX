// WebSocket client for real-time market data

// Use environment variable for WebSocket URL, with fallback
// For cloud deployment, use wss:// (secure WebSocket)
const getWebSocketUrl = () => {
  const wsUrl = process.env.NEXT_PUBLIC_WS_URL
  if (wsUrl) {
    return wsUrl.startsWith('ws://') || wsUrl.startsWith('wss://') 
      ? wsUrl 
      : `wss://${wsUrl}`
  }
  
  // Fallback: derive from API URL
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  if (apiUrl.startsWith('https://')) {
    return apiUrl.replace('https://', 'wss://')
  } else if (apiUrl.startsWith('http://')) {
    return apiUrl.replace('http://', 'ws://')
  }
  
  return 'ws://localhost:8000'
}

const WS_URL = getWebSocketUrl()

export class MarketDataWebSocket {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5

  constructor(private onMessage: (data: any) => void) {}

  connect() {
    try {
      this.ws = new WebSocket(`${WS_URL}/api/market/ws`)
      
      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0
      }
      
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        this.onMessage(data)
      }
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      
      this.ws.onclose = () => {
        console.log('WebSocket closed')
        this.reconnect()
      }
    } catch (error) {
      console.error('Failed to connect WebSocket:', error)
      this.reconnect()
    }
  }

  subscribe(symbols: string[], assetType: string = 'equity') {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        action: 'subscribe',
        symbols,
        asset_type: assetType
      }))
    }
  }

  unsubscribe(symbols: string[]) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        action: 'unsubscribe',
        symbols
      }))
    }
  }

  private reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      setTimeout(() => {
        console.log(`Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
        this.connect()
      }, 3000 * this.reconnectAttempts)
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }
}
