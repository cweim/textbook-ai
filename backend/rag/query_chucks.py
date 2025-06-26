# query_chunks.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Sample queries (replace or extend as needed)
sample_queries = [
    "What is mode 3 knowledge production?",
    "Explain the relevance gap in management research.",
    "Who are Huff and Huff?",
    "What is evidence-based management?",
    "What is design science in management?"
]

# Load index + metadata
index = faiss.read_index("output/faiss.index")
with open("output/metadata.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

for query in sample_queries:
    print(f"\n🔍 Query: {query}")
    query_embedding = model.encode(query).astype("float32")
    D, I = index.search(np.array([query_embedding]), k=5)

    top_chunks = [chunks[i] for i in I[0]]

    print("📄 Top Relevant Chunks:\n")
    for i, chunk in enumerate(top_chunks, 1):
        print(f"[{i}] {chunk['text'][:300]}...\n")
    print("=" * 80)

