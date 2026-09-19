# Lab 00 — Primitive Playground

[English](README.md) | [简体中文](README.zh-CN.md)

## 目标

通过对**同一个 State** 一次性提出三种不同的问题，理解 TypeSafe 最核心的三个 primitive。

这个例子的 State 是一段生产事故描述：

> After today's deployment, users are getting 502 errors when uploading files. About 30% of upload requests are failing.

我们同时问三个语义问题：

| 问题 | Primitive | 为什么 |
| --- | --- | --- |
| 这是什么类型的问题？ | `Choice` | 答案来自一组固定、没有顺序关系的选项。 |
| 生产用户现在是否受到影响？ | `Noul` | 这是 yes/no 判断，而且“yes 的概率”本身有价值。 |
| 影响有多严重？ | `Score` | Severity 是一个有顺序、可以定义等级的连续概念。 |

## 运行

```bash
cp .env.example .env
# 只需要把真实 TYPESAFE_API_KEY 写进 .env 一次。

uv run --env-file .env python labs/00_primitives/main.py
```

根目录的 `.gitignore` 已经忽略 `.env`，因此真实 key 只保留在本机。

## 重点观察什么

### Choice

`Choice` 会返回：

- 最终选中的 option
- 每一个 option 的 probability
- 单独的 confidence

不要只看最终 winner。完整的 probability distribution 可以告诉你还有哪些候选答案也比较合理。

### Noul

`Noul` 返回 0 到 1 之间的数字：

```text
0.0  -> 强烈倾向 no
0.5  -> 不确定 / yes 和 no 概率接近
1.0  -> 强烈倾向 yes
```

特别重要：**Noul 没有另外一个 confidence 字段。** 它返回的值本身，就是“答案为 yes”的概率。

所以 `0.5` 并不是“中等程度”，而是表示模型对这个 yes/no 判断拿不准。

### Score

`Score` 使用有顺序的 rubric levels。Jev 返回的是 expected score，所以结果可以落在两个整数等级之间。

例如 rubric 是 0 到 4，结果为 `2.7` 并不奇怪，它说明 probability mass 分布在相邻的 severity levels 之间，而不是强制输出某个整数。

## 为什么三个问题放在同一次调用里

三个判断都基于同一个 State，而且彼此独立。TypeSafe 会独立计算同一个 request 里面的问题，因此这是理解下面这个 mental model 的最简单例子：

> 一次提出多个 atomic judgments，然后由代码读取和组合这些 typed answers。

## 练习

只修改 incident report，然后重新运行，例如：

1. 文档里的一个 typo
2. 一个 feature request
3. 一个目前没有 exploitation 证据的 security vulnerability
4. 完整 production outage
5. 信息非常少、很模糊的 report

不要只观察最终答案，也要观察 probability distribution 如何变化。

## 核心结论

根据**你的代码最终需要什么形状的答案**来选择 primitive：

- `Choice`：是哪一个？
- `Noul`：是不是？
- `Score`：程度是多少？
