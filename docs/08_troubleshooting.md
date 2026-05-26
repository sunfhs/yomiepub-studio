# Troubleshooting

## Built-in reader keeps loading

Cause: the built-in reader may not support EPUB3, ruby tags, strict ZIP packaging, or complex CSS.

Fix:

1. Try the KOReader-friendly EPUB output.
2. If it still fails, test a no-furigana output.
3. If no-furigana works but furigana does not, the reader likely cannot handle ruby.
4. Use KOReader for ruby EPUB.

## Furigana does not appear

Cause: the reader may not support HTML ruby rendering.

Fix:

- Open with KOReader or another ruby-aware reader.
- Confirm the EPUB contains `<ruby><rt>...</rt></ruby>`.

## Text is too small

Fix:

- Increase `--font-size`.
- Increase `--line-height` for readability.
- Use KOReader's font and margin settings.

## Japanese font looks wrong

Fix:

- Install a Japanese-capable font on the device.
- Recommended families include Noto Serif CJK JP and Noto Sans CJK JP.
- Do not bundle third-party fonts in this repository unless the license permits redistribution.

## EPUB import fails

Fix:

- Make sure `mimetype` is the first ZIP entry and stored without compression.
- Avoid directory entries before `mimetype`.
- Keep the EPUB filename simple when testing.

