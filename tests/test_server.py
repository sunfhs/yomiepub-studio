from __future__ import annotations

from jp_ebook_pipeline.server import output_filename


def test_output_filename_preserves_japanese_title_marks() -> None:
    filename = (
        "日本の「神話」と「古代史」がよくわかる本 "
        "(日本博学倶楽部) (z-library.sk, 1lib.sk, z-lib.sk).epub"
    )

    result = output_filename(filename)

    assert result == "日本の「神話」と「古代史」がよくわかる本 (日本博学倶楽部)Yomi.epub"
