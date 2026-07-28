# Module 1 — WeatherRAG: The Structured Path

You will build a RAG system over **ten years of hourly Bengaluru weather**, and you will
build it backwards from a failure: first you make the naive approach die at the context
window, then every step after that is a direct response to the traceback you collected.

The driving question for the whole module:

> *"My sister's wedding is in Bengaluru this August. From the last ten years of data,
> which weekend is least likely to rain?"*

Work from this directory. For each step: read the section → fill the TODOs in the step
file → run it → run the check → move on.

```bash
cd module1_weather
```

---

## Step 0 — Reproduce the failure

**File:** `step0_break_it.py` · **Check:** `python checks/check_step0.py`

**Concept.** Rule for every system you will ever debug: before you fix it, make it break
on purpose, so you know your fix touched the real problem. The theory lecture predicted
the wedding query dies at the **augmentation** step — at one exact line, with one exact
error. Tonight you collect the evidence.

**Your task.** Three TODOs:
1. Complete the `params` dict for Open-Meteo's archive API (the free stand-in for
   OpenWeatherMap's paid history endpoint — the provider changed, not one principle did).
2. Implement `count_tokens` with tiktoken. You are about to need proof of a number.
3. Send the doomed request: all ten years of raw JSON, stuffed into one user message.

**What you should see.** Ten years of hourly readings is 87,648 timestamps. The print
lands **north of 600,000 tokens against a 128K window**, and the API returns an error whose
code is `context_length_exceeded`.

**Stop and think.** Read the traceback and notice three things:
- The *retrieval* worked — the data is sitting in your variable.
- Your backend held it without complaint — no memory error.
- The failure fired at the boundary where your code hands the payload to the model.

**Augmentation is the bottleneck.** Everything that follows is a response to this one traceback.

> **Why we ingest more than the query needs.** The wedding query only needs Augusts, but
> your app must serve queries you have not seen yet: hottest day of 2022, a birthday in
> March. So the corpus is the full ten years and *the query decides what gets loaded*.
> You never fix the corpus to fit the window; you fix what you *select* from it.

---

## Step 1 — Chunking is a for loop

**File:** `step1_chunk.py` · **Check:** `python checks/check_step1.py`

**Concept.** The generalized version of "split the ten years in two" is embarrassingly
small: one chunk per year, one JSON file per chunk. That is the whole technique.

**Your task.** Write the loop: for each year 2016–2025, fetch that year and write it to
`chunks/bengaluru_<year>.json`.

**Stop and think.** The decision is hidden in the loop header: `range(2016, 2026)` is a
*breakpoint choice*. Our data has a clean seam (the calendar), so the choice is free. An
insurance agent with 10,000 unstructured policy PDFs gets no free seam — that is why
chunking is a research field for documents and a one-liner for us. Enjoy the one-liner
and remember it is a special case.

---

## Step 2 — The index is a list of dictionaries

**File:** `step2_index.py` · **Check:** `python checks/check_step2.py`

**Concept.** The chunks exist, but nothing knows what lives where. The physics book needs
its index page. Ours is ten dictionaries, each carrying **metadata** — data about the
data — written down as fields.

**Your task.** Build the index as a list comprehension: one dict per year with
`chunk_id`, `city`, `country`, `year`, `granularity`, `variables`, `path`. Save as `index.json`.

**Stop and think.** Open `index.json` and look at it. The entire file is smaller than one
hour of raw data, and it is the *only* thing consulted before deciding what to load. This
is the two-tier move of the whole module: reason over the small structure, and only the
winning chunk ever approaches the context window.

---

## Step 3 — Metadata filtering: the retrieval tool itself

**File:** `step3_retrieve.py` · **Check:** `python checks/check_step3.py`

**Concept.** The tool's job description: filter the index on metadata, open **only** the
matching chunk files, keep only the matching days, hand back something small. Note what it
is *not* doing: no embeddings, no vectors, no GPU. This is the MVP rule, running.

**Your task.** Three TODOs inside `get_weather_history`:
1. The metadata filter — a list comprehension over the index (city match + year range).
2. The day filters — skip timestamps outside the date range or the requested month.
3. The aggregation — sum rain per day, track the max temperature.

**What you should see.** Run it by hand before wiring it to anything:

```python
get_weather_history("Bengaluru", "2016-01-01", "2025-12-31", month=8)
```

returns **310 daily summaries, roughly 12,000 tokens**. The 600,000-token monster from
Step 0 just became a payload that fits with room to spare — and nothing the wedding
question needs was lost.

> **The aggregation move, and when it is legal.** The function quietly compresses hourly
> readings into daily totals. Summarization is lossy, and lossy is a bug *when the question
> needs what you dropped*. Here the question asks about rain per day, so collapsing 24
> hourly readings into one daily total discards nothing the question can see. Lossless for
> this query, done in the deterministic layer where arithmetic is guaranteed correct — and
> it is the single biggest token saving in the whole pipeline. The design question to sit
> with for your own use case: **what can my execution environment pre-compute so the model
> receives conclusion-ready data instead of raw records?**

---

## Step 4 — Wiring it into the three layers

**File:** `step4_toolcall.py` · **Check:** `python checks/check_step4.py` *(makes live API calls)*

**Concept.** The plumbing is character-for-character the pattern from the tool-calling
practical. The only novelty is psychological: you now know this tool is a RAG system,
because its output used to be too big and no longer is.

One honest substitution, measured not vibed: this step uses `llama-3.3-70b-versatile`.
The 8B model stays accurate for routing and plain generation, but in live testing it
garbled tool-call syntax roughly half the time. "The smallest model that stays accurate"
is a **per-job** decision — and two schema details are load-bearing: the description
(the model decides to call you by reading it) and nullable types on optional parameters
(models emit `"month": null`, and the API validates arguments against your schema).

**Your task.**
1. Write the tool schema (name, description, parameters) for `get_weather_history`.
2. Complete the agent loop: when the model asks for the tool, *you* execute it and append
   the result as a `tool` message.

**What you should see.** Run the wedding query through `keyword_answer` and watch it come
back with an actual weekend recommendation, grounded in 310 real data points.

**Stop and think.** Look at the three comments in the loop:
```
result = get_weather_history(**args)      # retrieval
messages.append({... tool result ...})    # augmentation
return msg.content                        # generation
```
You just wrote R, A, and G as three lines of a while loop.

---

## Step 5 — Prove it: measure the win

**File:** `step5_prove_it.py` · **Check:** `python checks/check_step5.py`

**Concept.** "It feels smaller" is not engineering; a number is. You already have both
payloads on disk — the raw corpus (your chunks) and the retrieved answer (step 3's
output). Measure them in the model's units.

**Your task.** Implement `measure()`: token-count the naive payload (all ten chunk files
concatenated) and the RAG payload (step 3's August summaries), return both.

**What you should see.** A compression ratio north of **200×**, from a filter and a
`defaultdict`. No embeddings were harmed in the making of this number.

**Stop and think.** The architecture *is* the bill. When someone shows you a RAG stack,
you can now read its monthly cost off its diagram before a single query runs.

---

## Done?

You built the keyword path: corpus → chunks → index → metadata filter → tool call → answer.

Now go to [`../module2_sage/`](../module2_sage/) — and meet a query that has **nothing to
filter on**.
