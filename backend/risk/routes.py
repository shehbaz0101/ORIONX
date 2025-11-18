"""
Risk API routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.db import get_db
from backend.risk import risk_service
from backend.portfolio.service import get_portfolio_holdings
from backend.auth.dependencies import get_current_user
from backend.db.models import User
from uuid import UUID

router = APIRouter(prefix="/api/risk", tags=["risk"])

@router.get("/overview")
async def get_risk_overview(
    portfolio_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive risk overview"""
    holdings = await get_portfolio_holdings(db, portfolio_id)
    risk_data = await risk_service.calculate_portfolio_risk(holdings)
    return risk_data
