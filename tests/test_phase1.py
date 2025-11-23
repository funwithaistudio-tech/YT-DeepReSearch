"""Unit tests for Phase 1 - Query Decomposition."""

import pytest
from unittest.mock import Mock, MagicMock
from src.phases.phase1_query_decomposition import Phase1QueryDecomposition


class TestPhase1QueryDecomposition:
    """Test Phase 1: Query Decomposition."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.mock_gemini = Mock()
        self.phase1 = Phase1QueryDecomposition(self.mock_gemini)
    
    def test_execute_success(self):
        """Test successful query decomposition."""
        # Mock Gemini response
        self.mock_gemini.generate_structured_content.return_value = {
            "main_topic": "Quantum Computing",
            "sub_queries": [
                {"query": "What is quantum computing?", "focus": "background"},
                {"query": "History of quantum computing", "focus": "history"}
            ],
            "keywords": ["quantum", "computing", "qubit"],
            "complexity_level": "advanced"
        }
        
        result = self.phase1.execute("Quantum Computing")
        
        assert result["status"] == "completed"
        assert result["phase"] == 1
        assert "sub_queries" in result["data"]
        assert len(result["data"]["sub_queries"]) >= 2
    
    def test_execute_fallback(self):
        """Test fallback when API fails."""
        # Mock Gemini failure
        self.mock_gemini.generate_structured_content.side_effect = Exception("API Error")
        
        result = self.phase1.execute("Test Topic")
        
        assert result["status"] == "failed"
        assert "error" in result
        assert "sub_queries" in result["data"]  # Fallback should provide queries
    
    def test_generate_fallback_queries(self):
        """Test fallback query generation."""
        topic = "Machine Learning"
        fallback = self.phase1._generate_fallback_queries(topic)
        
        assert fallback["main_topic"] == topic
        assert len(fallback["sub_queries"]) == 8
        assert all("query" in q and "focus" in q for q in fallback["sub_queries"])
