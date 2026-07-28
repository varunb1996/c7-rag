# Module 2 — Sage: The Semantic Path

Sage is the support bot for the **100x Applied AI cohort**. Its corpus is the course
itself: the post-read notes of past lectures (in `data/notes/`) and the cohort schedule
(in `data/sessions.json`). No weather anywhere — this is a different system with a
different corpus, on purpose.

Sage's driving question is the one that killed it in production:

> *"When will I learn how to automate my job?"*

Look at that query the way Module 1 taught you to. **No city. No date. No field to filter
on.** The keyword machinery you built in Module 1 has nothing to grab. The query is about
*meaning* — and meaning needs a different retrieval mechanism.

But not every Sage query is like that. *"What week is the RAG practical?"* has a clean
filter (week, topic, track — it's the weather query wearing a hoodie). Real traffic splits
roughly **75% filterable / 25% semantic**, and paying embedding prices for filterable
questions is the $1,000-invoice mistake. So Sage gets both paths and a **router** in front.

Work from this directory:

```bash
cd module2_sage
```

---

## Step 1 — An embedding is a list of numbers

**File:** `step1_embed.py` · **Check:** `python checks/check_step1.py`

**Concept.** An embedding model maps text to a vector such that texts with similar
*meaning* land near each other. Meaning becomes geometry; "find related text" becomes
"find nearby points". Tonight's model is `all-MiniLM-L6-v2`: 384 dimensions, free, runs
on your laptop CPU. (OpenAI's `text-embedding-3-large` uses 3,072 — more ways to
distinguish meanings, same object.)

**Your task.** Implement `embed(texts)` — encode with the model, normalized. Then run the
file and **stare at the printed vector**. That wall of floats is the whole mystique of
embeddings, demystified by `print`.

**What you should see.** "A cat sat on the mat" scores high against "A kitten rested on
the rug" and low against "The stock market fell sharply today" — despite the first pair
sharing almost no words. *That* is the thing keyword search structurally cannot do.

---

## Step 2 — Cosine similarity is a dot product

**File:** `step2_cosine.py` · **Check:** `python checks/check_step2.py`

**Concept.** Similarity is the cosine of the angle between two vectors. The blog-post
formula has a fraction in it: dot product over the product of the lengths. But if every
vector is already normalized to length 1, the denominator is 1 — and the whole formula
collapses to a dot product.

**Your task.** Pure numpy, no model, no API: implement `cosine_full` (the fraction) and
`cosine_normalized` (the dot product), then prove to yourself they agree.

**Stop and think.** This step exists so that when a vector-store product shows you a
"similarity score", you can say exactly what arithmetic produced it. Never operate magic
you cannot price.

---

## Step 3 — Semantic search over the course notes

**File:** `step3_search.py` · **Check:** `python checks/check_step3.py`

**Concept.** Load the six course notes, embed them once into a matrix. Search is then one
line: `matrix @ q` scores every chunk against the query simultaneously. For a corpus of
hundreds or thousands of chunks, **that matrix in RAM is your vector database** — faster
than a network hop to a managed one. Pinecone and friends earn their place when the array
outgrows memory or needs many writers. Reach for them at that boundary, not before.

**Your task.** Build the corpus, build the matrix, implement `semantic_search(query, k=3)`.

**What you should see.** Ask the Sage-killer — *"When will I learn how to automate my
job?"* — and the top chunk is the workflows-and-agents note, even though the query shares
almost no keywords with it. You just did the impossible-for-grep thing in ~20 lines on a CPU.

---

## Step 4 — Generation, and the honest miss

**File:** `step4_generate.py` · **Check:** `python checks/check_step4.py` *(live API calls)*

**Concept.** Retrieval will **always return something** — the most similar chunks that
exist — even when no chunk actually answers the question. Similarity is not correctness.
Without a guardrail, the model happily synthesizes an answer from near-miss context:
hallucination with citations.

**Your task.** Implement `sage_answer(query)`: retrieve top chunks, join them into a
context block, and generate — with the one-sentence guardrail in the system prompt:
**"If the answer is not there, say so."**

**What you should see.** Run both test queries. The in-corpus one gets a grounded answer.
The out-of-corpus one (*"What is the refund policy?"*) should get an **honest miss** — and
your log of honest misses is precisely the list of documents your corpus is missing.

---

## Step 5 — Sage's keyword path: the schedule tool

**File:** `step5_schedule.py` · **Check:** `python checks/check_step5.py`

**Concept.** *"What week is the RAG practical?"* needs no embeddings — `data/sessions.json`
has `week`, `track`, `type`, `topics` fields. This is Module 1's metadata filter, rebuilt
in sixty seconds in a new domain. That speed is the point: the structured path is always
cheap to build, which is why you build it **first** and let embeddings handle only the residue.

**Your task.** Implement `get_sessions(week, track, topic)` — a filter over a list of
dicts — then wire it into the same three-layer tool-calling loop you wrote in Module 1.

---

## Step 6 — The router: a receptionist in eleven lines

**File:** `step6_router.py` · **Check:** `python checks/check_step6.py` *(live API calls)*

**Concept.** A receptionist in front whose only job is to redirect — it never answers.
It is a prompt, not a framework, and the constraint that makes it reliable is that it may
only reply with one JSON object, so it cannot wander off and try to solve the query. It
costs one cheap call, and it protects the invoice: everything routed to `logistics` runs
on filters that cost approximately nothing; only the residue pays for embeddings.

**Your task.** Write `ROUTER_PROMPT` yourself (the two routes are `"logistics"` and
`"content"`), and implement `route(query)` with `response_format={"type": "json_object"}`.

---

## Step 7 — The whole machine

**File:** `step7_pipeline.py` · **Check:** `python checks/check_step7.py` *(live API calls)*

**Concept.** One entry point, one router decision, two paths — and both paths end at the
same three letters: retrieve, augment, generate.

**Your task.** Implement `rag(query)`: route, then branch to the schedule path or the
semantic path.

**Then interrogate it.** Ask the automate-my-job query, the what-week-is-X query, the
why-does-it-hallucinate query — and at least five questions *designed to make it fail*.
For every wrong answer, name the failure class:

| Failure class | What broke | The fix lives in |
|---|---|---|
| Wrong route | receptionist sent it down the wrong path | step 6's prompt |
| Wrong chunk | retrieval returned near-misses | corpus / chunking / k |
| Wrong generation | right context, bad answer | step 4's prompt |

Being able to *name which one you are looking at* is the debugging skill this module exists to build.

---

## Step 8 — Prove it: ten golden pairs

**File:** `step8_eval.py` · **Check:** `python checks/check_step8.py` *(live API calls)*

**Concept.** A working demo is not a working system; the difference is measurement. Ten
labeled query→route pairs are deliberately tiny — they are the embryo of the evals module.

**Your task.** Six golden pairs are given; write at least four more from queries *you*
asked in step 7. Implement the scorer. Then:

1. **Run it three times.** The router is probabilistic; single runs lie. Watch the number move.
2. **Change one word** of your router prompt and re-run. Did the score improve?

You are now doing prompt engineering against a metric instead of against vibes — which is
the entire posture of the evals module, in one loop.

---

## Done?

Swap the corpus. Your documents in `data/notes/`, your structured records in place of
`sessions.json`, your golden pairs in step 8. The Sage scaffolding should peel away in
under an hour; if it does not, find the coupling and remove it.
