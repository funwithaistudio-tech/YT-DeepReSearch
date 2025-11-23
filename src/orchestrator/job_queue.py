"""Job queue management using Excel spreadsheet.

This module provides Excel-based job queue functionality for tracking
research topics and their processing status.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from config import (
    JOB_QUEUE_FILE,
    ExcelColumns,
    JobStatus,
    MAX_RETRIES,
    RETRY_DELAY
)


class JobQueue:
    """Manages job queue using Excel spreadsheet."""
    
    def __init__(self, queue_file: Optional[Path] = None):
        """Initialize job queue.
        
        Args:
            queue_file: Path to Excel file. Defaults to JOB_QUEUE_FILE.
        """
        self.queue_file = queue_file or JOB_QUEUE_FILE
        self._ensure_queue_file()
    
    def _ensure_queue_file(self) -> None:
        """Ensure queue file exists with proper headers."""
        if not self.queue_file.exists():
            self._create_queue_file()
    
    def _create_queue_file(self) -> None:
        """Create new queue file with headers."""
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Research Queue"
        
        # Set headers
        headers = [
            ExcelColumns.TOPIC,
            ExcelColumns.STATUS,
            ExcelColumns.TIMESTAMP_START,
            ExcelColumns.TIMESTAMP_END,
            ExcelColumns.DURATION_SECONDS,
            ExcelColumns.QUALITY_SCORE,
            ExcelColumns.ERROR_MESSAGE,
            ExcelColumns.NOTES,
        ]
        
        for col_idx, header in enumerate(headers, start=1):
            sheet.cell(row=1, column=col_idx, value=header)
        
        # Save workbook
        workbook.save(self.queue_file)
    
    def _load_workbook(self, retries: int = MAX_RETRIES) -> openpyxl.Workbook:
        """Load workbook with retry logic for file locking.
        
        Args:
            retries: Number of retry attempts
            
        Returns:
            Loaded workbook
            
        Raises:
            Exception: If unable to load after all retries
        """
        for attempt in range(retries):
            try:
                return openpyxl.load_workbook(self.queue_file)
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    raise Exception(f"Failed to load workbook after {retries} attempts: {e}")
    
    def _save_workbook(self, workbook: openpyxl.Workbook, retries: int = MAX_RETRIES) -> None:
        """Save workbook with retry logic for file locking.
        
        Args:
            workbook: Workbook to save
            retries: Number of retry attempts
            
        Raises:
            Exception: If unable to save after all retries
        """
        for attempt in range(retries):
            try:
                workbook.save(self.queue_file)
                return
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    raise Exception(f"Failed to save workbook after {retries} attempts: {e}")
    
    def _find_topic_row(self, sheet: Worksheet, topic: str) -> Optional[int]:
        """Find row number for a given topic.
        
        Args:
            sheet: Worksheet to search
            topic: Topic to find
            
        Returns:
            Row number if found, None otherwise
        """
        for row_idx in range(2, sheet.max_row + 1):
            cell_value = sheet.cell(row=row_idx, column=1).value
            if cell_value and cell_value.strip() == topic.strip():
                return row_idx
        return None
    
    def add_topic(self, topic: str, notes: str = "") -> bool:
        """Add a new topic to the queue.
        
        Args:
            topic: Research topic
            notes: Optional notes
            
        Returns:
            True if topic was added, False if it already exists
        """
        workbook = self._load_workbook()
        sheet = workbook.active
        
        # Check if topic already exists
        if self._find_topic_row(sheet, topic):
            workbook.close()
            return False
        
        # Add new row
        new_row = sheet.max_row + 1
        sheet.cell(row=new_row, column=1, value=topic)
        sheet.cell(row=new_row, column=2, value=JobStatus.PENDING.value)
        sheet.cell(row=new_row, column=8, value=notes)
        
        self._save_workbook(workbook)
        workbook.close()
        return True
    
    def get_next_pending_topic(self) -> Optional[str]:
        """Get the next pending topic from the queue.
        
        Returns:
            Topic string if found, None otherwise
        """
        workbook = self._load_workbook()
        sheet = workbook.active
        
        for row_idx in range(2, sheet.max_row + 1):
            status = sheet.cell(row=row_idx, column=2).value
            if status and status.strip() == JobStatus.PENDING.value:
                topic = sheet.cell(row=row_idx, column=1).value
                workbook.close()
                return topic.strip() if topic else None
        
        workbook.close()
        return None
    
    def update_status(
        self,
        topic: str,
        status: JobStatus,
        timestamp_start: Optional[str] = None,
        timestamp_end: Optional[str] = None,
        duration_seconds: Optional[float] = None,
        quality_score: Optional[float] = None,
        error_message: Optional[str] = None,
        notes: Optional[str] = None
    ) -> None:
        """Update status and metadata for a topic.
        
        Args:
            topic: Research topic
            status: New job status
            timestamp_start: Start timestamp
            timestamp_end: End timestamp
            duration_seconds: Duration in seconds
            quality_score: Quality score (0-100)
            error_message: Error message if any
            notes: Additional notes
        """
        workbook = self._load_workbook()
        sheet = workbook.active
        
        row_idx = self._find_topic_row(sheet, topic)
        if not row_idx:
            # Topic not found, add it
            row_idx = sheet.max_row + 1
            sheet.cell(row=row_idx, column=1, value=topic)
        
        # Update cells
        sheet.cell(row=row_idx, column=2, value=status.value)
        
        if timestamp_start:
            sheet.cell(row=row_idx, column=3, value=timestamp_start)
        
        if timestamp_end:
            sheet.cell(row=row_idx, column=4, value=timestamp_end)
        
        if duration_seconds is not None:
            sheet.cell(row=row_idx, column=5, value=duration_seconds)
        
        if quality_score is not None:
            sheet.cell(row=row_idx, column=6, value=quality_score)
        
        if error_message:
            sheet.cell(row=row_idx, column=7, value=error_message)
        
        if notes:
            sheet.cell(row=row_idx, column=8, value=notes)
        
        self._save_workbook(workbook)
        workbook.close()
    
    def get_topic_status(self, topic: str) -> Optional[Dict[str, Any]]:
        """Get complete status information for a topic.
        
        Args:
            topic: Research topic
            
        Returns:
            Dictionary with topic status, or None if not found
        """
        workbook = self._load_workbook()
        sheet = workbook.active
        
        row_idx = self._find_topic_row(sheet, topic)
        if not row_idx:
            workbook.close()
            return None
        
        status_info = {
            "topic": sheet.cell(row=row_idx, column=1).value,
            "status": sheet.cell(row=row_idx, column=2).value,
            "timestamp_start": sheet.cell(row=row_idx, column=3).value,
            "timestamp_end": sheet.cell(row=row_idx, column=4).value,
            "duration_seconds": sheet.cell(row=row_idx, column=5).value,
            "quality_score": sheet.cell(row=row_idx, column=6).value,
            "error_message": sheet.cell(row=row_idx, column=7).value,
            "notes": sheet.cell(row=row_idx, column=8).value,
        }
        
        workbook.close()
        return status_info
