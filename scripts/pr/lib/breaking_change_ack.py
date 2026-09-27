#!/usr/bin/env python3
"""Extract an explicit breaking-change acknowledgement reason.

The acknowledgement is intentionally reason-bearing rather than a bare flag.
For staged/pre-PR checks, MCP_BREAKING_CHANGE_ACKNOWLEDGED provides the reason.
For PR checks, callers can pipe a PR body and commit messages containing:

    Breaking-Change-Acknowledged: <why this intentional break is required>
"""

from __future__ import annotations

import os
import re
import sys

MARKER = re.compile(
    r"(?im)^\s*Breaking-Change-Acknowledged:\s*(\S(?:.*\S)?)\s*$"
)


def acknowledgement_reason(text: str, env_reason: str | None = None) -> str | None:
    reason = (env_reason or "").strip()
    if reason:
        return reason

    match = MARKER.search(text)
    if match:
        return match.group(1).strip()
    return None


def main() -> int:
    reason = acknowledgement_reason(
        sys.stdin.read(),
        os.environ.get("MCP_BREAKING_CHANGE_ACKNOWLEDGED"),
    )
    if not reason:
        return 1
    print(reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
