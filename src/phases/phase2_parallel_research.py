"""Phase 2: Parallel Multi-Source Research - Execute research queries in parallel."""

import concurrent.futures
from typing import Dict, List
from loguru import logger
from research.perplexity_client import PerplexityClient


class Phase2ParallelResearch:
    """Phase 2: Execute parallel research queries across multiple sources."""
    
    def __init__(self, perplexity_client: PerplexityClient, max_workers: int = 5):
        """
        Initialize Phase 2.
        
        Args:
            perplexity_client: Perplexity client for research
            max_workers: Maximum parallel workers
        """
        self.perplexity = perplexity_client
        self.max_workers = max_workers
    
    def execute(self, phase1_output: Dict) -> Dict[str, any]:
        """
        Execute Phase 2: Parallel Multi-Source Research.
        
        Args:
            phase1_output: Output from Phase 1
        
        Returns:
            Dictionary with research results
        """
        logger.info("Phase 2: Starting parallel multi-source research")
        
        sub_queries = phase1_output.get("data", {}).get("sub_queries", [])
        
        if not sub_queries:
            logger.error("No sub-queries provided from Phase 1")
            return {
                "phase": 2,
                "status": "failed",
                "error": "No sub-queries provided"
            }
        
        # Execute queries in parallel
        research_results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all queries
            future_to_query = {
                executor.submit(self._research_query, query): query
                for query in sub_queries
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    result = future.result()
                    research_results.append(result)
                    logger.info(f"Completed research for: {query.get('query', '')[:50]}...")
                except Exception as e:
                    logger.error(f"Research failed for query: {str(e)}")
                    research_results.append({
                        "query": query,
                        "content": "",
                        "citations": [],
                        "error": str(e)
                    })
        
        logger.info(f"Phase 2 complete: Researched {len(research_results)} queries")
        
        return {
            "phase": 2,
            "status": "completed",
            "data": {
                "research_results": research_results,
                "total_queries": len(sub_queries),
                "successful_queries": sum(1 for r in research_results if not r.get("error"))
            }
        }
    
    def _research_query(self, query: Dict) -> Dict:
        """
        Research a single query.
        
        Args:
            query: Query dictionary with 'query' and 'focus' keys
        
        Returns:
            Research result dictionary
        """
        query_text = query.get("query", "")
        focus = query.get("focus", "general")
        
        try:
            # Enhance query with focus context
            enhanced_query = f"{query_text}\n\nFocus area: {focus}\nProvide detailed, well-cited information."
            
            response = self.perplexity.search(
                query=enhanced_query,
                max_tokens=4000,
                temperature=0.2
            )
            
            content = self.perplexity.extract_content(response)
            citations = self.perplexity.extract_citations(response)
            
            return {
                "query": query,
                "content": content,
                "citations": citations,
                "word_count": len(content.split()),
                "focus": focus
            }
        
        except Exception as e:
            logger.error(f"Failed to research query '{query_text}': {str(e)}")
            raise
