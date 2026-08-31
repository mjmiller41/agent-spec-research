---
type: Primary Source
title: "SGLang: Efficient Execution of Structured Language Model Programs"
description: "Companion markdown representation and technical summary of Zheng et al.'s research on RadixAttention and compressed FSM constrained decoding."
tags: [sglang, kv-cache, radix-attention, compressed-fsm, high-throughput]
status: stable
generated:
  by: research-agent/deep-research
  at: 2026-08-31T12:00:00Z
verified:
  - by: process:academic-verify
    at: 2026-08-31T12:00:00Z
sources:
  - id: zheng-sglang-2023
    resource: https://doi.org/10.48550/arXiv.2312.07104
    title: "SGLang: Efficient Execution of Structured Language Model Programs"
    author: Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, et al.
    last_modified: 2023-12-12T00:00:00Z
---

# Document Summary

Zheng et al. introduce **SGLang**, a co-designed frontend programming language and runtime execution engine engineered for high-throughput multi-call structured LLM programs.[^zheng-sglang-2023] By combining **RadixAttention** (prefix KV-cache sharing across complex branching agent trajectories) with **Compressed Finite-State Machines (FSMs)** for structured grammar decoding, SGLang achieves up to 6.4× higher execution throughput.[^zheng-sglang-2023]

# Technical Architecture

```mermaid
graph TD
    A[Structured Agent Program] --> B[SGLang Frontend Interpreter]
    B --> C[Radix Tree KV Cache Engine]
    C -->|Prefix Cache Hit| D[Zero-Compute Prompt Context Reuse]
    B --> E[Compressed FSM Token Masker]
    E -->|Pre-compiled Jump Transitions| F[Accelerated Constrained Logit Engine]
    D & F --> G[High-Throughput Multi-Agent Execution]
```
*Diagram 1: SGLang execution architecture showing RadixAttention and Compressed FSM jump decoding. Source: Zheng et al. (2023).*

## Core Findings & Innovations

1. **RadixAttention**: Maintains a radix tree of Key-Value caches across diverse prompt prefixes, allowing autonomous multi-turn agents to branch and backtrack with near-zero latency penalty.[^zheng-sglang-2023]
2. **Compressed FSM Jump Decoding**: Compresses consecutive deterministic token transitions into single jump steps, avoiding token-by-token mask recalculations during JSON decoding.[^zheng-sglang-2023]
3. **6.4× Throughput Improvement**: Outperforms conventional inference backends across JSON schema generation, retrieval-augmented pipelines, and multi-agent loops.[^zheng-sglang-2023]

# References & Citations

[^zheng-sglang-2023]: Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C. H., Cao, S., Christodoulou, C., Yang, E. K., Gonzalez, J. E., & Stoica, I. (2023, December 12). "SGLang: Efficient Execution of Structured Language Model Programs". *arXiv preprint*, arXiv:2312.07104. https://doi.org/10.48550/arXiv.2312.07104. Retrieved 2026-08-31.
