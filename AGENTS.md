# AGENTS.md: Universal AI Agent Operating Handbook

Welcome to the **Open Knowledge Format (OKF v0.2)** agent workspace. This repository is configured so that any CLI-based AI agent (e.g., Claude Code, Codex CLI, Antigravity, Aider, OpenCode, Goose, Cursor Agent) can autonomously initialize, author, and maintain a multi-domain knowledge corpus inside `./bundle/`.

---

## 1. Core Operating Principles

1. **Domain-Agnostic Knowledge**: The knowledge bundle in `./bundle/` can represent any domain—business strategy, historical archives, scientific research, architectural decision records, legal policies, entity profiles, or data catalogs.
2. **Minimal & Organic Taxonomy**: Do not force artificial directory structures. Subfolders inside `./bundle/` should be created dynamically based on what naturally organizes the specific domain (e.g., `bundle/memos/`, `bundle/events/`, `bundle/synthesis/`, `bundle/entities/`, `bundle/media/`).
3. **Mandatory Deep Research Engine**: Any research conducted to discover, synthesize, or expand knowledge for inclusion in the bundle **MUST use the `/deep-research` skill** installed in this repo (`.agents/skills/deep-research/SKILL.md` / `.claude/skills/deep-research`). Do not rely on shallow single-search lookups for multi-source knowledge synthesis.
4. **The Core Credibility Doctrine**:
   > **"It is better to be wrong with sources, than right without them."**
   * Strict adherence to sources and citations is critical to corpus credibility and must never be omitted.
   * Every factual claim, statistical figure, benchmark, historical event, technical specification, and direct quotation **MUST** be backed by a verifiable source.
   * Zero unsourced claims: if an assertion cannot be corroborated, it must either be grounded or explicitly marked as `[Hypothesis]` or `[Unverified Assumption]`.
5. **Wikipedia-Style Footnotes & Citations**: All final reports, compendiums, and concept documents must use inline reference markers (`[^source-id]`) tied to frontmatter `sources:` metadata and expanded in a full Wikipedia-style bibliographic footnote section (Author, Date, Title, Publisher/Journal, URL/DOI, Access Date).
6. **Rich Media & Visual Provenance**: Research documents should incorporate visual media (diagrams, architecture charts, photos, data plots, maps) whenever appropriate. Every embedded media asset **MUST** include complete attribution of author/creator, source, and license/rights in its caption.
7. **Digital Source Preservation & Companion Markdown**: Whenever research uncovers digital versions of primary/original sources (PDFs, papers, transcripts, reports, datasets), the original digital file **MUST** be copied into the bundle, and a companion `.md` concept document with inline images/media created in addition when necessary. Both files **MUST** strictly follow the standardized naming convention: `<document-title>_<author-name>_<year-published>.<ext>`.
8. **Strict OKF v0.2 Conformance**: All concept documents must follow the [OKF v0.2 Specification](SPEC.md).
9. **Deterministic Tooling**: The repo includes a zero-dependency CLI tool (`okf`) for validation, recursive indexing, changelog tracking, and graph visualization. **Always run the maintenance chain after modifying concepts.**

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

---

### SOP 2: Conducting Research with `/deep-research`
When gathering information or conducting investigations to author concepts for the bundle:

1. **Activate the Skill**: Read and execute the workflow defined in [`.agents/skills/deep-research/SKILL.md`](.agents/skills/deep-research/SKILL.md).
2. **Consult Detailed Phase Guidelines**:
   * **Phases 1–7 (Methodology & Evidence Loop)**: Follow [`.agents/skills/deep-research/reference/methodology.md`](.agents/skills/deep-research/reference/methodology.md).
   * **Phase 8 (Report Assembly & Structuring)**: Follow [`.agents/skills/deep-research/reference/report-assembly.md`](.agents/skills/deep-research/reference/report-assembly.md).
   * **Quality & Verification Gates**: Follow [`.agents/skills/deep-research/reference/quality-gates.md`](.agents/skills/deep-research/reference/quality-gates.md).
3. **Execute Research Phases**:
   * **Scope & Plan**: Define research questions, assumptions, and required evidence density (minimum 10+ sources for comprehensive topics).
   * **Retrieve & Triangulate**: Gather multi-perspective evidence from peer-reviewed literature, primary documentation, authoritative reporting, and official archives.
   * **Evidence Persistence**: Record retrieved items in `sources.jsonl`, extract concrete quotes/data in `evidence.jsonl`, and track atomic claim verification in `claims.jsonl`.
   * **Synthesize & Critique**: Structure the findings into a cohesive, analytical narrative with claim-level attribution.
