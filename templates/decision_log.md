---
type: Decision Record
title: "ADR-001: Adoption of Open Knowledge Format for Universal Context"
description: Architectural Decision Record capturing context, options evaluated, rationale, and consequences.
tags: [adr, architecture, engineering, decision]
status: stable
generated:
  by: architect-agent/claude-3.7-sonnet
  at: 2026-08-31T08:00:00Z
verified:
  - by: human:lead-architect
    at: 2026-08-31T08:30:00Z
sources:
  - id: okf-spec-v02
    resource: /SPEC.md
    title: Open Knowledge Format Specification v0.2
    author: Google Cloud & Open Source Community
---

# Context & Problem Statement

Modern AI agent workflows require context to be human-readable, version-controlled via git, easily diffed in code review, and portable across LLM providers without proprietary vendor lock-in.[^okf-spec-v02]

# Decision Drivers

* Support for progressive disclosure without loading massive corpora into memory.
* Explicit provenance tracking with per-claim attribution.
* Zero external proprietary database requirements for knowledge storage.

# Considered Options

1. **Option 1: Vector Database with Custom JSON API**
2. **Option 2: Git-backed Markdown with YAML Frontmatter (OKF v0.2)**
3. **Option 3: Proprietary SaaS Knowledge Base**

# Decision Outcome

Chosen option: **Option 2 (OKF v0.2)**, because it integrates seamlessly with developer git workflows, provides instant human readability, and decouples knowledge authoring from specific model harnesses.[^okf-spec-v02]

# Positive Consequences

* Engineers can use `git blame`, pull requests, and standard markdown tools.
* Agents can navigate hierarchical indices progressively.
* Self-contained interactive graph visualizations can be generated offline.

# Negative & Mitigated Consequences

* Graph queries over large corpora require local filesystem walks or precomputed index files. (Mitigated by `okf index` and `okf viz`).

[^okf-spec-v02]: Open Knowledge Format Specification v0.2
