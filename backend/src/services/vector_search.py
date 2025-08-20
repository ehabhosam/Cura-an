"""
FAISS-based search implementation.
"""
import faiss
import numpy as np
import json
from .search_service import SearchService


class VectorSearchService(SearchService):
    """FAISS-based vector search implementation."""
    
    def __init__(self, embeddings_path: str, metadata_path: str, model_name: str = 'multi-qa-mpnet-base-dot-v1'):
        self.embeddings_path = embeddings_path
        self.metadata_path = metadata_path
        self.model_name = model_name
        self.index = None
        self.verses = []
        self.model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize FAISS index with precomputed embeddings."""
        # Load precomputed embeddings
        embeddings = np.load(self.embeddings_path)
        
        # Load metadata
        with open(self.metadata_path) as f:
            self.verses = json.load(f)
        
        # Create FAISS index (cosine similarity)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
    
    def search(self, query: str, k: int = 5) -> list:
        """Search for similar verses."""
        from sentence_transformers import SentenceTransformer
        
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
        
        # Encode query (normalize for cosine similarity)
        query_emb = self.model.encode([query], normalize_embeddings=True)
        
        # Search using FAISS
        D, I = self.index.search(query_emb, k)
        
        # Format results with scores
        results = []
        for score, idx in zip(D[0], I[0]):
            verse = self.verses[idx].copy()
            verse['score'] = float(score)
            results.append(verse)
        
        return results
