"""Phase 4: Hierarchical Tier Generation - Create multi-tier summarization."""

from typing import Dict, List
from loguru import logger
from content.gemini_client import GeminiClient
from utils.helpers import chunk_text, estimate_tokens


class Phase4HierarchicalTiers:
    """Phase 4: Generate hierarchical tiers for narrative structure."""
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize Phase 4.
        
        Args:
            gemini_client: Gemini client for summarization
        """
        self.gemini = gemini_client
    
    def execute(self, phase3_output: Dict, phase2_output: Dict) -> Dict[str, any]:
        """
        Execute Phase 4: Hierarchical Tier Generation.
        
        Args:
            phase3_output: Output from Phase 3 (knowledge graph)
            phase2_output: Output from Phase 2 (research results)
        
        Returns:
            Dictionary with hierarchical tiers
        """
        logger.info("Phase 4: Generating hierarchical tiers")
        
        graph = phase3_output.get("data", {})
        research_results = phase2_output.get("data", {}).get("research_results", [])
        
        try:
            # Generate three tiers: Executive, Intermediate, Detailed
            tiers = {
                "tier1_executive": self._generate_executive_tier(graph, research_results),
                "tier2_intermediate": self._generate_intermediate_tier(graph, research_results),
                "tier3_detailed": self._generate_detailed_tier(graph, research_results)
            }
            
            logger.info("Phase 4 complete: Generated 3 hierarchical tiers")
            
            return {
                "phase": 4,
                "status": "completed",
                "data": tiers
            }
        
        except Exception as e:
            logger.error(f"Phase 4 failed: {str(e)}")
            return {
                "phase": 4,
                "status": "failed",
                "error": str(e)
            }
    
    def _generate_executive_tier(self, graph: Dict, research_results: List[Dict]) -> Dict:
        """Generate executive summary tier (highest level)."""
        key_insights = graph.get("key_insights", [])
        nodes = graph.get("nodes", [])
        
        # Get top concepts
        high_importance_nodes = [n for n in nodes if n.get("importance") == "high"]
        
        prompt = f"""Create an executive summary (300-400 words) based on this knowledge graph.

Key Insights:
{chr(10).join(f'- {insight}' for insight in key_insights[:5])}

Main Concepts:
{chr(10).join(f'- {n.get("label")}' for n in high_importance_nodes[:5])}

Focus on:
1. The most important takeaway
2. Why this topic matters
3. Core concepts in simple terms
4. One compelling hook or story

Write in an engaging, accessible style suitable for a YouTube video introduction."""
        
        summary = self.gemini.generate_content(
            prompt=prompt,
            max_tokens=800,
            temperature=0.7,
            system_instruction="You are a master storyteller creating engaging educational content."
        )
        
        return {
            "level": "executive",
            "summary": summary,
            "word_count": len(summary.split()),
            "key_points": key_insights[:3]
        }
    
    def _generate_intermediate_tier(self, graph: Dict, research_results: List[Dict]) -> Dict:
        """Generate intermediate tier with moderate detail."""
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        key_insights = graph.get("key_insights", [])
        
        prompt = f"""Create an intermediate-level summary (800-1000 words) that elaborates on the key concepts.

Knowledge Graph:
- {len(nodes)} main concepts
- {len(edges)} relationships
- Key insights: {len(key_insights)}

Main Concepts:
{chr(10).join(f'- {n.get("label")} ({n.get("type")})' for n in nodes[:10])}

Key Insights:
{chr(10).join(f'- {insight}' for insight in key_insights[:8])}

Structure:
1. Context and background (2-3 paragraphs)
2. Main concepts explained (3-4 paragraphs)
3. How concepts connect (2 paragraphs)
4. Significance and implications (1-2 paragraphs)

Use storytelling techniques and real-world examples."""
        
        summary = self.gemini.generate_content(
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7,
            system_instruction="You are an expert educator creating comprehensive educational content."
        )
        
        return {
            "level": "intermediate",
            "summary": summary,
            "word_count": len(summary.split()),
            "concepts_covered": [n.get("label") for n in nodes[:10]]
        }
    
    def _generate_detailed_tier(self, graph: Dict, research_results: List[Dict]) -> Dict:
        """Generate detailed tier with full information."""
        # Combine all research content
        all_content = []
        for result in research_results:
            if result.get("content"):
                all_content.append(result["content"])
        
        combined = "\n\n".join(all_content)
        
        # Estimate tokens and chunk if necessary
        tokens = estimate_tokens(combined)
        
        if tokens > 12000:
            # Chunk and summarize
            chunks = chunk_text(combined, max_tokens=12000)
            chunk_summaries = []
            
            for i, chunk in enumerate(chunks[:3]):  # Limit to 3 chunks
                summary = self._summarize_chunk(chunk, i + 1, len(chunks))
                chunk_summaries.append(summary)
            
            detailed_content = "\n\n".join(chunk_summaries)
        else:
            detailed_content = combined
        
        return {
            "level": "detailed",
            "summary": detailed_content,
            "word_count": len(detailed_content.split()),
            "sources": len(research_results),
            "total_citations": sum(len(r.get("citations", [])) for r in research_results)
        }
    
    def _summarize_chunk(self, chunk: str, chunk_num: int, total_chunks: int) -> str:
        """Summarize a chunk of detailed content."""
        prompt = f"""Summarize this research content (chunk {chunk_num} of {total_chunks}), preserving all important details, facts, and insights.

Content:
{chunk}

Create a comprehensive summary that:
1. Preserves all key facts and data
2. Maintains technical accuracy
3. Keeps important examples and case studies
4. Retains citations and references

Write in clear, educational prose."""
        
        return self.gemini.generate_content(
            prompt=prompt,
            max_tokens=3000,
            temperature=0.3
        )
