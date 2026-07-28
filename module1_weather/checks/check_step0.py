"""Check step 0. Verifies your fetch + token counting WITHOUT re-running the
doomed request. (The doomed request's traceback was the point — this check
assumes you already watched it fail.)

Run from module1_weather/:  python checks/check_step0.py
"""
from _util import MODULE_ROOT, done, fail, ok  # noqa: F401  (sets sys.path)

try:
    from step0_break_it import count_tokens, fetch_hourly_history
except NotImplementedError:
    fail("step0_break_it.py raised NotImplementedError on import",
         "keep the doomed request under `if __name__ == '__main__':` so imports stay safe")

print("Fetching one small week from Open-Meteo to test your params...")
data = fetch_hourly_history(12.97, 77.59, "2024-08-01", "2024-08-07")

if "hourly" not in data:
    fail(f"API response has no 'hourly' key. Got keys: {list(data.keys())}",
         "check your params dict — the API tells you what it didn't like in data['reason']")
ok("'hourly' key present")

hours = data["hourly"]
for key in ("time", "temperature_2m", "precipitation"):
    if key not in hours:
        fail(f"hourly data missing '{key}'",
             'hourly must be "temperature_2m,precipitation"')
ok("temperature_2m and precipitation both present")

n = len(hours["time"])
if n != 7 * 24:
    fail(f"expected {7*24} hourly timestamps for one week, got {n}")
ok(f"{n} hourly timestamps for 7 days — granularity is right")

try:
    t = count_tokens("retrieval augmented generation")
except NotImplementedError:
    fail("count_tokens is not implemented yet")
if not isinstance(t, int) or not 2 <= t <= 8:
    fail(f"count_tokens('retrieval augmented generation') returned {t!r}",
         "return len(enc.encode(text))")
ok(f"count_tokens works ({t} tokens)")

print("\nOne more thing — answer out loud before moving on:")
print("  At which of the three R-A-G stages did step 0's traceback fire, and how do you know?")
done("Step 0")
