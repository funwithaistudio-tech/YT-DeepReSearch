"""Script Generator - Generates video scripts from research."""

from typing import Dict
from loguru import logger
from .gemini_client import GeminiClient


class ScriptGenerator:
    """Video script generator using Gemini API."""
    
    def __init__(self, gemini_api_key: str):
        """
        Initialize Script Generator.
        
        Args:
            gemini_api_key: Gemini API key
        """
        self.gemini = GeminiClient(api_key=gemini_api_key)
        logger.info("ScriptGenerator initialized")
    
    def generate_script(
        self,
        research_data: Dict,
        style: str = "educational",
        length: str = "medium"
    ) -> str:
        """
        Generate video script from research data.
        
        Args:
            research_data: Research results
            style: Script style (educational, entertaining, documentary)
            length: Script length (short, medium, long)
        
        Returns:
            Generated script text
        """
        logger.info(f"Generating {length} {style} script")
        
        topic = research_data.get("topic", "Unknown Topic")
        results = research_data.get("results", [])
        
        # Combine research content
        combined_content = "\n\n".join([
            f"## Research Query: {r['query']}\n{r.get('content', '')}"
            for r in results if r.get('content')
        ])
        
        # Determine target word count
        target_words = {"short": 500, "medium": 1500, "long": 2500}.get(length, 1500)
        
        # Generate script
        prompt = f"""Create an engaging educational YouTube video script about "{topic}".

Style: {style} (inspired by channels like Veritasium, Dhruv Rathee, Fern)
Target length: {target_words} words

Research Content:
{combined_content[:10000]}

Structure:
1. HOOK (first 30 seconds): Start with a fascinating question or surprising fact
2. INTRODUCTION: Brief overview and why it matters
3. MAIN CONTENT: Explain key concepts with examples and stories
4. CONCLUSION: Tie it all together with key takeaway

Guidelines:
- Write as spoken narration (conversational, engaging)
- Use [VISUAL: description] markers for key visuals
- Include questions to engage viewers
- Use analogies and real-world examples
- Maintain good pacing
- Add personality and enthusiasm

Generate the complete video script now."""
        
        script = self.gemini.generate_content(
            prompt=prompt,
            max_tokens=target_words * 2,  # Allow some overhead
            temperature=0.7,
            system_instruction=f"You are an expert YouTube scriptwriter creating {style} educational content."
        )
        
        logger.info(f"Generated script: {len(script.split())} words")
        
        return script
