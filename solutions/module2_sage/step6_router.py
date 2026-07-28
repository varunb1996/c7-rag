"""Step 6 — SOLUTION. The router: a receptionist in eleven lines."""
import json

from groq import Groq

client = Groq()

ROUTER_PROMPT = """Classify the user query into exactly one route.
"logistics": answerable by filtering the cohort schedule on week, date, track, or session title.
"content": about ideas taught in the course, advice, meaning, or anything with no clean filter.
Reply with JSON only, e.g. {"route": "logistics"}"""


def route(query):
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": query},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)["route"]


if __name__ == "__main__":
    for q in [
        "What week is the RAG practical?",
        "When will I learn how to automate my job?",
        "Is there a no-code session in week 3?",
        "Why does my model make things up?",
    ]:
        print(f"{route(q):>10}  <-  {q}")
