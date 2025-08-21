"""
Application service manager.
"""
import os
import logging
from .vector_search import VectorSearchService
from .genai import GenAIService

logger = logging.getLogger(__name__)


class AppServices:
    """Manages application services."""
    
    def __init__(self):
        self._search_service = None
        self._genai_service = None
    
    def initialize_search_service(self, embeddings_path: str, metadata_path: str) -> bool:
        """Initialize the search service."""
        try:
            self._search_service = VectorSearchService(embeddings_path, metadata_path)
            return True
        except Exception as e:
            logger.error(f"Failed to initialize search service: {e}")
            self._search_service = None
            return False
    
    def initialize_genai_service(self, model_function) -> bool:
        """Initialize the GenAI service with a model function."""
        try:
            self._genai_service = GenAIService(model_function)
            return True
        except Exception as e:
            logger.error(f"Failed to initialize GenAI service: {e}")
            self._genai_service = None
            return False
    
    @property
    def search(self):
        """Get the search service."""
        return self._search_service
    
    @property
    def genai(self):
        """Get the GenAI service."""
        return self._genai_service


# Global services instance
services = AppServices()
from .auth import *