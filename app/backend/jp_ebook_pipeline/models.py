from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConvertOptions:
    horizontal: bool = True
    furigana: bool = False
    font_size: str = "1.05em"
    line_height: str = "1.85"
    bilingual: bool = False
    bilingual_mode: str = "paragraph"

