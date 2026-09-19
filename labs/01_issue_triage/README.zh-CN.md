# Lab 01 — GitHub Issue Triage

[English](README.md) | [简体中文](README.zh-CN.md)

## 目标

从“会调用 Jev”进一步走到“会设计一个小型 typed decision system”。

Lab 00 学的是 `Choice`、`Noul`、`Score`。Lab 01 新增四个重点：

1. structured state
2. 在 `instructions` 里明确引用 State 字段
3. 对同一个 State 做多个 atomic judgment
4. 明确区分 semantic judgment 和 deterministic policy

## 场景

我们使用一个完全虚构的 GitHub issue：

> **Upload API returns 502 after v2.4.0**
>
> After upgrading to v2.4.0, POST /uploads returns 502 for about 30% of requests in production. Rolling back to v2.3.7 restores normal behavior. We reproduced this in us-west-2 and us-east-1. Logs show upstream connection reset errors.

State 不再只是一个扁平字符串，而是结构化数据：

```python
STATE = {
    "issue": {
        "title": "...",
        "body": "...",
    }
}
```

Question 会明确引用 `issue.title`、`issue.body`。

## 四个语义判断

| ID | Primitive | 判断什么 |
| --- | --- | --- |
| `issue_type` | `Choice` | 这是什么类型的 issue？ |
| `production_impact` | `Noul` | 当前 production users 是否受到影响？ |
| `severity` | `Score` | 当前用户影响有多严重？ |
| `actionable` | `Noul` | 信息是否足够让工程师开始调查？ |

每个 question 只判断一件事。我们不会让 Jev 直接决定整个 workflow。

## Question ID 是给代码看的

例如：

```python
"production_impact": Noul(...)
```

`production_impact` 这个 key 是为了让 Python 找到答案。真正的问题仍然必须完整写在 `instructions` 里。

## 最重要的 architecture boundary

Jev 输出 semantic measurements：

```text
issue_type
production_impact
severity
actionable
```

然后普通 Python 决定：

```text
labels
route
```

例如：

```python
if production_impact >= 0.5:
    labels.append("impact:production")

if issue_type == "security":
    route = "security-review"
elif production_impact >= 0.5 and severity >= 2.5:
    route = "on-call"
```

这里的 threshold 只是教学用的简单 policy，并不是通用最佳实践。Lab 02 会正式学习 confidence-gated policy。

## 运行

在 repository root：

```bash
uv run --env-file .env python labs/01_issue_triage/main.py
```

## 运行以后看什么

输出故意分成两部分：

```text
Semantic judgments from Jev
...

Deterministic policy
...
```

问自己：

- 哪些值来自模型？
- 哪些决定来自 Python？
- 如果 business policy 改了，应该改哪一边？
- 如果 issue 文本变了，哪一边负责重新理解语义？

## 练习

只修改 `STATE`，分别试：

1. `Uploads are broken.`
2. resumable uploads 的 feature request
3. documentation typo
4. possible authentication vulnerability
5. production outage，但几乎没有 reproduction detail

然后反过来：完全不改 Jev questions，只修改 Python policy。

## 核心结论

> **Jev 用来测量语义；代码负责 policy 和 action。**
