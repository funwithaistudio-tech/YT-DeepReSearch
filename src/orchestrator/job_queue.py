"""Job queue management using Excel files."""

from pathlib import Path
from typing import Optional
import openpyxl
from openpyxl import Workbook


class JobQueue:
    """Manages research topics in an Excel-based job queue."""

    def __init__(self, queue_file: str = "topics.xlsx"):
        """
        Initialize JobQueue.
        
        Args:
            queue_file: Path to the Excel file containing topics
        """
        self.queue_file = Path(queue_file)
        self._ensure_queue_exists()

    def _ensure_queue_exists(self) -> None:
        """Create the queue file if it doesn't exist."""
        if not self.queue_file.exists():
            wb = Workbook()
            ws = wb.active
            ws.title = "Topics"
            
            # Create header row
            headers = ["Topic", "Status", "Claimed_By", "Started_At", "Completed_At", "Error"]
            ws.append(headers)
            
            # Add some example topics for testing
            ws.append(["The History of Quantum Computing", "Pending", "", "", "", ""])
            ws.append(["How Black Holes Form", "Pending", "", "", "", ""])
            ws.append(["The Science of Climate Change", "Pending", "", "", "", ""])
            
            wb.save(self.queue_file)

    def get_next_pending_topic(self) -> Optional[str]:
        """
        Get the next topic with 'Pending' status.
        
        Returns:
            Topic string or None if no pending topics
        """
        wb = openpyxl.load_workbook(self.queue_file)
        ws = wb.active
        
        # Skip header row (row 1)
        for row in range(2, ws.max_row + 1):
            status = ws.cell(row=row, column=2).value
            topic = ws.cell(row=row, column=1).value
            
            if status == "Pending" and topic:
                wb.close()
                return topic
        
        wb.close()
        return None

    def claim_topic(self, topic: str, claimed_by: str = "orchestrator") -> bool:
        """
        Claim a topic by updating its status to 'In_Progress'.
        
        Args:
            topic: Topic string to claim
            claimed_by: Identifier of the claimer
            
        Returns:
            True if successfully claimed, False otherwise
        """
        from datetime import datetime
        
        wb = openpyxl.load_workbook(self.queue_file)
        ws = wb.active
        
        # Find the topic row
        for row in range(2, ws.max_row + 1):
            current_topic = ws.cell(row=row, column=1).value
            current_status = ws.cell(row=row, column=2).value
            
            if current_topic == topic:
                # Only claim if status is Pending
                if current_status != "Pending":
                    wb.close()
                    return False
                
                # Update status to In_Progress
                ws.cell(row=row, column=2, value="In_Progress")
                ws.cell(row=row, column=3, value=claimed_by)
                ws.cell(row=row, column=4, value=datetime.now().isoformat())
                
                wb.save(self.queue_file)
                wb.close()
                return True
        
        wb.close()
        return False

    def update_status(
        self, 
        topic: str, 
        status: str, 
        error: Optional[str] = None
    ) -> bool:
        """
        Update the status of a topic.
        
        Args:
            topic: Topic string to update
            status: New status value (e.g., "Completed", "Failed")
            error: Optional error message if status is "Failed"
            
        Returns:
            True if successfully updated, False otherwise
        """
        from datetime import datetime
        
        wb = openpyxl.load_workbook(self.queue_file)
        ws = wb.active
        
        # Find the topic row
        for row in range(2, ws.max_row + 1):
            current_topic = ws.cell(row=row, column=1).value
            
            if current_topic == topic:
                # Update status
                ws.cell(row=row, column=2, value=status)
                
                # Update completed_at if status is Completed
                if status == "Completed":
                    ws.cell(row=row, column=5, value=datetime.now().isoformat())
                
                # Update error if provided
                if error:
                    ws.cell(row=row, column=6, value=error)
                
                wb.save(self.queue_file)
                wb.close()
                return True
        
        wb.close()
        return False

    def add_topic(self, topic: str) -> bool:
        """
        Add a new topic to the queue.
        
        Args:
            topic: Topic string to add
            
        Returns:
            True if successfully added, False if topic already exists
        """
        wb = openpyxl.load_workbook(self.queue_file)
        ws = wb.active
        
        # Check if topic already exists
        for row in range(2, ws.max_row + 1):
            existing_topic = ws.cell(row=row, column=1).value
            if existing_topic == topic:
                wb.close()
                return False
        
        # Add new topic
        ws.append([topic, "Pending", "", "", "", ""])
        wb.save(self.queue_file)
        wb.close()
        return True

    def get_all_topics(self) -> list:
        """
        Get all topics with their status.
        
        Returns:
            List of dictionaries containing topic information
        """
        wb = openpyxl.load_workbook(self.queue_file)
        ws = wb.active
        
        topics = []
        # Skip header row
        for row in range(2, ws.max_row + 1):
            topic_data = {
                "topic": ws.cell(row=row, column=1).value,
                "status": ws.cell(row=row, column=2).value,
                "claimed_by": ws.cell(row=row, column=3).value,
                "started_at": ws.cell(row=row, column=4).value,
                "completed_at": ws.cell(row=row, column=5).value,
                "error": ws.cell(row=row, column=6).value,
            }
            if topic_data["topic"]:  # Only add if topic is not empty
                topics.append(topic_data)
        
        wb.close()
        return topics
