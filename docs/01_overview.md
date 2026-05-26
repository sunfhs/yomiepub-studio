# Overview

This project solves a practical reading problem: Japanese EPUB files often depend on vertical writing, ruby furigana, CJK fonts, and CSS behavior that built-in readers on Android-based e-ink devices do not always handle well.

The recommended workflow is:

1. Prepare a legally obtained local Japanese ebook.
2. Convert it to horizontal layout.
3. Add furigana using standard HTML ruby tags.
4. Export a clean EPUB package.
5. Transfer it to the e-ink device.
6. Read it in KOReader instead of the built-in reader.

## Why KOReader

KOReader is an open-source document reader designed for e-ink use. It has Android builds and supports many document formats, including EPUB, PDF, MOBI, TXT, HTML, RTF, and CHM.

Official links:

- https://koreader.rocks/
- https://github.com/koreader/koreader/releases

## Non-goals

This project does not download ebooks, scrape book sources, bypass DRM, or provide copyrighted content.

