"""
Real-Time Drawdown Watcher Agent
"""
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.portfolio.service import get_portfolio_holdings
from backend.portfolio.pnl import calculate_portfolio_pnl
from uuid import UUID

async def run_drawdown_watcher(db: AsyncSession, portfolio_id: UUID, threshold: float = -5.0) -> Dict:
    """Monitor portfolio drawdowns"""
    try:
        holdings = await get_portfolio_holdings(db, portfolio_id)
        pnl_data = await calculate_portfolio_pnl(holdings)
        
        drawdown_pct = pnl_data.get("total_pnl_pct", 0)
        
        alert = None
        if drawdown_pct < threshold:
            alert = {
                "type": "drawdown_alert",
                "portfolio_id": str(portfolio_id),
                "drawdown_pct": drawdown_pct,
                "threshold": threshold,
                "message": f"Portfolio drawdown exceeded threshold: {drawdown_pct:.2f}%"
            }
            logger.warning(f"Drawdown alert: {drawdown_pct:.2f}%")
        
        return {
            "drawdown_pct": drawdown_pct,
            "alert": alert
        }
    
    except Exception as e:
        logger.error(f"Error in drawdown watcher: {e}")
        return {"error": str(e)}
