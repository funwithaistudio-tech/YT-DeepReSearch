"""Pipeline Orchestrator - Manages the multi-phase pipeline execution."""

from typing import Dict, Optional
from loguru import logger

from config.settings import Settings
from research.perplexity_client import PerplexityClient
from content.gemini_client import GeminiClient
from phases.phase1_query_decomposition import Phase1QueryDecomposition
from phases.phase2_parallel_research import Phase2ParallelResearch
from phases.phase3_graph_construction import Phase3GraphConstruction
from phases.phase4_hierarchical_tiers import Phase4HierarchicalTiers
from phases.phase5_narrative_outline import Phase5NarrativeOutline
from phases.phase6_script_generation import Phase6ScriptGeneration
from phases.phase7_validation import Phase7Validation
from phases.phase8_finalization import Phase8Finalization


class PipelineOrchestrator:
    """Orchestrates the complete multi-phase pipeline."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize Pipeline Orchestrator.
        
        Args:
            settings: Application settings
        """
        self.settings = settings or Settings()
        
        # Initialize API clients
        self.perplexity = PerplexityClient(self.settings.perplexity_api_key)
        self.gemini = GeminiClient(
            api_key=self.settings.gemini_api_key,
            project_id=self.settings.google_cloud_project
        )
        
        # Initialize phases
        self.phase1 = Phase1QueryDecomposition(self.gemini)
        self.phase2 = Phase2ParallelResearch(self.perplexity)
        self.phase3 = Phase3GraphConstruction(self.gemini)
        self.phase4 = Phase4HierarchicalTiers(self.gemini)
        self.phase5 = Phase5NarrativeOutline(self.gemini)
        self.phase6 = Phase6ScriptGeneration(self.gemini)
        self.phase7 = Phase7Validation(self.gemini)
        self.phase8 = Phase8Finalization(self.settings.output_dir)
        
        logger.info("PipelineOrchestrator initialized with all 8 phases")
    
    def execute_pipeline(self, topic: str) -> Dict:
        """
        Execute the complete 8-phase pipeline for a topic.
        
        Args:
            topic: Research topic
        
        Returns:
            Dictionary with pipeline results
        """
        logger.info(f"=" * 80)
        logger.info(f"Starting pipeline execution for topic: {topic}")
        logger.info(f"=" * 80)
        
        results = {
            "topic": topic,
            "status": "in_progress",
            "phases": {}
        }
        
        try:
            # Phase 1: Query Decomposition
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 1: Query Decomposition")
            logger.info("=" * 80)
            phase1_output = self.phase1.execute(topic)
            results["phases"]["phase1"] = phase1_output
            
            if phase1_output["status"] == "failed":
                logger.error("Phase 1 failed, aborting pipeline")
                results["status"] = "failed"
                results["error_phase"] = 1
                return results
            
            # Phase 2: Parallel Multi-Source Research
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 2: Parallel Multi-Source Research")
            logger.info("=" * 80)
            phase2_output = self.phase2.execute(phase1_output)
            results["phases"]["phase2"] = phase2_output
            
            if phase2_output["status"] == "failed":
                logger.error("Phase 2 failed, aborting pipeline")
                results["status"] = "failed"
                results["error_phase"] = 2
                return results
            
            # Phase 3: Graph Construction
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 3: Knowledge Graph Construction")
            logger.info("=" * 80)
            phase3_output = self.phase3.execute(phase2_output)
            results["phases"]["phase3"] = phase3_output
            
            if phase3_output["status"] == "failed":
                logger.error("Phase 3 failed, aborting pipeline")
                results["status"] = "failed"
                results["error_phase"] = 3
                return results
            
            # Phase 4: Hierarchical Tier Generation
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 4: Hierarchical Tier Generation")
            logger.info("=" * 80)
            phase4_output = self.phase4.execute(phase3_output, phase2_output)
            results["phases"]["phase4"] = phase4_output
            
            if phase4_output["status"] == "failed":
                logger.error("Phase 4 failed, aborting pipeline")
                results["status"] = "failed"
                results["error_phase"] = 4
                return results
            
            # Phase 5: Narrative Outline
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 5: Narrative Outline Creation")
            logger.info("=" * 80)
            phase5_output = self.phase5.execute(phase4_output, phase3_output)
            results["phases"]["phase5"] = phase5_output
            
            if phase5_output["status"] == "failed":
                logger.error("Phase 5 failed, aborting pipeline")
                results["status"] = "failed"
                results["error_phase"] = 5
                return results
            
            # Phase 6: Script Generation
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 6: Video Script Generation")
            logger.info("=" * 80)
            phase6_output = self.phase6.execute(
                phase5_output,
                phase4_output,
                phase2_output,
                script_style=self.settings.content_style
            )
            results["phases"]["phase6"] = phase6_output
            
            if phase6_output["status"] == "failed":
                logger.error("Phase 6 failed, aborting pipeline")
                results["status"] = "failed"
                results["error_phase"] = 6
                return results
            
            # Phase 7: Validation
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 7: Script Validation")
            logger.info("=" * 80)
            phase7_output = self.phase7.execute(phase6_output, phase2_output)
            results["phases"]["phase7"] = phase7_output
            
            if phase7_output["status"] == "failed":
                logger.error("Phase 7 failed, aborting pipeline")
                results["status"] = "failed"
                results["error_phase"] = 7
                return results
            
            # Phase 8: Finalization
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 8: Artifact Finalization")
            logger.info("=" * 80)
            phase8_output = self.phase8.execute(
                topic,
                phase1_output,
                phase2_output,
                phase3_output,
                phase4_output,
                phase5_output,
                phase6_output,
                phase7_output
            )
            results["phases"]["phase8"] = phase8_output
            
            if phase8_output["status"] == "failed":
                logger.error("Phase 8 failed")
                results["status"] = "failed"
                results["error_phase"] = 8
                return results
            
            # Pipeline completed successfully
            results["status"] = "completed"
            results["output_directory"] = phase8_output["data"]["output_directory"]
            
            logger.info("\n" + "=" * 80)
            logger.info(f"✅ PIPELINE COMPLETED SUCCESSFULLY")
            logger.info(f"Output directory: {results['output_directory']}")
            logger.info("=" * 80)
            
            return results
        
        except Exception as e:
            logger.error(f"Pipeline execution failed with exception: {str(e)}")
            results["status"] = "failed"
            results["error"] = str(e)
            return results
