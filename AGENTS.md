# AGENTS.md: Universal AI Agent Operating Handbook

Welcome to the **Open Knowledge Format (OKF v0.2)** agent workspace. This repository is configured so that any CLI-based AI agent (e.g., Claude Code, Codex CLI, Antigravity, Aider, OpenCode, Goose, Cursor Agent) can autonomously initialize, author, and maintain a multi-domain knowledge corpus inside `./bundle/`.

---

## 1. Core Operating Principles

1. **Domain-Agnostic Knowledge**: The knowledge bundle in `./bundle/` can represent any domain—business strategy, historical archives, scientific research, architectural decision records, legal policies, entity profiles, or data catalogs.
2. **Minimal & Organic Taxonomy**: Do not force artificial directory structures. Subfolders inside `./bundle/` should be created dynamically based on what naturally organizes the specific domain (e.g., `bundle/memos/`, `bundle/events/`, `bundle/studies/`, `bundle/entities/`).
3. **Strict OKF v0.2 Conformance**: All concept documents must follow the [OKF v0.2 Specification](SPEC.md).
4. **Deterministic Tooling**: The repo includes a zero-dependency CLI tool (`okf`) for validation, recursive indexing, changelog tracking, and graph visualization. **Always run the maintenance chain after modifying concepts.**

---

## 2. Standard Operating Procedures (SOPs)

### SOP 1: Initializing a New Bundle
If `./bundle/` does not exist or needs initialization:
```bash
# Using virtualenv CLI or python module:
okf init --bundle ./bundle --title "Domain Title" --description "Summary of domain corpus"
# Or:
python -m okf_cli.cli init --bundle ./bundle --title "Domain Title" --description "Summary of domain corpus"
```
This generates:
* `bundle/index.md` (root progressive-disclosure index with `okf_version: "0.2"`)
* `bundle/log.md` (initial update log)

### SOP 2: Scaffolding Concepts from Templates
Browse and scaffold concepts using built-in templates from `templates/`:
```bash
# List available templates:
okf template list

# Scaffold a concept:
okf template executive_memo --out bundle/memos/q3-strategy.md
okf template research_compendium --out bundle/synthesis/crispr-delivery.md
okf template historical_narrative --out bundle/events/apollo-11.md
okf template decision_log --out bundle/decisions/adr-001.md
okf template generic_concept --out bundle/topics/overview.md
```

### SOP 3: Concept Authoring Standards
Every concept document (`bundle/<folder>/<concept>.md`) must be UTF-8 markdown with YAML frontmatter:

```markdown
---
type: Executive Memo                  # REQUIRED: Concept type name (any descriptive string)
title: Q3 International Expansion     # Recommended display name
description: Strategic roadmap...     # Recommended one-line summary
tags: [strategy, europe, q3]          # Optional tags
status: stable                        # draft | stable | deprecated (default: stable)
generated:
  by: strategy-agent/claude-3.7-sonnet # Actor convention: <producer>/<version>
  at: 2026-08-31T12:00:00Z            # ISO 8601 UTC timestamp
verified:
  - by: human:cso                     # human:<id> or process:<id>
    at: 2026-08-31T14:00:00Z
sources:                              # Provenance list
  - id: market-report-2026            # Stable join key for footnotes
    resource: https://example.com/rep # Canonical URI or path
    title: Global Market Dynamics     # Human-readable source title
    author: Analyst Group             # Author or organization
    last_modified: 2026-08-01T00:00:00Z
---

# Overview

Primary narrative goes here. Every verifiable factual claim should be cited using footnote syntax.[^market-report-2026]

# Relationships & Cross-Links

Link to neighboring concepts using bundle-relative paths (starting with `/`):
* [Customer Acquisition Cost](/metrics/customer-acquisition-cost.md)
* [Target Competitor](/competitors/acme-corp.md)

[^market-report-2026]: Global Market Dynamics
```

### SOP 4: The Post-Edit Maintenance Chain
Whenever you add, modify, or deprecate concepts in `./bundle/`, you **MUST execute the maintenance chain**:

```bash
# 1. Validate bundle syntax, links, and footnotes
okf validate --bundle ./bundle

# 2. Regenerate all index.md files recursively
okf index --bundle ./bundle

# 3. Log your change in log.md
okf log Update "Added market expansion memo and updated CAC links" --bundle ./bundle

# 4. Refresh the interactive graph visualization
okf viz --bundle ./bundle
```

---

## 3. CLI Command Reference

| Command | Usage | Description |
| :--- | :--- | :--- |
| `okf init` | `okf init [--bundle <dir>] [--title <t>] [--desc <d>]` | Scaffolds a clean bundle with `index.md` & `log.md`. |
| `okf template` | `okf template [list \| <name> --out <path>]` | Lists or copies templates from `templates/`. |
| `okf validate` | `okf validate [--bundle <dir>] [--strict]` | Lints frontmatter YAML, dates, footnote joins, and link targets. |
| `okf index` | `okf index [--bundle <dir>]` | Recursively updates all `index.md` directory indices. |
| `okf log` | `okf log <Action> <Message> [--bundle <dir>]` | Appends a structured changelog entry under today's date in `log.md`. |
| `okf viz` | `okf viz [--bundle <dir>] [--out <path>]` | Generates a zero-dependency interactive HTML graph viewer (`viz.html`). |

---

## 4. Multi-Domain Reference Examples

Refer to the curated example bundles in `examples/` for architectural guidance:
* `examples/business_strategy/` - Corporate memos, competitor profiles, OKRs, financial metrics.
* `examples/historical_archive/` - Historical events, biographies, telemetry records, primary sources.
* `examples/scientific_research/` - Research compendiums, study records, methodology protocols.
* `examples/data_catalog/` - Data assets, schemas, SQL computations, and table dictionaries.
