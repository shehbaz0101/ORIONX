"""
Screener Intelligence Agent
"""
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.screener.service import run_fundamental_screen
from typing import List

async def run_screener_agent(db: AsyncSession, symbols: List[str], filters: dict = None) -> Dict:
    """Run intelligent screener and explain results"""
    try:
        results = await run_fundamental_screen(symbols, filters or {})
        
        return {
            "symbols_screened": len(symbols),
            "matches": len(results),
            "results": results[:10],  # Top 10
            "summary": f"Found {len(results)} matches out of {len(symbols)} symbols"
        }
    
    except Exception as e:
        logger.error(f"Error in screener agent: {e}")
        return {"error": str(e)}
