"""Step 4 — Wiring it into the three layers.

Character-for-character the pattern from the tool-calling practical. The only
novelty is psychological: you now know this tool is a RAG system, because its
output used to be too big and no longer is.

Run:    python step4_toolcall.py
Check:  python checks/check_step4.py     (makes live API calls)
"""
import json

from groq import Groq

from step3_retrieve import get_weather_history

client = Groq()

# TODO(1): THE TOOL SCHEMA. Describe get_weather_history to the model.
# Fill in the "function" dict:
#   name        — "get_weather_history"
#   description — say what it returns AND what the optional month does; the
#                 model reads this description to decide when to call you.
#   parameters  — JSON schema: city (string), start_date (string, "YYYY-MM-DD"),
#                 end_date (string, "YYYY-MM-DD"), month (optional — and because
#                 models often emit "month": null, give it type
#                 ["integer", "null"], not plain "integer"; the API validates
#                 the model's arguments against your schema).
#                 required: city, start_date, end_date.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_history",
            "description": (
                "Returns daily rain totals (mm) and max temperature for a city "
                "between two dates, from ten years of historical Bengaluru "
                "weather data. Pass month (1-12) to keep only that month across "
                "the date range, e.g. every August across all ten years."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. Bengaluru"},
                    "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "month": {
                        "type": ["integer", "null"],
                        "description": "Optional month 1-12 to filter to across the date range",
                    },
                },
                "required": ["city", "start_date", "end_date"],
            },
        },
    }
]


def keyword_answer(query):
    messages = [
        {
            "role": "system",
            "content": "Use the tool for any historical weather question. "
            "Answer only from tool output.",
        },
        {"role": "user", "content": query},
    ]
    while True:
        # Note the model change: 8B stays accurate for routing and plain
        # generation, but it garbles tool-call syntax often enough to hurt.
        # "The smallest model that stays accurate" is a PER-JOB decision.
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages, tools=TOOLS
        )
        msg = resp.choices[0].message
        if not msg.tool_calls:
            return msg.content  # generation

        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = get_weather_history(**args)  # retrieval
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),  # augmentation
                }
            )


if __name__ == "__main__":
    print(
        keyword_answer(
            "My sister's wedding is in Bengaluru this August. From the last ten "
            "years of data, which weekend is least likely to rain?"
        )
    )
    # The query that produced a 600,000-token traceback in step 0 now comes
    # back with a weekend recommendation grounded in 310 real data points.
    # Find the three letters R, A, G in the loop above before moving on.
