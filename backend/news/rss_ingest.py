"""
RSS ingestion for news feeds
"""
import feedparser
import httpx
from typing import List, Dict, Optional
from datetime import datetime
from backend.utils.logger import logger
import re

RSS_FEEDS = {
    "yahoo_finance": "https://finance.yahoo.com/news/rssindex",
    "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "marketwatch": "https://feeds.marketwatch.com/marketwatch/topstories"
}

def extract_tickers(text: str) -> List[str]:
    """Extract ticker symbols from text using regex"""
    # Pattern for ticker symbols (1-5 uppercase letters, optionally with dots)
    pattern = r'\b([A-Z]{1,5}(?:\.[A-Z]{1,5})?)\b'
    matches = re.findall(pattern, text)
    
    # Filter out common false positives
    false_positives = {"THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM", "HIS", "HOW", "ITS", "MAY", "NEW", "NOW", "OLD", "SEE", "TWO", "WHO", "WAY", "USE", "SHE", "HER", "HIM", "HIS", "ITS", "OUR", "THEIR"}
    
    tickers = []
    for match in matches:
        if match not in false_positives and len(match) >= 1:
            tickers.append(match)
    
    return list(set(tickers))  # Remove duplicates

async def fetch_rss_feed(url: str) -> Optional[feedparser.FeedParserDict]:
    """Fetch and parse RSS feed"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            return feed
    except Exception as e:
        logger.error(f"Error fetching RSS feed {url}: {e}")
        return None

async def parse_feed_articles(feed: feedparser.FeedParserDict, source: str) -> List[Dict]:
    """Parse articles from RSS feed"""
    articles = []
    
    for entry in feed.entries:
        try:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "") or entry.get("description", "")
            published = entry.get("published_parsed")
            
            # Parse published date
            published_at = None
            if published:
                try:
                    published_at = datetime(*published[:6])
                except:
                    pass
            
            if not published_at:
                published_at = datetime.utcnow()
            
            # Extract tickers from title and summary
            text = f"{title} {summary}"
            tickers = extract_tickers(text)
            
            article = {
                "title": title,
                "content": summary,
                "url": link,
                "source": source,
                "published_at": published_at.isoformat(),
                "tickers": tickers
            }
            
            articles.append(article)
        
        except Exception as e:
            logger.warning(f"Error parsing article: {e}")
            continue
    
    return articles

async def ingest_all_feeds() -> List[Dict]:
    """Ingest all RSS feeds"""
    all_articles = []
    
    for source, url in RSS_FEEDS.items():
        logger.info(f"Ingesting RSS feed: {source}")
        feed = await fetch_rss_feed(url)
        
        if feed:
            articles = await parse_feed_articles(feed, source)
            all_articles.extend(articles)
            logger.info(f"Parsed {len(articles)} articles from {source}")
    
    return all_articles
