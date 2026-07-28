"""Step 4 — SOLUTION. Generation, and the honest miss."""
from groq import Groq

from step3_search import semantic_search

client = Groq()

SAGE_SYSTEM = (
    "Answer only from the context. If the answer is not there, say so."
)


def sage_answer(query):
    chunks = semantic_search(query)  # retrieval
    context = "\n\n".join(text for _, _, text in chunks)  # augmentation
    resp = client.chat.completions.create(  # generation
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SAGE_SYSTEM},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION: {query}"},
        ],
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    print("— in-corpus question —")
    print(sage_answer("Why does my model make things up?"))

    print("\n— OUT-of-corpus question (watch for the honest miss) —")
    print(sage_answer("What is the refund policy for the cohort?"))
