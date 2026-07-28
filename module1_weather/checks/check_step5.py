"""Check step 5: the win is measured, not vibed.

Run from module1_weather/:  python checks/check_step5.py
"""
from _util import done, fail, ok  # noqa: F401

from step5_prove_it import measure

naive, rag = measure()

if not (isinstance(naive, int) and isinstance(rag, int)):
    fail(f"measure() must return two ints, got ({type(naive).__name__}, {type(rag).__name__})")

if naive < 400_000:
    fail(f"naive payload is only {naive:,} tokens — that's not all ten chunk files",
         "read every file in chunks/, not a sample")
ok(f"naive payload: {naive:,} tokens — comfortably past the 128K window")

if not 1_000 <= rag <= 25_000:
    fail(f"rag payload is {rag:,} tokens — expected roughly 12,000",
         "it should be step 3's August daily summaries, nothing more")
ok(f"rag payload: {rag:,} tokens")

ratio = naive / rag
if ratio < 20:
    fail(f"compression is only {ratio:.1f}x — something is off in one of the payloads")
ok(f"compression: {ratio:,.0f}x — from a metadata filter and a defaultdict, zero GPUs")

done("Step 5 — Module 1 complete. Go meet the query with nothing to filter on: ../module2_sage/")
