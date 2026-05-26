from __future__ import annotations

import zipfile

from jp_ebook_pipeline.converter import convert_file
from jp_ebook_pipeline.models import ConvertOptions


def test_txt_conversion_writes_koreader_friendly_epub(tmp_path) -> None:
    src = tmp_path / "sample.txt"
    dst = tmp_path / "sample.epub"
    src.write_text("日本語の文章です。", encoding="utf-8")

    convert_file(src, dst, ConvertOptions(horizontal=True, furigana=False))

    with zipfile.ZipFile(dst) as zf:
        first = zf.infolist()[0]
        assert first.filename == "mimetype"
        assert first.compress_type == zipfile.ZIP_STORED
        assert zf.read("mimetype") == b"application/epub+zip"
        chapter = zf.read("OEBPS/chapter_001.xhtml").decode("utf-8")
        assert "writing-mode: horizontal-tb" in chapter

