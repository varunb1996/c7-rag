"""Step 0 — SOLUTION."""
import json

import requests
import tiktoken
from groq import Groq

enc = tiktoken.get_encoding("cl100k_base")


def fetch_hourly_history(lat, lon, start, end):
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
    return len(enc.encode(text))


if __name__ == "__main__":
    data = fetch_hourly_history(12.97, 77.59, "2016-01-01", "2025-12-31")
    payload = json.dumps(data)
    print(f"{len(payload):,} chars, ~{count_tokens(payload):,} tokens")

    client = Groq()
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Answer only from the data provided."},
            {
                "role": "user",
                "content": "My sister's wedding is in Bengaluru this August. "
                "From the last ten years of data, which weekend is least likely "
                "to rain? DATA: " + payload,
            },
        ],
    )
    # Never reached: the API raises an error whose code is
    # context_length_exceeded. Retrieval worked (data is in your variable),
    # your backend held it (no memory error) — the failure fires at the
    # boundary where the payload is handed to the model. Augmentation is the
    # bottleneck.
    print(resp.choices[0].message.content)
