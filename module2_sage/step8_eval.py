"""Step 8 — Prove it: ten golden pairs, the seed of your evals.

A working demo is not a working system; the difference is measurement.

Run:    python step8_eval.py      (three times — watch the number move)
Check:  python checks/check_step8.py     (live API calls)
"""
from step6_router import route

# Six are given. TODO(1): add AT LEAST four more from queries you actually
# asked in step 7 — including at least one that fooled the router. A golden
# set made only of easy cases measures nothing.
GOLDEN = [
    ("What week is the RAG practical?",                  "logistics"),
    ("Is there a no-code session in week 3?",            "logistics"),
    ("What date is the evals lecture?",                  "logistics"),
    ("When will I learn how to automate my job?",        "content"),
    ("Why does my model make things up?",                "content"),
    ("What's the difference between a workflow and an agent?", "content"),
    ("Is there a session in week 10?",                   "logistics"),
    ("Tell me about week 4.",                            "logistics"),
    ("What is the refund policy for the cohort?",        "content"),
    ("What topics does week 4 cover?",                   "logistics"),  # fools the router: reads as content, is actually a clean filter
]

score = sum(route(q) == label for q, label in GOLDEN)
print(f"router accuracy: {score}/{len(GOLDEN)}")

# Then the part that separates engineers from demo-builders:
#   1. Run this file THREE times. The router is probabilistic; single runs lie.
#      Write down your range.
#   2. Change ONE WORD of ROUTER_PROMPT in step6. Re-run three times.
#      Better or worse? You are now doing prompt engineering against a metric
#      instead of against vibes.
#   3. Below 8/10? Iterate the prompt BEFORE adding any machinery.
