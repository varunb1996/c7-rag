"""Step 1 — SOLUTION. An embedding is a list of numbers."""
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(texts):
    return model.encode(texts, normalize_embeddings=True)


if __name__ == "__main__":
    vecs = embed(
        [
            "A cat sat on the mat",
            "A kitten rested on the rug",
            "The stock market fell sharply today",
        ]
    )
    print("shape:", vecs.shape)
    print("\nfirst vector, first 12 of its 384 numbers:")
    print(np.round(vecs[0][:12], 4))
    print("length of the vector:", round(float(np.linalg.norm(vecs[0])), 4))
    print("\ncat-vs-kitten similarity :", round(float(vecs[0] @ vecs[1]), 3))
    print("cat-vs-stocks similarity :", round(float(vecs[0] @ vecs[2]), 3))
