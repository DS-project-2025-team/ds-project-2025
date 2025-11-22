"""Pytest configuration helpers for local test runs.

This file ensures the `src/` directory is on `sys.path` so tests can
import modules using the project `src` layout (e.g. `entities.*`).

It's a lightweight solution for local development and CI where the
project root is the test collection root.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC.resolve()))
