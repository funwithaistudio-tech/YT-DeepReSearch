"""Job Queue management using Excel for tracking research topics."""

import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from openpyxl import Workbook, load_workbook
import threading


class JobQueue:
    """
    Manages job queue stored in an Excel file with concurrency support.

    Excel Format:
    - Column A: Topic (string)
    - Column B: Status (Pending/In_Progress/Completed/Error)
    - Column C: Timestamp_Start
    - Column D: Timestamp_End
    - Column E: Duration_Seconds
    - Column F: Error_Message
    - Column G: Output_Path
    """

    def __init__(self, excel_path: str = "job_queue.xlsx"):
        """
        Initialize JobQueue.

        Args:
            excel_path: Path to the Excel file for job queue
        """
        self.excel_path = Path(excel_path)
        self.lock = threading.Lock()
        self._ensure_excel_exists()

    def _ensure_excel_exists(self):
        """Create Excel file with headers if it doesn't exist."""
        if not self.excel_path.exists():
            wb = Workbook()
            ws = wb.active
            ws.title = "JobQueue"

            # Set headers
            headers = [
                "Topic",
                "Status",
                "Timestamp_Start",
                "Timestamp_End",
                "Duration_Seconds",
                "Error_Message",
                "Output_Path"
            ]
            for col_idx, header in enumerate(headers, 1):
                ws.cell(row=1, column=col_idx, value=header)

            wb.save(self.excel_path)
            wb.close()

    def _load_workbook(self):
        """Load workbook with retry logic for concurrency."""
        max_retries = 5
        retry_delay = 0.5

        for attempt in range(max_retries):
            try:
                wb = load_workbook(self.excel_path)
                return wb
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise RuntimeError(
                        f"Failed to load workbook after {max_retries} attempts: {e}"
                    )

    def _save_workbook(self, wb):
        """Save workbook with retry logic for concurrency."""
        max_retries = 5
        retry_delay = 0.5

        for attempt in range(max_retries):
            try:
                wb.save(self.excel_path)
                wb.close()
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise RuntimeError(
                        f"Failed to save workbook after {max_retries} attempts: {e}"
                    )

    def get_next_pending_job(self) -> Optional[str]:
        """
        Get the next job with Status="Pending".

        Returns:
            Topic string if found, None otherwise
        """
        with self.lock:
            wb = self._load_workbook()
            ws = wb.active

            try:
                # Start from row 2 (skip header)
                for row_idx in range(2, ws.max_row + 1):
                    status = ws.cell(row=row_idx, column=2).value
                    if status and status.strip().lower() == "pending":
                        topic = ws.cell(row=row_idx, column=1).value
                        wb.close()
                        return topic

                wb.close()
                return None
            except Exception as e:
                wb.close()
                raise RuntimeError(f"Error reading job queue: {e}")

    def claim_job(self, topic: str) -> bool:
        """
        Claim a job by updating its status to "In_Progress".

        Args:
            topic: Topic to claim

        Returns:
            True if job was successfully claimed, False otherwise
        """
        with self.lock:
            wb = self._load_workbook()
            ws = wb.active

            try:
                # Find the row with this topic
                for row_idx in range(2, ws.max_row + 1):
                    cell_topic = ws.cell(row=row_idx, column=1).value
                    status = ws.cell(row=row_idx, column=2).value

                    if cell_topic == topic and status and status.strip().lower() == "pending":
                        # Update status and timestamp
                        ws.cell(row=row_idx, column=2, value="In_Progress")
                        ws.cell(row=row_idx, column=3, value=datetime.now().isoformat())
                        self._save_workbook(wb)
                        return True

                wb.close()
                return False
            except Exception as e:
                wb.close()
                raise RuntimeError(f"Error claiming job: {e}")

    def update_job_status(
        self,
        topic: str,
        status: str,
        error_message: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> bool:
        """
        Update job status to "Completed" or "Error".

        Args:
            topic: Topic to update
            status: New status (Completed/Error)
            error_message: Optional error message if status is Error
            output_path: Optional path to output directory

        Returns:
            True if job was successfully updated, False otherwise
        """
        with self.lock:
            wb = self._load_workbook()
            ws = wb.active

            try:
                # Find the row with this topic
                for row_idx in range(2, ws.max_row + 1):
                    cell_topic = ws.cell(row=row_idx, column=1).value

                    if cell_topic == topic:
                        # Get start timestamp
                        start_time_str = ws.cell(row=row_idx, column=3).value
                        end_time = datetime.now()

                        # Calculate duration
                        duration_seconds = None
                        if start_time_str:
                            try:
                                start_time = datetime.fromisoformat(start_time_str)
                                duration_seconds = (end_time - start_time).total_seconds()
                            except ValueError:
                                pass

                        # Update cells
                        ws.cell(row=row_idx, column=2, value=status)
                        ws.cell(row=row_idx, column=4, value=end_time.isoformat())
                        if duration_seconds is not None:
                            ws.cell(row=row_idx, column=5, value=duration_seconds)
                        if error_message:
                            ws.cell(row=row_idx, column=6, value=error_message)
                        if output_path:
                            ws.cell(row=row_idx, column=7, value=output_path)

                        self._save_workbook(wb)
                        return True

                wb.close()
                return False
            except Exception as e:
                wb.close()
                raise RuntimeError(f"Error updating job status: {e}")

    def add_job(self, topic: str, status: str = "Pending") -> bool:
        """
        Add a new job to the queue.

        Args:
            topic: Topic to add
            status: Initial status (default: Pending)

        Returns:
            True if job was added successfully
        """
        with self.lock:
            wb = self._load_workbook()
            ws = wb.active

            try:
                # Check if topic already exists
                for row_idx in range(2, ws.max_row + 1):
                    cell_topic = ws.cell(row=row_idx, column=1).value
                    if cell_topic == topic:
                        wb.close()
                        return False  # Topic already exists

                # Add new row
                next_row = ws.max_row + 1
                ws.cell(row=next_row, column=1, value=topic)
                ws.cell(row=next_row, column=2, value=status)

                self._save_workbook(wb)
                return True
            except Exception as e:
                wb.close()
                raise RuntimeError(f"Error adding job: {e}")

    def get_job_status(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        Get the full status of a job.

        Args:
            topic: Topic to query

        Returns:
            Dictionary with job details or None if not found
        """
        with self.lock:
            wb = self._load_workbook()
            ws = wb.active

            try:
                for row_idx in range(2, ws.max_row + 1):
                    cell_topic = ws.cell(row=row_idx, column=1).value

                    if cell_topic == topic:
                        status_dict = {
                            "topic": cell_topic,
                            "status": ws.cell(row=row_idx, column=2).value,
                            "timestamp_start": ws.cell(row=row_idx, column=3).value,
                            "timestamp_end": ws.cell(row=row_idx, column=4).value,
                            "duration_seconds": ws.cell(row=row_idx, column=5).value,
                            "error_message": ws.cell(row=row_idx, column=6).value,
                            "output_path": ws.cell(row=row_idx, column=7).value,
                        }
                        wb.close()
                        return status_dict

                wb.close()
                return None
            except Exception as e:
                wb.close()
                raise RuntimeError(f"Error getting job status: {e}")
