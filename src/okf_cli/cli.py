from __future__ import annotations

import argparse
import sys
from pathlib import Path

from okf_cli.init import init_bundle
from okf_cli.validate import validate_bundle
from okf_cli.index import regenerate_indexes
from okf_cli.log import append_log
from okf_cli.viz import generate_visualization
from okf_cli.template import list_templates, apply_template


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="okf",
        description="Platform-agnostic CLI toolkit for Open Knowledge Format (OKF v0.2) bundles",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    init_cmd = sub.add_parser("init", help="Initialize a clean minimal OKF bundle in ./bundle")
    init_cmd.add_argument(
        "--bundle", "-b", type=Path, default=Path("./bundle"),
        help="Path to the bundle directory (default: ./bundle)",
    )
    init_cmd.add_argument(
        "--title", "-t", default="Knowledge Bundle",
        help="Display title of the knowledge bundle",
    )
    init_cmd.add_argument(
        "--description", "-d",
        default="Curated multi-domain knowledge corpus adhering to OKF v0.2.",
        help="Brief overview summary of the bundle",
    )
    init_cmd.add_argument(
        "--force", "-f", action="store_true",
        help="Overwrite existing index.md/log.md files",
    )

    # validate
    val_cmd = sub.add_parser("validate", help="Validate an OKF bundle against OKF v0.2 specification")
    val_cmd.add_argument(
        "--bundle", "-b", type=Path, default=Path("./bundle"),
        help="Path to the bundle directory (default: ./bundle)",
    )
    val_cmd.add_argument(
        "--strict", "-s", action="store_true",
        help="Treat warnings as errors (e.g. broken links, invalid timestamp formats)",
    )

    # index
    idx_cmd = sub.add_parser("index", help="Recursively generate and update index.md for all directories")
    idx_cmd.add_argument(
        "--bundle", "-b", type=Path, default=Path("./bundle"),
        help="Path to the bundle directory (default: ./bundle)",
    )

    # log
    log_cmd = sub.add_parser("log", help="Append a structured changelog entry to log.md")
    log_cmd.add_argument("action", help="Action label (e.g. Update, Creation, Deprecation, Review)")
    log_cmd.add_argument("message", help="Description of the change or concept updated")
    log_cmd.add_argument(
        "--bundle", "-b", type=Path, default=Path("./bundle"),
        help="Path to the bundle directory (default: ./bundle)",
    )

    # viz
    viz_cmd = sub.add_parser("viz", help="Generate self-contained interactive HTML graph visualization")
    viz_cmd.add_argument(
        "--bundle", "-b", type=Path, default=Path("./bundle"),
        help="Path to the bundle directory (default: ./bundle)",
    )
    viz_cmd.add_argument(
        "--out", "-o", type=Path, default=None,
        help="Output HTML path (default: <bundle>/viz.html)",
    )
    viz_cmd.add_argument(
        "--name", "-n", default=None,
        help="Display name for the bundle header in the viewer",
    )

    # template
    tpl_cmd = sub.add_parser("template", help="Scaffold concepts from reusable templates")
    tpl_cmd.add_argument(
        "name", nargs="?", default=None,
        help="Template name (run 'okf template' without arguments to list)",
    )
    tpl_cmd.add_argument(
        "--out", "-o", type=Path, default=None,
        help="Target output file path",
    )
    tpl_cmd.add_argument(
        "--force", "-f", action="store_true",
        help="Overwrite target file if it already exists",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        try:
            idx, log = init_bundle(
                args.bundle, title=args.title, description=args.description, force=args.force
            )
            print(f"Initialized OKF bundle at: {args.bundle.resolve()}")
            print(f"  ├── {idx.name}")
            print(f"  └── {log.name}")
            return 0
        except Exception as e:
            print(f"Error initializing bundle: {e}", file=sys.stderr)
            return 1

    if args.command == "validate":
        report = validate_bundle(args.bundle, strict=args.strict)
        print(f"Validated bundle at '{args.bundle}' ({report.concepts_checked} concept documents checked)")
        if report.issues:
            for issue in report.issues:
                prefix = f"[{issue.level}]"
                print(f"  {prefix} {issue.file_path}: {issue.message}", file=sys.stderr if issue.level == "ERROR" else sys.stdout)
        
        if report.errors or (args.strict and report.warnings):
            print(f"\nFAILED: {len(report.errors)} error(s), {len(report.warnings)} warning(s)", file=sys.stderr)
            return 1
        print(f"\nPASSED: 0 errors, {len(report.warnings)} warning(s)")
        return 0

    if args.command == "index":
        written = regenerate_indexes(args.bundle)
        print(f"Regenerated {len(written)} index.md file(s) across '{args.bundle}':")
        for p in written:
            rel = p.relative_to(Path.cwd()) if p.is_relative_to(Path.cwd()) else p
            print(f"  └── {rel}")
        return 0

    if args.command == "log":
        log_path = append_log(args.bundle, message=args.message, action=args.action)
        print(f"Appended log entry to: {log_path}")
        return 0

    if args.command == "viz":
        try:
            stats = generate_visualization(args.bundle, out_path=args.out, bundle_name=args.name)
            out_file = args.out or (args.bundle / "viz.html")
            print(f"Generated OKF graph visualization:")
            print(f"  Output:   {out_file}")
            print(f"  Concepts: {stats['concepts']}")
            print(f"  Edges:    {stats['edges']}")
            print(f"  Size:     {stats['bytes']} bytes")
            return 0
        except Exception as e:
            print(f"Error generating visualization: {e}", file=sys.stderr)
            return 1

    if args.command == "template":
        if not args.name or args.name == "list":
            templates = list_templates()
            print("Available OKF templates:")
            for t in templates:
                print(f"  - {t}")
            print("\nUsage: okf template <name> --out <path/to/concept.md>")
            return 0
        if not args.out:
            print("Error: --out <target_file> is required when applying a template", file=sys.stderr)
            return 1
        try:
            out_file = apply_template(args.name, args.out, force=args.force)
            print(f"Created concept from template '{args.name}' at: {out_file}")
            return 0
        except Exception as e:
            print(f"Error applying template: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
