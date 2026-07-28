"""Step 6 — The router: a receptionist in eleven lines.

The receptionist redirects; it never solves. It is a prompt, not a framework.

Run:    python step6_router.py
Check:  python checks/check_step6.py     (live API calls)
"""
import json

from groq import Groq

client = Groq()

# TODO(1): write the receptionist's job description YOURSELF. Requirements:
#   - classify into exactly one of two routes:
#       "logistics" — answerable by filtering the cohort schedule
#                     (weeks, dates, tracks, session titles)
#       "content"   — about ideas taught in the course, advice, meaning,
#                     anything with no clean filter
#   - it must reply with JSON ONLY, e.g. {"route": "logistics"}
#     (that constraint is what stops it wandering off and trying to answer)
# Keep it under ~8 lines. You classified 100 query pairs for homework —
# this prompt is that judgment, codified.
ROUTER_PROMPT = """You are a routing receptionist. You never answer the query
yourself — you only classify it into exactly one route.

- "logistics": answerable by filtering the cohort schedule on week, date,
  track, or session topics (a clean filter exists).
- "content": about ideas, meaning, or advice from the course, with no clean
  filter to apply.

Reply with JSON ONLY, e.g. {"route": "logistics"} or {"route": "content"}.
No other text."""

def route(query):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": query},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)["route"]


if __name__ == "__main__":
    for q in [
        "What week is the RAG practical?",           # clean filter -> logistics
        "When will I learn how to automate my job?", # no filter    -> content
        "Is there a no-code session in week 3?",     # logistics
        "Why does my model make things up?",         # content
    ]:
        print(f"{route(q):>10}  <-  {q}")
