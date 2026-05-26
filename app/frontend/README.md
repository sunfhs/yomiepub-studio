# Frontend Skeleton

The MVP is CLI-first. This folder reserves the future React/Vite UI.

Planned screens:

1. Upload local EPUB/TXT/HTML.
2. Choose conversion options.
3. Preview a small rendered sample.
4. Download final EPUB.

Planned controls:

- Convert to horizontal layout
- Add furigana
- Future bilingual mode
- Font size
- Line height
- KOReader compatibility optimization

Backend endpoint:

```text
POST /convert
```

The backend already exposes a minimal FastAPI endpoint in:

```text
app/backend/jp_ebook_pipeline/server.py
```

