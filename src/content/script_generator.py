"""Script generator for creating educational video scripts."""

import json
from pathlib import Path
from typing import List

from src.config.settings import Settings
from src.domain.questions import QuestionFramework
from src.domain.research import SubQuestionResearch
from src.domain.script import MainSegment, Script, SubSegment
from src.research.perplexity_client import PerplexityClient
from src.utils.logger import get_logger


class ScriptGenerator:
    """Generates educational video scripts from research data.
    
    Creates 5 main segments with 2 subsegments each (10 total).
    """

    def __init__(self, settings: Settings):
        """Initialize the script generator.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.perplexity = PerplexityClient(settings)
        self.logger = get_logger()
        
        # Load prompt templates
        prompts_dir = Path(__file__).parent / "prompts"
        
        with open(prompts_dir / "deep_subsegment_prompt.txt", "r", encoding="utf-8") as f:
            self.subsegment_prompt_template = f.read()
        
        with open(prompts_dir / "main_segment_title_prompt.txt", "r", encoding="utf-8") as f:
            self.segment_title_prompt_template = f.read()

    def generate_script(
        self,
        framework: QuestionFramework,
        research_results: List[SubQuestionResearch]
    ) -> Script:
        """Generate a complete video script from research.
        
        Args:
            framework: The question framework
            research_results: List of research results (10 items)
            
        Returns:
            Complete Script object with 5 main segments
            
        Raises:
            Exception: If script generation fails
        """
        logger = self.logger.with_context(
            topic_id=framework.topic_id,
            phase="script_generation"
        )
        
        logger.info("Starting script generation")
        
        # Create a mapping of research results by (main_index, sub_index)
        research_map = {
            (r.main_index, r.sub_index): r
            for r in research_results
        }
        
        main_segments: List[MainSegment] = []
        global_subsegment_index = 0
        
        # Generate each main segment
        for main_q in framework.main_questions:
            subsegments: List[SubSegment] = []
            
            # Generate subsegments for this main question
            for sub_q in main_q.subquestions:
                global_subsegment_index += 1
                
                # Get corresponding research
                research = research_map.get((main_q.main_index, sub_q.sub_index))
                if not research:
                    raise ValueError(
                        f"Missing research for M{main_q.main_index}.S{sub_q.sub_index}"
                    )
                
                subsegment = self._generate_subsegment(
                    index=global_subsegment_index,
                    role=sub_q.role,
                    sub_question=sub_q.question,
                    research=research,
                    topic=framework.topic,
                    main_question=main_q.main_question,
                    style=framework.style,
                    logger=logger
                )
                subsegments.append(subsegment)
            
            # Generate main segment title and summary
            main_segment = self._create_main_segment(
                index=main_q.main_index,
                role=main_q.role,
                main_question=main_q.main_question,
                subsegments=subsegments,
                topic=framework.topic,
                logger=logger
            )
            main_segments.append(main_segment)
        
        # Calculate total word count
        total_word_count = sum(ms.total_words for ms in main_segments)
        
        # Create Script object
        script = Script(
            topic_id=framework.topic_id,
            topic=framework.topic,
            style=framework.style,
            language=framework.language,
            total_word_count=total_word_count,
            main_segments=main_segments
        )
        
        # Save to file
        output_path = self.settings.generated_dir / f"script_topic_{framework.topic_id}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script.model_dump_json(indent=2))
        
        logger.info(
            f"Script generated successfully: {total_word_count} words, "
            f"{len(main_segments)} main segments, "
            f"{script.total_subsegments} subsegments"
        )
        logger.info(f"Script saved to: {output_path}")
        
        return script

    def _generate_subsegment(
        self,
        index: int,
        role: str,
        sub_question: str,
        research: SubQuestionResearch,
        topic: str,
        main_question: str,
        style: str,
        logger
    ) -> SubSegment:
        """Generate a single subsegment script.
        
        Args:
            index: Global subsegment index (1-10)
            role: Role/purpose of this subsegment
            sub_question: The sub-question to answer
            research: Research data for this sub-question
            topic: Main topic
            main_question: Parent main question
            style: Content style
            logger: Logger instance
            
        Returns:
            SubSegment object with generated text
        """
        logger.info(f"Generating subsegment {index}: '{sub_question[:50]}...'")
        
        # Build prompt by replacing placeholders
        prompt = self.subsegment_prompt_template
        prompt = prompt.replace("[TOPIC_PLACEHOLDER]", topic)
        prompt = prompt.replace("[MAIN_QUESTION_PLACEHOLDER]", main_question)
        prompt = prompt.replace("[SUB_QUESTION_PLACEHOLDER]", sub_question)
        prompt = prompt.replace("[STYLE_PLACEHOLDER]", style)
        prompt = prompt.replace("[SUMMARY_PLACEHOLDER]", research.summary)
        prompt = prompt.replace(
            "[KEY_POINTS_PLACEHOLDER]",
            json.dumps(research.key_points, indent=2)
        )
        prompt = prompt.replace(
            "[SOURCES_JSON_PLACEHOLDER]",
            json.dumps([s.model_dump() for s in research.sources], indent=2)
        )
        prompt = prompt.replace(
            "[WORDS_MIN]",
            str(self.settings.words_per_subsegment_min)
        )
        prompt = prompt.replace(
            "[WORDS_MAX]",
            str(self.settings.words_per_subsegment_max)
        )
        
        # Generate subsegment text
        try:
            response_json = self.perplexity.chat_json(
                prompt=prompt,
                model="sonar-pro"
            )
            
            response_data = json.loads(response_json)
            text = response_data["text"]
            sources_used = response_data.get("sources_used", [])
            
            # Calculate word count
            word_count = len(text.split())
            
            # Warn if outside expected range
            if word_count < self.settings.words_per_subsegment_min:
                logger.warning(
                    f"Subsegment {index} is too short: {word_count} words "
                    f"(min: {self.settings.words_per_subsegment_min})"
                )
            elif word_count > self.settings.words_per_subsegment_max:
                logger.warning(
                    f"Subsegment {index} is too long: {word_count} words "
                    f"(max: {self.settings.words_per_subsegment_max})"
                )
            
            return SubSegment(
                index=index,
                role=role,
                sub_question=sub_question,
                text=text,
                word_count=word_count,
                sources_used=sources_used
            )
            
        except Exception as e:
            logger.error(f"Failed to generate subsegment {index}: {e}")
            raise

    def _create_main_segment(
        self,
        index: int,
        role: str,
        main_question: str,
        subsegments: List[SubSegment],
        topic: str,
        logger
    ) -> MainSegment:
        """Create a main segment with title and summary.
        
        Args:
            index: Main segment index (1-5)
            role: Role/purpose of this segment
            main_question: The main question
            subsegments: List of 2 subsegments
            topic: Main topic
            logger: Logger instance
            
        Returns:
            MainSegment object with title and summary
        """
        logger.info(f"Creating main segment {index}: '{main_question[:50]}...'")
        
        # Combine subsegment texts
        combined_text = "\n\n".join(sub.text for sub in subsegments)
        
        # Build prompt
        prompt = self.segment_title_prompt_template
        prompt = prompt.replace("[TOPIC_PLACEHOLDER]", topic)
        prompt = prompt.replace("[MAIN_QUESTION_PLACEHOLDER]", main_question)
        prompt = prompt.replace("[SEGMENT_TEXT_PLACEHOLDER]", combined_text[:2000])  # Limit length
        
        try:
            response_json = self.perplexity.chat_json(
                prompt=prompt,
                model="sonar-pro"
            )
            
            response_data = json.loads(response_json)
            title = response_data["title"]
            summary = response_data["summary"]
            
            return MainSegment(
                index=index,
                role=role,
                main_question=main_question,
                title=title,
                summary=summary,
                subsegments=subsegments
            )
            
        except Exception as e:
            logger.error(f"Failed to create main segment {index}: {e}")
            raise
