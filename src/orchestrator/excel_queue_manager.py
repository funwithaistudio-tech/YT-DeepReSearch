"""Excel Queue Manager - Manages topic queue from Excel file."""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger


class ExcelQueueManager:
    """Manages research topics queue from Excel file."""
    
    def __init__(self, excel_path: str, sheet_name: str = "Topics"):
        """
        Initialize Excel Queue Manager.
        
        Args:
            excel_path: Path to Excel file
            sheet_name: Name of the sheet containing topics
        """
        self.excel_path = Path(excel_path)
        self.sheet_name = sheet_name
        
        # Create file if it doesn't exist
        if not self.excel_path.exists():
            self._create_template()
        
        logger.info(f"ExcelQueueManager initialized with {self.excel_path}")
    
    def _create_template(self):
        """Create template Excel file with required columns."""
        self.excel_path.parent.mkdir(parents=True, exist_ok=True)
        
        template_df = pd.DataFrame({
            "Topic": ["Example: The Science of Black Holes"],
            "Status": ["pending"],
            "Priority": [1],
            "Added_Date": [datetime.now().strftime("%Y-%m-%d")],
            "Started_Date": [""],
            "Completed_Date": [""],
            "Output_Directory": [""],
            "Error_Message": [""],
            "Notes": [""]
        })
        
        template_df.to_excel(self.excel_path, sheet_name=self.sheet_name, index=False)
        logger.info(f"Created template Excel file: {self.excel_path}")
    
    def get_pending_topics(self) -> List[Dict]:
        """
        Get all pending topics from Excel.
        
        Returns:
            List of topic dictionaries
        """
        try:
            df = pd.read_excel(self.excel_path, sheet_name=self.sheet_name)
            
            # Filter for pending topics
            pending_df = df[df["Status"].str.lower() == "pending"]
            
            # Sort by priority
            if "Priority" in pending_df.columns:
                pending_df = pending_df.sort_values("Priority", ascending=False)
            
            topics = []
            for idx, row in pending_df.iterrows():
                topics.append({
                    "index": idx,
                    "topic": row["Topic"],
                    "priority": row.get("Priority", 1),
                    "notes": row.get("Notes", "")
                })
            
            logger.info(f"Found {len(topics)} pending topics")
            return topics
        
        except Exception as e:
            logger.error(f"Failed to read Excel file: {str(e)}")
            return []
    
    def update_status(
        self,
        topic_index: int,
        status: str,
        output_dir: Optional[str] = None,
        error_message: Optional[str] = None
    ):
        """
        Update topic status in Excel.
        
        Args:
            topic_index: Row index in Excel
            status: New status (pending, processing, completed, failed)
            output_dir: Output directory path
            error_message: Error message if failed
        """
        try:
            df = pd.read_excel(self.excel_path, sheet_name=self.sheet_name)
            
            # Update status
            df.at[topic_index, "Status"] = status
            
            # Update timestamps
            if status == "processing":
                df.at[topic_index, "Started_Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif status in ["completed", "failed"]:
                df.at[topic_index, "Completed_Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update output directory
            if output_dir:
                df.at[topic_index, "Output_Directory"] = output_dir
            
            # Update error message
            if error_message:
                df.at[topic_index, "Error_Message"] = error_message
            
            # Save back to Excel
            df.to_excel(self.excel_path, sheet_name=self.sheet_name, index=False)
            
            logger.info(f"Updated topic {topic_index} status to: {status}")
        
        except Exception as e:
            logger.error(f"Failed to update Excel file: {str(e)}")
    
    def add_topic(
        self,
        topic: str,
        priority: int = 1,
        notes: str = ""
    ):
        """
        Add a new topic to the queue.
        
        Args:
            topic: Topic description
            priority: Priority level (higher = more important)
            notes: Additional notes
        """
        try:
            df = pd.read_excel(self.excel_path, sheet_name=self.sheet_name)
            
            new_row = {
                "Topic": topic,
                "Status": "pending",
                "Priority": priority,
                "Added_Date": datetime.now().strftime("%Y-%m-%d"),
                "Started_Date": "",
                "Completed_Date": "",
                "Output_Directory": "",
                "Error_Message": "",
                "Notes": notes
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(self.excel_path, sheet_name=self.sheet_name, index=False)
            
            logger.info(f"Added new topic: {topic}")
        
        except Exception as e:
            logger.error(f"Failed to add topic: {str(e)}")
    
    def get_statistics(self) -> Dict:
        """
        Get queue statistics.
        
        Returns:
            Dictionary with statistics
        """
        try:
            df = pd.read_excel(self.excel_path, sheet_name=self.sheet_name)
            
            stats = {
                "total": len(df),
                "pending": len(df[df["Status"].str.lower() == "pending"]),
                "processing": len(df[df["Status"].str.lower() == "processing"]),
                "completed": len(df[df["Status"].str.lower() == "completed"]),
                "failed": len(df[df["Status"].str.lower() == "failed"])
            }
            
            return stats
        
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}
