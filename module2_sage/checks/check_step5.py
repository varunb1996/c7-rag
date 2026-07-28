"""Check step 5: the schedule filter is exact, and the three layers survive.

The filter checks are offline; the last check makes ONE live API call.

Run from module2_sage/:  python checks/check_step5.py
"""
from _util import done, fail, ok  # noqa: F401

import step5_schedule
from step5_schedule import get_sessions

# --- deterministic filter checks (no LLM anywhere) --------------------------
if len(get_sessions()) != 12:
    fail(f"no filters -> all 12 sessions, got {len(get_sessions())}")
ok("no filters returns the full schedule (12 sessions)")

wk4 = get_sessions(week=4)
if len(wk4) != 3 or not all(s["week"] == 4 for s in wk4):
    fail(f"week=4 should return exactly the 3 week-4 sessions, got {len(wk4)}")
ok("week=4 -> 3 sessions")

code_wk4 = get_sessions(week=4, track="code")
if len(code_wk4) != 2:
    fail(f"week=4 + track='code' should return 2 sessions "
         f"(the 'both' lecture + the code practical), got {len(code_wk4)}",
         "sessions marked track='both' must match EVERY track filter")
ok("track filter treats 'both' as matching — filters compose")

rag_sessions = get_sessions(topic="rag")
if len(rag_sessions) != 4:
    fail(f"topic='rag' should return 4 sessions, got {len(rag_sessions)}",
         "topics is a LIST — test membership, not equality")
ok("topic='rag' -> 4 sessions (membership test on the topics list)")

# --- one pass through the three layers (live) ------------------------------
calls = []
real = step5_schedule.get_sessions


def spy(*args, **kwargs):
    calls.append(kwargs or args)
    return real(*args, **kwargs)


step5_schedule.get_sessions = spy

print("Asking: 'What week is the evals lecture?' (live call)...")
try:
    ans = step5_schedule.logistics_answer("What week is the evals lecture?")
finally:
    step5_schedule.get_sessions = real

if not calls:
    fail("the model never called get_sessions",
         "re-read your tool schema description — it's load-bearing prose")
ok(f"model called get_sessions with {calls[0]}")
if not (isinstance(ans, str) and "6" in ans):
    fail(f"expected an answer mentioning week 6, got: {ans!r}")
ok(f"answer grounded in tool output: {ans.strip()[:120]}")

print("\nSixty seconds of work, zero embeddings. This is why the structured")
print("path gets built FIRST, and why the router in step 6 exists to protect it.")
done("Step 5")
