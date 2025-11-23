"""Unit tests for utility functions."""

import pytest
from src.utils.helpers import (
    estimate_tokens,
    chunk_text,
    sanitize_filename
)


class TestHelpers:
    """Test helper utility functions."""
    
    def test_estimate_tokens(self):
        """Test token estimation."""
        text = "This is a test sentence with some words."
        tokens = estimate_tokens(text)
        assert tokens > 0
        assert tokens == len(text) // 4
    
    def test_chunk_text_small(self):
        """Test chunking text that doesn't need splitting."""
        text = "Short text"
        chunks = chunk_text(text, max_tokens=100)
        assert len(chunks) == 1
        assert chunks[0] == text
    
    def test_chunk_text_large(self):
        """Test chunking large text."""
        text = "word " * 5000  # Large text
        chunks = chunk_text(text, max_tokens=1000, overlap=100)
        assert len(chunks) > 1
        # Each chunk should be within limits
        for chunk in chunks:
            assert len(chunk) <= 1000 * 4 + 500  # Allow some margin
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test invalid characters
        filename = 'test<file>name:with*invalid?chars'
        sanitized = sanitize_filename(filename)
        assert '<' not in sanitized
        assert '>' not in sanitized
        assert ':' not in sanitized
        assert '*' not in sanitized
        assert '?' not in sanitized
        
        # Test length limit
        long_filename = "a" * 300
        sanitized = sanitize_filename(long_filename)
        assert len(sanitized) <= 200
