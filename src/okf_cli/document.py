from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# OKF v0.2 §11: `type` is the only always-required frontmatter key.
REQUIRED_FRONTMATTER_KEYS = ("type",)
_FRONTMATTER_DELIM = "---"
_LINK_RE = re.compile(r"\]\(([^)\s]+\.md)(?:#[A-Za-z0-9_\-]*)?\)")
_FOOTNOTE_RE = re.compile(r"\[\^([A-Za-z0-9_\-]+)\]")


class _Loader(yaml.SafeLoader):
    """SafeLoader that leaves timestamps as the text the author wrote."""


_Loader.yaml_implicit_resolvers = {
    ch: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for ch, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


class OKFDocumentError(ValueError):
    """Raised when an OKF document is malformed or invalid."""


@dataclass
class OKFDocument:
    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""

    @classmethod
    def parse(cls, text: str) -> "OKFDocument":
        lines = text.splitlines()
        if not lines or lines[0].strip() != _FRONTMATTER_DELIM:
            return cls(frontmatter={}, body=text)

        end_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == _FRONTMATTER_DELIM:
                end_idx = i
                break
        if end_idx is None:
            raise OKFDocumentError("Unterminated YAML frontmatter block")

        fm_text = "\n".join(lines[1:end_idx])
        try:
            fm = yaml.load(fm_text, Loader=_Loader) or {}
        except yaml.YAMLError as e:
            raise OKFDocumentError(f"Invalid YAML in frontmatter: {e}") from e
        if not isinstance(fm, dict):
            raise OKFDocumentError("Frontmatter must be a YAML mapping")

        body = "\n".join(lines[end_idx + 1 :])
        if body.startswith("\n"):
            body = body[1:]
        return cls(frontmatter=fm, body=body)

    def serialize(self) -> str:
        fm_text = yaml.safe_dump(
            self.frontmatter, sort_keys=False, allow_unicode=True
        ).rstrip()
        body = self.body if self.body.endswith("\n") else self.body + "\n"
        return f"{_FRONTMATTER_DELIM}\n{fm_text}\n{_FRONTMATTER_DELIM}\n\n{body}"

    def validate(self) -> None:
        missing = [k for k in REQUIRED_FRONTMATTER_KEYS if not self.frontmatter.get(k)]
        if missing:
            raise OKFDocumentError(
                f"Missing required frontmatter keys: {', '.join(missing)}"
            )

    def extract_links(self, doc_path: Path, bundle_root: Path) -> list[str]:
        """Extract valid target concept IDs referenced via markdown links."""
        out: list[str] = []
        seen: set[str] = set()
        bundle_root_resolved = bundle_root.resolve()
        doc_dir = doc_path.parent.resolve()

        for m in _LINK_RE.finditer(self.body):
            target = m.group(1).strip()
            if "://" in target or target.startswith("mailto:"):
                continue
            if target.startswith("/"):
                # Absolute within bundle: /tables/orders.md -> tables/orders
                clean = target.lstrip("/")
                if clean.endswith(".md"):
                    clean = clean[:-3]
                if clean and clean not in seen:
                    seen.add(clean)
                    out.append(clean)
            else:
                # Relative to current doc_dir
                try:
                    resolved = (doc_dir / target).resolve().relative_to(bundle_root_resolved)
                    rel = resolved.as_posix()
                    if rel.endswith(".md"):
                        rel = rel[:-3]
                    if rel and rel not in seen:
                        seen.add(rel)
                        out.append(rel)
                except ValueError:
                    continue
        return out

    def extract_footnotes(self) -> list[str]:
        """Extract footnote keys like [^source-id] used in body."""
        return [m.group(1) for m in _FOOTNOTE_RE.finditer(self.body)]


def normalize_verified(frontmatter: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the `verified` events as a list (OKF v0.2 §5.2)."""
    verified = frontmatter.get("verified")
    if verified is None:
        return []
    if isinstance(verified, dict):
        return [verified]
    if isinstance(verified, list):
        return [v for v in verified if isinstance(v, dict)]
    return []


def trust_tier(frontmatter: dict[str, Any]) -> str:
    """Derive a concept's trust tier from `verified` (OKF v0.2 §5.3)."""
    events = normalize_verified(frontmatter)
    if not events:
        return "unverified"
    for event in events:
        by = str(event.get("by") or "")
        if by.startswith("human:"):
            return "human-reviewed"
    return "machine-confirmed"


def is_stale(frontmatter: dict[str, Any], now: datetime | None = None) -> bool:
    """Whether a concept is stale per `stale_after` (OKF v0.2 §5.5)."""
    raw = str(frontmatter.get("stale_after") or "")
    if not raw or "T" not in raw:
        return False
    try:
        stale_after = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return False
    if stale_after.tzinfo is None:
        return False
    current_time = now or datetime.now(timezone.utc)
    return current_time >= stale_after
