#!/usr/bin/env python3
"""Run all project unit tests with a single command."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    tests_dir = repo_root / "tests"

    if not tests_dir.exists():
        print("No tests directory found.", file=sys.stderr)
        return 1

    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    completed = subprocess.run(command, cwd=repo_root)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
