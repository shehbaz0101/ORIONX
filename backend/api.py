"""
Main API router - combines all route modules
"""
from fastapi import APIRouter
from backend.auth import routes as auth_routes
from backend.market_data import routes as market_routes
from backend.news import routes as news_routes
from backend.filings_rag import routes as filings_routes
from backend.portfolio import routes as portfolio_routes
from backend.risk import routes as risk_routes
from backend.screener import routes as screener_routes
from backend.scenario import routes as scenario_routes
from backend.ai_copilot import routes as ai_routes

# Create main router
router = APIRouter()

# Include all route modules
router.include_router(auth_routes.router)
router.include_router(market_routes.router)
router.include_router(news_routes.router)
router.include_router(filings_routes.router)
router.include_router(portfolio_routes.router)
router.include_router(risk_routes.router)
router.include_router(screener_routes.router)
router.include_router(scenario_routes.router)
router.include_router(ai_routes.router)
