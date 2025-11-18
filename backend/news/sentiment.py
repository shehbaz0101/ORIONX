"""
Sentiment analysis for news articles using AI
"""
import httpx
import os
from typing import Dict, Optional
from backend.utils.logger import logger

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def analyze_sentiment(text: str) -> Dict[str, float]:
    """Analyze sentiment of news text using DeepSeek via OpenRouter"""
    if not OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY not set, skipping sentiment analysis")
        return {"score": 0.0, "label": "neutral"}
    
    try:
        prompt = f"""Analyze the sentiment of this financial news text and return a JSON object with:
- "score": a float between -1 (very negative) and 1 (very positive)
- "label": one of "positive", "negative", or "neutral"

Text: {text[:1000]}  # Limit to 1000 chars

Return only the JSON object, no other text."""

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-chat",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 100
                }
            )
            response.raise_for_status()
            data = response.json()
            
            content = data["choices"][0]["message"]["content"]
            
            # Try to parse JSON from response
            import json
            try:
                # Extract JSON from response
                content = content.strip()
                if content.startswith("```"):
                    # Remove code block markers
                    lines = content.split("\n")
                    content = "\n".join(lines[1:-1])
                
                sentiment = json.loads(content)
                return sentiment
            except:
                # Fallback: simple keyword-based sentiment
                return simple_sentiment(text)
    
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return simple_sentiment(text)

def simple_sentiment(text: str) -> Dict[str, float]:
    """Simple keyword-based sentiment fallback"""
    text_lower = text.lower()
    
    positive_words = ["gain", "rise", "up", "surge", "rally", "profit", "growth", "beat", "strong", "positive"]
    negative_words = ["fall", "drop", "down", "plunge", "loss", "decline", "miss", "weak", "negative", "crash"]
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        score = min(0.7, 0.3 + (positive_count - negative_count) * 0.1)
        label = "positive"
    elif negative_count > positive_count:
        score = max(-0.7, -0.3 - (negative_count - positive_count) * 0.1)
        label = "negative"
    else:
        score = 0.0
        label = "neutral"
    
    return {"score": score, "label": label}
