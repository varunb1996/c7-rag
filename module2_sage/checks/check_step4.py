"""Check step 4: the semantic path answers, and the guardrail sentence exists.

Makes LIVE API calls (needs GROQ_API_KEY).

Run from module2_sage/:  python checks/check_step4.py
"""
from _util import done, fail, ok  # noqa: F401

import step4_generate
from step4_generate import SAGE_SYSTEM, sage_answer

if not isinstance(SAGE_SYSTEM, str) or len(SAGE_SYSTEM) < 20:
    fail("SAGE_SYSTEM isn't written yet")

lowered = SAGE_SYSTEM.lower()
if "context" not in lowered:
    fail("the system prompt never mentions the context",
         "sentence 1: answer only from the provided context")
if not any(phrase in lowered for phrase in ("say so", "say that", "admit", "not there", "not in the context", "doesn't contain", "does not contain")):
    fail("the honest-miss guardrail is missing from SAGE_SYSTEM",
         'the load-bearing sentence: "If the answer is not there, say so."')
ok("system prompt has both sentences — including the honest-miss guardrail")

print("Asking an in-corpus question (live call)...")
ans = sage_answer("Why does my model make things up?")
if not (isinstance(ans, str) and len(ans.strip()) > 40):
    fail(f"sage_answer returned {ans!r}")
ok("grounded answer returned for an in-corpus question")
print(f"\n  Sage: {ans.strip()[:250]}...\n")

print("Asking an OUT-of-corpus question (live call)...")
miss = sage_answer("What is the refund policy for the cohort?")
ok("now YOU judge this one — the check can't do it for you:")
print(f"\n  Sage: {miss.strip()[:400]}\n")
print("  Did Sage admit the context doesn't cover refunds (honest miss),")
print("  or did it synthesize a policy from near-miss chunks (hallucination")
print("  with citations)? If it hallucinated: tighten SAGE_SYSTEM and re-run.")

done("Step 4")
