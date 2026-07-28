"""Check step 1: the chunks exist, one per year, each one small enough to matter.

Run from module1_weather/:  python checks/check_step1.py
"""
import json

from _util import MODULE_ROOT, done, fail, ok

chunk_dir = MODULE_ROOT / "chunks"
if not chunk_dir.is_dir():
    fail("no chunks/ directory", "run: python step1_chunk.py")

total_bytes = 0
for year in range(2016, 2026):
    path = chunk_dir / f"bengaluru_{year}.json"
    if not path.exists():
        fail(f"missing {path.name}", "the loop should cover range(2016, 2026)")
    data = json.loads(path.read_text())
    times = data.get("hourly", {}).get("time", [])
    if not times:
        fail(f"{path.name} has no hourly.time data",
             "did the fetch for this year succeed? re-run step1")
    if not times[0].startswith(str(year)):
        fail(f"{path.name} starts at {times[0]} — wrong year inside the file",
             "check the start/end dates you pass for each year")
    total_bytes += path.stat().st_size
ok("10 chunk files, 2016–2025, each containing its own year")

one_chunk = (chunk_dir / "bengaluru_2020.json").stat().st_size
if not one_chunk < total_bytes / 5:
    fail("chunks look suspiciously uniform in the wrong way")
ok(f"corpus is {total_bytes/1e6:.1f} MB total; one chunk is ~{one_chunk/1e6:.1f} MB — "
   "a query that needs one year now loads a tenth of the corpus")

print("\nAnswer out loud: what was the chunking DECISION here, and why was it free")
print("for weather data but a research problem for 10,000 insurance PDFs?")
done("Step 1")
