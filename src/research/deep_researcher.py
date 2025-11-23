"""Deep researcher for gathering information on sub-questions."""

import json
from pathlib import Path
from typing import List

from src.config.settings import Settings
from src.domain.questions import QuestionFramework
from src.domain.research import Source, SubQuestionResearch
from src.research.perplexity_client import PerplexityClient
from src.utils.logger import get_logger


class DeepResearcher:
    """Performs deep research for each sub-question using Perplexity search.
    
    For each sub-question in the framework, searches for information and
    creates a structured research result.
    """

    def __init__(self, settings: Settings):
        """Initialize the deep researcher.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.perplexity = PerplexityClient(settings)
        self.logger = get_logger()

    def research_topic(self, framework: QuestionFramework) -> List[SubQuestionResearch]:
        """Perform deep research for all sub-questions in the framework.
        
        Args:
            framework: The question framework to research
            
        Returns:
            List of SubQuestionResearch objects (10 total)
            
        Raises:
            Exception: If research fails for any sub-question
        """
        logger = self.logger.with_context(
            topic_id=framework.topic_id,
            phase="deep_research"
        )
        
        logger.info(
            f"Starting deep research for {framework.total_subquestions} sub-questions"
        )
        
        all_research: List[SubQuestionResearch] = []
        
        # Process each main question and its sub-questions
        for main_q in framework.main_questions:
            for sub_q in main_q.subquestions:
                research = self._research_subquestion(
                    framework=framework,
                    main_index=main_q.main_index,
                    main_question=main_q.main_question,
                    sub_index=sub_q.sub_index,
                    sub_question=sub_q.question,
                    logger=logger
                )
                all_research.append(research)
        
        logger.info(f"Deep research completed: {len(all_research)} results")
        return all_research

    def _research_subquestion(
        self,
        framework: QuestionFramework,
        main_index: int,
        main_question: str,
        sub_index: int,
        sub_question: str,
        logger
    ) -> SubQuestionResearch:
        """Research a single sub-question.
        
        Args:
            framework: The parent question framework
            main_index: Index of the main question
            main_question: Text of the main question
            sub_index: Index of the sub-question
            sub_question: Text of the sub-question
            logger: Logger instance with context
            
        Returns:
            SubQuestionResearch with sources and summary
        """
        # Build search query combining topic, main question, and sub-question
        search_query = f"{framework.topic} {main_question} {sub_question}"
        
        logger.info(
            f"Researching M{main_index}.S{sub_index}: '{sub_question[:60]}...'"
        )
        
        try:
            # Perform search
            search_results = self.perplexity.search(search_query, max_results=7)
            
            # Map results to Source objects
            sources = self._map_sources(search_results)
            
            # Create basic summary and key points
            # TODO: In future, use Gemini/Vertex to generate better summaries
            summary = self._create_basic_summary(search_results, sub_question)
            key_points = self._extract_key_points(search_results)
            
            # Create SubQuestionResearch object
            research = SubQuestionResearch(
                topic_id=framework.topic_id,
                topic=framework.topic,
                main_index=main_index,
                sub_index=sub_index,
                main_question=main_question,
                sub_question=sub_question,
                search_query=search_query,
                sources=sources,
                summary=summary,
                key_points=key_points
            )
            
            # Save to file
            output_path = (
                self.settings.research_dir /
                f"topic_{framework.topic_id}_m{main_index}_s{sub_index}.json"
            )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(research.model_dump_json(indent=2))
            
            logger.info(
                f"Research saved: M{main_index}.S{sub_index} "
                f"({research.source_count} sources)"
            )
            
            return research
            
        except Exception as e:
            logger.error(
                f"Failed to research M{main_index}.S{sub_index}: {e}"
            )
            raise

    def _map_sources(self, search_results: dict) -> List[Source]:
        """Map Perplexity search results to Source objects.
        
        Args:
            search_results: Raw search results from Perplexity API
            
        Returns:
            List of Source objects
        """
        sources = []
        results = search_results.get("results", [])
        
        for idx, result in enumerate(results, start=1):
            source = Source(
                id=f"src_{idx}",
                title=result.get("title", "Unknown Title"),
                url=result.get("url", ""),
                publisher=result.get("publisher"),
                date=result.get("date"),
                snippet=result.get("snippet")
            )
            sources.append(source)
        
        return sources

    def _create_basic_summary(self, search_results: dict, sub_question: str) -> str:
        """Create a basic summary from search results.
        
        TODO: Replace with Gemini/Vertex AI for better summarization.
        
        Args:
            search_results: Raw search results
            sub_question: The sub-question being answered
            
        Returns:
            Basic summary string
        """
        # For now, concatenate snippets with a note
        snippets = []
        for result in search_results.get("results", [])[:3]:
            snippet = result.get("snippet", "")
            if snippet:
                snippets.append(snippet)
        
        if snippets:
            summary = " ".join(snippets)
            return f"Research for '{sub_question}': {summary}"
        else:
            return f"Research conducted for: {sub_question}"

    def _extract_key_points(self, search_results: dict) -> List[str]:
        """Extract key points from search results.
        
        TODO: Replace with Gemini/Vertex AI for better extraction.
        
        Args:
            search_results: Raw search results
            
        Returns:
            List of key point strings
        """
        # For now, use first sentence of each snippet
        key_points = []
        for result in search_results.get("results", [])[:5]:
            snippet = result.get("snippet", "")
            if snippet:
                # Get first sentence
                first_sentence = snippet.split(".")[0] + "."
                key_points.append(first_sentence)
        
        return key_points if key_points else ["Research findings compiled"]
