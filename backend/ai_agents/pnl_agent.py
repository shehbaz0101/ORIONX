"""
PnL Explanation Agent
"""
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.portfolio.service import get_portfolio_holdings
from backend.portfolio.pnl import calculate_portfolio_pnl
from uuid import UUID

async def run_pnl_explanation(db: AsyncSession, portfolio_id: UUID) -> Dict:
    """Explain portfolio PnL"""
    try:
        holdings = await get_portfolio_holdings(db, portfolio_id)
        pnl_data = await calculate_portfolio_pnl(holdings)
        
        # Generate explanation
        explanation = {
            "portfolio_id": str(portfolio_id),
            "total_pnl": pnl_data.get("total_pnl", 0),
            "total_pnl_pct": pnl_data.get("total_pnl_pct", 0),
            "top_contributors": sorted(
                pnl_data.get("positions", []),
                key=lambda x: x.get("unrealized_pnl", 0),
                reverse=True
            )[:5],
            "explanation": f"Portfolio PnL: {pnl_data.get('total_pnl_pct', 0):.2f}%"
        }
        
        return explanation
    
    except Exception as e:
        logger.error(f"Error in PnL explanation: {e}")
        return {"error": str(e)}
