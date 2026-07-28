"""Step 2 — The index is a list of dictionaries.

The chunks exist, but nothing knows what lives where. The physics book needs
its index page. Ours is ten dicts of metadata: data about the data.

Run:    python step2_index.py
Check:  python checks/check_step2.py
"""
import json

# TODO: build `index` as a list comprehension — one dict per year 2016..2025,
# with exactly these fields:
#
#   chunk_id     — f"bengaluru_{year}"
#   city         — "Bengaluru"
#   country      — "India"
#   year         — the int year
#   granularity  — "hourly"
#   variables    — ["temperature_2m", "precipitation"]
#   path         — f"chunks/bengaluru_{year}.json"
#
# These fields are the Amazon left rail for your corpus: everything a future
# filter might want to narrow on, written down at ingestion time.
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

# Now open index.json in your editor and LOOK at it. The whole file is smaller
# than one hour of raw data — and it is the only thing the system will consult
# before deciding what to load.
