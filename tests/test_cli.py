from __future__ import annotations

from pathlib import Path
import pytest
from okf_cli.document import OKFDocument
from okf_cli.init import init_bundle
from okf_cli.validate import validate_bundle
from okf_cli.index import regenerate_indexes
from okf_cli.log import append_log
from okf_cli.viz import generate_visualization
from okf_cli.template import list_templates, apply_template
from okf_cli.cli import main


def test_init_and_validate(tmp_path: Path):
    bundle_dir = tmp_path / "bundle"
    init_bundle(bundle_dir, title="My Custom Bundle", description="Test Description")

    assert (bundle_dir / "index.md").exists()
    assert (bundle_dir / "log.md").exists()

    report = validate_bundle(bundle_dir)
    assert report.is_valid
    assert len(report.errors) == 0


def test_add_concepts_and_index(tmp_path: Path):
    bundle_dir = tmp_path / "bundle"
    init_bundle(bundle_dir)

    memos_dir = bundle_dir / "memos"
    memos_dir.mkdir()

    memo_file = memos_dir / "q3_memo.md"
    memo_file.write_text(
        """---
type: Executive Memo
title: Q3 Strategic Update
description: Quarterly executive briefing.
sources:
  - id: src1
    resource: https://example.com/data
---

# Executive Summary

Key metrics and initiatives.[^src1]
""",
        encoding="utf-8",
    )

    written = regenerate_indexes(bundle_dir)
    assert len(written) == 2  # memos/index.md and bundle/index.md

    root_index = (bundle_dir / "index.md").read_text(encoding="utf-8")
    root_doc = OKFDocument.parse(root_index)
    assert root_doc.frontmatter.get("okf_version") == "0.2"
    assert "Memos" in root_index

    # Check viz generation
    stats = generate_visualization(bundle_dir)
    assert stats["concepts"] == 1
    assert (bundle_dir / "viz.html").exists()


def test_log_append(tmp_path: Path):
    bundle_dir = tmp_path / "bundle"
    init_bundle(bundle_dir)

    append_log(bundle_dir, message="Added Q3 memo", action="Creation", date_str="2026-08-31")
    append_log(bundle_dir, message="Updated figures", action="Update", date_str="2026-08-31")

    log_text = (bundle_dir / "log.md").read_text(encoding="utf-8")
    assert "## 2026-08-31" in log_text
    assert "* **Creation**: Added Q3 memo" in log_text
    assert "* **Update**: Updated figures" in log_text


def test_template_operations(tmp_path: Path):
    templates = list_templates()
    assert len(templates) > 0
    assert "executive_memo" in templates

    out_file = tmp_path / "new_memo.md"
    apply_template("executive_memo", out_file)
    assert out_file.exists()
    assert "type: Executive Memo" in out_file.read_text(encoding="utf-8")


def test_cli_subcommands(tmp_path: Path, monkeypatch):
    bundle_dir = tmp_path / "cli_bundle"
    
    # okf init
    ret = main(["init", "--bundle", str(bundle_dir), "--title", "CLI Bundle"])
    assert ret == 0

    # okf template
    concept_path = bundle_dir / "memo.md"
    ret = main(["template", "generic_concept", "--out", str(concept_path)])
    assert ret == 0

    # okf log
    ret = main(["log", "Creation", "Created test memo", "--bundle", str(bundle_dir)])
    assert ret == 0

    # okf index
    ret = main(["index", "--bundle", str(bundle_dir)])
    assert ret == 0

    # okf validate
    ret = main(["validate", "--bundle", str(bundle_dir)])
    assert ret == 0

    # okf viz
    ret = main(["viz", "--bundle", str(bundle_dir)])
    assert ret == 0
