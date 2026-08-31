from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def init_bundle(
    bundle_path: Path,
    title: str = "Knowledge Bundle",
    description: str = "Curated multi-domain knowledge corpus adhering to OKF v0.2.",
    force: bool = False,
) -> tuple[Path, Path]:
    """Initialize a minimal, clean OKF bundle folder with index.md and log.md.

    Does NOT generate hardcoded concept subdirectories so the bundle remains
    open to any knowledge domain.
    """
    bundle_path = Path(bundle_path)
    bundle_path.mkdir(parents=True, exist_ok=True)

    index_path = bundle_path / "index.md"
    log_path = bundle_path / "log.md"

    if (index_path.exists() or log_path.exists()) and not force:
        raise FileExistsError(
            f"Bundle already initialized at '{bundle_path}'. Use --force to overwrite."
        )

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    index_content = f"""---
okf_version: "0.2"
title: {title}
description: {description}
---

# Overview

{description}

# Sections
"""

    log_content = f"""# Directory Update Log

## {today}
* **Initialization**: Initialized knowledge bundle `{title}` adhering to Open Knowledge Format (OKF) v0.2.
"""

    index_path.write_text(index_content, encoding="utf-8")
    log_path.write_text(log_content, encoding="utf-8")

    return index_path, log_path
