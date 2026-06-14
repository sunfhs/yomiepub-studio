# Troubleshooting

## macOS app does not open the browser

Cause: macOS may block a downloaded app on first launch, or the browser may stay in the background.

Fix:

1. Right-click `YomiEpub Studio.app` and choose **Open** the first time.
2. Wait for the first dependency install to finish. The first launch can take a few minutes.
3. Open `http://127.0.0.1:8765` manually if the browser does not come forward.
4. Check logs at `~/Library/Logs/yomiepub-studio-app.log`.
5. If the app still does not start, use `start_yomiepub.command` as the Terminal fallback.

The macOS app stores its runtime environment in `~/Library/Application Support/YomiEpub Studio/venv`.

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
