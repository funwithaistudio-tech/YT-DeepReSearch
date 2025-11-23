"""Deep Researcher - Orchestrates multi-source research."""

from typing import Dict, List
from loguru import logger
from .perplexity_client import PerplexityClient


class DeepResearcher:
    """Deep research orchestrator using Perplexity API."""
    
    def __init__(self, perplexity_api_key: str, gemini_api_key: str = None):
        """
        Initialize Deep Researcher.
        
        Args:
            perplexity_api_key: Perplexity API key
            gemini_api_key: Gemini API key (optional, for compatibility)
        """
        self.perplexity = PerplexityClient(perplexity_api_key)
        logger.info("DeepResearcher initialized")
    
    def research(self, topic: str, depth: str = "deep") -> Dict:
        """
        Perform deep research on a topic.
        
        Args:
            topic: Research topic
            depth: Research depth (quick, medium, deep)
        
        Returns:
            Research data dictionary
        """
        logger.info(f"Starting research on topic: {topic} (depth: {depth})")
        
        # Determine number of queries based on depth
        num_queries = {"quick": 3, "medium": 5, "deep": 8}.get(depth, 5)
        
        # Generate research queries
        queries = self._generate_queries(topic, num_queries)
        
        # Execute research
        results = []
        for query in queries:
            try:
                response = self.perplexity.search(query)
                content = self.perplexity.extract_content(response)
                citations = self.perplexity.extract_citations(response)
                
                results.append({
                    "query": query,
                    "content": content,
                    "citations": citations
                })
                
                logger.info(f"Completed query: {query[:50]}...")
            
            except Exception as e:
                logger.error(f"Failed query '{query}': {str(e)}")
                results.append({
                    "query": query,
                    "content": "",
                    "citations": [],
                    "error": str(e)
                })
        
        return {
            "topic": topic,
            "depth": depth,
            "results": results,
            "total_queries": len(queries),
            "successful_queries": sum(1 for r in results if not r.get("error"))
        }
    
    def _generate_queries(self, topic: str, num_queries: int) -> List[str]:
        """Generate research queries for a topic."""
        base_queries = [
            f"What is {topic}? Provide comprehensive overview with examples.",
            f"History and evolution of {topic}",
            f"Latest developments and current state of {topic}",
            f"Key figures and contributors in {topic}",
            f"Technical details and mechanisms of {topic}",
            f"Real-world applications and case studies of {topic}",
            f"Controversies and debates about {topic}",
            f"Future trends and implications of {topic}"
        ]
        
        return base_queries[:num_queries]
