"""Unit tests for Excel Queue Manager."""

import pytest
import pandas as pd
from pathlib import Path
from src.orchestrator.excel_queue_manager import ExcelQueueManager


class TestExcelQueueManager:
    """Test Excel Queue Manager."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.test_excel = "/tmp/test_queue.xlsx"
        # Clean up if exists
        if Path(self.test_excel).exists():
            Path(self.test_excel).unlink()
    
    def teardown_method(self):
        """Clean up test files."""
        if Path(self.test_excel).exists():
            Path(self.test_excel).unlink()
    
    def test_create_template(self):
        """Test template creation."""
        manager = ExcelQueueManager(self.test_excel)
        
        assert Path(self.test_excel).exists()
        df = pd.read_excel(self.test_excel)
        assert "Topic" in df.columns
        assert "Status" in df.columns
        assert len(df) >= 1  # Template has at least one example
    
    def test_add_topic(self):
        """Test adding a new topic."""
        manager = ExcelQueueManager(self.test_excel)
        
        manager.add_topic("Test Topic", priority=5, notes="Test note")
        
        df = pd.read_excel(self.test_excel)
        assert len(df) >= 2  # Template + new topic
        assert "Test Topic" in df["Topic"].values
    
    def test_get_pending_topics(self):
        """Test getting pending topics."""
        manager = ExcelQueueManager(self.test_excel)
        
        manager.add_topic("Topic 1", priority=1)
        manager.add_topic("Topic 2", priority=2)
        
        pending = manager.get_pending_topics()
        assert len(pending) >= 2
        # Should be sorted by priority
        assert pending[0]["priority"] >= pending[1]["priority"]
    
    def test_update_status(self):
        """Test updating topic status."""
        manager = ExcelQueueManager(self.test_excel)
        
        manager.add_topic("Test Topic")
        pending = manager.get_pending_topics()
        topic_index = pending[-1]["index"]
        
        manager.update_status(topic_index, "completed", output_dir="/output/test")
        
        df = pd.read_excel(self.test_excel)
        assert df.at[topic_index, "Status"] == "completed"
        assert df.at[topic_index, "Output_Directory"] == "/output/test"
    
    def test_get_statistics(self):
        """Test getting queue statistics."""
        manager = ExcelQueueManager(self.test_excel)
        
        manager.add_topic("Topic 1")
        manager.add_topic("Topic 2")
        
        stats = manager.get_statistics()
        assert "total" in stats
        assert "pending" in stats
        assert stats["total"] >= 2
