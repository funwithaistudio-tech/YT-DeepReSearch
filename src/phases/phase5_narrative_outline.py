"""Phase 5: Narrative Outline - Create structured story outline."""

from typing import Dict, List
from loguru import logger
from content.gemini_client import GeminiClient


class Phase5NarrativeOutline:
    """Phase 5: Create narrative outline for video script."""
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize Phase 5.
        
        Args:
            gemini_client: Gemini client for outline generation
        """
        self.gemini = gemini_client
    
    def execute(self, phase4_output: Dict, phase3_output: Dict) -> Dict[str, any]:
        """
        Execute Phase 5: Narrative Outline.
        
        Args:
            phase4_output: Output from Phase 4 (hierarchical tiers)
            phase3_output: Output from Phase 3 (knowledge graph)
        
        Returns:
            Dictionary with narrative outline
        """
        logger.info("Phase 5: Creating narrative outline")
        
        tiers = phase4_output.get("data", {})
        graph = phase3_output.get("data", {})
        
        try:
            outline = self._create_narrative_outline(tiers, graph)
            
            logger.info(f"Phase 5 complete: Created outline with {len(outline.get('acts', []))} acts")
            
            return {
                "phase": 5,
                "status": "completed",
                "data": outline
            }
        
        except Exception as e:
            logger.error(f"Phase 5 failed: {str(e)}")
            return {
                "phase": 5,
                "status": "failed",
                "error": str(e)
            }
    
    def _create_narrative_outline(self, tiers: Dict, graph: Dict) -> Dict:
        """
        Create narrative outline following story structure.
        
        Args:
            tiers: Hierarchical tiers from Phase 4
            graph: Knowledge graph from Phase 3
        
        Returns:
            Narrative outline structure
        """
        executive = tiers.get("tier1_executive", {})
        intermediate = tiers.get("tier2_intermediate", {})
        
        prompt = f"""Create a compelling narrative outline for an educational YouTube video following a three-act structure.

Executive Summary:
{executive.get('summary', '')[:500]}

Key Concepts:
{', '.join(graph.get('key_insights', [])[:5])}

Create an outline with:

ACT 1 - THE HOOK (2-3 minutes)
- Opening hook: Start with a fascinating question, paradox, or surprising fact
- Personal connection: Why should viewers care?
- Promise: What will they learn?
- Context setup: Brief background

ACT 2 - THE EXPLORATION (8-12 minutes)
- Part A: Foundation building
  - Explain core concepts with analogies
  - Use visual examples
- Part B: Deep dive
  - Detailed mechanisms/processes
  - Real-world applications
- Part C: Connections
  - How everything fits together
  - Unexpected insights

ACT 3 - THE RESOLUTION (2-3 minutes)
- Synthesis: Tie everything together
- "Aha" moment: The big revelation
- Implications: Why it matters
- Call to action: What next?

Provide response as JSON:
{{
    "title": "video title",
    "hook": "opening hook description",
    "acts": [
        {{
            "act_number": 1,
            "name": "The Hook",
            "duration_minutes": 3,
            "sections": [
                {{"title": "section title", "content": "what to cover", "duration_seconds": 60, "visual_notes": "suggested visuals"}},
                ...
            ]
        }},
        ...
    ],
    "narrative_arc": ["point 1", "point 2", ...],
    "key_transitions": ["transition 1", "transition 2", ...],
    "estimated_total_duration_minutes": 15
}}"""
        
        outline = self.gemini.generate_structured_content(
            prompt=prompt,
            schema={"title": "str", "acts": "list", "narrative_arc": "list"},
            temperature=0.7
        )
        
        return outline
