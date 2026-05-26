"""Placeholder for future Chinese-Japanese paragraph alignment.

The MVP intentionally does not call any translation service. Future versions
should accept user-provided translations or a user-configured local/API backend.
"""

from __future__ import annotations


def align_paragraphs(japanese: list[str], chinese: list[str]) -> list[tuple[str, str]]:
    return list(zip(japanese, chinese))

