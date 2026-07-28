"""Step 2 — SOLUTION. Cosine similarity is a dot product."""
import numpy as np


def cosine_full(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def normalize(v):
    return v / np.linalg.norm(v)


def cosine_normalized(a, b):
    return np.dot(a, b)  # the denominator was 1 * 1 — only the top survived


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    a, b = rng.normal(size=384), rng.normal(size=384)

    full = cosine_full(a, b)
    fast = cosine_normalized(normalize(a), normalize(b))
    print(f"full formula          : {full:.6f}")
    print(f"normalized dot product: {fast:.6f}")
    print(f"identical             : {np.isclose(full, fast)}")

    print("\ncosine(v, v)      =", round(cosine_full(a, a), 4))
    print("cosine(v, -v)     =", round(cosine_full(a, -a), 4))
    print("cosine(x-axis, y-axis) =",
          round(cosine_full(np.array([1.0, 0.0]), np.array([0.0, 1.0])), 4))
