"""Excel-based job queue for managing research topics."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import openpyxl
from openpyxl import Workbook


class JobQueue:
    """Manages the topics.xlsx file for job queue operations."""

    def __init__(self, excel_path: str = "topics.xlsx"):
        """
        Initialize the JobQueue.

        Args:
            excel_path: Path to the Excel file containing topics
        """
        self.excel_path = Path(excel_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the Excel file with headers if it doesn't exist."""
        if not self.excel_path.exists():
            wb = Workbook()
            ws = wb.active
            ws.title = "Topics"
            # Set up headers
            headers = [
                "Topic",
                "Status",
                "Timestamp_Start",
                "Timestamp_End",
                "Duration_Seconds",
                "Quality_Score",
                "Error_Message",
                "Workspace_Path"
            ]
            ws.append(headers)
            wb.save(self.excel_path)

    def get_next_pending(self) -> Optional[Dict[str, Any]]:
        """
        Find the next pending topic in the queue.

        Returns:
            Dictionary with 'row_index' and 'topic', or None if no pending topics
        """
        try:
            wb = openpyxl.load_workbook(self.excel_path)
            ws = wb.active

            # Iterate through rows (skip header)
            for row_idx in range(2, ws.max_row + 1):
                status = ws.cell(row=row_idx, column=2).value
                if status == "Pending":
                    topic = ws.cell(row=row_idx, column=1).value
                    return {
                        "row_index": row_idx,
                        "topic": topic
                    }

            return None
        finally:
            wb.close()

    def claim_topic(self, row_index: int, topic: str) -> bool:
        """
        Claim a topic by updating its status to In_Progress.

        Args:
            row_index: Excel row index (1-based)
            topic: Topic name (for verification)

        Returns:
            True if successful, False otherwise
        """
        try:
            wb = openpyxl.load_workbook(self.excel_path)
            ws = wb.active

            # Verify the topic matches
            current_topic = ws.cell(row=row_index, column=1).value
            if current_topic != topic:
                return False

            # Update status and start time
            ws.cell(row=row_index, column=2, value="In_Progress")
            ws.cell(row=row_index, column=3, value=datetime.now().isoformat())

            wb.save(self.excel_path)
            return True
        finally:
            wb.close()

    def update_status(
        self,
        topic: str,
        status: str,
        end_time: Optional[datetime] = None,
        duration: Optional[float] = None,
        quality_score: Optional[float] = None,
        error_message: Optional[str] = None,
        workspace_path: Optional[str] = None
    ) -> bool:
        """
        Update the status and metadata of a topic.

        Args:
            topic: Topic name
            status: New status (e.g., "Completed", "Failed")
            end_time: End timestamp
            duration: Duration in seconds
            quality_score: Quality score
            error_message: Error message if failed
            workspace_path: Path to workspace directory

        Returns:
            True if successful, False otherwise
        """
        try:
            wb = openpyxl.load_workbook(self.excel_path)
            ws = wb.active

            # Find the row with the matching topic
            row_index = None
            for row_idx in range(2, ws.max_row + 1):
                if ws.cell(row=row_idx, column=1).value == topic:
                    row_index = row_idx
                    break

            if row_index is None:
                return False

            # Update status
            ws.cell(row=row_index, column=2, value=status)

            # Update end time
            if end_time:
                ws.cell(row=row_index, column=4, value=end_time.isoformat())

            # Update duration
            if duration is not None:
                ws.cell(row=row_index, column=5, value=duration)

            # Update quality score
            if quality_score is not None:
                ws.cell(row=row_index, column=6, value=quality_score)

            # Update error message
            if error_message is not None:
                ws.cell(row=row_index, column=7, value=error_message)

            # Update workspace path
            if workspace_path is not None:
                ws.cell(row=row_index, column=8, value=workspace_path)

            wb.save(self.excel_path)
            return True
        finally:
            wb.close()

    def add_topic(self, topic: str, status: str = "Pending") -> bool:
        """
        Add a new topic to the queue.

        Args:
            topic: Topic name
            status: Initial status (default: "Pending")

        Returns:
            True if successful, False otherwise
        """
        try:
            wb = openpyxl.load_workbook(self.excel_path)
            ws = wb.active

            # Check if topic already exists
            for row_idx in range(2, ws.max_row + 1):
                if ws.cell(row=row_idx, column=1).value == topic:
                    return False

            # Add new row
            ws.append([topic, status, None, None, None, None, None, None])
            wb.save(self.excel_path)
            return True
        finally:
            wb.close()
