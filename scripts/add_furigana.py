from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from jp_ebook_pipeline.furigana import add_furigana_to_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Add ruby furigana to plain text.")
    parser.add_argument("text")
    args = parser.parse_args()
    print(add_furigana_to_text(args.text))


if __name__ == "__main__":
    main()