4. **Format into OKF Concept**: Transform the synthesized research into an OKF v0.2 concept file under `./bundle/<category>/<topic>.md` adhering to the citation and media standards below.


---

### SOP 3: Scaffolding Concepts from Templates
Browse and scaffold concepts using built-in templates from `templates/`:
```bash
# List available templates:
okf template list

# Scaffold a concept:
okf template research_compendium --out bundle/synthesis/crispr-delivery.md
okf template primary_source --out bundle/sources/in_vivo_crispr_delivery_doudna_2024.md
okf template executive_memo --out bundle/memos/q3-strategy.md
okf template historical_narrative --out bundle/events/apollo-11.md
okf template decision_log --out bundle/decisions/adr-001.md
okf template generic_concept --out bundle/topics/overview.md
```

---

### SOP 4: Concept Authoring & Wikipedia-Style Citation Standards
Every concept document (`bundle/<folder>/<concept>.md`) must be UTF-8 markdown with YAML frontmatter containing provenance metadata, inline footnote markers, and full Wikipedia-style footnote definitions:

```markdown
---
type: Research Compendium              # REQUIRED: Concept type name
title: In Vivo CRISPR-Cas9 Delivery    # Recommended display name
description: Comprehensive synthesis of vector delivery platforms.
tags: [crispr, gene-editing, nanomedicine]
status: stable                        # draft | stable | deprecated (default: stable)
generated:
  by: research-agent/deep-research     # Actor convention: <producer>/<version>
  at: 2026-08-31T12:00:00Z            # ISO 8601 UTC timestamp
verified:
  - by: human:lead-investigator       # human:<id> or process:<id>
    at: 2026-08-31T14:00:00Z
sources:                              # Provenance list (join keys for footnotes)
  - id: doudna-nature-2024
    resource: https://doi.org/10.1038/s41586-024-07100-1
    title: Precision Genome Editing in Human Therapeutics
    author: Jennifer Doudna et al.
    last_modified: 2024-03-15T00:00:00Z
  - id: fda-guidance-2025
    resource: https://www.fda.gov/regulatory-information/gene-therapy-guidance-2025
    title: Human Gene Therapy Products Incorporating Genome Editing
    author: U.S. Food and Drug Administration (FDA)
    last_modified: 2025-01-10T00:00:00Z
---

# Executive Summary

Therapeutic translation of CRISPR-Cas9 relies critically on tissue-specific delivery modalities that minimize immunogenicity and off-target cleavages.[^doudna-nature-2024] The FDA's updated regulatory framework establishes accelerated preclinical pathways for non-viral lipid nanoparticle (LNP) formulations.[^fda-guidance-2025]

# Key Findings

1. **LNP Efficiency**: Lipid nanoparticle formulations demonstrated a 94.2% delivery efficiency in hepatic target tissues with transient mRNA expression lasting under 48 hours.[^doudna-nature-2024]
2. **Regulatory Milestones**: Phase I/II safety trial thresholds require comprehensive off-target cleavage assays across at least three independent donor cohorts.[^fda-guidance-2025]

# Visual Architecture & Schematics

![Figure 1: Comparison of viral vs. non-viral CRISPR delivery modalities.](file:///bundle/media/crispr-delivery-vectors.png)
*Figure 1: Architectural comparison between AAV viral capsids and ionizable lipid nanoparticles. Source: Nature Biotechnology / Doudna Lab (2024). License: CC BY 4.0.*

# Relationships & Cross-Links

* [LNP Assembly Protocol](/methodologies/lipid-nanoparticles.md)
* [Clinical Trial Benchmarks](/studies/clinical-trials-2025.md)

# References & Citations

[^doudna-nature-2024]: Doudna, J., Weissman, I., & Chen, K. (2024). "Precision Genome Editing in Human Therapeutics". *Nature*, 628(8007), pp. 301–315. https://doi.org/10.1038/s41586-024-07100-1. Retrieved 2026-08-31.
[^fda-guidance-2025]: U.S. Food and Drug Administration (FDA) (2025, January 10). "Human Gene Therapy Products Incorporating Human Genome Editing: Guidance for Industry". *FDA Center for Biologics Evaluation and Research*. https://www.fda.gov/regulatory-information/gene-therapy-guidance-2025. Retrieved 2026-08-31.
```

