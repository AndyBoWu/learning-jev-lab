# Why Typed Decisions Can Be Much Faster Than Text Generation

The short answer is:

> Typed decision models do not remove semantic understanding. They remove the need to express a decision through autoregressive text generation.

That distinction matters.

## Generative path

Suppose the application only needs to decide whether an issue affects production.

A general-purpose generative LLM may be asked to return JSON:

```text
state
  ↓
large language model
  ↓
prefill / semantic processing
  ↓
generate "{"
  ↓
generate "\"production_impact\""
  ↓
generate ":"
  ↓
generate "true"
  ↓
generate "}"
  ↓
parse / validate
  ↓
boolean
```

Even with a KV cache, output tokens are autoregressive: token N depends on the generated prefix through token N-1.

The application only needed one semantic value, but the system paid for producing a textual representation of that value.

## Typed-decision path

A typed decision model can instead expose the actual decision surface directly:

```text
state + question
       ↓
semantic encoder / representation
       ↓
decision head
       ↓
P(false), P(true)
```

Or for a choice:

```text
                 ┌─ billing probability
representation ──┼─ technical probability
                 └─ sales probability
```

The final application value comes directly from logits / probabilities.

There are **zero generated output tokens**.

## What work is actually removed?

Typed decisions can remove several forms of overhead:

1. **Autoregressive decoding**

   A generative model produces output tokens sequentially. A decision head can produce a fixed-size output in one model evaluation.

2. **Unnecessary natural-language representation**

   The model does not need to convert an internal semantic judgment into prose or JSON merely so software can convert it back into a typed value.

3. **Output-format overhead**

   There is no need to generate keys, punctuation, explanations, Markdown, or schema boilerplate.

4. **Parsing and repair**

   The application does not need JSON parsing, schema repair, retry prompts, or handling malformed free-form output.

5. **Large generative model capacity**

   A specialized decision model can often be much smaller than a general-purpose multi-billion-parameter language model because it does not need to support open-ended generation.

6. **Efficient batching of decisions**

   Multiple typed questions can often be evaluated as batched classification/scoring rows instead of independent text-generation sequences.

## What work is *not* removed?

The model still has to understand the input.

For example:

```text
"Checkout is returning 500s in three regions after today's deploy."
```

The model still needs semantic representations that capture concepts such as:

- checkout
- production failures
- deployment timing
- blast radius
- severity

Typed decisions do **not** mean:

```text
no reasoning
no semantics
simple keyword matching
```

A better mental model is:

```text
Generative LLM

semantic computation
        +
autoregressive expression of the answer
        ↓
text / JSON


Typed decision model

semantic computation
        +
direct decision scoring
        ↓
probability / score / label
```

The second path removes the **expression layer**, not the semantic layer.

## Why the speed difference can be large

The performance difference is usually a combination of multiple factors rather than one trick:

```text
smaller specialized model
        ×
no autoregressive output loop
        ×
fixed output space
        ×
parallel option scoring
        ×
efficient batching
        ×
no parsing / retries
```

For Laya specifically, the architecture is a bidirectional encoder plus decision heads. Candidate options are represented inside the input, and their marker representations are scored directly.

Laya-MLX then adds another optimization dimension: the same Laya model behavior is reimplemented in Apple's MLX runtime for Apple Silicon.

## Does this replace generative LLMs?

No.

Typed decisions are strongest when the required output has a known semantic shape:

- classification
- routing
- binary proposition
- ordinal score
- moderation decision
- risk dimension
- confidence-gated automation

Generative models are still appropriate when the system needs:

- open-ended writing
- explanation
- code generation
- summarization
- synthesis
- multi-step planning with unknown output structure

A useful architecture is often:

```text
                request
                   │
           typed decision layer
             /             \
       simple path       complex path
           │                 │
 deterministic code     generative LLM
```

The typed-decision layer does not replace the LLM. It prevents the system from paying for open-ended generation when the task only requires a constrained semantic decision.
