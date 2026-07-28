"""Step 4 — SOLUTION. The three layers, with the new tool behind the socket."""
import json

from groq import Groq

from step3_retrieve import get_weather_history

client = Groq()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_history",
            "description": "Daily weather summaries for a city between two "
            "dates. Optional month (1-12) keeps only that month across the "
            "range, e.g. every August of the last ten years.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                    # optional params must allow null: models often emit
                    # "month": null, and Groq validates against this schema
                    "month": {"type": ["integer", "null"]},
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
        # 8B garbles tool-call syntax often; tool calling gets the 70B model.
        # "The smallest model that stays accurate" is a per-job decision.
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages, tools=TOOLS
        )
        msg = resp.choices[0].message
        if not msg.tool_calls:
            return msg.content  # generation
        messages.append(msg)
        for call in msg.tool_calls:  # the execution environment, i.e. you
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
