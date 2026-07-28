"""Step 3 — SOLUTION. Semantic search, no vector database."""
import glob

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

corpus = [
    {"id": path, "text": open(path).read()}
    for path in sorted(glob.glob("data/notes/*.txt"))
]

matrix = model.encode(
    [c["text"] for c in corpus], normalize_embeddings=True
)  # one vector per chunk; this array IS the vector database


def semantic_search(query, k=3):
    q = model.encode([query], normalize_embeddings=True)[0]
    scores = matrix @ q  # cosine similarity: a dot product
    top = np.argsort(scores)[::-1][:k]
    return [(corpus[i]["id"], float(scores[i]), corpus[i]["text"]) for i in top]


if __name__ == "__main__":
    for qid, score, text in semantic_search("When will I learn how to automate my job?"):
        print(f"{score:.3f}  {qid}")
        print(f"       {text.splitlines()[0]}\n")
