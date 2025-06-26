# embed_chunks.py
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

with open("output/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

for chunk in chunks:
    chunk["embedding"] = model.encode(chunk["text"]).tolist()

with open("output/chunks_with_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f)

print("✅ Saved embedded chunks to output/chunks_with_embeddings.json")
