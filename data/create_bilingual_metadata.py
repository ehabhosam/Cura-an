#!/usr/bin/env python3
"""
Script to create a bilingual metadata file combining English and Arabic Quran verses.
This script reads the English metadata and Arabic surah files to create a unified dataset.
"""

import json
import os
import re
from pathlib import Path

def parse_verse_id(verse_id: str) -> tuple:
    """Parse verse ID like '1:1' into (surah_number, verse_number)."""
    surah, verse = verse_id.split(':')
    return int(surah), int(verse)

def normalize_verse_key(verse_key: str) -> int:
    """Convert verse_X to integer X."""
    if verse_key.startswith('verse_'):
        return int(verse_key.replace('verse_', ''))
    return int(verse_key)

def load_arabic_surahs(surah_dir: Path) -> dict:
    """Load all Arabic surah files into a dictionary."""
    arabic_data = {}
    
    for i in range(1, 115):  # Surah 1 to 114
        surah_file = surah_dir / f"surah_{i}.json"
        if surah_file.exists():
            with open(surah_file, 'r', encoding='utf-8') as f:
                surah_data = json.load(f)
                
            # Extract verses and normalize keys
            verses = {}
            for verse_key, verse_text in surah_data['verse'].items():
                verse_num = normalize_verse_key(verse_key)
                # Skip verse_0 as it's usually Bismillah and not part of main verses
                if verse_num > 0:
                    verses[verse_num] = verse_text
                    
            arabic_data[i] = {
                'name': surah_data.get('name', f'Surah {i}'),
                'verses': verses
            }
        else:
            print(f"Warning: {surah_file} not found")
            
    return arabic_data

def create_bilingual_metadata(english_metadata_path: Path, surah_dir: Path, output_path: Path):
    """Create bilingual metadata file."""
    
    # Load English metadata
    print("Loading English metadata...")
    with open(english_metadata_path, 'r', encoding='utf-8') as f:
        english_verses = json.load(f)
    
    # Load Arabic surahs
    print("Loading Arabic surahs...")
    arabic_data = load_arabic_surahs(surah_dir)
    
    # Create bilingual dataset
    print("Creating bilingual dataset...")
    bilingual_verses = []
    
    for verse in english_verses:
        verse_id = verse['id']
        english_text = verse['text']
        
        try:
            surah_num, verse_num = parse_verse_id(verse_id)
            
            # Get Arabic text
            arabic_text = None
            if surah_num in arabic_data and verse_num in arabic_data[surah_num]['verses']:
                arabic_text = arabic_data[surah_num]['verses'][verse_num]
            
            # Create bilingual verse entry
            bilingual_verse = {
                'id': verse_id,
                'verse_en': english_text,
                'verse_ar': arabic_text,
                'surah_name': arabic_data.get(surah_num, {}).get('name', f'Surah {surah_num}')
            }
            
            bilingual_verses.append(bilingual_verse)
            
        except (ValueError, KeyError) as e:
            print(f"Warning: Could not process verse {verse_id}: {e}")
            # Add entry with missing Arabic
            bilingual_verse = {
                'id': verse_id,
                'verse_en': english_text,
                'verse_ar': None,
                'surah_name': f'Surah {surah_num}' if 'surah_num' in locals() else 'Unknown'
            }
            bilingual_verses.append(bilingual_verse)
    
    # Save bilingual metadata
    print(f"Saving bilingual metadata to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(bilingual_verses, f, ensure_ascii=False, indent=2)
    
    print(f"Created bilingual metadata with {len(bilingual_verses)} verses")
    
    # Print some statistics
    arabic_count = sum(1 for v in bilingual_verses if v['verse_ar'] is not None)
    print(f"Verses with Arabic text: {arabic_count}/{len(bilingual_verses)}")
    
    return bilingual_verses

def main():
    # Set up paths
    script_dir = Path(__file__).parent
    english_metadata_path = script_dir / "quran_metadata.json"
    surah_dir = script_dir / "surah"
    output_path = script_dir / "quran_bilingual_metadata.json"
    
    # Check if input files exist
    if not english_metadata_path.exists():
        print(f"Error: {english_metadata_path} not found")
        return
    
    if not surah_dir.exists():
        print(f"Error: {surah_dir} not found")
        return
    
    # Create bilingual metadata
    try:
        bilingual_verses = create_bilingual_metadata(english_metadata_path, surah_dir, output_path)
        print("✅ Successfully created bilingual metadata!")
        
        # Show a sample
        print("\nSample entries:")
        for i, verse in enumerate(bilingual_verses[:3]):
            print(f"\nVerse {verse['id']}:")
            print(f"  English: {verse['verse_en']}")
            print(f"  Arabic: {verse['verse_ar']}")
            print(f"  Surah: {verse['surah_name']}")
            
    except Exception as e:
        print(f"Error creating bilingual metadata: {e}")
        raise

if __name__ == "__main__":
    main()
