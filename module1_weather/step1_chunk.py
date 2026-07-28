"""Step 1 — Chunking is a for loop.

One chunk per year, one JSON file per chunk. That is the whole technique.

Run:    python step1_chunk.py      (10 fetches — takes a minute or two)
Check:  python checks/check_step1.py
"""
import json
import os

from step0_break_it import fetch_hourly_history

os.makedirs("chunks", exist_ok=True)

for year in range(2016, 2026):
    data = fetch_hourly_history(12.97, 77.59, f"{year}-01-01", f"{year}-12-31")
    path = f"chunks/bengaluru_{year}.json"
    with open(path, "w") as f:
        json.dump(data, f)
    print(path)
