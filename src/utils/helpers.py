"""Helper utilities for YT-DeepReSearch system."""

import time
import functools
from typing import Callable, Any, List
from loguru import logger


def retry_with_backoff(max_retries: int = 3, initial_delay: int = 5, backoff_factor: int = 2):
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay between retries
    
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay} seconds..."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_retries} attempts failed for {func.__name__}: {str(e)}"
                        )
            
            raise last_exception
        
        return wrapper
    return decorator


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    Uses a simple heuristic: ~4 characters per token.
    
    Args:
        text: Input text
    
    Returns:
        Estimated token count
    """
    return len(text) // 4


def chunk_text(text: str, max_tokens: int = 4000, overlap: int = 200) -> List[str]:
    """
    Chunk text into smaller pieces with overlap.
    
    Args:
        text: Input text to chunk
        max_tokens: Maximum tokens per chunk
        overlap: Number of tokens to overlap between chunks
    
    Returns:
        List of text chunks
    """
    max_chars = max_tokens * 4  # Approximate conversion
    overlap_chars = overlap * 4
    
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_chars
        
        # If not the last chunk, try to break at a sentence boundary
        if end < len(text):
            # Look for sentence endings within the last 200 characters
            search_start = max(end - 200, start)
            last_period = text.rfind('.', search_start, end)
            last_newline = text.rfind('\n', search_start, end)
            
            break_point = max(last_period, last_newline)
            if break_point > start:
                end = break_point + 1
        
        chunks.append(text[start:end])
        
        # Move start forward, accounting for overlap
        start = end - overlap_chars if end < len(text) else end
    
    return chunks


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a string to be used as a filename.
    
    Args:
        filename: Input filename
    
    Returns:
        Sanitized filename
    """
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    max_length = 200
    if len(filename) > max_length:
        filename = filename[:max_length]
    
    return filename
