"""
Database connection and session management
"""
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.utils.logger import logger

# Database URL from environment (Supabase)
# Use SUPABASE_DB_URL for cloud deployment, fallback to DATABASE_URL for local dev
# Cloud deployments require SSL: add ?sslmode=require to connection string
database_url = os.getenv(
    "SUPABASE_DB_URL",
    os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/orionx"
    )
)

# Ensure SSL is enabled for cloud deployments (Supabase requires SSL)
if "supabase.co" in database_url and "sslmode" not in database_url:
    separator = "&" if "?" in database_url else "?"
    database_url = f"{database_url}{separator}sslmode=require"

DATABASE_URL = database_url

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()

async def get_db() -> AsyncSession:
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database - create tables and extensions"""
    from backend.db.init_db import create_tables, setup_extensions
    await setup_extensions()
    await create_tables()
    logger.info("Database initialized successfully")
