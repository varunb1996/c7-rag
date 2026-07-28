# Build RAG From First Principles — Interactive Exercises

Hands-on companion to the **"Now Build the RAG"** practical (100xEngineers · LLM Deep Dive · Code Track).

This is not a reading track. You will build two small, real RAG systems by typing every
important line yourself, running it, watching it fail on schedule, and fixing it.

## The one rule

> Every line of code here is a whiteboard box made executable. Chunking is a for loop.
> The index is a list of dictionaries. Metadata filtering is a comparison inside that loop.
> The router is a system prompt that returns one word. An embedding is a list of numbers.
> Cosine similarity is a dot product.
>
> **If any part of your pipeline ever feels like magic, stop and re-derive it. Do not copy-paste forward.**

## Two systems, kept deliberately separate

The live lecture wove two examples together. Here they are two independent builds, because
each teaches a different half of RAG in its own domain:

| Module | System | What it teaches |
|---|---|---|
| [`module1_weather/`](module1_weather/) | **WeatherRAG** — ten years of Bengaluru weather | The **structured / keyword path**: token limits, chunking, an index, metadata filtering, pre-aggregation, tool calling |
| [`module2_sage/`](module2_sage/) | **Sage** — the support bot for the 100x Applied AI cohort | The **semantic path**: embeddings, cosine similarity, top-k search, honest misses — plus a router, a full pipeline, and your first eval |

Do them **in order**. Module 2 assumes you have felt Module 1's failure with your own eyes.

## How each exercise works

Every step follows the same loop:

1. **Read** the step's section in the module README — concept first, always from first principles.
2. **Open** the matching `stepN_*.py` starter file. The plumbing is written; the *ideas* are
   `TODO`s. You write those lines.
3. **Run** the file from the module directory: `python step1_chunk.py`.
4. **Check** yourself: `python checks/check_step1.py`. Green means move on. Red means the
   check just taught you something — read its message.
5. Only then read the next section.

Some steps are *supposed* to fail (step 0 of Module 1 ends in a traceback — that traceback
is the lesson). The README tells you what you should see before you run.

Stuck for more than ~20 minutes on one TODO? Read the matching file in [`solutions/`](solutions/),
then **close it and retype the idea from memory**. Copying a solution you haven't re-derived
is how magic gets back into your pipeline.

## Setup (once)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="gsk_..."   # same key as the weather/tool-calling practical
python check_setup.py           # verifies everything before you start
```

What each library is for, so nothing arrives as magic:

- `groq` — the LLM API (same model as the tool-calling practical: `llama-3.1-8b-instant`, 128K window)
- `requests` — fetching the weather corpus from Open-Meteo's free archive API
- `tiktoken` — counting tokens, so context failures become predictable numbers instead of surprises
- `numpy` — multiplying vectors (Module 2)
- `sentence-transformers` — a small **local** embedding model, so the semantic path costs you nothing while you learn it

## Time budget

- Module 1: ~60 minutes from empty folder to a tool-calling weather RAG
- Module 2: ~75 minutes from first embedding to a routed, evaluated Sage

## When you finish

Point the machinery at your own use case: your documents in the corpus, your metadata
fields in the index, your filters in the tool, your golden pairs in the eval. The scaffolding
should peel away in under an hour; if it does not, find the coupling and remove it.
