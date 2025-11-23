"""Configuration module for YT-DeepReSearch system.

This module loads environment variables and defines system-wide constants
for the Hybrid Hierarchical-GraphRAG pipeline.
"""

import os
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Directory Paths
BASE_DIR = Path(__file__).parent.parent
JOB_QUEUE_DIR = BASE_DIR / "job_queue"
PROJECTS_DIR = BASE_DIR / "projects"

# Ensure directories exist
JOB_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

# Job Queue Excel Configuration
JOB_QUEUE_FILE = JOB_QUEUE_DIR / "research_queue.xlsx"

# Excel Column Names
class ExcelColumns:
    """Excel column names for job queue."""
    TOPIC = "Topic"
    STATUS = "Status"
    TIMESTAMP_START = "Timestamp_Start"
    TIMESTAMP_END = "Timestamp_End"
    DURATION_SECONDS = "Duration_Seconds"
    QUALITY_SCORE = "Quality_Score"
    ERROR_MESSAGE = "Error_Message"
    NOTES = "Notes"


# Status Values
class JobStatus(str, Enum):
    """Job status enumeration."""
    PENDING = "Pending"
    IN_PROGRESS = "In_Progress"
    COMPLETED = "Completed"
    ERROR = "Error"
    CANCELLED = "Cancelled"


# Phase Configuration
class Phase(str, Enum):
    """Pipeline phase enumeration."""
    PHASE_0_ORCHESTRATION = "Phase_0_Orchestration"
    PHASE_1_DECOMPOSITION = "Phase_1_Decomposition"
    PHASE_2_RESEARCH = "Phase_2_Research"
    PHASE_3_COMPRESSION = "Phase_3_Compression"
    PHASE_4_GRAPH_CONSTRUCTION = "Phase_4_Graph_Construction"
    PHASE_5_HIERARCHY = "Phase_5_Hierarchy"
    PHASE_6_PLANNING = "Phase_6_Planning"
    PHASE_7_GENERATION = "Phase_7_Generation"
    PHASE_8_FINAL_OUTPUT = "Phase_8_Final_Output"


# Workspace Configuration
MANIFEST_FILENAME = "manifest.json"
STATE_FILENAME = "state.json"

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
