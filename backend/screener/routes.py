"""
Screener API routes
"""
from fastapi import APIRouter, Depends, Query
from backend.screener import service, nlp_screen
from typing import List, Optional, Dict

router = APIRouter(prefix="/api/screener", tags=["screener"])

@router.post("/run")
async def run_screener(
    symbols: List[str] = Query(...),
    filters: Optional[Dict] = Query(None),
    screen_type: str = Query("technical", regex="^(technical|fundamental|both)$")
):
    """Run screener"""
    results = []
    
    if screen_type in ["technical", "both"]:
        tech_results = await service.run_technical_screen(symbols, filters or {})
        results.extend(tech_results)
    
    if screen_type in ["fundamental", "both"]:
        fund_results = await service.run_fundamental_screen(symbols, filters or {})
        results.extend(fund_results)
    
    return {"results": results, "count": len(results)}

@router.post("/nlp")
async def nlp_screener(
    query: str = Query(...),
    symbols: List[str] = Query(...)
):
    """Run NLP-based screener"""
    filters = await nlp_screen.parse_nlp_query(query)
    results = await service.run_fundamental_screen(symbols, filters)
    return {"filters": filters, "results": results, "count": len(results)}
