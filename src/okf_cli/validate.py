from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from okf_cli.document import OKFDocument, OKFDocumentError

_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))?$")
_VALID_STATUSES = {"draft", "stable", "deprecated"}


@dataclass
class ValidationIssue:
    file_path: Path
    level: str  # "ERROR" or "WARNING"
    message: str
    line: int | None = None


@dataclass
class ValidationReport:
    bundle_root: Path
    concepts_checked: int = 0
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.level == "ERROR"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.level == "WARNING"]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def _validate_iso_timestamp(ts: str) -> bool:
    if not isinstance(ts, str) or not ts.strip():
        return False
    if not _ISO_DATE_RE.match(ts.strip()):
        return False
    try:
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_bundle(bundle_root: Path, strict: bool = False) -> ValidationReport:
    bundle_root = Path(bundle_root).resolve()
    report = ValidationReport(bundle_root=bundle_root)

    if not bundle_root.is_dir():
        report.issues.append(
            ValidationIssue(
                file_path=bundle_root,
                level="ERROR",
                message=f"Bundle directory does not exist: {bundle_root}",
            )
        )
        return report

    all_md_files = list(bundle_root.rglob("*.md"))
    bundle_files_set = {p.resolve() for p in all_md_files}

    for md_path in sorted(all_md_files):
        rel_path = md_path.relative_to(bundle_root)
        filename = md_path.name

        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            report.issues.append(
                ValidationIssue(
                    file_path=rel_path,
                    level="ERROR",
                    message=f"Could not read file: {e}",
                )
            )
            continue

        if filename == "index.md":
            # Root index.md may have okf_version frontmatter; others must not.
            if md_path != bundle_root / "index.md":
                if content.strip().startswith("---"):
                    report.issues.append(
                        ValidationIssue(
                            file_path=rel_path,
                            level="ERROR",
                            message="Non-root index.md MUST NOT contain YAML frontmatter (OKF v0.2 §8).",
                        )
                    )
            continue

        if filename == "log.md":
            # Reserved update log format
            continue

        # Concept Document
        report.concepts_checked += 1
        try:
            doc = OKFDocument.parse(content)
        except OKFDocumentError as e:
            report.issues.append(
                ValidationIssue(
                    file_path=rel_path,
                    level="ERROR",
                    message=f"Invalid OKF document structure: {e}",
                )
            )
            continue

        fm = doc.frontmatter
        if not fm:
            report.issues.append(
                ValidationIssue(
                    file_path=rel_path,
                    level="ERROR",
                    message="Concept document is missing YAML frontmatter (OKF v0.2 §4).",
                )
            )
            continue

        # Check required type
        concept_type = fm.get("type")
        if not concept_type or not isinstance(concept_type, str) or not concept_type.strip():
            report.issues.append(
                ValidationIssue(
                    file_path=rel_path,
                    level="ERROR",
                    message="Missing or invalid required frontmatter key 'type' (OKF v0.2 §4.1).",
                )
            )

        # Check status if present
        status = fm.get("status")
        if status and status not in _VALID_STATUSES:
            report.issues.append(
                ValidationIssue(
                    file_path=rel_path,
                    level="ERROR",
                    message=f"Invalid status '{status}'. Must be one of {sorted(_VALID_STATUSES)} (OKF v0.2 §5.4).",
                )
            )

        # Check generated field
        generated = fm.get("generated")
        if generated is not None:
            if not isinstance(generated, dict):
                report.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="ERROR",
                        message="'generated' frontmatter must be a mapping with 'by' (and optional 'at') (OKF v0.2 §5.2).",
                    )
                )
            else:
                if "by" not in generated:
                    report.issues.append(
                        ValidationIssue(
                            file_path=rel_path,
                            level="ERROR",
                            message="'generated' is missing required 'by' actor string (OKF v0.2 §5.2).",
                        )
                    )
                if "at" in generated and not _validate_iso_timestamp(str(generated["at"])):
                    report.issues.append(
                        ValidationIssue(
                            file_path=rel_path,
                            level="ERROR" if strict else "WARNING",
                            message=f"'generated.at' value '{generated['at']}' is not a valid ISO 8601 timestamp.",
                        )
                    )

        # Check verified field
        verified = fm.get("verified")
        if verified is not None:
            verified_list = [verified] if isinstance(verified, dict) else verified
            if not isinstance(verified_list, list):
                report.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="ERROR",
                        message="'verified' frontmatter must be a mapping or list of mappings (OKF v0.2 §5.2).",
                    )
                )
            else:
                for item in verified_list:
                    if not isinstance(item, dict) or "by" not in item:
                        report.issues.append(
                            ValidationIssue(
                                file_path=rel_path,
                                level="ERROR",
                                message="Each 'verified' entry must include a 'by' actor string (OKF v0.2 §5.2).",
                            )
                        )
                    if isinstance(item, dict) and "at" in item and not _validate_iso_timestamp(str(item["at"])):
                        report.issues.append(
                            ValidationIssue(
                                file_path=rel_path,
                                level="ERROR" if strict else "WARNING",
                                message=f"'verified.at' value '{item.get('at')}' is not a valid ISO 8601 timestamp.",
                            )
                        )

        # Check stale_after
        stale_after = fm.get("stale_after")
        if stale_after and not _validate_iso_timestamp(str(stale_after)):
            report.issues.append(
                ValidationIssue(
                    file_path=rel_path,
                    level="ERROR" if strict else "WARNING",
                    message=f"'stale_after' value '{stale_after}' is not a valid ISO 8601 timestamp.",
                )
            )

        # Check sources and footnotes
        sources = fm.get("sources")
        source_ids: set[str] = set()
        if sources is not None:
            sources_list = [sources] if isinstance(sources, dict) else sources
            if not isinstance(sources_list, list):
                report.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="ERROR",
                        message="'sources' must be a list of source entries (OKF v0.2 §5.1).",
                    )
                )
            else:
                for s in sources_list:
                    if not isinstance(s, dict) or "resource" not in s:
                        report.issues.append(
                            ValidationIssue(
                                file_path=rel_path,
                                level="ERROR",
                                message="Each 'sources' entry must contain a 'resource' field (OKF v0.2 §5.1).",
                            )
                        )
                    elif "id" in s:
                        source_ids.add(str(s["id"]))

        # Check body footnotes match source IDs
        footnotes = doc.extract_footnotes()
        for fn in footnotes:
            if fn not in source_ids:
                report.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="WARNING" if not strict else "ERROR",
                        message=f"Footnote [^{fn}] does not match any source id in 'sources' frontmatter (OKF v0.2 §5.1).",
                    )
                )

        # Check Attested Computation requirements
        if concept_type == "Attested Computation":
            if "runtime" not in fm:
                report.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="ERROR",
                        message="'Attested Computation' concepts must specify a 'runtime' in frontmatter (OKF v0.2 §10.2).",
                    )
                )

        # Check internal link targets
        for link_target in doc.extract_links(md_path, bundle_root):
            target_path = (bundle_root / f"{link_target}.md").resolve()
            if target_path not in bundle_files_set:
                report.issues.append(
                    ValidationIssue(
                        file_path=rel_path,
                        level="WARNING" if not strict else "ERROR",
                        message=f"Target of internal link '{link_target}.md' was not found in bundle.",
                    )
                )

    return report
