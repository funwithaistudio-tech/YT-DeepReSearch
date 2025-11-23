"""Phase 6: Script Generation - Generate full video script."""

from typing import Dict, List
from loguru import logger
from content.gemini_client import GeminiClient


class Phase6ScriptGeneration:
    """Phase 6: Generate complete video script."""
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize Phase 6.
        
        Args:
            gemini_client: Gemini client for script generation
        """
        self.gemini = gemini_client
    
    def execute(
        self,
        phase5_output: Dict,
        phase4_output: Dict,
        phase2_output: Dict,
        script_style: str = "educational"
    ) -> Dict[str, any]:
        """
        Execute Phase 6: Script Generation.
        
        Args:
            phase5_output: Output from Phase 5 (narrative outline)
            phase4_output: Output from Phase 4 (hierarchical tiers)
            phase2_output: Output from Phase 2 (research results)
            script_style: Style of script (educational, entertaining, documentary)
        
        Returns:
            Dictionary with generated script
        """
        logger.info("Phase 6: Generating video script")
        
        outline = phase5_output.get("data", {})
        tiers = phase4_output.get("data", {})
        research_results = phase2_output.get("data", {}).get("research_results", [])
        
        try:
            script = self._generate_script(outline, tiers, research_results, script_style)
            
            logger.info(f"Phase 6 complete: Generated script with {script.get('word_count', 0)} words")
            
            return {
                "phase": 6,
                "status": "completed",
                "data": script
            }
        
        except Exception as e:
            logger.error(f"Phase 6 failed: {str(e)}")
            return {
                "phase": 6,
                "status": "failed",
                "error": str(e)
            }
    
    def _generate_script(
        self,
        outline: Dict,
        tiers: Dict,
        research_results: List[Dict],
        style: str
    ) -> Dict:
        """
        Generate complete script based on outline and research.
        
        Args:
            outline: Narrative outline
            tiers: Hierarchical tiers
            research_results: Research findings
            style: Script style
        
        Returns:
            Complete script structure
        """
        acts = outline.get("acts", [])
        
        # Generate script for each act
        act_scripts = []
        
        for act in acts:
            act_script = self._generate_act_script(act, tiers, style)
            act_scripts.append(act_script)
        
        # Combine all acts
        full_script = "\n\n".join([act["script"] for act in act_scripts])
        
        # Generate metadata
        citations = []
        for result in research_results:
            citations.extend(result.get("citations", []))
        
        return {
            "title": outline.get("title", "Untitled"),
            "full_script": full_script,
            "acts": act_scripts,
            "word_count": len(full_script.split()),
            "estimated_duration_minutes": len(full_script.split()) / 150,  # ~150 words per minute
            "citations": list(set(citations)),  # Unique citations
            "style": style
        }
    
    def _generate_act_script(self, act: Dict, tiers: Dict, style: str) -> Dict:
        """Generate script for a single act."""
        act_number = act.get("act_number", 1)
        act_name = act.get("name", "")
        sections = act.get("sections", [])
        
        # Get relevant content from tiers
        if act_number == 1:
            context = tiers.get("tier1_executive", {}).get("summary", "")
        elif act_number == 2:
            context = tiers.get("tier2_intermediate", {}).get("summary", "")
        else:
            context = tiers.get("tier1_executive", {}).get("summary", "")
        
        # Build section descriptions
        section_desc = "\n".join([
            f"- {s.get('title')}: {s.get('content')} (Visual: {s.get('visual_notes', 'standard')})"
            for s in sections
        ])
        
        prompt = f"""Write a compelling script for Act {act_number} - {act_name} of an educational YouTube video.

Style: {style} (like Veritasium, Dhruv Rathee, or Fern)

Context:
{context[:1000]}

Sections to cover:
{section_desc}

Guidelines:
1. Write as spoken narration (conversational, engaging)
2. Use storytelling techniques (hooks, transitions, callbacks)
3. Include [VISUAL: description] markers for key visuals
4. Add [PAUSE] for dramatic effect
5. Use rhetorical questions to engage viewers
6. Include specific examples and analogies
7. Maintain pacing: vary sentence length
8. Add personality and enthusiasm

Write the complete narration script for this act."""
        
        script_text = self.gemini.generate_content(
            prompt=prompt,
            max_tokens=4000,
            temperature=0.8,
            system_instruction=f"You are a master YouTube scriptwriter creating {style} content."
        )
        
        return {
            "act_number": act_number,
            "act_name": act_name,
            "script": script_text,
            "word_count": len(script_text.split()),
            "sections": sections
        }
