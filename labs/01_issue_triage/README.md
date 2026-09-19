# Lab 01 — GitHub Issue Triage

[English](README.md) | [简体中文](README.zh-CN.md)

## Goal

Move from **calling Jev** to designing a small typed decision system.

Lab 00 introduced `Choice`, `Noul`, and `Score`. Lab 01 adds:

1. structured state
2. explicit field references in `instructions`
3. several atomic judgments over the same state
4. a clear boundary between semantic judgment and deterministic policy

## Scenario

The lab uses a fictional GitHub issue:

> **Upload API returns 502 after v2.4.0**
>
> After upgrading to v2.4.0, POST /uploads returns 502 for about 30% of requests in production. Rolling back to v2.3.7 restores normal behavior. We reproduced this in us-west-2 and us-east-1. Logs show upstream connection reset errors.

The state is structured instead of being one flat string:

```python
STATE = {
    "issue": {
        "title": "...",
        "body": "...",
    }
}
```

Questions explicitly refer to fields such as `issue.title` and `issue.body`.

## Four semantic judgments

| ID | Primitive | Question |
| --- | --- | --- |
| `issue_type` | `Choice` | What kind of issue is this? |
| `production_impact` | `Noul` | Are production users currently affected? |
| `severity` | `Score` | How severe is the current user impact? |
| `actionable` | `Noul` | Is there enough concrete evidence to begin investigation? |

Each question asks one focused thing. Jev is **not** asked to decide the whole workflow.

## Question IDs are for code

The key:

```python
"production_impact": Noul(...)
```

lets Python retrieve the answer. The complete semantic question still belongs in `instructions`.

That matters because TypeSafe question IDs are for application code; the model needs the actual question spelled out.

## The key architecture boundary

Jev returns semantic measurements:

```text
issue_type
production_impact
severity
actionable
```

Then normal Python decides:

```text
labels
route
```

For example:

```python
if production_impact >= 0.5:
    labels.append("impact:production")

if issue_type == "security":
    route = "security-review"
elif production_impact >= 0.5 and severity >= 2.5:
    route = "on-call"
```

The thresholds here are intentionally simple teaching policy, not universal best practices. Lab 02 will add confidence-gated policy.

## Run

From the repository root:

```bash
uv run --env-file .env python labs/01_issue_triage/main.py
```

## What to observe

The output is split into two sections:

```text
Semantic judgments from Jev
...

Deterministic policy
...
```

Ask yourself:

- Which values came from the model?
- Which decisions came from Python?
- If business policy changes, which code should change?
- If the issue text changes, which part re-evaluates its meaning?

## Exercises

Change only `STATE` and rerun with:

1. `Uploads are broken.`
2. A feature request for resumable uploads
3. A documentation typo
4. A possible authentication vulnerability
5. A production outage with almost no reproduction detail

Then do the opposite: keep all Jev questions unchanged and modify only the Python policy.

## Key takeaway

> **Use Jev to measure meaning. Use code to own policy and action.**
