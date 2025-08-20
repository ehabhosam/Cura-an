"""
Data models for the search service.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchResult:
    """Represents a search result with verse and similarity score."""
    id: str
    text: str
    score: float
    
    @classmethod
    def from_verse_with_score(cls, verse: dict, score: float) -> 'SearchResult':
        """Create a SearchResult from a verse dict and score."""
        return cls(
            id=verse['id'],
            text=verse['text'],
            score=score
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'text': self.text,
            'score': self.score
        }
