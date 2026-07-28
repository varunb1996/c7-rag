"""Step 5 — SOLUTION. Measure the win."""
import glob
import json

import tiktoken

from step3_retrieve import get_weather_history

enc = tiktoken.get_encoding("cl100k_base")


def measure():
    """Return (naive_tokens, rag_tokens) for the wedding query."""
    chunks = [json.load(open(p)) for p in sorted(glob.glob("chunks/*.json"))]
    naive_tokens = len(enc.encode(json.dumps(chunks)))

    result = get_weather_history("Bengaluru", "2016-01-01", "2025-12-31", month=8)
    rag_tokens = len(enc.encode(json.dumps(result)))

    return naive_tokens, rag_tokens


if __name__ == "__main__":
    naive, rag = measure()
    print(f"naive payload : {naive:>9,} tokens   (step 0 — died at 128K)")
    print(f"rag payload   : {rag:>9,} tokens   (step 3 — fits with room to spare)")
    print(f"compression   : {naive / rag:,.0f}x, from a filter and a defaultdict")
