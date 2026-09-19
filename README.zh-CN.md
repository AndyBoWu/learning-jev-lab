# learning-jev-lab

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个用于学习 **TypeSafe Jev** 和 typed AI decision systems（类型化 AI 决策系统）的动手实验仓库。

这个仓库的目标不是复制整套官方文档，而是把最重要、最实用的概念压缩成少量可运行的 Lab，让工程师可以更快建立正确的直觉。

> Jev 负责语义判断（semantic judgment），代码负责工作流和最终行为（workflow / policy）。

## 你会学到什么

- 什么时候应该使用 `Choice`、`Noul`、`Score`
- 怎样设计 State 和 atomic questions（原子问题）
- 怎样正确理解 confidence，而不是随便写一个 magic number
- Speculative fan-out 和 confidence-gated routing
- 用 deterministic code 做 composite scoring
- Agent Skill Router 的设计
- Evals、accuracy、coverage 和 threshold tuning

## 学习路线

| Lab | 主题 | 核心概念 |
| --- | --- | --- |
| 00 | Primitive Playground | `Choice`、`Noul`、`Score` |
| 01 | [GitHub Issue Triage](labs/01_issue_triage/) | State、instructions、typed judgments |
| 02 | [DevOps Incident Triage](labs/02_incident_triage/) | Fan-out、confidence gating |
| 03 | Deployment Risk Scoring | Atomic judgments、composite scoring |
| 04 | Agent Skill Router | Ranking、two-stage routing |
| 05 | Evals & Threshold Tuning | Accuracy、coverage、threshold |

完整的学习规划记录在 [Issue #1](https://github.com/AndyBoWu/learning-jev-lab/issues/1)。

## 快速开始

### 1. 安装依赖

这个仓库使用 [uv](https://docs.astral.sh/uv/)：

```bash
uv sync
```

### 2. 设置 TypeSafe API Key

先从公开模板创建本地 `.env` 文件：

```bash
cp .env.example .env
```

然后把 `.env` 里的 placeholder 换成你真实的 TypeSafe API key：

```dotenv
TYPESAFE_API_KEY=your-real-api-key
```

`.env` 已经被 Git ignore，真实 API key 不应该提交到 GitHub。

### 3. 运行 Lab 00

运行时让 uv 显式加载本地 `.env`：

```bash
uv run --env-file .env python labs/00_primitives/main.py
```

## 这个仓库遵循的原则

1. **每个 Lab 重点学习一个核心概念。**
2. **先写可以运行的例子，再做抽象。**
3. **语义判断交给 Jev；业务规则和最终行为留在 deterministic code。**
4. **不仅展示 happy path，也解释容易出错的地方和 trade-off。**
5. **所有内容都必须适合公开分享：**不放公司数据、内部 prompt、客户数据或 secret。
6. **English + 中文双语文档**，方便中英文读者学习。

## 参考资料

- [TypeSafe Introduction](https://docs.typesafe.ai/introduction)
- [TypeSafe Primitives](https://docs.typesafe.ai/primitives)
- [TypeSafe Python SDK](https://docs.typesafe.ai/sdk/python)
- [TypeSafe Agent Skill](https://docs.typesafe.ai/agent-skill)

## 当前进度

- [x] Learning plan
- [x] Lab 00 — Primitive Playground
- [x] Lab 01 — GitHub Issue Triage
- [ ] Lab 02 — DevOps Incident Triage
- [ ] Lab 03 — Deployment Risk Scoring
- [ ] Lab 04 — Agent Skill Router
- [ ] Lab 05 — Evals & Threshold Tuning
