"""Step 1 — SOLUTION. Chunking is a for loop."""
import json
import os

from step0_break_it import fetch_hourly_history

os.makedirs("chunks", exist_ok=True)

# The chunking DECISION hides in the loop header: range(2016, 2026) splits the
# corpus at a calendar seam. Free for weather; a research field for PDFs.
for year in range(2016, 2026):
    data = fetch_hourly_history(12.97, 77.59, f"{year}-01-01", f"{year}-12-31")
    with open(f"chunks/bengaluru_{year}.json", "w") as f:
        json.dump(data, f)
    print(f"wrote chunks/bengaluru_{year}.json")
