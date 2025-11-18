"""
ORIONX FastAPI Main Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from backend.utils.logger import logger
from backend.api import router
from backend.db.init_db import init_db
from backend.utils.redis_client import get_redis, close_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    # Startup
    logger.info("Starting ORIONX backend...")
    try:
        await init_db()
        await get_redis()  # Initialize Redis connection
        logger.info("ORIONX backend started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down ORIONX backend...")
    await close_redis()
    logger.info("ORIONX backend shut down")

# Create FastAPI app
app = FastAPI(
    title="ORIONX API",
    description="AI-powered Bloomberg Terminal alternative",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
# Allow localhost for development and cloud domains for production
import os

# Check if CORS_ORIGINS is set to "*" for production
cors_origins_env = os.getenv("CORS_ORIGINS", "")

if cors_origins_env == "*":
    # Production: Allow all origins
    cors_origins = ["*"]
else:
    # Development: Specific origins
    cors_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Add Vercel frontend URL if provided
    vercel_url = os.getenv("VERCEL_URL")
    if vercel_url:
        cors_origins.append(f"https://{vercel_url}")
        cors_origins.append(f"https://*.vercel.app")
    
    # Add custom domain if provided
    custom_domain = os.getenv("FRONTEND_DOMAIN")
    if custom_domain:
        cors_origins.append(f"https://{custom_domain}")
        cors_origins.append(f"https://*.{custom_domain}")
    
    # Allow all Vercel preview deployments
    cors_origins.append("https://*.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include main router
app.include_router(router)

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ORIONX"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ORIONX API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
