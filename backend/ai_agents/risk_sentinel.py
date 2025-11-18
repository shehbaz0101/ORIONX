"""
Risk Sentinel Agent
"""
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.risk.risk_service import calculate_portfolio_risk
from backend.portfolio.service import get_portfolio_holdings
from uuid import UUID

async def run_risk_sentinel(db: AsyncSession, portfolio_id: UUID) -> Dict:
    """Monitor risk metrics and generate warnings"""
    try:
        holdings = await get_portfolio_holdings(db, portfolio_id)
        risk_data = await calculate_portfolio_risk(holdings)
        
        warnings = risk_data.get("warnings", [])
        
        return {
            "portfolio_id": str(portfolio_id),
            "risk_metrics": {
                "max_volatility": max(risk_data.get("volatilities", {}).values()) if risk_data.get("volatilities") else 0,
                "max_concentration": risk_data.get("concentration", {}).get("max_concentration", 0),
                "var_95_pct": risk_data.get("var", {}).get("var_95_pct", 0)
            },
            "warnings": warnings,
            "alert_level": "high" if len(warnings) > 2 else "medium" if warnings else "low"
        }
    
    except Exception as e:
        logger.error(f"Error in risk sentinel: {e}")
        return {"error": str(e)}
