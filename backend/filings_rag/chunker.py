"""
Text chunker for RAG - split documents into chunks
"""
from typing import List
import re

def chunk_text(text: str, chunk_size: int = 1024, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    # Split by sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence.split())
        
        if current_length + sentence_length > chunk_size and current_chunk:
            # Save current chunk
            chunk_text = " ".join(current_chunk)
            chunks.append(chunk_text)
            
            # Start new chunk with overlap
            overlap_words = chunk_text.split()[-overlap:] if len(chunk_text.split()) > overlap else []
            current_chunk = overlap_words
            current_length = len(overlap_words)
        
        current_chunk.append(sentence)
        current_length += sentence_length
    
    # Add final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def chunk_by_paragraphs(text: str, max_chunk_size: int = 1024) -> List[str]:
    """Chunk text by paragraphs, respecting max size"""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_length = 0
    
    for para in paragraphs:
        para_length = len(para.split())
        
        if current_length + para_length > max_chunk_size and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_length = para_length
        else:
            current_chunk.append(para)
            current_length += para_length
    
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    
    return chunks
