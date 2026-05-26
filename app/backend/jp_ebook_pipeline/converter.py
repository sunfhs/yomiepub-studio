from __future__ import annotations

from pathlib import Path

from jp_ebook_pipeline.epub import (
    build_epub_from_html,
    build_epub_from_text,
    convert_epub,
    guess_input_kind,
)
from jp_ebook_pipeline.models import ConvertOptions


def convert_file(
    input_path: str | Path,
    output_path: str | Path,
    options: ConvertOptions,
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
    if kind == "epub":
        return convert_epub(src, dst, options)
    if kind == "txt":
        return build_epub_from_text(src, dst, options)
    if kind == "html":
        return build_epub_from_html(src, dst, options)
    raise ValueError(f"Unsupported input type: {src}")

