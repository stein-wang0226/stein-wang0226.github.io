#!/usr/bin/env python3
"""Copy the checked build artifact's manifest allowlist; never compile or scan sources."""
import sys
sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path
import shutil

from check import validate
from render import DEFAULT_OUTPUT, ROOT, external_output


def export(output=DEFAULT_OUTPUT, dest=None):
    output = external_output(output)
    if dest is None:
        raise ValueError("--dest is required; --output identifies the existing build artifact")
    dest = external_output(dest)
    if dest == output or dest.is_relative_to(output) or output.is_relative_to(dest):
        raise ValueError("Export destination must not overlap the build artifact")
    if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
        raise ValueError("Use an empty export destination to avoid stale public files")
    errors, _ = validate(output)
    if errors:
        raise ValueError("Refusing to export an invalid artifact:\n" + "\n".join(errors))
    info = json.loads((output / "build-info.json").read_text(encoding="utf-8"))
    paths = sorted(set(info["files"]) | {"build-info.json"})
    dest.mkdir(parents=True, exist_ok=True)
    for relative in paths:
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(output / relative, target)
    return len(paths)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "--site", type=Path, default=DEFAULT_OUTPUT,
                        help="Existing checked build artifact (default: /tmp/my-blogs-site-build)")
    parser.add_argument("--dest", type=Path, required=True, help="External empty export destination")
    args = parser.parse_args(argv)
    try:
        count = export(args.output, args.dest)
    except (ValueError, OSError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"Exported {count} manifest-allowlisted files from {args.output.resolve()} to {args.dest.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
