"""Step 5 — SOLUTION. Sage's keyword path: the schedule tool."""
import json

from groq import Groq

client = Groq()

SESSIONS = json.load(open("data/sessions.json"))


def get_sessions(week=None, track=None, topic=None):
    """Filter the cohort schedule."""
    return [
        s
        for s in SESSIONS
        if (week is None or s["week"] == week)
        and (track is None or s["track"] in (track, "both"))
        and (topic is None or topic in s["topics"])
    ]


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_sessions",
            "description": "Look up sessions in the 100x Applied AI cohort "
            "schedule. Filter by week number, track ('code' or 'no-code'), "
            "and/or topic tag (e.g. 'rag', 'prompting', 'tool-calling', "
            "'evals'). All filters optional; returns matching sessions with "
            "week, date, title, type and track.",
            "parameters": {
                "type": "object",
                "properties": {
                    # all optional -> all nullable: models often emit null for
                    # filters they don't need, and the API validates against
                    # this schema
                    "week": {"type": ["integer", "null"]},
                    "track": {"type": ["string", "null"],
                              "description": "'code' or 'no-code'"},
                    "topic": {"type": ["string", "null"]},
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
        # tool calling runs on the 70B model — 8B doesn't stay accurate
        # at tool-call syntax
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
    print(json.dumps(get_sessions(week=4), indent=2))
    print(logistics_answer("What week is the RAG practical, and what date for the code track?"))
