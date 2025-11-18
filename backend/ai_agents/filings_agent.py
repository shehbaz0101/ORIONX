"""
SEC Filing Intelligence Agent
"""
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.db.models import FilingDocument
from sqlalchemy import select, desc
from datetime import datetime, timedelta

async def run_filings_agent(db: AsyncSession) -> Dict:
    """Monitor new SEC filings and extract insights"""
    try:
        # Get recent filings (last 7 days)
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        
        result = await db.execute(
            select(FilingDocument)
            .where(FilingDocument.filing_date >= cutoff_date)
            .order_by(desc(FilingDocument.filing_date))
            .limit(20)
        )
        recent_filings = result.scalars().all()
        
        return {
            "date": datetime.utcnow().isoformat(),
            "recent_filings_count": len(recent_filings),
            "filings": [
                {
                    "ticker": f.ticker,
                    "filing_type": f.filing_type,
                    "filing_date": f.filing_date.isoformat()
                }
                for f in recent_filings
            ]
        }
    
    except Exception as e:
        logger.error(f"Error in filings agent: {e}")
        return {"error": str(e)}
