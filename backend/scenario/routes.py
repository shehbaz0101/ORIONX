"""
Scenario API routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.db import get_db
from backend.scenario import service
from backend.portfolio.service import get_portfolio_holdings
from backend.auth.dependencies import get_current_user
from backend.db.models import User
from uuid import UUID

router = APIRouter(prefix="/api/scenario", tags=["scenario"])

@router.post("/simulate")
async def simulate_scenario(
    portfolio_id: UUID = Query(...),
    scenario_type: str = Query(..., regex="^(rate_shock|fx_shock|volatility_shock)$"),
    params: dict = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Run scenario simulation"""
    holdings = await get_portfolio_holdings(db, portfolio_id)
    
    if scenario_type == "rate_shock":
        shock_bps = params.get("shock_bps", 100)
        result = await service.simulate_rate_shock(holdings, shock_bps)
    elif scenario_type == "fx_shock":
        currency = params.get("currency", "EUR")
        shock_pct = params.get("shock_pct", 10.0)
        result = await service.simulate_fx_shock(holdings, currency, shock_pct)
    elif scenario_type == "volatility_shock":
        vol_mult = params.get("vol_multiplier", 2.0)
        result = await service.simulate_volatility_shock(holdings, vol_mult)
    else:
        return {"error": "Invalid scenario type"}
    
    return result
