"""
Database initialization - create tables and setup extensions
"""
from sqlalchemy import text
from backend.db.db import engine, Base
from backend.utils.logger import logger

async def setup_extensions():
    """Setup PostgreSQL extensions (pgvector only - TimescaleDB not available in Supabase)"""
    async with engine.begin() as conn:
        try:
            # Enable pgvector extension (required for Supabase)
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            logger.info("pgvector extension enabled")
        except Exception as e:
            logger.warning(f"Could not enable pgvector extension: {e}")
        
        # Note: TimescaleDB is not available in Supabase free tier
        # Use regular PostgreSQL tables with proper indexing instead

async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        # Import all models to ensure they're registered
        from backend.db import models
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

async def drop_tables():
    """Drop all database tables (use with caution)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.warning("All database tables dropped")
