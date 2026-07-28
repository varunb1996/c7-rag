"""Step 2 — Cosine similarity is a dot product.

Pure numpy. No model, no API, no magic. The blog-post formula has a fraction
in it; you are about to watch the fraction disappear.

Run:    python step2_cosine.py
Check:  python checks/check_step2.py
"""
import numpy as np


def cosine_full(a, b):
    """The textbook formula: dot(a, b) / (|a| * |b|).

    Works on ANY two vectors, normalized or not.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def normalize(v):
    """Scale v to length 1."""
    return v / np.linalg.norm(v)


def cosine_normalized(a, b):
    """The same similarity when a and b are ALREADY length 1."""
    return np.dot(a, b)


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    a, b = rng.normal(size=384), rng.normal(size=384)  # same dims as MiniLM

    full = cosine_full(a, b)
    fast = cosine_normalized(normalize(a), normalize(b))
    print(f"full formula          : {full:.6f}")
    print(f"normalized dot product: {fast:.6f}")
    print(f"identical             : {np.isclose(full, fast)}")

    # Sanity anchors — predict all three before running:
    print("\ncosine(v, v)      =", round(cosine_full(a, a), 4), " (same direction)")
    print("cosine(v, -v)     =", round(cosine_full(a, -a), 4), " (opposite)")
    print("cosine(x-axis, y-axis) =",
          round(cosine_full(np.array([1.0, 0.0]), np.array([0.0, 1.0])), 4),
          " (unrelated)")

    # This is why step 1 passed normalize_embeddings=True: pay the division
    # ONCE at encoding time, and every search after that is a bare dot product.
