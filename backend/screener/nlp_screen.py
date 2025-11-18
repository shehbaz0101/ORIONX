"""
NLP screen builder - convert natural language to filters
"""
import httpx
import os
import json
from typing import Dict
from backend.utils.logger import logger

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def parse_nlp_query(query: str) -> Dict:
    """Parse natural language query into filter dict"""
    if not OPENROUTER_API_KEY:
        return {}
    
    try:
        prompt = f"""Convert this stock screening query into a JSON filter object:
Query: {query}

Return JSON with possible fields:
- min_market_cap: number
- max_pe_ratio: number
- min_roe: number
- rsi_oversold: boolean
- rsi_overbought: boolean
- sector: string
- industry: string

Return only the JSON object, no other text."""

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 200
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            # Extract JSON
            content = content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])
            
            filters = json.loads(content)
            return filters
    
    except Exception as e:
        logger.error(f"Error parsing NLP query: {e}")
        return {}
