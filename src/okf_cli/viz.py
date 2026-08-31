from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from okf_cli.document import (
    OKFDocument,
    OKFDocumentError,
    is_stale,
    normalize_verified,
    trust_tier,
)

_INDEX_NAME = "index.md"
_LOG_NAME = "log.md"

_BASE_TYPE_PALETTE = {
    # Business & Strategy
    "Executive Memo": "#3b82f6",
    "Strategic Goal": "#2563eb",
    "Market Analysis": "#0284c7",
    "Decision Record": "#6366f1",
    # Research & Science
    "Research Compendium": "#8b5cf6",
    "Scientific Study": "#a855f7",
    "Methodology": "#7c3aed",
    # History & Narrative
    "Historical Event": "#d97706",
    "Archival Record": "#b45309",
    "Biography": "#f59e0b",
    # Entities
    "Entity Profile": "#10b981",
    "Organization": "#059669",
    "System": "#14b8a6",
    # Technical & Computations
    "Attested Computation": "#ef4444",
    "Metric": "#f43f5e",
    "Dataset": "#8b5cf6",
    "Table": "#3b82f6",
    "BigQuery Dataset": "#8b5cf6",
    "BigQuery Table": "#3b82f6",
    "Reference": "#10b981",
    "Playbook": "#06b6d4",
}

_PALETTE_COLORS = [
    "#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#06b6d4",
    "#ec4899", "#84cc16", "#14b8a6", "#6366f1", "#f97316", "#a855f7"
]


def _get_type_color(type_name: str) -> str:
    if type_name in _BASE_TYPE_PALETTE:
        return _BASE_TYPE_PALETTE[type_name]
    # Deterministic hash to palette color
    h = int(hashlib.md5(type_name.encode("utf-8")).hexdigest(), 16)
    return _PALETTE_COLORS[h % len(_PALETTE_COLORS)]


@dataclass
class ConceptNode:
    id: str
    type: str
    title: str
    description: str
    resource: str
    tags: list[str]
    body: str
    status: str = "stable"
    generated: dict[str, Any] = field(default_factory=dict)
    verified: list[dict[str, Any]] = field(default_factory=list)
    stale_after: str = ""
    sources: list[dict[str, Any]] = field(default_factory=list)
    trust_tier: str = "unverified"
    stale: bool = False
    links_to: list[str] = field(default_factory=list)

    def to_cytoscape_node(self) -> dict[str, Any]:
        color = _get_type_color(self.type)
        return {
            "data": {
                "id": self.id,
                "label": self.title or self.id,
                "type": self.type,
                "description": self.description,
                "resource": self.resource,
                "tags": self.tags,
                "status": self.status,
                "generated": self.generated,
                "verified": self.verified,
                "stale_after": self.stale_after,
                "sources": self.sources,
                "trust_tier": self.trust_tier,
                "stale": self.stale,
                "color": color,
                "size": 30 + min(60, len(self.body) // 200),
            }
        }


def _walk_concepts(bundle_root: Path) -> list[ConceptNode]:
    concepts: list[ConceptNode] = []
    bundle_root_resolved = bundle_root.resolve()

    for md_path in sorted(bundle_root.rglob("*.md")):
        if md_path.name in (_INDEX_NAME, _LOG_NAME) or md_path.name.startswith("."):
            continue
        rel = md_path.relative_to(bundle_root).with_suffix("")
        concept_id = "/".join(rel.parts)
        try:
            doc = OKFDocument.parse(md_path.read_text(encoding="utf-8"))
        except OKFDocumentError:
            continue

        fm = doc.frontmatter or {}
        tags = fm.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)]
        generated = fm.get("generated") if isinstance(fm.get("generated"), dict) else {}
        sources = fm.get("sources")
        if isinstance(sources, dict):
            sources = [sources]
        elif not isinstance(sources, list):
            sources = []

        concept = ConceptNode(
            id=concept_id,
            type=str(fm.get("type") or "Concept"),
            title=str(fm.get("title") or concept_id.split("/")[-1].replace("-", " ").title()),
            description=str(fm.get("description") or ""),
            resource=str(fm.get("resource") or ""),
            tags=[str(t) for t in tags],
            body=doc.body or "",
            status=str(fm.get("status") or "stable"),
            generated=generated or {},
            verified=normalize_verified(fm),
            stale_after=str(fm.get("stale_after") or ""),
            sources=[s for s in sources if isinstance(s, dict)],
            trust_tier=trust_tier(fm),
            stale=is_stale(fm),
            links_to=doc.extract_links(md_path, bundle_root_resolved),
        )
        concepts.append(concept)
    return concepts


def _build_graph(concepts: list[ConceptNode]) -> dict[str, Any]:
    ids = {c.id for c in concepts}
    nodes = [c.to_cytoscape_node() for c in concepts]
    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str]] = set()

    for c in concepts:
        for target in c.links_to:
            if target == c.id or target not in ids:
                continue
            key = (c.id, target)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append({
                "data": {
                    "id": f"{c.id}__{target}",
                    "source": c.id,
                    "target": target,
                }
            })

    bodies = {c.id: c.body for c in concepts}
    types = sorted({c.type for c in concepts})
    palette = {t: _get_type_color(t) for t in types}

    return {
        "nodes": nodes,
        "edges": edges,
        "bodies": bodies,
        "types": types,
        "palette": palette,
    }


def _load_asset_file(rel_path: str) -> str:
    path = Path(__file__).parent / "viewer" / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Viewer asset not found at {path}")
    return path.read_text(encoding="utf-8")


def generate_visualization(
    bundle_root: Path,
    out_path: Path | None = None,
    *,
    bundle_name: str | None = None,
) -> dict[str, int]:
    """Walk an OKF bundle and write a single self-contained HTML interactive graph visualization."""
    bundle_root = Path(bundle_root).resolve()
    if not bundle_root.is_dir():
        raise FileNotFoundError(f"Bundle directory not found: {bundle_root}")

    out_file = Path(out_path).resolve() if out_path else (bundle_root / "viz.html")
    concepts = _walk_concepts(bundle_root)
    graph = _build_graph(concepts)

    template = _load_asset_file("templates/viz.html")
    css = _load_asset_file("static/viz.css")
    js = _load_asset_file("static/viz.js")
    name = bundle_name or bundle_root.name.replace("-", " ").replace("_", " ").title()

    html = (
        template
        .replace("/*__VIZ_CSS__*/", css)
        .replace("/*__VIZ_JS__*/", js)
        .replace("__BUNDLE_NAME__", json.dumps(name))
        .replace("__BUNDLE_DATA__", json.dumps(graph, default=str))
    )

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")

    return {
        "concepts": len(concepts),
        "edges": len(graph["edges"]),
        "bytes": len(html.encode("utf-8")),
    }
