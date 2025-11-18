"""
AI Agents Runner - Schedule and execute agents
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from backend.utils.logger import logger
from backend.utils.redis_client import get_redis
from backend.ai_agents import (
    morning_briefing,
    drawdown_watcher,
    pnl_agent,
    earnings_agent,
    filings_agent,
    news_agent,
    risk_sentinel,
    screener_agent,
    scenario_agent
)
import asyncio
from datetime import datetime

scheduler = AsyncIOScheduler()

async def run_agent_task(agent_func, *args, **kwargs):
    """Wrapper to run agent task"""
    try:
        result = await agent_func(*args, **kwargs)
        logger.info(f"Agent {agent_func.__name__} completed")
        return result
    except Exception as e:
        logger.error(f"Agent {agent_func.__name__} failed: {e}")
        return {"error": str(e)}

def setup_agents(db_session_factory):
    """Setup scheduled agents"""
    
    # Morning Briefing - Daily at 8 AM
    scheduler.add_job(
        lambda: asyncio.create_task(
            run_agent_task(morning_briefing.run_morning_briefing, None, "system")
        ),
        trigger=CronTrigger(hour=8, minute=0),
        id="morning_briefing"
    )
    
    # Earnings Agent - Daily at 9 AM
    scheduler.add_job(
        lambda: asyncio.create_task(
            run_agent_task(earnings_agent.run_earnings_agent, None)
        ),
        trigger=CronTrigger(hour=9, minute=0),
        id="earnings_agent"
    )
    
    # Filings Agent - Daily at 10 AM
    scheduler.add_job(
        lambda: asyncio.create_task(
            run_agent_task(filings_agent.run_filings_agent, None)
        ),
        trigger=CronTrigger(hour=10, minute=0),
        id="filings_agent"
    )
    
    # News Agent - Every 4 hours
    scheduler.add_job(
        lambda: asyncio.create_task(
            run_agent_task(news_agent.run_news_agent, None)
        ),
        trigger=CronTrigger(hour="*/4"),
        id="news_agent"
    )
    
    logger.info("AI Agents scheduler configured")

def start_agents():
    """Start the agent scheduler"""
    scheduler.start()
    logger.info("AI Agents scheduler started")

def stop_agents():
    """Stop the agent scheduler"""
    scheduler.shutdown()
    logger.info("AI Agents scheduler stopped")
