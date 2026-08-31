from __future__ import annotations

from datetime import datetime, timezone
import pytest
from okf_cli.document import (
    OKFDocument,
    OKFDocumentError,
    normalize_verified,
    trust_tier,
    is_stale,
)


def test_parse_valid_okf_document():
    text = """---
type: Executive Memo
title: Test Title
description: Test Description
tags: [tag1, tag2]
generated:
  by: agent/test
  at: 2026-08-31T12:00:00Z
verified:
  - by: human:reviewer
    at: 2026-08-31T12:00:00Z
---

# Overview

Sample body with [link](/section/target.md) and citation.[^src1]
"""
    doc = OKFDocument.parse(text)
    assert doc.frontmatter["type"] == "Executive Memo"
    assert doc.frontmatter["title"] == "Test Title"
    assert "Sample body with [link]" in doc.body
    assert doc.extract_footnotes() == ["src1"]


def test_document_validation():
    doc = OKFDocument(frontmatter={"type": "Concept"}, body="# Hello")
    doc.validate()

    doc_invalid = OKFDocument(frontmatter={"title": "Missing Type"}, body="# Hello")
    with pytest.raises(OKFDocumentError):
        doc_invalid.validate()


def test_trust_tier():
    assert trust_tier({}) == "unverified"
    assert trust_tier({"verified": [{"by": "process:nightly", "at": "2026-08-31T00:00:00Z"}]}) == "machine-confirmed"
    assert trust_tier({"verified": {"by": "human:reviewer", "at": "2026-08-31T00:00:00Z"}}) == "human-reviewed"


def test_is_stale():
    assert not is_stale({})
    # Future date
    assert not is_stale({"stale_after": "2099-01-01T00:00:00Z"}, now=datetime(2026, 8, 31, tzinfo=timezone.utc))
    # Past date
    assert is_stale({"stale_after": "2020-01-01T00:00:00Z"}, now=datetime(2026, 8, 31, tzinfo=timezone.utc))
