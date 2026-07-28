"""Step 4 — Generation, and the honest miss.

The retriever will ALWAYS return something. This step is about what saves you
when "something" isn't an answer.

Run:    python step4_generate.py
Check:  python checks/check_step4.py     (live API calls)
"""
from groq import Groq

from step3_search import semantic_search

client = Groq()

# TODO(1): write the system prompt. Two sentences:
#   - answer only from the provided context
#   - if the answer is not in the context, SAY SO
# That second sentence is your entire first line of defense against
# hallucination-with-citations. Do not skip it.
SAGE_SYSTEM = (
    "Answer only using the provided context. "
    "If the answer is not there, say so — do not guess or make anything up."
)


def sage_answer(query):
    """Retrieve -> augment -> generate. The semantic path, end to end."""
    chunks = semantic_search(query)  # retrieval
    context = "\n\n".join(text for _id, _score, text in chunks)  # augmentation

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SAGE_SYSTEM},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION: {query}"},
        ],
    )
    return response.choices[0].message.content  # generation


if __name__ == "__main__":
    print("— in-corpus question —")
    print(sage_answer("Why does my model make things up?"))

    print("\n— OUT-of-corpus question (watch for the honest miss) —")
    print(sage_answer("What is the refund policy for the cohort?"))
    # The retriever still returned three chunks for that second question —
    # the most similar chunks THAT EXIST. Similarity is not correctness.
    # If Sage admitted the context doesn't cover refunds: that's an honest
    # miss. Log those. They are the exact list of docs your corpus is missing.
