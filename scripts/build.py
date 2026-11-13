#!/usr/bin/env python3
"""Build and validate the static site outside the source repository."""
import sys
sys.dont_write_bytecode = True

import argparse
from pathlib import Path

from pipeline import build
from render import DEFAULT_OUTPUT


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="External artifact directory (default: /tmp/my-blogs-site-build)")
    args = parser.parse_args(argv)
    try:
        pages, files = build(args.output)
    except (ValueError, OSError, ImportError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"Built and checked {pages} HTML pages / {files} public files in {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
