from __future__ import annotations

import argparse
from pathlib import Path

from jp_ebook_pipeline.converter import convert_file
from jp_ebook_pipeline.models import ConvertOptions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert local Japanese ebooks into KOReader-friendly EPUB."
    )
    parser.add_argument("input", help="Local EPUB/TXT/HTML file")
    parser.add_argument("-o", "--output", required=True, help="Output EPUB path")
    parser.add_argument(
        "--horizontal",
        action="store_true",
        default=False,
        help="Force horizontal writing mode",
    )
    parser.add_argument(
        "--furigana",
        action="store_true",
        help="Add ruby furigana above kanji",
    )
    parser.add_argument("--font-size", default="1.05em")
    parser.add_argument("--line-height", default="1.85")
    parser.add_argument(
        "--bilingual",
        action="store_true",
        help="Reserved for future Chinese-Japanese bilingual output",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    options = ConvertOptions(
        horizontal=args.horizontal,
        furigana=args.furigana,
        font_size=args.font_size,
        line_height=args.line_height,
        bilingual=args.bilingual,
    )
    output = convert_file(Path(args.input), Path(args.output), options)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()

