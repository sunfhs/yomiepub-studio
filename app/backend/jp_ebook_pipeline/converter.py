from __future__ import annotations

from pathlib import Path
from typing import Callable

from jp_ebook_pipeline.epub import (
    build_epub_from_html,
    build_epub_from_text,
    convert_epub,
    guess_input_kind,
)
from jp_ebook_pipeline.models import ConvertOptions

ProgressCallback = Callable[[int, str], None]


def convert_file(
    input_path: str | Path,
    output_path: str | Path,
    options: ConvertOptions,
    progress: ProgressCallback | None = None,
) -> Path:
    src = Path(input_path)
    dst = Path(output_path)
    if options.bilingual:
        raise NotImplementedError(
            "Bilingual translation/layout is reserved for a future version."
        )
    if not src.exists():
        raise FileNotFoundError(src)

    kind = guess_input_kind(src)
    if progress:
        progress(24, "Input detected")
    if kind == "epub":
        return convert_epub(src, dst, options, progress=progress)
    if kind == "txt":
        return build_epub_from_text(src, dst, options, progress=progress)
    if kind == "html":
        return build_epub_from_html(src, dst, options, progress=progress)
    raise ValueError(f"Unsupported input type: {src}")
