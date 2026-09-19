# Lab 02 — DevOps Incident Triage

[English](README.md) | [简体中文](README.zh-CN.md)

## 目标

学习两个让 Jev 真正进入工程系统的关键 pattern：

1. **Speculative fan-out**：多个彼此独立的语义判断一次性全部问完，即使其中某些结果最后可能不会使用。
2. **Confidence-gated policy**：answer 表示“模型认为是什么”，certainty + action risk 决定“系统敢不敢执行动作”。

Lab 01 已经把 semantic judgment 和 deterministic policy 分开；Lab 02 再把 uncertainty 加进来。

## 为什么需要这一课

Lab 01 里可能出现这种结果：

```text
severity = 2.46
confidence = 0.62
```

`2.46` 表示模型对严重程度的估计；`0.62` 表示这个估计本身并不是特别确定。

这两个信号不是一回事。

## 两个场景

程序内置两个 fixture：

- `clear`：deployment timing、metrics、rollback evidence 都比较清楚
- `ambiguous`：metrics 不完整、时间关系不清楚、blast radius 不确定

分别运行：

```bash
uv run --env-file .env python labs/02_incident_triage/main.py --scenario clear

uv run --env-file .env python labs/02_incident_triage/main.py --scenario ambiguous
```

## Speculative fan-out

一次 request 同时问：

| Judgment | Primitive |
| --- | --- |
| incident type | `Choice` |
| customer impact | `Noul` |
| deployment related? | `Noul` |
| rollback candidate? | `Noul` |
| severity | `Score` |
| security sensitive? | `Noul` |

`rollback_candidate` 是一个故意设计的 speculative question。

如果最后判断 incident 和 deployment 没关系，policy 直接忽略 rollback 的结果即可，不需要先 classify，再发第二次 model call。

## Confidence 和 probability 不是一回事

`Choice` 和 `Score` 都有从 probability distribution 计算出来的 `confidence`。

`Noul` 没有额外的 confidence 字段，它本身返回的就是 `P(yes)`。

所以代码里会同时看到两种 gating：

```text
Choice / Score
→ answer + confidence

Noul
→ 直接 threshold P(yes)
```

## Action risk 越高，threshold 越应该保守

这个 Lab 故意给不同动作设置不同要求。

### 低风险动作

加一个 incident type label 很容易撤销，所以 threshold 可以比较宽松：

```python
if incident_type_confidence >= 0.55:
    actions.append(f"label:type:{incident_type}")
```

### 较高风险动作

page on-call 会打扰人，所以要求更强的 impact evidence 和更高的 severity confidence：

```python
if customer_impact >= 0.80 and severity >= 2.50:
    if severity_confidence >= 0.80:
        actions.append("notify:on-call")
    else:
        actions.append("review:on-call-decision")
```

### Rollback

即使 rollback 很可能有效，这一课也只输出：

```text
recommend:rollback
require:human-confirmation-before-rollback
```

模型不会直接执行 destructive remediation。

## Threshold 只是教学值

`0.55`、`0.80` 等数字不是 Jev 的 universal best practice。

这一课真正要学的是：

> consequence 越高，对 evidence / confidence 的要求越高。

Lab 05 才会用 labeled eval data 来真正调 threshold。

## 运行后重点比较

分别运行 `clear` 和 `ambiguous`，看：

- `incident_type.confidence`
- `severity.confidence`
- 各个 Noul 的 probability
- 哪些动作被允许自动执行
- 哪些动作因为 uncertainty 被送到 human review

最有意思的情况不一定是 classification 不同；也可能是 **classification 一样，但 confidence 不一样，所以系统行为不同**。

## 核心结论

> **Answer 决定系统认为发生了什么；confidence 和 action risk 决定系统是否应该行动。**
