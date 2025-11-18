"""
Portfolio service - CSV ingestion and portfolio management
"""
import csv
import io
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.models import Portfolio, Holding
from backend.market_data import metadata
from backend.utils.logger import logger
from typing import List, Dict
from uuid import UUID

async def create_portfolio(
    db: AsyncSession,
    user_id: UUID,
    name: str,
    description: str = None
) -> Portfolio:
    """Create a new portfolio"""
    portfolio = Portfolio(
        user_id=user_id,
        name=name,
        description=description
    )
    db.add(portfolio)
    await db.commit()
    await db.refresh(portfolio)
    return portfolio

async def parse_csv_holdings(csv_content: str) -> List[Dict]:
    """Parse CSV content into holdings list"""
    holdings = []
    reader = csv.DictReader(io.StringIO(csv_content))
    
    for row in reader:
        try:
            symbol = row.get("symbol", "").strip().upper()
            quantity = float(row.get("quantity", 0))
            cost_basis = float(row.get("cost_basis", 0))
            currency = row.get("currency", "USD").strip().upper()
            asset_type = row.get("asset_type", "equity").strip().lower()
            
            if symbol and quantity > 0:
                holdings.append({
                    "symbol": symbol,
                    "quantity": quantity,
                    "cost_basis": cost_basis,
                    "currency": currency,
                    "asset_type": asset_type
                })
        except Exception as e:
            logger.warning(f"Error parsing CSV row: {e}")
            continue
    
    return holdings

async def add_holdings_to_portfolio(
    db: AsyncSession,
    portfolio_id: UUID,
    holdings_data: List[Dict]
) -> int:
    """Add holdings to portfolio"""
    added_count = 0
    
    for holding_data in holdings_data:
        # Check if holding already exists
        result = await db.execute(
            select(Holding).where(
                Holding.portfolio_id == portfolio_id,
                Holding.symbol == holding_data["symbol"]
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing
            existing.quantity = holding_data["quantity"]
            existing.cost_basis = holding_data["cost_basis"]
        else:
            # Create new
            holding = Holding(
                portfolio_id=portfolio_id,
                symbol=holding_data["symbol"],
                quantity=holding_data["quantity"],
                cost_basis=holding_data["cost_basis"],
                currency=holding_data.get("currency", "USD"),
                asset_type=holding_data.get("asset_type", "equity")
            )
            db.add(holding)
            added_count += 1
    
    await db.commit()
    return added_count

async def get_portfolio_holdings(
    db: AsyncSession,
    portfolio_id: UUID
) -> List[Holding]:
    """Get all holdings for a portfolio"""
    result = await db.execute(
        select(Holding).where(Holding.portfolio_id == portfolio_id)
    )
    return result.scalars().all()
