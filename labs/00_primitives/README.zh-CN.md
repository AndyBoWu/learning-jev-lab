# Lab 00 — Primitive Playground

[English](README.md) | [简体中文](README.zh-CN.md)

## 目标

用 **完全相同的 State、semantic questions 和 criteria**，分别跑 Jev 和 Laya，
真正理解 typed decision 最核心的三个 primitive。

这个 Lab 的目的不是单纯学习两个 SDK，而是把两件事情分开：

- 哪些东西属于 typed-decision architecture 的通用概念；
- 哪些东西只是 Jev / Laya 各自的 SDK、模型、calibration 和 deployment 差异。

共享的 incident state 是：

> After today's deployment, users are getting 502 errors when uploading files. About 30% of upload requests are failing.

两个 backend 都回答完全相同的三个问题：

| Semantic question | Jev | Laya | 含义 |
| --- | --- | --- | --- |
| 这是什么类型的问题？ | `Choice` | `choice` | 从固定、无顺序的候选项里选择一个。 |
| Production 用户是否受到影响？ | `Noul` | `noul` | 返回一个 yes/no proposition 为真的概率 P(true)。 |
| 影响有多严重？ | `Score` | `score` | 在一个有顺序的 rubric 上进行评分。 |

## 它们到底有多像？

在概念层，它们非常接近：

```text
state + typed question
        ↓
semantic judgment
        ↓
probability distribution / expected score
        ↓
deterministic code 决定最终 action
```

两个实现都不是先让模型生成一段 prose / JSON，再从文本里 parse 出 decision。

## 真正的差异在哪里？

| 维度 | Jev | Laya |
| --- | --- | --- |
| Execution | Hosted API | Open-weight model，在自己的 process 里运行 |
| Setup | API key | 本地 runtime + 下载 checkpoint |
| Question API | `Choice(...)` 等 Python class | 带 `type: "choice"` 的 dict |
| Model lifecycle | Service 帮你管理 | 你的 process 自己 load / 持有 checkpoint |
| Primitive | Choice / Noul / Score | choice / noul / score |
| Output | Structured probabilities / scores | Structured probabilities / scores |
| Calibration | Jev 自己的一套 | Laya 自己的一套 |
| Infrastructure | Network request | Local CPU/GPU inference |

这里最重要的一点：

> **Primitive 很像，不代表 confidence 可以直接互换。**

两个系统来自不同模型、不同训练和 calibration procedure。同一个 State 得到不同
probability 非常正常。到了 Lab 05，我们才会用 shared labeled dataset 去真正评估
threshold，而不是凭感觉说 0.8 在两个系统里意义完全一样。

## 文件结构

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

`shared.py` 保存 shared scenario 和 criteria，保证两个 backend 真正在回答同一个问题。

`main.py` 继续保留，兼容最早的 Jev 运行命令。

### 为什么文件不叫 `laya.py`？

如果直接运行一个叫 `laya.py` 的 Python 文件，它会在 `sys.path` 上遮蔽
安装好的 `laya` package。

结果：

```python
import laya
```

可能导入的是当前 Lab 自己的 `laya.py`，而不是真正安装的 package。

所以这里故意使用：

```text
laya_backend.py
```

这是一个很好的实际工程例子：学习计划里的目录规范，也要服从真实语言/runtime
的 import 规则。

## 安装

Jev SDK 属于 base dependencies：

```bash
uv sync
```

Laya 的模型/runtime stack 更重，因此放在 optional dependency：

```bash
uv sync --extra laya
```

目前这个 Lab pin 在 Laya 0.3.x API family。

## 运行 Jev

第一次先创建本地环境变量文件：

```bash
cp .env.example .env
```

设置：

```dotenv
TYPESAFE_API_KEY=your-real-api-key
```

然后：

```bash
uv run --env-file .env python labs/00_primitives/jev.py
```

以前的命令仍然可用：

```bash
uv run --env-file .env python labs/00_primitives/main.py
```

## 运行 Laya

```bash
uv run --extra laya python labs/00_primitives/laya_backend.py
```

这个 Lab 使用 Laya 的 `typed-decisions` checkpoint：

```text
convaiinnovations/laya / typed-decisions
```

第一次运行会下载模型 checkpoint；后面的调用会复用本地 Hugging Face cache。

我们故意选择针对 typed-decision workflow 的 checkpoint，而不是假设所有 Laya
checkpoint 都有完全相同的能力。**选哪个模型，本身就是 system design 的一部分。**

## 同时比较 Jev 和 Laya

配置好 Jev API key，并下载过 Laya checkpoint 后：

```bash
uv run --extra laya --env-file .env python labs/00_primitives/compare.py
```

输出会把三个 decision 并排放在一起：

```text
Decision               Jev                          Laya
----------------------------------------------------------------------------------
issue_type              ...
production_impact       ...
severity                ...
```

不要期待数字完全一样。真正应该观察的是：

1. 两个系统的 semantic answer 是否一致？
2. probability distribution 谁更集中？
3. expected severity score 相差多少？
4. 有没有一边很 confident、另一边却不确定？
5. 为了得到这个 decision，各自产生了什么 operational cost：network call 还是 local inference？

## 三个 Primitive

### Choice / choice

都返回一个 winner，同时保留 alternatives 的 probability distribution。

所以不要只看最终 label；near-tie 往往很有学习价值。

### Noul / noul

都表示一个 proposition 为真的概率：

```text
0.0  → 强烈 no
0.5  → 不确定
1.0  → 强烈 yes
```

它不是一个 severity level。

### Score / score

都把 ordered rubric 转换成 distribution，并返回 expected score。

因此结果完全可以是 2.3、2.7，而不一定必须是整数。

## 练习

只修改 incident report，然后分别跑两个 backend：

1. documentation typo；
2. feature request；
3. 没有 exploitation 证据的 security vulnerability；
4. 完整 production outage；
5. 故意写得很模糊的 report。

除了看 correctness，更要记录 **Jev / Laya disagreement**。

Disagreement 往往就是后续 eval dataset 最有价值的数据来源。

## 核心结论

你的直觉是对的：

> **Jev 和 Laya 在 typed-decision abstraction 上非常接近；真正不同的是 model、
> runtime、SDK、calibration 和 deployment trade-off。**

也正因为概念很像，我们才值得做同题对照实验：它能帮我们看清“架构”与“实现”
到底分别是什么。
