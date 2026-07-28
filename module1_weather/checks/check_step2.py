"""Check step 2: index.json is small, complete, and points at real files.

Run from module1_weather/:  python checks/check_step2.py
"""
import json

from _util import MODULE_ROOT, done, fail, ok

index_path = MODULE_ROOT / "index.json"
if not index_path.exists():
    fail("no index.json", "run: python step2_index.py")

index = json.loads(index_path.read_text())
if not isinstance(index, list) or len(index) != 10:
    fail(f"expected a list of 10 entries, got {type(index).__name__} "
         f"of length {len(index) if isinstance(index, list) else '?'}")
ok("index is a list of 10 dictionaries")

REQUIRED = {"chunk_id", "city", "country", "year", "granularity", "variables", "path"}
for entry in index:
    missing = REQUIRED - set(entry)
    if missing:
        fail(f"entry {entry.get('chunk_id', '?')} is missing fields: {sorted(missing)}")
    if not (MODULE_ROOT / entry["path"]).exists():
        fail(f"entry {entry['chunk_id']} points at {entry['path']}, which doesn't exist")
    if not isinstance(entry["year"], int):
        fail(f"'year' should be an int (you'll compare it numerically in step 3), "
             f"got {type(entry['year']).__name__}")
ok("every entry has all 7 metadata fields and points at a real chunk file")

years = sorted(e["year"] for e in index)
if years != list(range(2016, 2026)):
    fail(f"years are {years}, expected 2016..2025")
ok("years cover 2016–2025 exactly")

index_size = index_path.stat().st_size
corpus_size = sum(f.stat().st_size for f in (MODULE_ROOT / "chunks").glob("*.json"))
ok(f"index is {index_size:,} bytes; the corpus it describes is {corpus_size:,} — "
   f"{corpus_size // max(index_size, 1):,}x bigger")

print("\nThis ratio is the two-tier move: reason over the small thing,")
print("load only the winning slice of the big thing.")
done("Step 2")
