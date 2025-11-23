"""Phase 7: Validation - Validate script quality and accuracy."""

from typing import Dict, List
from loguru import logger
from content.gemini_client import GeminiClient


class Phase7Validation:
    """Phase 7: Validate and quality-check the generated script."""
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize Phase 7.
        
        Args:
            gemini_client: Gemini client for validation
        """
        self.gemini = gemini_client
    
    def execute(self, phase6_output: Dict, phase2_output: Dict) -> Dict[str, any]:
        """
        Execute Phase 7: Validation.
        
        Args:
            phase6_output: Output from Phase 6 (script)
            phase2_output: Output from Phase 2 (research results for fact-checking)
        
        Returns:
            Dictionary with validation results
        """
        logger.info("Phase 7: Validating script")
        
        script_data = phase6_output.get("data", {})
        research_results = phase2_output.get("data", {}).get("research_results", [])
        
        try:
            validation_results = {
                "quality_check": self._check_quality(script_data),
                "fact_check": self._check_facts(script_data, research_results),
                "coherence_check": self._check_coherence(script_data),
                "engagement_check": self._check_engagement(script_data)
            }
            
            # Calculate overall score
            scores = [
                validation_results["quality_check"]["score"],
                validation_results["fact_check"]["score"],
                validation_results["coherence_check"]["score"],
                validation_results["engagement_check"]["score"]
            ]
            overall_score = sum(scores) / len(scores)
            
            validation_results["overall_score"] = overall_score
            validation_results["passed"] = overall_score >= 0.7
            
            logger.info(f"Phase 7 complete: Overall score {overall_score:.2f}")
            
            return {
                "phase": 7,
                "status": "completed",
                "data": validation_results
            }
        
        except Exception as e:
            logger.error(f"Phase 7 failed: {str(e)}")
            return {
                "phase": 7,
                "status": "failed",
                "error": str(e)
            }
    
    def _check_quality(self, script_data: Dict) -> Dict:
        """Check overall script quality."""
        full_script = script_data.get("full_script", "")
        word_count = script_data.get("word_count", 0)
        
        issues = []
        score = 1.0
        
        # Check word count
        if word_count < 500:
            issues.append("Script is too short (< 500 words)")
            score -= 0.2
        elif word_count > 5000:
            issues.append("Script is very long (> 5000 words)")
            score -= 0.1
        
        # Check for visual markers
        visual_count = full_script.count("[VISUAL:")
        if visual_count < 5:
            issues.append("Insufficient visual markers (< 5)")
            score -= 0.1
        
        # Check structure
        acts = script_data.get("acts", [])
        if len(acts) < 3:
            issues.append("Script should have at least 3 acts")
            score -= 0.2
        
        return {
            "score": max(0, score),
            "issues": issues,
            "word_count": word_count,
            "visual_markers": visual_count
        }
    
    def _check_facts(self, script_data: Dict, research_results: List[Dict]) -> Dict:
        """Check factual accuracy against research."""
        # This is a simplified check - in production, would use more sophisticated fact-checking
        full_script = script_data.get("full_script", "")
        
        # Check if script references key concepts from research
        research_content = " ".join([r.get("content", "") for r in research_results])
        
        # Extract key terms from research (simplified)
        research_words = set(research_content.lower().split())
        script_words = set(full_script.lower().split())
        
        # Calculate overlap
        overlap = len(research_words.intersection(script_words))
        overlap_ratio = overlap / max(len(research_words), 1)
        
        score = min(1.0, overlap_ratio * 2)  # Scale up
        
        issues = []
        if score < 0.5:
            issues.append("Low alignment with research content")
        
        return {
            "score": score,
            "issues": issues,
            "research_alignment": overlap_ratio
        }
    
    def _check_coherence(self, script_data: Dict) -> Dict:
        """Check narrative coherence."""
        acts = script_data.get("acts", [])
        
        issues = []
        score = 1.0
        
        # Check act transitions
        if len(acts) > 1:
            for i in range(len(acts) - 1):
                current_act = acts[i].get("script", "")
                next_act = acts[i + 1].get("script", "")
                
                # Simple check: ensure acts have content
                if not current_act or not next_act:
                    issues.append(f"Act {i + 1} or {i + 2} is empty")
                    score -= 0.2
        
        # Check for good opening and closing
        full_script = script_data.get("full_script", "")
        if len(full_script) > 0:
            opening = full_script[:200].lower()
            closing = full_script[-200:].lower()
            
            # Check for engaging opening
            if not any(word in opening for word in ["imagine", "what if", "have you", "?", "surprising"]):
                issues.append("Opening could be more engaging")
                score -= 0.1
            
            # Check for conclusion
            if not any(word in closing for word in ["so", "therefore", "in conclusion", "remember", "final"]):
                issues.append("Closing could be stronger")
                score -= 0.1
        
        return {
            "score": max(0, score),
            "issues": issues
        }
    
    def _check_engagement(self, script_data: Dict) -> Dict:
        """Check engagement elements."""
        full_script = script_data.get("full_script", "")
        
        issues = []
        score = 1.0
        
        # Count engagement elements
        questions = full_script.count("?")
        pauses = full_script.count("[PAUSE]")
        visuals = full_script.count("[VISUAL:")
        
        # Normalized scores
        question_score = min(1.0, questions / 10)  # ~10 questions ideal
        pause_score = min(1.0, pauses / 5)  # ~5 pauses ideal
        visual_score = min(1.0, visuals / 15)  # ~15 visuals ideal
        
        avg_engagement = (question_score + pause_score + visual_score) / 3
        
        if questions < 3:
            issues.append("Add more rhetorical questions for engagement")
        if visuals < 5:
            issues.append("Add more visual markers")
        if pauses < 2:
            issues.append("Add dramatic pauses for emphasis")
        
        return {
            "score": avg_engagement,
            "issues": issues,
            "questions": questions,
            "pauses": pauses,
            "visuals": visuals
        }
