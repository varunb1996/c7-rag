"""Step 8 — SOLUTION. Ten golden pairs, scored."""
from step6_router import route

GOLDEN = [
    ("What week is the RAG practical?",                        "logistics"),
    ("Is there a no-code session in week 3?",                  "logistics"),
    ("What date is the evals lecture?",                        "logistics"),
    ("When will I learn how to automate my job?",              "content"),
    ("Why does my model make things up?",                      "content"),
    ("What's the difference between a workflow and an agent?", "content"),
    # four more, including deliberately tricky ones:
    ("When do we cover hallucinations?",                       "logistics"),  # sounds like content, but "when" = schedule
    ("What did the tool calling lecture say about descriptions?", "content"), # names a session, but asks about ideas
    ("Which sessions are practicals for the code track?",      "logistics"),
    ("Explain the physics book story",                         "content"),
]

score = sum(route(q) == label for q, label in GOLDEN)
print(f"router accuracy: {score}/{len(GOLDEN)}")

# Run three times; the router is probabilistic and single runs lie.
# Then change one word of ROUTER_PROMPT and re-run: prompt engineering
# against a metric instead of against vibes.
