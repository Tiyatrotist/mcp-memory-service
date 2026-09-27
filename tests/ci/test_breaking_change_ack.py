from __future__ import annotations

import importlib.util
from pathlib import Path

HELPER = Path(__file__).parents[2] / "scripts" / "pr" / "lib" / "breaking_change_ack.py"
_spec = importlib.util.spec_from_file_location("breaking_change_ack", HELPER)
module = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(module)


def test_marker_requires_a_reason():
    assert module.acknowledgement_reason("Breaking-Change-Acknowledged:   ") is None


def test_marker_extracts_reason_from_pr_or_commit_text():
    text = """Security hardening

Breaking-Change-Acknowledged: remove unauthenticated statistics after GHSA review
"""

    assert module.acknowledgement_reason(text) == (
        "remove unauthenticated statistics after GHSA review"
    )


def test_environment_reason_supports_staged_mode():
    assert module.acknowledgement_reason("", "intentional advisory response hardening") == (
        "intentional advisory response hardening"
    )


def test_environment_reason_must_not_be_blank():
    assert module.acknowledgement_reason("", "   ") is None
