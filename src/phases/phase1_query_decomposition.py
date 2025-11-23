"""Phase 1: Query Decomposition - Break down complex topics into sub-queries."""

from typing import Dict, List
from loguru import logger
from content.gemini_client import GeminiClient


class Phase1QueryDecomposition:
    """Phase 1: Decompose research topic into focused sub-queries."""
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize Phase 1.
        
        Args:
            gemini_client: Gemini client for query decomposition
        """
        self.gemini = gemini_client
    
    def execute(self, topic: str) -> Dict[str, any]:
        """
        Execute Phase 1: Query Decomposition.
        
        Args:
            topic: Research topic
        
        Returns:
            Dictionary with decomposed queries and metadata
        """
        logger.info(f"Phase 1: Decomposing topic: {topic}")
        
        prompt = f"""You are a research planning expert. Given a research topic, break it down into 5-8 focused sub-queries that will help gather comprehensive information.

Research Topic: {topic}

Generate sub-queries that cover:
1. Background and fundamentals
2. Historical context and evolution
3. Current state and recent developments
4. Key figures and contributors
5. Technical/Scientific details
6. Real-world applications and examples
7. Controversies and debates
8. Future implications and trends

Provide your response as a JSON object with this structure:
{{
    "main_topic": "{topic}",
    "sub_queries": [
        {{"query": "sub-query 1", "focus": "background"}},
        {{"query": "sub-query 2", "focus": "history"}},
        ...
    ],
    "keywords": ["keyword1", "keyword2", ...],
    "complexity_level": "basic|intermediate|advanced"
}}"""
        
        try:
            result = self.gemini.generate_structured_content(
                prompt=prompt,
                schema={"main_topic": "str", "sub_queries": "list", "keywords": "list"},
                temperature=0.3
            )
            
            # Validate result
            if "sub_queries" not in result or not result["sub_queries"]:
                logger.warning("No sub-queries generated, using fallback")
                result = self._generate_fallback_queries(topic)
            
            logger.info(f"Phase 1 complete: Generated {len(result.get('sub_queries', []))} sub-queries")
            
            return {
                "phase": 1,
                "status": "completed",
                "data": result
            }
        
        except Exception as e:
            logger.error(f"Phase 1 failed: {str(e)}")
            return {
                "phase": 1,
                "status": "failed",
                "error": str(e),
                "data": self._generate_fallback_queries(topic)
            }
    
    def _generate_fallback_queries(self, topic: str) -> Dict:
        """Generate fallback queries if API fails."""
        return {
            "main_topic": topic,
            "sub_queries": [
                {"query": f"What is {topic}? Provide a comprehensive overview.", "focus": "background"},
                {"query": f"What is the history and evolution of {topic}?", "focus": "history"},
                {"query": f"What are the latest developments in {topic}?", "focus": "current"},
                {"query": f"Who are the key figures and contributors in {topic}?", "focus": "people"},
                {"query": f"What are the technical details and mechanisms of {topic}?", "focus": "technical"},
                {"query": f"What are real-world applications and examples of {topic}?", "focus": "applications"},
                {"query": f"What are the controversies and debates surrounding {topic}?", "focus": "controversies"},
                {"query": f"What is the future outlook for {topic}?", "focus": "future"}
            ],
            "keywords": topic.split(),
            "complexity_level": "intermediate"
        }
