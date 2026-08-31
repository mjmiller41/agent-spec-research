from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def append_log(
    bundle_root: Path,
    message: str,
    action: str = "Update",
    date_str: str | None = None,
) -> Path:
    """Append a structured changelog entry to log.md (OKF v0.2 §9)."""
    bundle_root = Path(bundle_root).resolve()
    log_path = bundle_root / "log.md"

    today = date_str or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    clean_action = action.strip().capitalize()
    clean_message = message.strip()

    entry_line = f"* **{clean_action}**: {clean_message}"
    date_header = f"## {today}"

    if not log_path.exists():
        content = f"# Directory Update Log\n\n{date_header}\n{entry_line}\n"
        log_path.write_text(content, encoding="utf-8")
        return log_path

    text = log_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Look for existing date header
    date_idx = None
    for i, line in enumerate(lines):
        if line.strip() == date_header:
            date_idx = i
            break

    if date_idx is not None:
        # Insert entry line right after the date header (or after existing entries under this date)
        lines.insert(date_idx + 1, entry_line)
    else:
        # Insert new date header and entry after the top title
        insert_idx = 1
        for i, line in enumerate(lines):
            if line.startswith("# "):
                insert_idx = i + 1
                break
        new_block = ["", date_header, entry_line]
        lines = lines[:insert_idx] + new_block + lines[insert_idx:]

    output = "\n".join(lines).strip() + "\n"
    log_path.write_text(output, encoding="utf-8")
    return log_path
