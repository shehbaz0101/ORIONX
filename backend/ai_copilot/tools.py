"""
AI Copilot tool registry
"""
from typing import Dict, List, Any, Callable
import inspect
from backend.utils.logger import logger

# Tool registry
TOOLS = {}

def register_tool(name: str, description: str, parameters: Dict):
    """Decorator to register a tool"""
    def decorator(func: Callable):
        TOOLS[name] = {
            "function": func,
            "description": description,
            "parameters": parameters,
            "name": name
        }
        return func
    return decorator

def get_tools_schema() -> List[Dict]:
    """Get JSON schema for all tools"""
    schemas = []
    
    for name, tool_info in TOOLS.items():
        schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": tool_info["description"],
                "parameters": tool_info["parameters"]
            }
        }
        schemas.append(schema)
    
    return schemas

async def call_tool(name: str, arguments: Dict) -> Any:
    """Call a tool by name with arguments"""
    if name not in TOOLS:
        raise ValueError(f"Tool {name} not found")
    
    tool = TOOLS[name]["function"]
    
    # Check if function is async
    if inspect.iscoroutinefunction(tool):
        return await tool(**arguments)
    else:
        return tool(**arguments)

# Register tools
@register_tool(
    "get_realtime_price",
    "Get real-time price for a symbol",
    {
        "type": "object",
        "properties": {
            "symbol": {"type": "string", "description": "Stock or crypto symbol"}
        },
        "required": ["symbol"]
    }
)
async def tool_get_realtime_price(symbol: str) -> Dict:
    """Get real-time price"""
    from backend.market_data.history import get_historical_data
    data = await get_historical_data(symbol, period="1d", interval="1d")
    if data and data.get("data"):
        return {"symbol": symbol, "price": data["data"][-1]["close"]}
    return {"symbol": symbol, "price": None}

@register_tool(
    "get_historical",
    "Get historical price data",
    {
        "type": "object",
        "properties": {
            "symbol": {"type": "string"},
            "period": {"type": "string", "default": "1mo"},
            "interval": {"type": "string", "default": "1d"}
        },
        "required": ["symbol"]
    }
)
async def tool_get_historical(symbol: str, period: str = "1mo", interval: str = "1d") -> Dict:
    """Get historical data"""
    from backend.market_data.history import get_historical_data
    return await get_historical_data(symbol, period, interval) or {}

@register_tool(
    "run_screener",
    "Run stock screener",
    {
        "type": "object",
        "properties": {
            "symbols": {"type": "array", "items": {"type": "string"}},
            "filters": {"type": "object"}
        },
        "required": ["symbols"]
    }
)
async def tool_run_screener(symbols: List[str], filters: Dict = None) -> Dict:
    """Run screener"""
    from backend.screener.service import run_fundamental_screen
    results = await run_fundamental_screen(symbols, filters or {})
    return {"results": results, "count": len(results)}

@register_tool(
    "get_news",
    "Get news articles",
    {
        "type": "object",
        "properties": {
            "ticker": {"type": "string"},
            "limit": {"type": "integer", "default": 10}
        }
    }
)
async def tool_get_news(ticker: str = None, limit: int = 10) -> Dict:
    """Get news"""
    # This would need db session - simplified for now
    return {"message": "News retrieval requires database session"}

@register_tool(
    "summarize_filings",
    "Summarize SEC filings for a ticker",
    {
        "type": "object",
        "properties": {
            "ticker": {"type": "string"}
        },
        "required": ["ticker"]
    }
)
async def tool_summarize_filings(ticker: str) -> Dict:
    """Summarize filings"""
    return {"message": "Filings summary requires database session"}

@register_tool(
    "explain_pnl",
    "Explain portfolio PnL",
    {
        "type": "object",
        "properties": {
            "portfolio_id": {"type": "string"}
        },
        "required": ["portfolio_id"]
    }
)
async def tool_explain_pnl(portfolio_id: str) -> Dict:
    """Explain PnL"""
    return {"message": "PnL explanation requires database session"}

@register_tool(
    "compute_risk",
    "Compute portfolio risk metrics",
    {
        "type": "object",
        "properties": {
            "portfolio_id": {"type": "string"}
        },
        "required": ["portfolio_id"]
    }
)
async def tool_compute_risk(portfolio_id: str) -> Dict:
    """Compute risk"""
    return {"message": "Risk computation requires database session"}

@register_tool(
    "simulate_scenario",
    "Run scenario simulation",
    {
        "type": "object",
        "properties": {
            "portfolio_id": {"type": "string"},
            "scenario_type": {"type": "string"},
            "params": {"type": "object"}
        },
        "required": ["portfolio_id", "scenario_type"]
    }
)
async def tool_simulate_scenario(portfolio_id: str, scenario_type: str, params: Dict = None) -> Dict:
    """Simulate scenario"""
    return {"message": "Scenario simulation requires database session"}

@register_tool(
    "analyze_portfolio",
    "Analyze portfolio composition and performance",
    {
        "type": "object",
        "properties": {
            "portfolio_id": {"type": "string"}
        },
        "required": ["portfolio_id"]
    }
)
async def tool_analyze_portfolio(portfolio_id: str) -> Dict:
    """Analyze portfolio"""
    return {"message": "Portfolio analysis requires database session"}
