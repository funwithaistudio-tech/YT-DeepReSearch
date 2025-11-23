# Architecture Documentation

## System Overview

YT-DeepReSearch is a comprehensive AI-powered system for generating educational video scripts through an 8-phase pipeline that transforms research topics into high-quality, narrative-driven content.

## Architecture Layers

### 1. **Orchestration Layer**
- **Pipeline Orchestrator**: Manages end-to-end execution of all 8 phases
- **Excel Queue Manager**: Handles job queue from Excel spreadsheet
- **Status Management**: Updates topic status throughout pipeline

### 2. **API Integration Layer**
- **Perplexity Client**: Deep research using Perplexity API
- **Gemini Client**: Content generation using Vertex AI/Gemini
- **Retry Logic**: Exponential backoff for API failures

### 3. **Processing Phases**

#### Phase 0: System Orchestration
- Read pending topics from Excel
- Initialize pipeline components
- Manage execution flow

#### Phase 1: Query Decomposition
- Break complex topics into 5-8 sub-queries
- Identify focus areas (background, history, technical, etc.)
- Extract keywords and assess complexity

#### Phase 2: Parallel Multi-Source Research
- Execute sub-queries in parallel (up to 5 workers)
- Gather comprehensive research from multiple sources
- Collect citations and metadata

#### Phase 3: Graph Construction
- Build knowledge graph from research findings
- Identify nodes (concepts, entities, facts)
- Map relationships and hierarchies

#### Phase 4: Hierarchical Tier Generation
- Generate 3-tier summaries

#### Phase 5: Narrative Outline
- Create 3-act story structure

#### Phase 6: Script Generation
- Generate complete video script

#### Phase 7: Validation
- Quality and fact-checking

#### Phase 8: Finalization
- Package all artifacts
