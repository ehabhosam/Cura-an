from sentence_transformers import SentenceTransformer
import numpy as np
import json

# Load model
model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

# Load verses from .txt file
verses = []
with open("en.quraan.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        chapter, verse, text = parts
        verses.append({"id": f"{chapter}:{verse}", "text": text})

# Encode all verses
texts = [v["text"] for v in verses]
embeddings = model.encode(texts, normalize_embeddings=True)

# Save embeddings + metadata
np.save("quran_embeddings.npy", embeddings)       # vector data
with open("quran_metadata.json", "w") as f:
    json.dump(verses, f, ensure_ascii=False, indent=2)
