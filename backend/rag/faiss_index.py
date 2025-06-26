# build_faiss_index.py
import json
import numpy as np
import faiss

with open("output/chunks_with_embeddings.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = np.array([chunk["embedding"] for chunk in chunks]).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "output/faiss.index")
with open("output/metadata.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f)

print("✅ FAISS index and metadata saved to output/")
