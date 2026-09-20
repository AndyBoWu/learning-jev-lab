# Typed Decision Lab

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个用于学习 **Jev、Laya 和 typed AI decision systems（类型化 AI 决策系统）** 的动手实验仓库。

这个项目最初是一个 TypeSafe Jev 学习仓库。现在我们把它提升成一个更通用的学习项目，重点理解下面这套架构：

<p align="center">
  <img src="docs/assets/typed-decision-architecture.svg" alt="Typed Decision Architecture：state 通过 Jev 或 Laya 做 typed decisions，输出 probabilities，再由 deterministic policy 决定最终 action。" width="100%">
</p>

目标不是单纯学习两个 SDK，而是理解：

- 什么时候 typed decision 比 free-form text generation 更合适；
- Jev 和 Laya 在同一个问题上的设计和行为有什么差异；
- 如何把 semantic judgment 和 deterministic policy 分开；
- 如何把这些 decision safely 地接入 production workflow。

> Decision model 负责语义判断；代码负责 policy 和最终 action。

## 这个仓库覆盖的系统

### TypeSafe Jev

一个 hosted typed-decision system，也是这个仓库最早几个 Lab 使用的实现。Jev 很适合学习 typed primitives、confidence-aware automation 和 production workflow，而不需要自己管理模型基础设施。

### Laya

一个 open-weight、non-autoregressive 的 System 1 decision model。Laya 直接针对 `choice`、`score` 和 `noul` 输出 probability distribution，而不是先生成自由文本。

- Upstream: https://github.com/NandhaKishorM/laya

### Laya-MLX

Laya 的独立 Apple Silicon / MLX port。它非常适合继续学习 local inference、runtime engineering、模型 parity、batching、compilation 和 latency optimization。

- MLX runtime: https://github.com/mizorewww/laya-mlx

两个 Laya 仓库的关系见 [docs/references.md](docs/references.md)。

## 你会学到什么

- `Choice`、`Noul`、`Score` / `choice`、`noul`、`score`
- 怎样设计 State 和 atomic semantic questions
- 为什么 typed decision 可以比 autoregressive text generation 快很多
- 怎样理解 probability 和 confidence，而不是把它们当 magic number
- confidence-gated automation 和 human-review thresholds
- speculative fan-out 和 parallel judgments
- deterministic code 中的 composite scoring
- Agent / model routing
- eval、calibration、coverage 和 threshold tuning
- Production 中的 retry、idempotency、auditability、versioning 和 observability
- 进阶：Laya internals 与 Apple Silicon inference

## 学习路线

前面的 Lab 在实际可行时，会让 **Jev 和 Laya 使用同一份 state、同一组 semantic questions、同一套 deterministic policy**。这样我们能真正看清两个实现的差异，而不是一开始就用统一 adapter 把差异隐藏掉。

| Lab | 主题 | 核心概念 |
| --- | --- | --- |
| 00 | Primitive Playground | 三种 typed-decision primitive |
| 01 | [GitHub Issue Triage](labs/01_issue_triage/) | State、instructions、semantic judgments、deterministic policy |
| 02 | DevOps Incident Triage | Fan-out、confidence gating |
| 03 | Deployment Risk Scoring | Atomic judgments、composite scoring |
| 04 | Agent / Model Router | Ranking、routing、two-stage decisions |
| 05 | Evals & Threshold Tuning | Accuracy、calibration、coverage、threshold |
| 06 | Production Issue Triage | Webhook → decisions → policy → actions → audit trail |
| 07 | Laya Internals | Marker scoring、decision heads、calibration、RLCD |
| 08 | Laya Runtime Engineering | PyTorch vs MLX、batching、compilation、memory、latency |

学习规划持续记录在 [Issue #1](https://github.com/AndyBoWu/typed-decision-lab/issues/1)。

## 为什么 Typed Decision 会更快？

Generative LLM 做分类/判断类问题时，通常会先理解输入，再通过 **autoregressive decoding** 一 token 一 token 地生成回答，例如解释文字或者 JSON。

Typed decision model 则可以直接做：

```text
state + typed question
        ↓
semantic representation
        ↓
decision head
        ↓
probabilities / score
```

这并不代表模型“不再做语义分析”。

真正省掉的是：

- token-by-token text generation；
- 为了表达答案而产生的大量 output tokens；
- JSON / free-form output parsing；
- 很多本来只是为了“把内部判断说出来”的生成工作。

更深入的解释见 [docs/why-typed-decisions.md](docs/why-typed-decisions.md)。

## 快速开始

### 1. 安装依赖

这个仓库使用 [uv](https://docs.astral.sh/uv/)：

```bash
uv sync
```

### 2. 配置 Jev

先从公开模板创建本地 `.env`：

```bash
cp .env.example .env
```

然后设置 TypeSafe API key：

```dotenv
TYPESAFE_API_KEY=your-real-api-key
```

真实 API key 不应该提交到 GitHub。

Laya 的安装会在第一个 comparative lab 里单独引入，而不是直接塞进 base install，因为它的本地模型/runtime 依赖比 Jev SDK 重很多。

### 3. 运行当前 Primitive Lab

```bash
uv run --env-file .env python labs/00_primitives/main.py
```

## 这个仓库遵循的原则

1. **每个 Lab 重点学习一个核心概念。**
2. **先写可以运行的例子，再做抽象。**
3. **Semantic judgment 交给 decision model；business policy 和 action 留给 deterministic code。**
4. **当 comparison 有学习价值时，让不同 backend 使用同一个 scenario。**
5. **不要过早用统一 adapter 隐藏 Jev 和 Laya 的真实差异。**
6. **不仅展示 happy path，也解释 failure mode 和 trade-off。**
7. **所有内容都必须适合公开分享：**不放公司数据、内部 prompt、客户数据或 secret。
8. **English + 中文双语文档。**

## 参考资料

- [TypeSafe Introduction](https://docs.typesafe.ai/introduction)
- [TypeSafe Primitives](https://docs.typesafe.ai/primitives)
- [TypeSafe Python SDK](https://docs.typesafe.ai/sdk/python)
- [Laya upstream](https://github.com/NandhaKishorM/laya)
- [Laya-MLX](https://github.com/mizorewww/laya-mlx)

## 当前进度

- [x] 原始 Jev learning plan
- [x] Lab 00 — Primitive Playground（Jev）
- [x] Lab 01 — GitHub Issue Triage（Jev）
- [ ] 给 Primitive / Issue Triage Lab 加入 Laya 版本
- [ ] Lab 02 — DevOps Incident Triage
- [ ] Lab 03 — Deployment Risk Scoring
- [ ] Lab 04 — Agent / Model Router
- [ ] Lab 05 — Evals & Threshold Tuning
- [ ] Lab 06 — Production Issue Triage
- [ ] Lab 07 — Laya Internals
- [ ] Lab 08 — Laya Runtime Engineering
