# Add Furigana

Furigana is represented with standard HTML ruby:

```html
<ruby>漢字<rt>かんじ</rt></ruby>
```

Run:

```bash
jp-ebook-convert input.epub --horizontal --furigana --output output.epub
```

## Reader Compatibility

Some built-in readers may:

- Show ruby correctly above kanji
- Turn ruby into parentheses
- Ignore ruby
- Freeze while loading

When the built-in reader is unstable, use KOReader. If KOReader is unavailable, generate a parentheses-furigana fallback in a future compatibility mode.

## Future Furigana Modes

Planned modes:

- All kanji
- Common difficult words only
- JLPT N2 and above
- User dictionary override

