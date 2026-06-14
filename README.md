# YomiEpub Studio

[简体中文](README.zh-CN.md) | English

<p align="center">
  <img src="docs/assets/yomiepub-studio-icon.png" alt="YomiEpub Studio app icon" width="112">
</p>

YomiEpub Studio is a small local web app for turning Japanese EPUB/TXT/HTML files into KOReader-friendly EPUBs with horizontal layout and furigana.

It is designed for people reading Japanese novels on Android-based e-ink readers, especially devices whose built-in reader does not handle vertical Japanese layout, ruby/furigana, or custom EPUB CSS reliably.

<p align="center">
  <img src="docs/assets/yomiepub-studio-home.png" alt="YomiEpub Studio local web UI" width="900">
</p>

## What It Does

- Converts local Japanese EPUB/TXT/HTML into horizontal EPUB.
- Adds furigana above kanji with standard HTML ruby tags.
- Repackages EPUBs in a KOReader-friendly way.
- Shows conversion progress and downloads the final `Yomi.epub` file automatically.
- Runs locally at `http://127.0.0.1:8765`.
- Keeps your files on your own computer. Nothing is uploaded to a cloud service.

Example ruby output:

```html
<ruby>日本語<rt>にほんご</rt></ruby>
```

## What It Does Not Do

This project does not provide ebook downloading, piracy search, Z-Library automation, DRM removal, or copyrighted content access.

Users must provide legally obtained local ebook files.

The screenshots in this repository avoid copyrighted book pages. If you add your own screenshots, prefer public-domain text or the app UI itself.

## Recommended Reading Setup

- Japanese novels with furigana/custom layout: KOReader
- General Chinese or English books: WeRead or your device's normal reader may be enough

KOReader supports Android and common ebook/document formats including EPUB, PDF, MOBI, TXT, HTML, RTF, and CHM.

- KOReader official site: https://koreader.rocks/
- KOReader GitHub Releases: https://github.com/koreader/koreader/releases

## Quick Start

### Download

- Project release: https://github.com/sunfhs/yomiepub-studio/releases/tag/v0.1.0
- Source code ZIP: use GitHub's **Code -> Download ZIP** button.
- Optional KOReader APK convenience attachment is available on the release page. For the latest official KOReader build, prefer the official KOReader links above.

### Easiest Way: macOS App Launcher

Download this project from GitHub as a ZIP, unzip it, then double-click:

- macOS: `YomiEpub Studio.app`
- Windows: `start_yomiepub.bat`

Prerequisite: install Python 3.10 or newer from https://www.python.org/downloads/ if your computer does not already have Python.

The macOS app launcher will:

1. create a local Python environment in `~/Library/Application Support/YomiEpub Studio/venv`
2. install the bundled YomiEpub Studio wheel into that environment
3. start the local web server in the background
4. open `http://127.0.0.1:8765` in your browser

First launch needs an internet connection so Python dependencies can be installed from PyPI. Later launches are faster.

If macOS blocks the app because it was downloaded from the Internet:

1. right-click `YomiEpub Studio.app`
2. choose **Open**
3. confirm **Open** once

If the browser does not come to the front, open this URL manually:

```text
http://127.0.0.1:8765
```

macOS fallback: double-click `start_yomiepub.command`. This opens a Terminal window and keeps the server attached to that window.

## Web UI Flow

1. Open `http://127.0.0.1:8765`.
2. Choose a legally obtained Japanese EPUB/TXT/HTML file.
3. Click **Convert & Download EPUB**.
4. Watch the progress bar.
5. Download the generated file named like `BookTitleYomi.epub`.
6. Transfer the EPUB to your e-ink reader.
7. Open it in KOReader.

## Command Line Setup

```bash
git clone https://github.com/sunfhs/yomiepub-studio.git
cd yomiepub-studio
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Start the local web UI:

```bash
jp-ebook-web
```

Then open:

```text
http://127.0.0.1:8765
```

Convert from the command line:

```bash
jp-ebook-convert input.epub --furigana --horizontal --output output.epub
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

- `--furigana`: add ruby furigana to Japanese kanji
- `--horizontal`: force horizontal writing mode
- `--font-size`: CSS font size for generated/overridden content
- `--line-height`: CSS line height for e-ink readability
- `--bilingual`: reserved for a future bilingual output flow

## Current Scope

Implemented:

- local FastAPI web UI
- native-style macOS `.app` launcher
- fallback double-click launchers for macOS and Windows
- EPUB/TXT/HTML input
- horizontal layout cleanup
- furigana insertion with `pykakasi`
- KOReader-friendly EPUB repacking
- conversion progress tracking
- local-only processing
- unit tests for core conversion behavior

Planned ideas:

- optional bilingual paragraph layout
- optional translation backend configured by the user
- JLPT/difficulty-aware furigana filtering
- richer desktop packaging

## Project Structure

```text
yomiepub-studio/
├── README.md
├── docs/
│   └── assets/
├── app/
│   ├── backend/
│   └── frontend/
├── samples/
├── scripts/
├── tests/
├── YomiEpub Studio.app/
├── start_yomiepub.command
├── start_yomiepub.bat
├── pyproject.toml
└── LICENSE
```

## E-Ink Reader SOP

1. Install KOReader Android APK from the official KOReader site or GitHub Releases.
2. Use YomiEpub Studio to convert your local Japanese ebook.
3. Transfer the generated EPUB to your e-ink reader by Wi-Fi transfer, USB, Syncthing, or another local method.
4. Set KOReader's root folder to the transfer directory.
5. Open the converted EPUB in KOReader.

## License

MIT

## Legal And Ethical Notes

YomiEpub Studio is a local format-conversion and reading-accessibility tool. It is intended for study, accessibility, and personal reading workflows involving legally obtained files.

Do not use this project to distribute copyrighted content, bypass DRM, scrape piracy sites, or automate unauthorized ebook downloads.
