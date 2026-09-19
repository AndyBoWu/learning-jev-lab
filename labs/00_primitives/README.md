# Lab 00 — Primitive Playground

[English](README.md) | [简体中文](README.zh-CN.md)

## Goal

Learn the three TypeSafe question primitives by asking all three against the **same state** in a single request.

The example state is a short production incident report:

> After today's deployment, users are getting 502 errors when uploading files. About 30% of upload requests are failing.

We ask three different semantic questions:

| Question | Primitive | Why |
| --- | --- | --- |
| What kind of issue is this? | `Choice` | The answer is one option from a fixed, unordered set. |
| Are production users impacted? | `Noul` | This is a yes/no judgment where the probability of "yes" is useful. |
| How severe is the impact? | `Score` | Severity lies on an ordered spectrum with defined levels. |

## Run it

```bash
export TYPESAFE_API_KEY="your-api-key"
uv run python labs/00_primitives/main.py
```

## What to look for

### Choice

A `Choice` answer gives you:

- the selected option
- a probability for every option
- a separate confidence value

Do not look only at the winning label. The full distribution tells you what alternatives were plausible.

### Noul

A `Noul` answer is a number from 0 to 1:

```text
0.0  -> strong no
0.5  -> uncertain / yes and no are equally likely
1.0  -> strong yes
```

Important: **Noul does not have a separate confidence field.** The value itself is the probability that the answer is yes.

A value of `0.5` does **not** mean "medium impact." It means the model is uncertain about the yes/no statement.

### Score

A `Score` uses ordered rubric levels. Jev returns an expected score, so it may fall between integer levels.

For example, if the rubric has levels 0 through 4, a result such as `2.7` means the probability mass sits between neighboring severity levels. It is not restricted to an integer.

## Why all three questions are in one call

All three judgments use the same state and are independent. TypeSafe evaluates questions in the same request independently, so this is the natural first example of the "ask several judgments, compose in code" mental model.

## Exercise

Change only the incident report and rerun the program with examples such as:

1. A typo in documentation
2. A feature request
3. A security vulnerability with no evidence of exploitation
4. A complete production outage
5. An ambiguous report with very little information

Observe how the selected primitive behaves and inspect the probability distributions instead of only the top answer.

## Key takeaway

Choose the primitive based on the **shape of the answer your code needs**:

- `Choice`: which option?
- `Noul`: is this true?
- `Score`: to what degree?
