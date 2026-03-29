# -*- coding: utf-8 -*-
"""
Learn From Feedback - Record and learn from user feedback

Note: This is a simplified version for PyPI release.
"""

from typing import Dict, Any, Optional
from datetime import datetime


class LearnFromFeedback:
    """
    Record and learn from user feedback
    
    Example:
        learner = LearnFromFeedback()
        learner.record(user_id="user123", feedback="Great job!", rating=5)
    """
    
    def __init__(self):
        """Initialize feedback learner"""
        self._feedback_records: list = []
    
    def record(
        self,
        feedback: str,
        rating: Optional[int] = None,
        category: str = "general",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record feedback
        
        Args:
            feedback: Feedback text
            rating: Rating score (1-5)
            category: Feedback category
            user_id: User identifier
        
        Returns:
            Feedback record
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback,
            "rating": rating,
            "category": category,
            "user_id": user_id
        }
        
        self._feedback_records.append(record)
        return record
    
    def get_feedback(
        self,
        category: Optional[str] = None,
        limit: int = 10
    ) -> list:
        """
        Get feedback records
        
        Args:
            category: Filter by category
            limit: Maximum records to return
        
        Returns:
            List of feedback records
        """
        if category:
            records = [
                r for r in self._feedback_records
                if r.get("category") == category
            ]
        else:
            records = self._feedback_records
        
        return records[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get feedback statistics
        
        Returns:
            Statistics dictionary
        """
        total = len(self._feedback_records)
        ratings = [r["rating"] for r in self._feedback_records if r.get("rating")]
        
        return {
            "total_feedback": total,
            "average_rating": sum(ratings) / len(ratings) if ratings else 0.0,
            "categories": list(set(r.get("category", "general") for r in self._feedback_records))
        }
