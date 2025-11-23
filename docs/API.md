# API Documentation

## Pipeline Orchestrator

### PipelineOrchestrator

Main orchestrator for the 8-phase pipeline.

```python
from src.orchestrator.pipeline_orchestrator import PipelineOrchestrator
orchestrator = PipelineOrchestrator(settings)
result = orchestrator.execute_pipeline("Topic Name")
```

## Excel Queue Manager

### ExcelQueueManager

Manages topic queue from Excel file.

```python
from src.orchestrator.excel_queue_manager import ExcelQueueManager
manager = ExcelQueueManager("./input/topics.xlsx")
pending = manager.get_pending_topics()
```

See full API documentation in the source code docstrings.
