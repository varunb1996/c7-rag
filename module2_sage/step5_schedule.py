"""Step 5 — Sage's keyword path: the schedule tool.

"What week is the RAG practical?" needs no embeddings. It's Module 1's
metadata filter in a new domain — and rebuilding it should take you about
sixty seconds. That speed is the point.

Run:    python step5_schedule.py
Check:  python checks/check_step5.py
"""
import json

from groq import Groq

client = Groq()

SESSIONS = json.load(open("data/sessions.json"))


def get_sessions(week=None, track=None, topic=None):
    """Filter the cohort schedule.

    week  — int, keep only that week
    track — "code" or "no-code"; sessions marked "both" always match
    topic — keep sessions whose topics list contains it, e.g. "rag"
    """
    return [
        s
        for s in SESSIONS
        if (week is None or s["week"] == week)
        and (track is None or s["track"] in (track, "both"))
        and (topic is None or topic in s["topics"])
    ]


# --- the same three layers you wired in Module 1 ---------------------------

# TODO(2): the tool schema. You wrote one of these for the weather tool;
# write this one from memory. name "get_sessions"; all three parameters
# optional (week integer, track string, topic string); required: [].
# Make the description earn its keep — the model routes by reading it.
# Remember the lesson from the weather schema: optional parameters need
# nullable types (e.g. ["integer", "null"]) because models emit null for
# filters they don't use, and the API validates against your schema.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_sessions",
            "description": (
                "Filters the 100x Applied AI cohort schedule. Returns sessions "
                "matching any combination of week number, track, and topic. "
                "Use for any question about session dates, weeks, tracks, or topics."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "week": {
                        "type": ["integer", "null"],
                        "description": "Week number to filter to, e.g. 4",
                    },
                    "track": {
                        "type": ["string", "null"],
                        "description": "'code' or 'no-code'; sessions marked 'both' always match",
                    },
                    "topic": {
                        "type": ["string", "null"],
                        "description": "Topic to filter to, e.g. 'rag'",
                    },
                },
                "required": [],
            },
        },
    }
]


def logistics_answer(query):
    messages = [
        {
            "role": "system",
            "content": "You answer questions about the 100x Applied AI cohort "
            "schedule. Use the tool. Answer only from tool output.",
        },
        {"role": "user", "content": query},
    ]
    while True:
        # tool calling runs on the 70B model — same lesson as Module 1:
        # "smallest model that stays accurate" is decided per job, and 8B
        # doesn't stay accurate at tool-call syntax
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages, tools=TOOLS
        )
        msg = resp.choices[0].message
        if not msg.tool_calls:
            return msg.content
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = get_sessions(**args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),
                }
            )


if __name__ == "__main__":
    # Filter by hand first — no LLM anywhere:
    print(json.dumps(get_sessions(week=4), indent=2))
    # Then through the three layers:
    print(logistics_answer("What week is the RAG practical, and what date for the code track?"))
