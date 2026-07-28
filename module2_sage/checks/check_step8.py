"""Check step 8: the golden set is real (10+, both labels, your own cases)
and the scorer runs.

Makes LIVE API calls (needs GROQ_API_KEY) — one router call per golden pair.

Run from module2_sage/:  python checks/check_step8.py
"""
import io
import runpy
import sys
from contextlib import redirect_stdout

from _util import MODULE_ROOT, done, fail, ok  # noqa: F401

buf = io.StringIO()
print("Running your step8_eval.py once (live router calls)...")
try:
    with redirect_stdout(buf):
        env = runpy.run_path(str(MODULE_ROOT / "step8_eval.py"), run_name="__main__")
except NotImplementedError:
    fail("step8_eval.py still raises NotImplementedError — write the scorer")
output = buf.getvalue()
print(output)

GOLDEN = env.get("GOLDEN", [])
if len(GOLDEN) < 10:
    fail(f"GOLDEN has {len(GOLDEN)} pairs — the exercise asks for at least 10",
         "add at least four queries YOU asked in step 7, including one that "
         "fooled the router")
ok(f"golden set has {len(GOLDEN)} pairs")

labels = {label for _, label in GOLDEN}
if labels != {"logistics", "content"}:
    fail(f"labels are {labels} — the set must contain both routes")
ok("both routes represented")

if "/" not in output or "accuracy" not in output.lower():
    fail("expected output like 'router accuracy: 8/10'",
         'print(f"router accuracy: {score}/{len(GOLDEN)}")')
ok("scorer prints accuracy as a fraction")

print("The check ran your eval ONCE. That number is a sample, not a truth —")
print("run step8 two more times yourself and write down the range.")
done("Step 8 — Sage is built, routed, and measured. Now swap in YOUR corpus.")
