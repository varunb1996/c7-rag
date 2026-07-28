"""Step 3 — Semantic search over the course notes. No vector database.

Run:    python step3_search.py
Check:  python checks/check_step3.py
"""
import glob

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

corpus = [
    {"id": path, "text": open(path, encoding="utf-8").read()}
    for path in sorted(glob.glob("data/notes/*.txt"))
]

matrix = model.encode([c["text"] for c in corpus], normalize_embeddings=True)


def semantic_search(query, k=3):
    """Return the top-k chunks for the query, as (id, score, text) tuples,
    highest score first."""
    q = model.encode(query, normalize_embeddings=True)
    scores = matrix @ q
    top_idx = np.argsort(scores)[::-1][:k]
    return [(corpus[i]["id"], float(scores[i]), corpus[i]["text"]) for i in top_idx]


if __name__ == "__main__":
    # The query that broke Sage in production. Note what it does NOT contain:
    # no week number, no lecture title, no keyword that appears in the notes.
    for qid, score, text in semantic_search("When will I learn how to automate my job?"):
        print(f"{score:.3f}  {qid}")
        print(f"       {text.splitlines()[0]}\n")
    # Expected on top: the workflows-and-agents note. Grep could never.
