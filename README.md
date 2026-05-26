# JP Ebook Furigana Bilingual Pipeline

A local toolkit and reading SOP for Japanese ebooks on Android-based e-ink readers, especially Chinese mainland devices whose built-in readers may not reliably support Japanese EPUB, vertical layout, ruby furigana, or bilingual layouts.

The recommended reading path is:

```text
Legally obtained local Japanese EPUB/TXT/HTML
  -> clean horizontal EPUB
  -> optional furigana as standard HTML ruby
  -> KOReader-friendly EPUB
  -> transfer to Android e-ink reader
  -> read with KOReader
```

## What This Project Does

- Converts Japanese EPUB/TXT/HTML into horizontal-layout EPUB.
- Adds furigana above Japanese kanji using standard HTML ruby tags:

```html
<ruby>日本語<rt>にほんご</rt></ruby>
```

- Generates EPUB packages with the `mimetype` entry first and uncompressed for better compatibility with stricter readers.
- Provides a practical SOP for Android e-ink readers such as Hanvon, BOOX/Onyx mainland devices, iReader-style Android devices, and similar APK-capable e-readers.
- Leaves room for future Chinese-Japanese bilingual output.

## What This Project Does Not Do

This project does **not** provide ebook downloading, Z-Library scraping, piracy workflows, DRM removal, or access to copyrighted books.

Users must provide legally obtained local ebook files.

## Recommended Setup

- General Chinese or English reading: WeRead or the device's normal reader may be enough.
- Japanese novels with furigana or custom layout: use KOReader.

KOReader supports Android and common document formats including EPUB, PDF, MOBI, TXT, HTML, RTF, and CHM. Download it from the official KOReader website or the official GitHub Releases page:

- https://koreader.rocks/
- https://github.com/koreader/koreader/releases

## MVP Status

Implemented now:

- CLI converter for local EPUB/TXT/HTML.
- Horizontal CSS cleanup/override.
- Furigana insertion with `pykakasi` when installed.
- KOReader-friendly EPUB repacking.
- Placeholder FastAPI backend and frontend project skeleton.
- Unit tests for furigana and EPUB packaging.

Planned:

- Local Web UI upload/preview/download flow.
- Bilingual paragraph layout.
- Optional translation backend, only when configured by the user.
- JLPT/difficulty-aware furigana filtering.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Convert an EPUB:

```bash
jp-ebook-convert input.epub --furigana --horizontal --output output.epub
```

Convert a TXT file:

```bash
jp-ebook-convert samples/sample_public_domain_text.txt --furigana --output output.epub
```

Run tests:

```bash
pytest
```

## CLI Options

```bash
jp-ebook-convert INPUT --output OUTPUT [--furigana] [--horizontal] [--font-size 1.05em] [--line-height 1.9]
```

Important options:

- `--furigana`: add ruby furigana to Japanese kanji.
- `--horizontal`: force horizontal writing mode.
- `--font-size`: CSS font size for generated/overridden content.
- `--line-height`: CSS line height for e-ink readability.
- `--bilingual`: reserved for future bilingual output; currently not implemented.

## Project Structure

```text
jp-ebook-furigana-bilingual-pipeline/
├── README.md
├── docs/
├── app/
│   ├── backend/
│   └── frontend/
├── scripts/
├── samples/
├── tests/
├── requirements.txt
├── pyproject.toml
└── LICENSE
```

## Reading SOP

1. Install KOReader Android APK from the official site or GitHub Releases.
2. Convert your local Japanese ebook:

```bash
jp-ebook-convert my-book.epub --furigana --horizontal --output my-book-koreader.epub
```

3. Transfer the output EPUB to the e-ink reader using WiFi transfer, USB, Syncthing, or another local method.
4. Set KOReader's root folder to the transfer directory.
5. Open the converted EPUB in KOReader.

## Legal And Ethical Notes

This project is a local format-conversion and reading-accessibility toolkit. It is intended for study, accessibility, and personal reading workflows involving legally obtained files.

Do not use this project to distribute copyrighted content, bypass DRM, scrape piracy sites, or automate unauthorized ebook downloads.

