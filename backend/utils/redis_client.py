"""
Redis client for caching and pub/sub
"""
import os
import json
import redis.asyncio as redis
from typing import Optional, Any
from backend.utils.logger import logger

_redis_client: Optional[redis.Redis] = None

async def get_redis() -> redis.Redis:
    """Get or create Redis connection (Upstash Redis)"""
    global _redis_client
    
    if _redis_client is None:
        # Use REDIS_URL (Upstash) for cloud deployment, fallback for local dev
        redis_url = os.getenv(
            "REDIS_URL",
            os.getenv("UPSTASH_REDIS_URL", "redis://localhost:6379/0")
        )
        
        # Upstash Redis supports both REST API and Redis protocol
        # If URL contains 'upstash.io', ensure proper connection handling
        try:
            _redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True,
                health_check_interval=30
            )
            # Test connection
            await _redis_client.ping()
            logger.info(f"Connected to Redis (Upstash)")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    return _redis_client

async def close_redis():
    """Close Redis connection"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None

async def cache_get(key: str) -> Optional[Any]:
    """Get value from cache"""
    client = await get_redis()
    value = await client.get(key)
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return None

async def cache_set(key: str, value: Any, ttl: int = 3600):
    """Set value in cache with TTL"""
    client = await get_redis()
    if isinstance(value, (dict, list)):
        value = json.dumps(value)
    await client.setex(key, ttl, value)

async def cache_delete(key: str):
    """Delete key from cache"""
    client = await get_redis()
    await client.delete(key)
