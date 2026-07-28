"""Step 1 — An embedding is a list of numbers.

Run:    python step1_embed.py     (first run downloads the model, ~90 MB)
Check:  python checks/check_step1.py
"""
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dims, free, local


def embed(texts):
    """Encode a list of strings into one NORMALIZED vector per string.

    Returns a numpy array of shape (len(texts), 384).
    """
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

    # STARE AT THIS. This wall of floats is the entire mystique of embeddings.
    print("\nfirst vector, first 12 of its 384 numbers:")
    print(np.round(vecs[0][:12], 4))
    print("length of the vector (should be 1.0 — that's 'normalized'):",
          round(float(np.linalg.norm(vecs[0])), 4))

    # Because they're normalized, similarity is just a dot product (step 2
    # proves why). Two sentences about small animals on floor coverings share
    # almost NO words — watch what happens anyway:
    print("\ncat-vs-kitten similarity :", round(float(vecs[0] @ vecs[1]), 3))
    print("cat-vs-stocks similarity :", round(float(vecs[0] @ vecs[2]), 3))
    # THAT gap is the thing keyword search structurally cannot see.
