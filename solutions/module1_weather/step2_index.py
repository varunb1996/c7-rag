"""Step 2 — SOLUTION. The index is a list of dictionaries."""
import json

index = [
    {
        "chunk_id": f"bengaluru_{year}",
        "city": "Bengaluru",
        "country": "India",
        "year": year,
        "granularity": "hourly",
        "variables": ["temperature_2m", "precipitation"],
        "path": f"chunks/bengaluru_{year}.json",
    }
    for year in range(2016, 2026)
]

json.dump(index, open("index.json", "w"), indent=2)
print(f"wrote index.json with {len(index)} entries")
