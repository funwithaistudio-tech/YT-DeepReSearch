"""Phase 3: Graph Construction - Build knowledge graph from research results."""

from typing import Dict, List, Set
from loguru import logger
from content.gemini_client import GeminiClient


class Phase3GraphConstruction:
    """Phase 3: Construct knowledge graph from research findings."""
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize Phase 3.
        
        Args:
            gemini_client: Gemini client for analysis
        """
        self.gemini = gemini_client
    
    def execute(self, phase2_output: Dict) -> Dict[str, any]:
        """
        Execute Phase 3: Graph Construction.
        
        Args:
            phase2_output: Output from Phase 2
        
        Returns:
            Dictionary with knowledge graph
        """
        logger.info("Phase 3: Building knowledge graph")
        
        research_results = phase2_output.get("data", {}).get("research_results", [])
        
        if not research_results:
            logger.error("No research results provided from Phase 2")
            return {
                "phase": 3,
                "status": "failed",
                "error": "No research results provided"
            }
        
        # Combine all research content
        combined_content = self._combine_research_content(research_results)
        
        # Build knowledge graph
        try:
            graph = self._build_knowledge_graph(combined_content, research_results)
            
            logger.info(f"Phase 3 complete: Built graph with {len(graph.get('nodes', []))} nodes")
            
            return {
                "phase": 3,
                "status": "completed",
                "data": graph
            }
        
        except Exception as e:
            logger.error(f"Phase 3 failed: {str(e)}")
            return {
                "phase": 3,
                "status": "failed",
                "error": str(e)
            }
    
    def _combine_research_content(self, research_results: List[Dict]) -> str:
        """Combine research results into single text."""
        combined = []
        
        for result in research_results:
            if result.get("content"):
                query_info = result.get("query", {})
                focus = query_info.get("focus", "general")
                combined.append(f"## {focus.upper()}\n{result['content']}\n")
        
        return "\n".join(combined)
    
    def _build_knowledge_graph(self, combined_content: str, research_results: List[Dict]) -> Dict:
        """
        Build knowledge graph from combined content.
        
        Args:
            combined_content: Combined research content
            research_results: Original research results
        
        Returns:
            Knowledge graph structure
        """
        prompt = f"""Analyze the following research content and extract a knowledge graph structure.

Research Content:
{combined_content[:15000]}  # Limit to avoid token overflow

Extract:
1. Main concepts and entities (nodes)
2. Relationships between concepts (edges)
3. Key facts and insights
4. Hierarchical structure (parent-child relationships)

Provide response as JSON:
{{
    "nodes": [
        {{"id": "node1", "label": "concept name", "type": "concept|person|event|fact", "importance": "high|medium|low"}},
        ...
    ],
    "edges": [
        {{"from": "node1", "to": "node2", "relationship": "causes|enables|related_to|...", "strength": 0.8}},
        ...
    ],
    "key_insights": ["insight 1", "insight 2", ...],
    "hierarchy_levels": ["level1", "level2", "level3"]
}}"""
        
        try:
            graph = self.gemini.generate_structured_content(
                prompt=prompt,
                schema={"nodes": "list", "edges": "list", "key_insights": "list"},
                temperature=0.3
            )
            
            # Add research metadata
            graph["research_sources"] = [
                {
                    "focus": r.get("query", {}).get("focus"),
                    "citations": r.get("citations", [])
                }
                for r in research_results
            ]
            
            return graph
        
        except Exception as e:
            logger.error(f"Failed to build knowledge graph: {str(e)}")
            # Return basic fallback structure
            return self._create_fallback_graph(research_results)
    
    def _create_fallback_graph(self, research_results: List[Dict]) -> Dict:
        """Create fallback graph structure."""
        nodes = []
        edges = []
        
        for i, result in enumerate(research_results):
            query_info = result.get("query", {})
            focus = query_info.get("focus", f"topic_{i}")
            
            nodes.append({
                "id": f"node_{i}",
                "label": focus,
                "type": "concept",
                "importance": "medium"
            })
            
            if i > 0:
                edges.append({
                    "from": f"node_{i-1}",
                    "to": f"node_{i}",
                    "relationship": "related_to",
                    "strength": 0.5
                })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "key_insights": ["Fallback graph structure generated"],
            "hierarchy_levels": ["level1", "level2"]
        }
