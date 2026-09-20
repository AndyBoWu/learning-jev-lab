# References and Project Map

This repository studies **typed AI decision systems** through multiple implementations.

The projects below are related, but they live at different layers.

## TypeSafe Jev

- Documentation: https://docs.typesafe.ai/
- Role in this lab: hosted typed-decision system
- Useful for studying:
  - typed semantic primitives
  - confidence-aware workflow design
  - production integration
  - deterministic policy around semantic judgments

Jev is treated as one implementation of the broader typed-decision architecture, not as the definition of the architecture itself.

## Laya

- Repository: https://github.com/NandhaKishorM/laya
- Role in this lab: open-weight typed-decision model and upstream implementation
- Useful for studying:
  - `choice`, `score`, and `noul`
  - non-autoregressive decision inference
  - probability calibration
  - decision-model architecture
  - RLCD training / fine-tuning
  - routing and application presets

Laya is the main reference when we want to understand how a typed decision model works internally.

## Laya-MLX

- Repository: https://github.com/mizorewww/laya-mlx
- Upstream: https://github.com/NandhaKishorM/laya
- Role in this lab: independent Apple Silicon / MLX inference port
- Useful for studying:
  - native MLX inference
  - removal of PyTorch / Transformers runtime dependencies
  - checkpoint conversion
  - numerical parity with upstream Laya
  - FP16 inference
  - batching
  - compilation
  - prompt-prefix tokenization reuse
  - local latency and memory behavior

Laya-MLX does **not** define a separate decision-model concept. It ports Laya's model behavior to another runtime.

## Relationship

```text
Typed Decision Systems
        │
        ├── TypeSafe Jev
        │      hosted implementation
        │
        └── Laya
               open-weight model / upstream
                  │
                  └── Laya-MLX
                         Apple Silicon runtime port
```

For the early labs, Jev and Laya should be compared on the same state and semantic questions.

For advanced labs:

- use **Laya** to study model architecture and training;
- use **Laya-MLX** to study runtime and AI infrastructure.
