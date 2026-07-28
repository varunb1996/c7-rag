"""Check step 6: the receptionist redirects reliably and never tries to solve.

Makes LIVE API calls (needs GROQ_API_KEY) — 8 cheap router calls.

Run from module2_sage/:  python checks/check_step6.py
"""
from _util import done, fail, ok  # noqa: F401

from step6_router import route

CASES = [
    ("What week is the RAG practical?", "logistics"),
    ("What date is the evals lecture?", "logistics"),
    ("Is there a no-code session in week 3?", "logistics"),
    ("When does the cohort's tool calling practical happen?", "logistics"),
    ("When will I learn how to automate my job?", "content"),
    ("Why does my model make things up?", "content"),
    ("What is the difference between a workflow and an agent?", "content"),
    ("Explain the physics book story", "content"),
]

hits = 0
for query, expected in CASES:
    got = route(query)
    if got not in ("logistics", "content"):
        fail(f"route() returned {got!r} — it must return exactly "
             f"'logistics' or 'content'",
             "parse the JSON and return only the route string")
    mark = "✓" if got == expected else "✗"
    if got == expected:
        hits += 1
    print(f"  {mark} {got:>10}  <-  {query}")

if hits < 7:
    fail(f"router got {hits}/8 — below the bar",
         "iterate ROUTER_PROMPT against these cases: describe the two routes "
         "by what makes them DIFFERENT (clean filter vs meaning)")
ok(f"router accuracy {hits}/8 on the smoke set")

print("\nRemember: this component is probabilistic. Step 8 makes you run it")
print("three times and watch the number move — single runs lie.")
done("Step 6")
