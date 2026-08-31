from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from okf_cli.document import OKFDocument

_INDEX_FILE = "index.md"
_LOG_FILE = "log.md"


def _load_doc(path: Path) -> OKFDocument | None:
    try:
        return OKFDocument.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _build_index_body(
    entries: list[tuple[str, str, str, str]], is_root: bool = False, root_title: str = ""
) -> str:
    # entries: (type, title, relative_link, description)
    grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for typ, title, link, desc in entries:
        category = typ if typ else "Concepts"
        grouped[category].append((title, link, desc))

    sections: list[str] = []

    # Sort types, putting Subdirectories at the bottom if present
    types = [t for t in sorted(grouped) if t != "Subdirectories"]
    if "Subdirectories" in grouped:
        types.append("Subdirectories")

    for typ in types:
        lines = [f"# {typ}", ""]
        for title, link, desc in sorted(grouped[typ], key=lambda e: e[0].lower()):
            suffix = f" - {desc}" if desc else ""
            lines.append(f"* [{title}]({link}){suffix}")
        sections.append("\n".join(lines))

    return "\n\n".join(sections) + "\n"


def _directories_to_index(bundle_root: Path) -> list[Path]:
    dirs: set[Path] = {bundle_root}
    for md in bundle_root.rglob("*.md"):
        cur = md.parent
        while cur != bundle_root.parent:
            dirs.add(cur)
            if cur == bundle_root:
                break
            cur = cur.parent
    return sorted(dirs)


def regenerate_indexes(bundle_root: Path) -> list[Path]:
    """Recursively discover and regenerate index.md for all directories in the bundle."""
    bundle_root = Path(bundle_root).resolve()
    written: list[Path] = []
    if not bundle_root.exists():
        return written

    directories = sorted(
        _directories_to_index(bundle_root),
        key=lambda p: (-len(p.relative_to(bundle_root).parts), str(p)),
    )

    dir_descriptions: dict[Path, str] = {}

    for directory in directories:
        entries: list[tuple[str, str, str, str]] = []

        for child in sorted(directory.iterdir()):
            if child.name in (_INDEX_FILE, _LOG_FILE) or child.name.startswith("."):
                continue
            if child.is_file() and child.suffix == ".md":
                doc = _load_doc(child)
                if doc is None:
                    continue
                fm = doc.frontmatter or {}
                title = str(fm.get("title") or child.stem.replace("-", " ").replace("_", " ").title())
                desc = str(fm.get("description") or "")
                typ = str(fm.get("type") or "Concepts")
                entries.append((typ, title, child.name, desc))
            elif child.is_dir():
                # Only include subdirectories that contain at least one .md file
                if any(child.rglob("*.md")):
                    sub_desc = dir_descriptions.get(child, f"Directory containing {child.name} concepts.")
                    entries.append(
                        ("Subdirectories", child.name.replace("-", " ").replace("_", " ").title(), f"{child.name}/{_INDEX_FILE}", sub_desc)
                    )

        if not entries and directory != bundle_root:
            continue

        index_path = directory / _INDEX_FILE
        is_root = directory == bundle_root

        if is_root and index_path.exists():
            existing_doc = _load_doc(index_path)
            fm = existing_doc.frontmatter if existing_doc else {}
            if "okf_version" not in fm:
                fm["okf_version"] = "0.2"
            title = fm.get("title") or "Knowledge Bundle"
            desc = fm.get("description") or "Curated knowledge corpus adhering to OKF v0.2."
            fm["title"] = title
            fm["description"] = desc

            body_content = f"# Overview\n\n{desc}\n\n" + _build_index_body(entries, is_root=True)
            doc_to_write = OKFDocument(frontmatter=fm, body=body_content)
            index_path.write_text(doc_to_write.serialize(), encoding="utf-8")
        elif is_root:
            fm = {
                "okf_version": "0.2",
                "title": directory.name.replace("-", " ").replace("_", " ").title(),
                "description": "Curated knowledge corpus adhering to OKF v0.2.",
            }
            body_content = f"# Overview\n\n{fm['description']}\n\n" + _build_index_body(entries, is_root=True)
            doc_to_write = OKFDocument(frontmatter=fm, body=body_content)
            index_path.write_text(doc_to_write.serialize(), encoding="utf-8")
        else:
            # Non-root index.md MUST NOT contain frontmatter per OKF v0.2 §8
            dir_title = directory.name.replace("-", " ").replace("_", " ").title()
            body_content = f"# {dir_title} Index\n\n" + _build_index_body(entries, is_root=False)
            index_path.write_text(body_content, encoding="utf-8")

        written.append(index_path)

        # Build directory summary for parent index
        if directory != bundle_root:
            concept_count = len([e for e in entries if e[0] != "Subdirectories"])
            dir_descriptions[directory] = f"Contains {concept_count} concept(s)."

    return written
