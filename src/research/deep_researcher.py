"""Deep research module using Perplexity API."""

import json
import time
from pathlib import Path
from typing import List
import requests

from src.domain.models import QuestionFramework, SubQuestionResearch, ResearchSource
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger()


class DeepResearcher:
    """Performs deep research using Perplexity API."""
    
    def __init__(self, settings: Settings):
        """Initialize deep researcher.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.api_key = settings.perplexity_api_key
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def research_framework(self, framework: QuestionFramework, topic_id: int) -> List[SubQuestionResearch]:
        """Research all sub-questions in the framework.
        
        Args:
            framework: Question framework to research
            topic_id: Topic ID for file naming
            
        Returns:
            List of SubQuestionResearch results
        """
        logger.info(f"Starting deep research for {len(framework.main_questions)} main questions")
        
        all_research = []
        
        for main_q in framework.main_questions:
            for sub_q in main_q.sub_questions:
                logger.info(f"Researching sub-question: {sub_q.text}")
                
                research = self._research_sub_question(sub_q.text, sub_q.id, main_q.id)
                all_research.append(research)
                
                # Save individual research
                self._save_research(research, topic_id)
                
                # Small delay to avoid rate limits
                time.sleep(1)
        
        logger.info(f"Completed research for {len(all_research)} sub-questions")
        return all_research
    
    def _research_sub_question(
        self, 
        question: str, 
        sub_q_id: str, 
        main_q_id: str
    ) -> SubQuestionResearch:
        """Research a single sub-question using Perplexity.
        
        Args:
            question: Question text
            sub_q_id: Sub-question ID
            main_q_id: Parent main question ID
            
        Returns:
            SubQuestionResearch with results
        """
        # For MVP, generate mock research
        # In production, this would call Perplexity API
        
        # Mock implementation
        research_content = f"Research findings for: {question}\n\n"
        research_content += "This is placeholder research content. "
        research_content += "In production, this would contain detailed research from Perplexity API "
        research_content += "including facts, data, and insights relevant to the question."
        
        sources = [
            ResearchSource(
                url=f"https://example.com/source_{sub_q_id}",
                title=f"Source for {sub_q_id}",
                relevance_score=0.95
            )
        ]
        
        return SubQuestionResearch(
            sub_question_id=sub_q_id,
            sub_question_text=question,
            main_question_id=main_q_id,
            research_content=research_content,
            sources=sources
        )
    
    def _call_perplexity_api(self, question: str) -> dict:
        """Call Perplexity API for research.
        
        Args:
            question: Research question
            
        Returns:
            API response dict
        """
        # This is a placeholder for actual Perplexity API integration
        # The actual implementation would use the Perplexity API client
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar-medium-online",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
        
        # Note: Actual implementation would make the API call
        # response = requests.post("https://api.perplexity.ai/chat/completions", 
        #                         json=payload, headers=headers)
        # return response.json()
        
        return {}
    
    def _save_research(self, research: SubQuestionResearch, topic_id: int):
        """Save research to JSON file.
        
        Args:
            research: Research results
            topic_id: Topic ID
        """
        filename = f"research_{research.sub_question_id}_topic_{topic_id}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(research.model_dump(), f, indent=2, default=str)
        
        logger.debug(f"Saved research to {filepath}")
