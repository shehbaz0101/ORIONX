"""
Scenario Simulation Agent
"""
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.scenario.service import simulate_rate_shock, simulate_fx_shock, simulate_volatility_shock
from backend.portfolio.service import get_portfolio_holdings
from uuid import UUID

async def run_scenario_agent(
    db: AsyncSession,
    portfolio_id: UUID,
    scenario_type: str = "rate_shock"
) -> Dict:
    """Run scenario simulation and explain outcomes"""
    try:
        holdings = await get_portfolio_holdings(db, portfolio_id)
        
        if scenario_type == "rate_shock":
            result = await simulate_rate_shock(holdings, shock_bps=100)
        elif scenario_type == "fx_shock":
            result = await simulate_fx_shock(holdings, currency="EUR", shock_pct=10.0)
        elif scenario_type == "volatility_shock":
            result = await simulate_volatility_shock(holdings, vol_multiplier=2.0)
        else:
            return {"error": "Invalid scenario type"}
        
        return {
            "portfolio_id": str(portfolio_id),
            "scenario": result,
            "explanation": f"Scenario impact: {result.get('impact_pct', 0):.2f}%"
        }
    
    except Exception as e:
        logger.error(f"Error in scenario agent: {e}")
        return {"error": str(e)}
