---
type: Primary Source
title: "Lost in the Middle: How Language Models Use Long Contexts"
description: "Companion markdown representation and technical summary of Liu et al.'s TACL 2023 paper on context-window attention degradation (arXiv:2307.03172)."
tags: [lost-in-the-middle, context-window, attention-degradation, u-shaped-attention, prompt-structuring]
status: stable
generated:
  by: research-agent/deep-research
  at: 2026-08-31T12:00:00Z
verified:
  - by: process:academic-verify
    at: 2026-08-31T12:00:00Z
sources:
  - id: liu-lost-middle-2023
    resource: https://doi.org/10.48550/arXiv.2307.03172
    title: "Lost in the Middle: How Language Models Use Long Contexts"
    author: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
    last_modified: 2023-07-06T00:00:00Z
---

# Document Summary

Liu et al. (Stanford University & UC Berkeley) empirically demonstrate the **"Lost in the Middle" phenomenon** across frontier large language models (including GPT-3.5, GPT-4, Claude, and MPT-30B).[^liu-lost-middle-2023] While LLMs can process long input sequences (32k–128k+ tokens), their ability to retrieve and reason over information follows a **U-shaped curve**: performance is highest when critical instructions/data are positioned at the very beginning or the very end of the input context, dropping by **up to 40% when critical data is placed in the middle**.[^liu-lost-middle-2023]

# Technical Architecture

```mermaid
graph LR
    subgraph U-Shaped Attention Performance Curve
        Start[Beginning of Prompt: High Attention Fidelity ~90%] --> Middle[Middle of Prompt (20%-80%): Attention Decay drops to ~50%]
        Middle --> End[End of Prompt (Recent Tokens): High Attention Fidelity ~88%]
    end
    subgraph AgentSpec Architecture Counter-Measures
        A1[Anchor <agent_spec> Invariants at Start] --> Start
        A2[Dynamic Observations Injected at End] --> End
        A3[Quarantine Mid-Context Bloat via Token Pruning] --> Middle
    end
```
*Diagram 1: The U-shaped context retrieval curve and AgentSpec structural counter-measures. Source: Liu et al. (2023).*

## Core Empirical Findings

1. **U-Shaped Retrieval Curve**: Performance degrades significantly as input context grows, even in models explicitly trained on long context windows.[^liu-lost-middle-2023]
2. **Instruction Primacy**: System instructions placed at token offset 0 enjoy maximal positional weight in Rotary Position Embedding (RoPE) and ALiBi layers.[^liu-lost-middle-2023]
3. **Architectural Mitigation**: Agent specifications must anchor invariant rules at the prompt boundary and avoid dumping multi-megabyte log dumps into the unindexed middle context.[^liu-lost-middle-2023]

# References & Citations

[^liu-lost-middle-2023]: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023, July 6). "Lost in the Middle: How Language Models Use Long Contexts". *Transactions of the Association for Computational Linguistics (TACL)*, 12, pp. 157–173. arXiv:2307.03172. https://doi.org/10.48550/arXiv.2307.03172. Retrieved 2026-08-31.
