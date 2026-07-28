"""Check step 2: the fraction and the dot product are the same number.

Run from module2_sage/:  python checks/check_step2.py
"""
import numpy as np

from _util import done, fail, ok  # noqa: F401

from step2_cosine import cosine_full, cosine_normalized, normalize

rng = np.random.default_rng(7)

# anchors with known answers
x, y = np.array([1.0, 0.0]), np.array([0.0, 1.0])
if not np.isclose(cosine_full(x, y), 0.0):
    fail(f"cosine of perpendicular vectors should be 0, got {cosine_full(x, y)}")
if not np.isclose(cosine_full(x, x), 1.0):
    fail(f"cosine of a vector with itself should be 1, got {cosine_full(x, x)}")
if not np.isclose(cosine_full(x, -x), -1.0):
    fail(f"cosine of opposite vectors should be -1, got {cosine_full(x, -x)}")
ok("anchors: same direction=1, perpendicular=0, opposite=-1")

# scale-invariance: cosine cares about ANGLE, not length
a, b = rng.normal(size=384), rng.normal(size=384)
if not np.isclose(cosine_full(a, b), cosine_full(a * 10, b * 0.01)):
    fail("cosine changed when the vectors were rescaled",
         "the norms in the denominator should cancel any scaling")
ok("scale-invariant: rescaling a vector doesn't change the angle")

# normalize()
na = normalize(a)
if not np.isclose(np.linalg.norm(na), 1.0):
    fail(f"normalize() output has length {np.linalg.norm(na):.4f}, expected 1.0")
ok("normalize() produces unit-length vectors")

# the collapse: fraction == dot product after normalization
for _ in range(5):
    u, v = rng.normal(size=384), rng.normal(size=384)
    if not np.isclose(cosine_full(u, v), cosine_normalized(normalize(u), normalize(v))):
        fail("cosine_full and cosine_normalized disagree on normalized inputs",
             "after normalizing, the denominator is 1x1 — only the dot product survives")
ok("the fraction collapses to a dot product on normalized vectors — 5/5 random trials")

done("Step 2")
