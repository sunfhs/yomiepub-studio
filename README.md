# YomiEpub Studio

YomiEpub Studio is a local toolkit and reading SOP for Japanese ebooks on Android-based e-ink readers, especially Chinese mainland devices whose built-in readers may not reliably support Japanese EPUB, vertical layout, ruby furigana, or bilingual layouts.

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
- Local Web UI for upload, options, conversion, and EPUB download.
- Horizontal CSS cleanup/override.
- Furigana insertion with `pykakasi` when installed.
- KOReader-friendly EPUB repacking.
- FastAPI backend.
- Placeholder React frontend skeleton for a future richer UI.
- Unit tests for furigana and EPUB packaging.

Planned:

- Bilingual paragraph layout.
- Optional translation backend, only when configured by the user.
- JLPT/difficulty-aware furigana filtering.

## Quick Start

### Easiest Way: Double-Click Launcher

For non-technical users, download the project ZIP from GitHub, unzip it, then use the launcher in the project folder:

- macOS: double-click `start_yomiepub.command`
- Windows: double-click `start_yomiepub.bat`

Prerequisite: install Python 3.10 or newer from https://www.python.org/downloads/ if your computer does not already have Python.

The launcher will:

1. create a local Python environment in `.venv`
2. install YomiEpub Studio on this computer
3. start the local web server
4. open `http://127.0.0.1:8765` in your browser

Keep the launcher window open while using the web page. Close it, or press `Ctrl+C`, to stop the local server.

If macOS blocks the launcher because it was downloaded from the Internet:

1. right-click `start_yomiepub.command`
2. choose **Open**
3. confirm **Open** once

After that, the browser page is:

```text
http://127.0.0.1:8765
```

Upload a legally obtained Japanese EPUB/TXT/HTML file, then download the generated `Yomi.epub` file.

### Command Line Setup

For someone who downloads this project from GitHub, the normal flow is:

1. Clone the repository or download and unzip it.
2. Install the local Python app.
3. Start the local web page.
4. Upload a legally obtained Japanese EPUB/TXT/HTML.
5. Download the converted horizontal furigana EPUB, named like `BookTitleYomi.epub`.
6. Transfer it to the e-ink reader and open it in KOReader.

```bash
git clone https://github.com/YOUR_NAME/jp-ebook-furigana-bilingual-pipeline.git
cd jp-ebook-furigana-bilingual-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Convert an EPUB:

```bash
jp-ebook-convert input.epub --furigana --horizontal --output output.epub
```

Start the local Web UI:

```bash
jp-ebook-web
```

Then open:

```text
http://127.0.0.1:8765
```

The local page lets you upload a Japanese EPUB/TXT/HTML file, then download a KOReader-friendly EPUB with horizontal layout and furigana enabled by default.
The web UI runs only on your own computer at `127.0.0.1`; files are not uploaded to a cloud service.

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
