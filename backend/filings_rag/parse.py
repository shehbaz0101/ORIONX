"""
Parse filing documents (HTML/PDF)
"""
from typing import Optional
from backend.utils.logger import logger

def parse_html_filing(html_content: str) -> Optional[str]:
    """Parse HTML filing and extract text"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    except Exception as e:
        logger.error(f"Error parsing HTML filing: {e}")
        return None

def parse_pdf_filing(pdf_content: bytes) -> Optional[str]:
    """Parse PDF filing and extract text"""
    try:
        from pypdf import PdfReader
        import io
        
        pdf_file = io.BytesIO(pdf_content)
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    
    except Exception as e:
        logger.error(f"Error parsing PDF filing: {e}")
        return None
