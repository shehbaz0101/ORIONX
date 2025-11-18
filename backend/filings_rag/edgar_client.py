"""
EDGAR client for fetching SEC filings
"""
import httpx
from typing import List, Dict, Optional
from backend.utils.logger import logger
import re

EDGAR_BASE = "https://www.sec.gov"
CIK_LOOKUP_URL = f"{EDGAR_BASE}/cgi-bin/browse-edgar"

# Common ticker to CIK mapping (we'll fetch dynamically)
_ticker_to_cik_cache = {}

async def get_cik_from_ticker(ticker: str) -> Optional[str]:
    """Get CIK from ticker symbol"""
    if ticker in _ticker_to_cik_cache:
        return _ticker_to_cik_cache[ticker]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Use SEC's company tickers JSON file
            url = f"{EDGAR_BASE}/files/company_tickers.json"
            response = await client.get(url, headers={"User-Agent": "ORIONX contact@example.com"})
            response.raise_for_status()
            data = response.json()
            
            # Find ticker in data
            for entry in data.values():
                if entry.get("ticker", "").upper() == ticker.upper():
                    cik = str(entry.get("cik_str", ""))
                    _ticker_to_cik_cache[ticker] = cik
                    return cik
    
    except Exception as e:
        logger.error(f"Error fetching CIK for {ticker}: {e}")
    
    return None

async def get_filing_index(cik: str, filing_type: str = "10-K") -> List[Dict]:
    """Get filing index for a CIK"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"{EDGAR_BASE}/cgi-bin/browse-edgar"
            params = {
                "action": "getcompany",
                "CIK": cik,
                "type": filing_type,
                "count": 10
            }
            response = await client.get(url, params=params, headers={"User-Agent": "ORIONX contact@example.com"})
            response.raise_for_status()
            
            # Parse HTML to extract filing links
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            filings = []
            for row in soup.find_all("tr")[1:]:  # Skip header
                cells = row.find_all("td")
                if len(cells) >= 4:
                    filing_date = cells[3].text.strip()
                    link = cells[1].find("a")
                    if link:
                        href = link.get("href")
                        if href:
                            filings.append({
                                "filing_date": filing_date,
                                "url": f"{EDGAR_BASE}{href}"
                            })
            
            return filings
    
    except Exception as e:
        logger.error(f"Error fetching filing index for CIK {cik}: {e}")
        return []

async def get_filing_content(filing_url: str) -> Optional[str]:
    """Download and extract text from filing"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(filing_url, headers={"User-Agent": "ORIONX contact@example.com"})
            response.raise_for_status()
            
            # If it's a link to the actual filing document
            if "ix?doc=" in filing_url:
                # Extract document URL
                doc_url = filing_url.split("ix?doc=")[1]
                doc_response = await client.get(doc_url, headers={"User-Agent": "ORIONX contact@example.com"})
                doc_response.raise_for_status()
                content = doc_response.text
            else:
                content = response.text
            
            # Extract text from HTML
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
    
    except Exception as e:
        logger.error(f"Error fetching filing content from {filing_url}: {e}")
        return None
