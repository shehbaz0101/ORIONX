"""
Portfolio API routes
"""
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.db import get_db
from backend.portfolio import service, pnl, exposure, factors
from backend.auth.dependencies import get_current_user
from backend.db.models import User, Portfolio
from typing import Optional
from uuid import UUID

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])

@router.post("/create")
async def create_portfolio(
    name: str = Query(...),
    description: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new portfolio"""
    portfolio = await service.create_portfolio(db, current_user.id, name, description)
    return {
        "id": str(portfolio.id),
        "name": portfolio.name,
        "description": portfolio.description
    }

@router.post("/upload")
async def upload_portfolio(
    portfolio_id: UUID = Query(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload portfolio holdings via CSV"""
    content = await file.read()
    csv_content = content.decode("utf-8")
    
    holdings_data = await service.parse_csv_holdings(csv_content)
    added_count = await service.add_holdings_to_portfolio(db, portfolio_id, holdings_data)
    
    return {
        "message": f"Added {added_count} holdings",
        "count": added_count
    }

@router.get("/valuation")
async def get_portfolio_valuation(
    portfolio_id: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get portfolio valuation and PnL"""
    holdings = await service.get_portfolio_holdings(db, portfolio_id)
    
    pnl_data = await pnl.calculate_portfolio_pnl(holdings)
    sector_exp = await exposure.calculate_sector_exposure(holdings)
    asset_exp = await exposure.calculate_asset_class_exposure(holdings)
    currency_exp = await exposure.calculate_currency_exposure(holdings)
    
    return {
        "pnl": pnl_data,
        "exposure": {
            "sector": sector_exp,
            "asset_class": asset_exp,
            "currency": currency_exp
        }
    }
