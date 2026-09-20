# Lab 00 — Primitive Playground

[English](README.md) | [简体中文](README.zh-CN.md)

## Goal

Learn the three core typed-decision shapes by running the **same state, same semantic
questions, and same criteria through both Jev and Laya**.

The point is not to learn two APIs for their own sake. It is to separate:

- the architecture that is common to typed decision systems; from
- backend-specific SDK, model, calibration, and deployment details.

The shared incident state is:

> After today's deployment, users are getting 502 errors when uploading files. About 30% of upload requests are failing.

Both backends answer the same three questions:

| Semantic question | Jev | Laya | Meaning |
| --- | --- | --- | --- |
| What kind of issue is this? | `Choice` | `choice` | Pick one option from a fixed unordered set. |
| Are production users impacted? | `Noul` | `noul` | Return P(true) for a yes/no proposition. |
| How severe is the impact? | `Score` | `score` | Place the state on an ordered rubric. |

## What is actually similar?

At the conceptual layer, the systems are very close:

```text
state + typed question
        ↓
semantic judgment
        ↓
probability distribution / expected score
        ↓
deterministic code decides what to do
```

Neither example asks the model to generate prose or JSON and then parse it back into a
decision.

## What is different?

| Dimension | Jev | Laya |
| --- | --- | --- |
| Execution | Hosted API | Open-weight model loaded into your process |
| Setup | API key | Local model/runtime + downloaded checkpoint |
| Question API | Python classes such as `Choice(...)` | JSON-like dictionaries with `type: "choice"` |
| Model lifecycle | Managed by the service | Your process loads and owns the checkpoint |
| Primitive shapes | Choice / Noul / Score | choice / noul / score |
| Output | Structured probabilities / scores | Structured probabilities / scores |
| Calibration | Jev-specific | Laya-specific |
| Infrastructure | Network request | Local CPU/GPU inference |

The key lesson is that **matching primitive names do not make confidence values
interchangeable**. Different models and calibration procedures can produce different
probabilities for the same state. Lab 05 will evaluate both backends on shared labeled data
before using thresholds for automation.

## Files

```text
labs/00_primitives/
├── README.md
├── README.zh-CN.md
├── shared.py
├── jev.py
├── laya_backend.py
├── compare.py
└── main.py
```

`shared.py` contains the scenario and criteria so both implementations receive the same
semantic task.

`main.py` remains as a backward-compatible Jev entry point.

### Why not call the file `laya.py`?

A directly executed Python file named `laya.py` would shadow the installed `laya`
package on `sys.path`. Then `import laya` could import the lab file itself instead of the
real package.

So this lab intentionally uses `laya_backend.py`.

That tiny naming issue is a useful example of the difference between an architecture-level
learning contract and a real executable Python project.

## Install

Base dependencies include the Jev SDK:

```bash
uv sync
```

Laya is an optional dependency because its model/runtime stack is substantially heavier:

```bash
uv sync --extra laya
```

The lab currently pins the Laya 0.3.x API family.

## Run Jev

Create the local environment file once:

```bash
cp .env.example .env
```

Set:

```dotenv
TYPESAFE_API_KEY=your-real-api-key
```

Then run:

```bash
uv run --env-file .env python labs/00_primitives/jev.py
```

The original command still works:

```bash
uv run --env-file .env python labs/00_primitives/main.py
```

## Run Laya

```bash
uv run --extra laya python labs/00_primitives/laya_backend.py
```

This lab uses Laya's `typed-decisions` checkpoint:

```text
convaiinnovations/laya / typed-decisions
```

The first run downloads the checkpoint. Later calls reuse the local Hugging Face cache.

We deliberately use the specialized typed-decisions checkpoint rather than pretending all
Laya checkpoints have identical behavior. Choosing the appropriate model is part of the
system design.

## Compare both

Once the Jev API key is configured and the Laya checkpoint is available:

```bash
uv run --extra laya --env-file .env python labs/00_primitives/compare.py
```

The comparison prints the same three decisions side by side:

```text
Decision               Jev                          Laya
----------------------------------------------------------------------------------
issue_type              ...
production_impact       ...
severity                ...
```

Do not expect identical numbers. The useful questions are:

1. Do the two systems choose the same semantic answer?
2. How concentrated is each probability distribution?
3. How different are the score expectations?
4. Does one backend look confident when the other is uncertain?
5. What operational cost produced that result: network call or local inference?

## Primitive notes

### Choice / choice

Both return a selected option plus a distribution over alternatives. This makes it possible
to inspect near-ties rather than treating the winner as absolute truth.

### Noul / noul

Both represent the probability that a proposition is true:

```text
0.0  → strong no
0.5  → uncertain
1.0  → strong yes
```

This is not an ordinal severity score.

### Score / score

Both represent an ordered rubric as a distribution and return an expected score. The result
can therefore fall between integer rubric levels.

## Exercise

Change only the incident report and rerun both backends:

1. a documentation typo;
2. a feature request;
3. a security vulnerability with no evidence of exploitation;
4. a complete production outage;
5. an intentionally vague report.

Record **disagreement**, not just correctness. Disagreement is often the fastest way to find
interesting evaluation cases for later labs.

## Key takeaway

Jev and Laya are **very similar at the typed-decision abstraction layer** but meaningfully
different as systems:

> Same decision architecture; different model, runtime, SDK, calibration, and deployment
> trade-offs.

That is exactly why implementing both is useful.
