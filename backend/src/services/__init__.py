"""
Application service manager.
"""
import os
from .vector_search import VectorSearchService


class AppServices:
    """Manages application services."""
    
    def __init__(self):
        self._search_service = None
    
    def initialize_search_service(self, embeddings_path: str, metadata_path: str) -> bool:
        """Initialize the search service."""
        try:
            self._search_service = VectorSearchService(embeddings_path, metadata_path)
            return True
        except Exception as e:
            print(f"Failed to initialize search service: {e}")
            self._search_service = None
            return False
    
    @property
    def search(self):
        """Get the search service."""
        return self._search_service


# Global services instance
services = AppServices()
from .auth import *