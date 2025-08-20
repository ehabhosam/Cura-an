import numpy as np
import json

# Paths
EMBEDDINGS_PATH = "quran_embeddings.npy"   # your saved embeddings
VERSES_PATH = "quran_metadata.json"          # JSON file with verse text + metadata

# Load embeddings
embeddings = np.load(EMBEDDINGS_PATH)

# Load verse metadata
with open(VERSES_PATH, "r", encoding="utf-8") as f:
    verses = json.load(f)

print(verses)  # Debugging line to check loaded verses

# Sanity check
print(f"Embeddings shape: {embeddings.shape}")
print(f"Number of verses: {len(verses)}")

# Iterate and log
for i, (verse, vector) in enumerate(zip(verses, embeddings)):
    verse_meta = verse.get("id").split(":")
    chapter = verse_meta[0]
    verse_num = verse_meta[1]
    text = verse.get("text")
    
    print(f"\n[{i}] Surah {chapter}, Verse {verse_num}")
    print(f"Text: {text}")
    print(f"Vector (first 10 dims): {vector[:10]} ...")  # shorten for readability
