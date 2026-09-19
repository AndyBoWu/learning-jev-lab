# learning-jev-lab

[English](README.md) | [简体中文](README.zh-CN.md)

A hands-on learning lab for **TypeSafe Jev** and typed AI decision systems.

The goal is not to reproduce the full official documentation. The goal is to compress the most useful concepts into a small set of runnable labs so engineers can build intuition quickly.

> Jev makes semantic judgments. Code owns the workflow.

## What you will learn

- When to use `Choice`, `Noul`, and `Score`
- How to structure state and atomic questions
- How to use confidence without turning it into a magic number
- Speculative fan-out and confidence-gated routing
- Composite scoring with deterministic policy in code
- Agent skill routing
- Evaluation and threshold tuning

## Learning path

| Lab | Topic | Main idea |
| --- | --- | --- |
| 00 | Primitive Playground | `Choice`, `Noul`, `Score` |
| 01 | [GitHub Issue Triage](labs/01_issue_triage/) | State, instructions, typed judgments |
| 02 | [DevOps Incident Triage](labs/02_incident_triage/) | Fan-out and confidence gating |
| 03 | Deployment Risk Scoring | Atomic judgments and composite scoring |
| 04 | Agent Skill Router | Ranking and two-stage routing |
| 05 | Evals & Threshold Tuning | Accuracy, coverage, and thresholds |

The full learning plan is tracked in [Issue #1](https://github.com/AndyBoWu/learning-jev-lab/issues/1).

## Quick start

### 1. Install dependencies

This repo uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

### 2. Set your TypeSafe API key

Create a local `.env` file from the public template:

```bash
cp .env.example .env
```

Then replace the placeholder in `.env` with your real TypeSafe API key:

```dotenv
TYPESAFE_API_KEY=your-real-api-key
```

The `.env` file is ignored by Git and must never be committed.

### 3. Run Lab 00

Load the local `.env` file explicitly when running with uv:

```bash
uv run --env-file .env python labs/00_primitives/main.py
```

## Repository principles

1. **One important concept per lab.**
2. **Runnable examples before abstraction.**
3. **Semantic judgment belongs to Jev; deterministic policy belongs to code.**
4. **Explain failure modes and trade-offs, not only happy paths.**
5. **Keep examples public-safe:** no company data, internal prompts, customer data, or secrets.
6. **English + 中文 documentation** so the material is useful to both audiences.

## References

- [TypeSafe Introduction](https://docs.typesafe.ai/introduction)
- [TypeSafe Primitives](https://docs.typesafe.ai/primitives)
- [TypeSafe Python SDK](https://docs.typesafe.ai/sdk/python)
- [TypeSafe Agent Skill](https://docs.typesafe.ai/agent-skill)

## Status

- [x] Learning plan
- [x] Lab 00 — Primitive Playground
- [x] Lab 01 — GitHub Issue Triage
- [ ] Lab 02 — DevOps Incident Triage
- [ ] Lab 03 — Deployment Risk Scoring
- [ ] Lab 04 — Agent Skill Router
- [ ] Lab 05 — Evals & Threshold Tuning