#### Wikipedia-Style Footnote Format Reference:
* **Academic Journals / Papers**:
  `[^id]: Author(s) (Year). "Article Title". *Journal Name*, Volume(Issue), Pages. DOI/URL. Retrieved YYYY-MM-DD.`
* **Books / Monographs**:
  `[^id]: Author(s) (Year). *Book Title* (Edition). Publisher, Location. ISBN/URL. Retrieved YYYY-MM-DD.`
* **Websites / Institutional Reports / Whitepapers**:
  `[^id]: Author or Organization (Year, Month Day). "Document or Page Title". *Publisher / Website Name*. URL. Retrieved YYYY-MM-DD.`
* **Primary Sources / Datasets / Telemetry Logs**:
  `[^id]: Creator / Agency (Year). "Dataset or Log Title" [Data set / Official Record]. Repository / Archive. URL. Retrieved YYYY-MM-DD.`

---

### SOP 5: Embedding Media & Visual Assets with Attribution
Agents should enrich concepts with diagrams, architecture graphs, data charts, and photos to provide visual clarity.

1. **Storage Location**: Place visual assets in `bundle/media/` or reference canonical, permanent URLs.
2. **Embedding Syntax**: Use standard markdown image syntax:
   ```markdown
   ![Figure Description](file:///bundle/media/filename.png)
   *Figure N: Caption explaining the asset. Source: [Author/Organization] ([Year]). License/Rights: [CC BY 4.0 / Public Domain / Fair Use / Internal Documentation].*
   ```
3. **Diagrams via Mermaid**: For architectural schemas or workflows, use native Mermaid blocks followed by an attribution note:
   ```markdown
   ```mermaid
   graph TD
       A[Target DNA] --> B[Cas9/gRNA Complex]
       B --> C[Double-Strand Break]
       C --> D[Homology-Directed Repair]
   ```
   *Diagram 1: Cas9 cleavage and repair mechanism. Generated by Deep Research Agent (2026).*
   ```

---

### SOP 6: Ingesting & Preserving Digital Primary Sources
When research discovers digital versions of primary/original source documents (e.g. PDF papers, governmental reports, historical transcripts, technical specs, whitepapers, dataset dumps):

1. **Copy Raw Artifact to Bundle**:
   Save the original raw file (e.g., `.pdf`, `.txt`, `.csv`, `.json`, `.docx`) into `bundle/sources/` or `bundle/references/`.
2. **Generate Companion Markdown Representation**:
   Create a companion `.md` concept document (scaffolded via `okf template primary_source`) providing a full-text markdown rendering, structured excerpts, and inline images/figures extracted from the document.
3. **Strict File Naming Convention**:
   Both the raw artifact and its companion `.md` file **MUST** be named using the standard pattern:
   ```text
   <document-title>_<author-name>_<year-published>.<ext>
   ```
   * **`<document-title>`**: Descriptive slug in snake_case (e.g., `in_vivo_crispr_delivery`, `apollo_11_mission_report`, `enterprise_saas_adoption`).
   * **`<author-name>`**: Primary author or issuing organization in snake_case (e.g., `doudna`, `nasa`, `gartner`, `federal_reserve`).
   * **`<year-published>`**: 4-digit publication year (e.g., `2024`, `1969`, `2026`).

   *Paired File Examples*:
   * Raw PDF: `bundle/sources/in_vivo_crispr_delivery_doudna_2024.pdf`
   * Companion MD: `bundle/sources/in_vivo_crispr_delivery_doudna_2024.md`
   * Raw Transcript: `bundle/sources/apollo_11_air_to_ground_transcript_nasa_1969.txt`
   * Companion MD: `bundle/sources/apollo_11_air_to_ground_transcript_nasa_1969.md`
   * Raw Report: `bundle/sources/enterprise_saas_adoption_gartner_2026.pdf`
   * Companion MD: `bundle/sources/enterprise_saas_adoption_gartner_2026.md`

---

### SOP 7: The Post-Edit Maintenance Chain
Whenever you add, modify, or deprecate concepts in `./bundle/`, you **MUST execute the maintenance chain**:

```bash
# 1. Validate bundle syntax, links, and footnotes (strict mode checks all warnings)
okf validate --bundle ./bundle --strict

# 2. Regenerate all index.md files recursively
okf index --bundle ./bundle

# 3. Log your change in log.md
okf log Update "Ingested digital primary sources and updated research synthesis" --bundle ./bundle

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


