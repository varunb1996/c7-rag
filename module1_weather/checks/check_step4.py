"""Check step 4: the model actually calls your tool, and the loop survives it.

Makes LIVE API calls (needs GROQ_API_KEY). Costs fractions of a paisa.

Run from module1_weather/:  python checks/check_step4.py
"""
from _util import done, fail, ok  # noqa: F401

import step4_toolcall

# Wrap the tool so we can prove the model routed through it (retrieval),
# rather than answering from thin air.
calls = []
real_tool = step4_toolcall.get_weather_history


def spy(*args, **kwargs):
    calls.append(kwargs or args)
    return real_tool(*args, **kwargs)


step4_toolcall.get_weather_history = spy

print("Asking: 'How much did it rain in Bengaluru on 15 August 2019?' (live call)...")
try:
    answer = step4_toolcall.keyword_answer(
        "How much did it rain in Bengaluru on 15 August 2019?"
    )
except NotImplementedError:
    fail("the agent loop body is not implemented yet (TODO 2)")

if not calls:
    fail("the model never called get_weather_history",
         "check your TOOLS schema — a vague description or wrong parameter names "
         "and the model won't reach for the tool")
ok(f"model called the tool with {calls[0]}")

if not (isinstance(answer, str) and answer.strip()):
    fail(f"keyword_answer returned {answer!r} instead of a text answer",
         "after the tool message is appended, the loop must go around again "
         "so the model can generate from the tool output")
ok("loop completed: retrieval -> augmentation -> generation")
print(f"\n  Sage says nothing here — this is WeatherRAG's answer:\n  {answer.strip()[:300]}")

print("\nNow run the wedding query yourself: python step4_toolcall.py")
done("Step 4")
