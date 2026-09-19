# Lab 02 — DevOps Incident Triage

[English](README.md) | [简体中文](README.zh-CN.md)

## Goal

Learn two patterns that make Jev much more useful in real systems:

1. **Speculative fan-out** — ask all independent semantic questions in one request, even when some answers may later be irrelevant.
2. **Confidence-gated policy** — let the answer describe *what the model believes*, and let certainty + action risk determine *whether the system should act*.

Lab 01 separated semantic judgment from deterministic policy. Lab 02 adds uncertainty to that boundary.

## Why this lab exists

In Lab 01, a result can look like:

```text
severity = 2.46
confidence = 0.62
```

The score says the incident looks moderately serious. The confidence says the model is not especially certain about that severity estimate.

Those are different signals.

## Two scenarios

The program includes two fixture incidents:

- `clear` — strong timing, metrics, and rollback evidence
- `ambiguous` — incomplete metrics, weak timing evidence, uncertain blast radius

Run them separately so you can compare the probability/uncertainty behavior without changing code.

```bash
uv run --env-file .env python labs/02_incident_triage/main.py --scenario clear

uv run --env-file .env python labs/02_incident_triage/main.py --scenario ambiguous
```

## Speculative fan-out

One request asks all of these questions:

| Judgment | Primitive |
| --- | --- |
| incident type | `Choice` |
| customer impact | `Noul` |
| deployment related? | `Noul` |
| rollback candidate? | `Noul` |
| severity | `Score` |
| security sensitive? | `Noul` |

`rollback_candidate` is intentionally speculative. If the incident turns out not to be deployment-related, the policy simply ignores that answer.

That avoids a second round trip such as:

```text
classify incident
→ discover it may be deployment-related
→ make another model call asking about rollback
```

## Confidence is not the same as probability

`Choice` and `Score` answers have a `confidence` derived from their probability distributions.

`Noul` has no separate confidence field. Its value is already `P(yes)`.

So this lab uses both patterns:

```text
Choice / Score
→ inspect answer + confidence

Noul
→ threshold P(yes) directly
```

## Action thresholds should scale with risk

The policy deliberately uses different requirements for different actions.

### Low-risk action

Adding an incident-type label is easy to undo:

```python
if incident_type_confidence >= 0.55:
    actions.append(f"label:type:{incident_type}")
```

### Higher-risk action

Paging on-call is noisy and costly, so the system requires both strong impact evidence and higher confidence in severity:

```python
if customer_impact >= 0.80 and severity >= 2.50:
    if severity_confidence >= 0.80:
        actions.append("notify:on-call")
    else:
        actions.append("review:on-call-decision")
```

### Rollback

Even when rollback looks plausible, this lab only **recommends** it:

```text
recommend:rollback
require:human-confirmation-before-rollback
```

The model does not directly execute a destructive remediation.

## Important: the thresholds are teaching values

`0.55`, `0.80`, and the other thresholds are not universal Jev best practices.

They demonstrate the architecture:

> higher consequence → stronger evidence / confidence requirement

Lab 05 will use labeled eval data to decide thresholds empirically.

## What to compare

Run both scenarios and compare:

- `incident_type.confidence`
- `severity.confidence`
- the Noul probabilities
- which policy actions are allowed
- which actions fall back to human review

The most interesting outcome is not necessarily a different classification. It may be the **same classification with different confidence, producing different behavior**.

## Key takeaway

> **The answer determines what the system believes. Confidence and action risk determine whether the system should act.**
