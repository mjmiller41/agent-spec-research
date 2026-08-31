from __future__ import annotations

from pathlib import Path
import shutil


def _find_templates_dir() -> Path:
    # Check project root templates/ first, then fallback
    cwd_templates = Path.cwd() / "templates"
    if cwd_templates.is_dir():
        return cwd_templates
    repo_root_templates = Path(__file__).resolve().parent.parent.parent / "templates"
    if repo_root_templates.is_dir():
        return repo_root_templates
    return cwd_templates


def list_templates() -> list[str]:
    """Return available template names."""
    tdir = _find_templates_dir()
    if not tdir.is_dir():
        return []
    return sorted([f.stem for f in tdir.glob("*.md")])


def apply_template(template_name: str, target_path: Path, force: bool = False) -> Path:
    """Copy a template to target_path."""
    tdir = _find_templates_dir()
    src = tdir / f"{template_name}.md"
    if not src.exists():
        src = tdir / template_name
    if not src.exists():
        available = ", ".join(list_templates())
        raise FileNotFoundError(
            f"Template '{template_name}' not found. Available templates: {available}"
        )

    target_path = Path(target_path).resolve()
    if target_path.exists() and not force:
        raise FileExistsError(f"Target file already exists: {target_path}. Use --force to overwrite.")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, target_path)
    return target_path
