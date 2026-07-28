"""Check step 3: the matrix is the vector database, and meaning finds the
right note without sharing its keywords.

Run from module2_sage/:  python checks/check_step3.py
"""
import numpy as np

from _util import done, fail, ok  # noqa: F401

import step3_search
from step3_search import corpus, matrix, semantic_search

if not (isinstance(corpus, list) and len(corpus) == 6):
    fail(f"corpus should be a list of 6 chunks (one per file in data/notes/), "
         f"got {len(corpus) if isinstance(corpus, list) else type(corpus).__name__}")
if not all(set(c) >= {"id", "text"} and c["text"].strip() for c in corpus):
    fail("every corpus entry needs an 'id' and non-empty 'text'")
ok("corpus: 6 chunks, one per course note")

if not (isinstance(matrix, np.ndarray) and matrix.shape == (6, 384)):
    fail(f"matrix should be shape (6, 384), got "
         f"{matrix.shape if isinstance(matrix, np.ndarray) else type(matrix).__name__}")
if not np.allclose(np.linalg.norm(matrix, axis=1), 1.0, atol=1e-3):
    fail("matrix rows aren't normalized", "encode with normalize_embeddings=True")
ok("matrix: (6, 384), rows normalized — this array IS your vector database")

results = semantic_search("When will I learn how to automate my job?", k=3)
if len(results) != 3:
    fail(f"k=3 should return 3 results, got {len(results)}")
ids = [r[0] for r in results]
scores = [r[1] for r in results]
if scores != sorted(scores, reverse=True):
    fail(f"scores not in descending order: {[round(s, 3) for s in scores]}",
         "np.argsort is ascending — reverse it before slicing the top k")
ok(f"top-3 sorted by score: {[round(s, 3) for s in scores]}")

if not any("workflows" in i for i in ids[:2]):
    fail(f"the Sage-killer query should surface the workflows-and-agents note "
         f"near the top; got {ids}",
         "check you're searching over the chunk TEXTS, not the file paths")
ok("'automate my job' found the workflows note — zero keywords shared. Grep could never.")

results = semantic_search("Why does the model confidently invent facts?", k=1)
if "hallucination" not in results[0][0]:
    fail(f"'invent facts' should retrieve the hallucination note, got {results[0][0]}")
ok("'invent facts' found the hallucination note")

done("Step 3")
