"""Step 0 — Reproduce the failure.

Before you fix a system, make it break on purpose, so you know your fix touched
the real problem. This script is SUPPOSED to end in a traceback. Read that
traceback carefully — it is the whole lesson.

Run:    python step0_break_it.py
Check:  python checks/check_step0.py
"""
import json

import requests
import tiktoken
from groq import Groq

enc = tiktoken.get_encoding("cl100k_base")


def fetch_hourly_history(lat, lon, start, end):
    """Hourly temperature and precipitation from Open-Meteo's free archive API."""
    r = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": lat,
            "longitude": lon,
            "start_date": start,
            "end_date": end,
            "hourly": "temperature_2m,precipitation",
            "timezone": "Asia/Kolkata",
        },
        timeout=60,
    )
    return r.json()


def count_tokens(text):
    """How big is this payload in the model's units?"""
    return len(enc.encode(text))


if __name__ == "__main__":
    # Ten years. All of it. The corpus is bigger than any one query needs —
    # that is deliberate (see the README callout).
    data = fetch_hourly_history(12.97, 77.59, "2016-01-01", "2025-12-31")
    payload = json.dumps(data)
    print(f"{len(payload):,} chars, ~{count_tokens(payload):,} tokens")

    # Predict the error code before you press enter. Then run it.
    wedding_query = (
        "My sister's wedding is in Bengaluru this August. From the last ten "
        "years of data, which weekend is least likely to rain?"
    )

    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Answer only from the data provided."},
            {"role": "user", "content": wedding_query + " DATA: " + payload},
        ],
    )
    print(response.choices[0].message.content)
