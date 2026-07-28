"""Check step 7: one entry point, two paths, both reachable.

Makes LIVE API calls (needs GROQ_API_KEY).

Run from module2_sage/:  python checks/check_step7.py
"""
from _util import done, fail, ok  # noqa: F401

import step7_pipeline

taken = []


def spy_logistics(q):
    taken.append("logistics")
    return step7_pipeline.__dict__["_real_logistics"](q)


def spy_semantic(q):
    taken.append("content")
    return step7_pipeline.__dict__["_real_semantic"](q)


step7_pipeline._real_logistics = step7_pipeline.logistics_answer
step7_pipeline._real_semantic = step7_pipeline.sage_answer
step7_pipeline.logistics_answer = spy_logistics
step7_pipeline.sage_answer = spy_semantic

print("Query 1: 'What week is the RAG practical?' (live)...")
a1 = step7_pipeline.rag("What week is the RAG practical?")
print("Query 2: 'When will I learn how to automate my job?' (live)...")
a2 = step7_pipeline.rag("When will I learn how to automate my job?")

if taken != ["logistics", "content"]:
    fail(f"paths taken were {taken}, expected ['logistics', 'content']",
         "rag() must branch on route(query) and call the matching path — "
         "if the paths are right but flipped, the bug is in step6's prompt")
ok("router sent the schedule question left and the meaning question right")

for name, a in (("schedule", a1), ("semantic", a2)):
    if not (isinstance(a, str) and a.strip()):
        fail(f"the {name} path returned {a!r}")
ok("both paths end in a generated answer — R, A, G on each side")

print(f"\n  logistics path: {a1.strip()[:160]}")
print(f"  semantic path : {a2.strip()[:160]}")
print("\nNow the real exercise: python step7_pipeline.py — and break it five ways.")
done("Step 7")
