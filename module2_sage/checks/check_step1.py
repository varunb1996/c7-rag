"""Check step 1: embed() returns normalized 384-dim vectors that put meaning,
not word overlap, near each other.

Run from module2_sage/:  python checks/check_step1.py
"""
import numpy as np

from _util import done, fail, ok  # noqa: F401

from step1_embed import embed

vecs = embed(
    [
        "A cat sat on the mat",
        "A kitten rested on the rug",
        "The stock market fell sharply today",
    ]
)

if not isinstance(vecs, np.ndarray):
    fail(f"embed() returned {type(vecs).__name__}, expected a numpy array")
if vecs.shape != (3, 384):
    fail(f"shape is {vecs.shape}, expected (3, 384)",
         "one row per input text; MiniLM produces 384 dimensions")
ok("shape (3, 384) — one 384-float vector per text")

norms = np.linalg.norm(vecs, axis=1)
if not np.allclose(norms, 1.0, atol=1e-3):
    fail(f"vector lengths are {np.round(norms, 3)}, expected all 1.0",
         "pass normalize_embeddings=True — step 2 explains what it buys you")
ok("every vector has length 1.0 — normalized")

related = float(vecs[0] @ vecs[1])
unrelated = float(vecs[0] @ vecs[2])
if not related > unrelated + 0.15:
    fail(f"cat-vs-kitten ({related:.3f}) should score clearly above "
         f"cat-vs-stocks ({unrelated:.3f})")
ok(f"meaning beats word overlap: cat~kitten {related:.3f} vs cat~stocks {unrelated:.3f}")

done("Step 1")
