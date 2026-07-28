"""Check step 3: the filter is correct AND the aggregation is lossless.

Run from module1_weather/:  python checks/check_step3.py
"""
import json

import tiktoken

from _util import MODULE_ROOT, done, fail, ok  # noqa: F401

from step3_retrieve import get_weather_history

# --- the wedding query's retrieval ---------------------------------------
result = get_weather_history("Bengaluru", "2016-01-01", "2025-12-31", month=8)

if len(result) != 310:
    fail(f"August filter returned {len(result)} days, expected 310 (31 days x 10 years)",
         "check your month filter and your date-range comparisons")
ok("310 August days across 10 years")

if not all(d["date"][5:7] == "08" for d in result):
    fail("some returned days are not in August", "month lives at day[5:7]")
ok("every returned day is an August day")

dates = [d["date"] for d in result]
if dates != sorted(dates):
    fail("days are not sorted by date")
ok("days come back sorted")

if not all(set(d) == {"date", "rain_mm", "t_max"} for d in result):
    fail(f"each day should have exactly date, rain_mm, t_max — got {sorted(result[0])}")
ok("each day is {date, rain_mm, t_max} — conclusion-ready, not raw records")

# --- case-insensitive city match ------------------------------------------
if len(get_weather_history("bengaluru", "2019-01-01", "2019-12-31")) != 365:
    fail("lowercase 'bengaluru' returned nothing or the wrong count",
         "compare cities case-insensitively")
ok("city match is case-insensitive; full 2019 has 365 days")

# --- THE LOSSLESS CHECK: recompute one day straight from the raw chunk -----
day = "2019-08-15"
hours = json.load(open(MODULE_ROOT / "chunks" / "bengaluru_2019.json"))["hourly"]
raw_rain = sum(
    (r or 0.0)
    for t, r in zip(hours["time"], hours["precipitation"])
    if t.startswith(day)
)
raw_tmax = max(
    t2 for t, t2 in zip(hours["time"], hours["temperature_2m"]) if t.startswith(day)
)
yours = next(d for d in result if d["date"] == day)
if abs(yours["rain_mm"] - raw_rain) > 0.5:
    fail(f"{day}: your rain_mm={yours['rain_mm']}, raw hourly data sums to {raw_rain:.1f}",
         "are you ADDING each hour's rain (None counts as 0.0)?")
if yours["t_max"] != raw_tmax:
    fail(f"{day}: your t_max={yours['t_max']}, raw hourly max is {raw_tmax}",
         "t_max starts as None — take the max of what you've seen, don't sum")
ok(f"{day} recomputed from raw hourly data matches your daily summary — "
   "the aggregation is LOSSLESS for this query")

# --- the number that answers step 0 ----------------------------------------
enc = tiktoken.get_encoding("cl100k_base")
tokens = len(enc.encode(json.dumps(result)))
if tokens > 25_000:
    fail(f"payload is {tokens:,} tokens — too big; are you returning hourly rows?")
ok(f"payload is ~{tokens:,} tokens. Step 0 needed ~600,000. Same question, same answer.")

done("Step 3")
