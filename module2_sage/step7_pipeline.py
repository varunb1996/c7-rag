"""Step 7 — The whole machine.

One entry point, one router decision, two paths — and both paths end at the
same three letters.

Run:    python step7_pipeline.py     (interactive — interrogate it)
Check:  python checks/check_step7.py     (live API calls)
"""
from step4_generate import sage_answer
from step5_schedule import logistics_answer
from step6_router import route


def rag(query):
    if route(query) == "logistics":
        return logistics_answer(query)
    return sage_answer(query)


if __name__ == "__main__":
    print("Sage — support bot for the 100x Applied AI cohort. Ctrl-C to exit.")
    print("Interrogate it: schedule questions, concept questions, and at least")
    print("five questions DESIGNED to make it fail. For every wrong answer,")
    print("name the failure class: wrong route, wrong chunk, or wrong generation.\n")
    while True:
        print(rag(input("Ask Sage: ")), "\n")
