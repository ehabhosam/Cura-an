"""
Data models for the search service.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SearchResult:
    """Represents a search result with bilingual verse and similarity score."""
    id: str
    verse_en: str
    verse_ar: str
    score: float
    surah_name: Optional[str] = None
    
    @classmethod
    def from_verse_with_score(cls, verse: dict, score: float) -> 'SearchResult':
        """Create a SearchResult from a verse dict and score."""
        return cls(
            id=verse['id'],
            verse_en=verse.get('verse_en', verse.get('text', '')),  # Fallback for old format
            verse_ar=verse.get('verse_ar', ''),
            score=score,
            surah_name=verse.get('surah_name')
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        result = {
            'id': self.id,
            'verse_en': self.verse_en,
            'verse_ar': self.verse_ar,
            'score': self.score
        }
        if self.surah_name:
            result['surah_name'] = self.surah_name
        return result
