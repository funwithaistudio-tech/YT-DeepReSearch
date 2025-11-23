"""Phase 8: Finalization - Finalize and package all artifacts."""

import json
from pathlib import Path
from typing import Dict
from datetime import datetime
from loguru import logger


class Phase8Finalization:
    """Phase 8: Finalize and package all artifacts."""
    
    def __init__(self, output_dir: str = "./output"):
        """
        Initialize Phase 8.
        
        Args:
            output_dir: Directory for output artifacts
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def execute(
        self,
        topic: str,
        phase1_output: Dict,
        phase2_output: Dict,
        phase3_output: Dict,
        phase4_output: Dict,
        phase5_output: Dict,
        phase6_output: Dict,
        phase7_output: Dict
    ) -> Dict[str, any]:
        """
        Execute Phase 8: Finalization.
        
        Args:
            topic: Research topic
            phase1_output through phase7_output: Outputs from previous phases
        
        Returns:
            Dictionary with finalization results
        """
        logger.info("Phase 8: Finalizing artifacts")
        
        try:
            # Create topic-specific directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_topic = self._sanitize_filename(topic)
            topic_dir = self.output_dir / f"{safe_topic}_{timestamp}"
            topic_dir.mkdir(parents=True, exist_ok=True)
            
            # Save all artifacts
            artifacts = self._save_artifacts(
                topic_dir,
                topic,
                phase1_output,
                phase2_output,
                phase3_output,
                phase4_output,
                phase5_output,
                phase6_output,
                phase7_output
            )
            
            logger.info(f"Phase 8 complete: Saved {len(artifacts)} artifacts to {topic_dir}")
            
            return {
                "phase": 8,
                "status": "completed",
                "data": {
                    "output_directory": str(topic_dir),
                    "artifacts": artifacts,
                    "timestamp": timestamp
                }
            }
        
        except Exception as e:
            logger.error(f"Phase 8 failed: {str(e)}")
            return {
                "phase": 8,
                "status": "failed",
                "error": str(e)
            }
    
    def _save_artifacts(
        self,
        topic_dir: Path,
        topic: str,
        phase1_output: Dict,
        phase2_output: Dict,
        phase3_output: Dict,
        phase4_output: Dict,
        phase5_output: Dict,
        phase6_output: Dict,
        phase7_output: Dict
    ) -> Dict[str, str]:
        """Save all artifacts to files."""
        artifacts = {}
        
        # 1. Save final script
        script_data = phase6_output.get("data", {})
        script_file = topic_dir / "script.txt"
        script_file.write_text(script_data.get("full_script", ""))
        artifacts["script"] = str(script_file)
        
        # 2. Save script with metadata
        script_json = topic_dir / "script_complete.json"
        script_json.write_text(json.dumps(script_data, indent=2))
        artifacts["script_json"] = str(script_json)
        
        # 3. Save narrative outline
        outline_file = topic_dir / "narrative_outline.json"
        outline_file.write_text(json.dumps(phase5_output.get("data", {}), indent=2))
        artifacts["outline"] = str(outline_file)
        
        # 4. Save knowledge graph
        graph_file = topic_dir / "knowledge_graph.json"
        graph_file.write_text(json.dumps(phase3_output.get("data", {}), indent=2))
        artifacts["graph"] = str(graph_file)
        
        # 5. Save hierarchical tiers
        tiers_file = topic_dir / "hierarchical_tiers.json"
        tiers_file.write_text(json.dumps(phase4_output.get("data", {}), indent=2))
        artifacts["tiers"] = str(tiers_file)
        
        # 6. Save research results
        research_file = topic_dir / "research_results.json"
        research_file.write_text(json.dumps(phase2_output.get("data", {}), indent=2))
        artifacts["research"] = str(research_file)
        
        # 7. Save validation report
        validation_file = topic_dir / "validation_report.json"
        validation_file.write_text(json.dumps(phase7_output.get("data", {}), indent=2))
        artifacts["validation"] = str(validation_file)
        
        # 8. Save citations
        citations = script_data.get("citations", [])
        citations_file = topic_dir / "citations.txt"
        citations_file.write_text("\n".join([f"- {c}" for c in citations]))
        artifacts["citations"] = str(citations_file)
        
        # 9. Save summary report
        summary = self._generate_summary_report(
            topic,
            phase1_output,
            phase2_output,
            phase6_output,
            phase7_output
        )
        summary_file = topic_dir / "SUMMARY.md"
        summary_file.write_text(summary)
        artifacts["summary"] = str(summary_file)
        
        # 10. Save complete pipeline output
        pipeline_file = topic_dir / "pipeline_complete.json"
        pipeline_output = {
            "topic": topic,
            "phase1": phase1_output,
            "phase2": phase2_output,
            "phase3": phase3_output,
            "phase4": phase4_output,
            "phase5": phase5_output,
            "phase6": phase6_output,
            "phase7": phase7_output
        }
        pipeline_file.write_text(json.dumps(pipeline_output, indent=2))
        artifacts["pipeline"] = str(pipeline_file)
        
        return artifacts
    
    def _generate_summary_report(
        self,
        topic: str,
        phase1_output: Dict,
        phase2_output: Dict,
        phase6_output: Dict,
        phase7_output: Dict
    ) -> str:
        """Generate human-readable summary report."""
        script_data = phase6_output.get("data", {})
        validation = phase7_output.get("data", {})
        
        report = f"""# Video Script Generation Summary

## Topic
{topic}

## Script Information
- **Title**: {script_data.get('title', 'Untitled')}
- **Word Count**: {script_data.get('word_count', 0)} words
- **Estimated Duration**: {script_data.get('estimated_duration_minutes', 0):.1f} minutes
- **Style**: {script_data.get('style', 'educational')}

## Validation Results
- **Overall Score**: {validation.get('overall_score', 0):.2%}
- **Status**: {'✅ PASSED' if validation.get('passed', False) else '⚠️ NEEDS REVIEW'}

### Quality Metrics
- Quality Score: {validation.get('quality_check', {}).get('score', 0):.2%}
- Fact Check Score: {validation.get('fact_check', {}).get('score', 0):.2%}
- Coherence Score: {validation.get('coherence_check', {}).get('score', 0):.2%}
- Engagement Score: {validation.get('engagement_check', {}).get('score', 0):.2%}

### Issues Found
"""
        
        all_issues = []
        for check_name in ['quality_check', 'fact_check', 'coherence_check', 'engagement_check']:
            issues = validation.get(check_name, {}).get('issues', [])
            all_issues.extend(issues)
        
        if all_issues:
            for issue in all_issues:
                report += f"- {issue}\n"
        else:
            report += "- No issues found ✅\n"
        
        report += f"""
## Research Summary
- **Sub-queries Researched**: {phase2_output.get('data', {}).get('total_queries', 0)}
- **Successful Queries**: {phase2_output.get('data', {}).get('successful_queries', 0)}
- **Total Citations**: {len(script_data.get('citations', []))}

## Output Files
All artifacts have been saved to the output directory:
- `script.txt` - Final video script
- `script_complete.json` - Script with full metadata
- `narrative_outline.json` - Narrative structure
- `knowledge_graph.json` - Knowledge graph
- `hierarchical_tiers.json` - Multi-tier summaries
- `research_results.json` - Raw research data
- `validation_report.json` - Detailed validation results
- `citations.txt` - All source citations
- `pipeline_complete.json` - Complete pipeline output

## Next Steps
1. Review the script in `script.txt`
2. Check validation issues if any
3. Review citations for accuracy
4. Use the script for video production

---
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem compatibility."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        filename = filename.strip('. ')
        return filename[:100]  # Limit length
