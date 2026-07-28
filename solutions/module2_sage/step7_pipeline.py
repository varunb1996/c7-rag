"""Step 7 — SOLUTION. The whole machine."""
from step4_generate import sage_answer
from step5_schedule import logistics_answer
from step6_router import route


def rag(query):
    if route(query) == "logistics":
        return logistics_answer(query)  # cheap path, ~75% of traffic
    return sage_answer(query)  # semantic path: retrieval, augmentation, generation


if __name__ == "__main__":
    print("Sage — support bot for the 100x Applied AI cohort. Ctrl-C to exit.\n")
    while True:
        print(rag(input("Ask Sage: ")), "\n")
