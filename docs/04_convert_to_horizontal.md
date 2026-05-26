# Convert To Horizontal Layout

Many Japanese EPUBs are vertical by default. Some Android e-ink readers handle vertical writing poorly, especially when furigana and complex CSS are also present.

The MVP converter adds a horizontal CSS override:

```css
html, body {
  writing-mode: horizontal-tb !important;
  -webkit-writing-mode: horizontal-tb !important;
}
```

Run:

```bash
jp-ebook-convert input.epub --horizontal --output output.epub
```

For better e-ink readability:

```bash
jp-ebook-convert input.epub --horizontal --font-size 1.08em --line-height 1.9 --output output.epub
```

