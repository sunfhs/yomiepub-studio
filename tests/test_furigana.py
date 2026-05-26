from __future__ import annotations

from jp_ebook_pipeline.furigana import StaticReadingProvider, add_furigana_to_text
from jp_ebook_pipeline.html_tools import add_furigana_to_html


def test_add_furigana_to_text_wraps_kanji_runs() -> None:
    provider = StaticReadingProvider({"日本語": "にほんご", "漢字": "かんじ"})

    result = add_furigana_to_text("日本語と漢字", provider)

    assert "<ruby>日本語<rt>にほんご</rt></ruby>" in result
    assert "<ruby>漢字<rt>かんじ</rt></ruby>" in result


def test_add_furigana_to_html_skips_existing_ruby() -> None:
    provider = StaticReadingProvider({"日本語": "にほんご", "漢字": "かんじ"})
    html = "<html><body><p>日本語</p><ruby>漢字<rt>かんじ</rt></ruby></body></html>"

    result = add_furigana_to_html(html, provider)

    assert result.count("<ruby>") == 2
    assert result.count("<rt>かんじ</rt>") == 1

