from __future__ import annotations

import zipfile

from jp_ebook_pipeline.converter import convert_file
from jp_ebook_pipeline.epub import _force_ltr_spine
from jp_ebook_pipeline.html_tools import normalize_html
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


def test_epub_html_output_does_not_keep_fake_xml_declaration() -> None:
    html = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html><body><p>日本語</p></body></html>"""

    result = normalize_html(
        html,
        ConvertOptions(horizontal=True, furigana=False),
        include_doctype=False,
    )

    assert not result.lower().startswith("<!doctype")
    assert "xml version" not in result.lower()
    assert not result.lstrip().startswith("html\n")
    assert "<html" in result


def test_force_ltr_spine_preserves_opf_namespace_text() -> None:
    opf = b"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0">
  <spine toc="ncx"><itemref idref="chapter"/></spine>
</package>
"""

    result = _force_ltr_spine(opf, ConvertOptions(horizontal=True))

    assert b"ns0:" not in result
    assert b"<package xmlns=" in result
    assert b'page-progression-direction="ltr"' in result
