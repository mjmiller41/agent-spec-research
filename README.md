# Open Knowledge Format (OKF) — Agent Workspace

[![OKF Specification](https://img.shields.io/badge/OKF-v0.2-blue.svg)](SPEC.md)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE.md)

A platform-agnostic, AI-agent-native workspace and CLI toolkit for initializing, authoring, and maintaining multi-domain **Open Knowledge Format (OKF v0.2)** knowledge bundles.

---

## What is OKF?

The [Open Knowledge Format (OKF)](SPEC.md) is an open, human- and agent-friendly standard for representing knowledge: metadata, strategic context, historical narratives, scientific compendiums, and curated insights.

* **Human- and Agent-Readable**: Plain markdown files with clean YAML frontmatter.
* **Version-Controllable**: Native git workflows—pull requests, line diffs, and blame work out of the box.
* **Domain-Agnostic**: Works across business strategy, historical archives, scientific research, architecture decision records, legal policies, or data catalogs.
* **First-Class Trust & Provenance**: Queryable credibility signals, footnotes linked to sources, trust tiers, and freshness tracking.
* **Zero Vendor Lock-in**: No proprietary database or heavy runtime required.

---

## Quick Start

### 1. Install

```bash
# Clone the repository
git clone https://github.com/mjmiller41/cli-agent-okf.git
cd cli-agent-okf

# Create environment and install okf-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Initialize a Bundle

```bash
# Scaffold a fresh, minimal knowledge bundle in ./bundle
okf init --bundle ./bundle --title "Enterprise Strategy & Knowledge"
```

### 3. Scaffold Concepts from Templates

```bash
# List available templates
okf template list

# Create concepts
okf template executive_memo --out bundle/memos/q3-strategy.md
okf template research_compendium --out bundle/research/ai-alignment.md
okf template decision_log --out bundle/decisions/adr-001.md
```

### 4. Execute the Maintenance Chain

Whenever concepts are created, updated, or deprecated, run:

```bash
# Validate frontmatter, links, and footnotes
okf validate --bundle ./bundle

# Re-index all directories recursively
okf index --bundle ./bundle

# Record update in the chronological log
okf log Update "Added strategic market expansion memo" --bundle ./bundle

# Generate interactive graph visualization
okf viz --bundle ./bundle
```

Open `bundle/viz.html` in any browser to explore the force-directed knowledge graph with search, type filters, and detail views.

---

## Multi-Domain Examples

Explore the curated sample bundles in [`examples/`](examples/):

| Example Bundle | Domain | Highlights |
| :--- | :--- | :--- |
| [`examples/business_strategy/`](examples/business_strategy/) | **Business & Corporate Strategy** | Strategic memos, competitor profiles, OKRs, customer acquisition cost metrics. |
| [`examples/historical_archive/`](examples/historical_archive/) | **Historical Archive & Milestones** | Apollo 11 mission narrative, astronaut biographies, booster telemetry records. |
| [`examples/scientific_research/`](examples/scientific_research/) | **Scientific & Medical Compendium** | In vivo CRISPR-Cas9 delivery synthesis, preclinical trials, LNP assembly protocols. |
| [`examples/data_catalog/`](examples/data_catalog/) | **Technical Data Catalog** | GA4 e-commerce tables, event datasets, references, and SQL queries. |

---

## For AI Agents

When opening a session in this repository:
* Read [AGENTS.md](AGENTS.md) for full operational rules, taxonomy guidelines, and authoring contracts.
* Read [SPEC.md](SPEC.md) for the complete OKF v0.2 specification.

---

## Development & Testing

Run the test suite with `pytest`:

```bash
pytest
```

---

## License

This project is licensed under the [Apache 2.0 License](LICENSE.md).
