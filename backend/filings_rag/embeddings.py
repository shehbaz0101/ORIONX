"""
Generate embeddings for filing chunks using OpenRouter
"""
import httpx
import os
from typing import List, Optional
from backend.utils.logger import logger

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
EMBEDDINGS_URL = "https://openrouter.ai/api/v1/embeddings"

async def generate_embedding(text: str) -> Optional[List[float]]:
    """Generate embedding for text using OpenRouter"""
    if not OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY not set, cannot generate embeddings")
        return None
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                EMBEDDINGS_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "text-embedding-ada-002",  # Using OpenAI model via OpenRouter
                    "input": text[:8000]  # Limit text length
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if "data" in data and len(data["data"]) > 0:
                return data["data"][0]["embedding"]
    
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None
    
    return None

async def generate_embeddings_batch(texts: List[str]) -> List[Optional[List[float]]]:
    """Generate embeddings for multiple texts"""
    embeddings = []
    for text in texts:
        embedding = await generate_embedding(text)
        embeddings.append(embedding)
    return embeddings
