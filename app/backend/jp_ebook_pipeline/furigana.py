from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Protocol


class ReadingProvider(Protocol):
    def reading(self, text: str) -> str:
        """Return hiragana reading for Japanese text."""


KANJI_START = "\u4e00"
KANJI_END = "\u9fff"


def is_kanji(char: str) -> bool:
    return KANJI_START <= char <= KANJI_END


@dataclass
class StaticReadingProvider:
    """Small deterministic fallback for tests and no-dependency demos."""

    readings: dict[str, str]

    def reading(self, text: str) -> str:
        return self.readings.get(text, "")


class KakasiReadingProvider:
    def __init__(self) -> None:
        try:
            import pykakasi
        except ImportError as exc:
            raise RuntimeError(
                "pykakasi is required for furigana generation. Install project dependencies first."
            ) from exc
        self._kakasi = pykakasi.kakasi()

    def reading(self, text: str) -> str:
        converted = self._kakasi.convert(text)
        return "".join(item.get("hira", "") for item in converted)


def add_furigana_to_text(
    text: str, provider: ReadingProvider | None = None
) -> str:
    """Wrap contiguous kanji runs in HTML ruby tags."""

    provider = provider or KakasiReadingProvider()
    output: list[str] = []
    i = 0
    while i < len(text):
        char = text[i]
        if not is_kanji(char):
            output.append(escape(char))
            i += 1
            continue

        start = i
        while i < len(text) and is_kanji(text[i]):
            i += 1
        surface = text[start:i]
        reading = provider.reading(surface)
        if reading and reading != surface:
            output.append(
                f"<ruby>{escape(surface)}<rt>{escape(reading)}</rt></ruby>"
            )
        else:
            output.append(escape(surface))
    return "".join(output)

