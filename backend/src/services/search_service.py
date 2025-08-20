"""
Search service interface.
"""
from abc import ABC, abstractmethod
from typing import List


class SearchService(ABC):
    """Interface for semantic search operations."""
    
    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[dict]:
        """
        Search for similar content.
        
        Args:
            query: Text to search for
            k: Number of results to return
            
        Returns:
            List of results with scores
        """
        pass
