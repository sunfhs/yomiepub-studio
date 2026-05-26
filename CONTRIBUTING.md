# Contributing

This project welcomes improvements to the local conversion pipeline, KOReader SOP, reader compatibility notes, and test coverage.

## Rules

- Do not add ebook downloaders, piracy-site integrations, DRM removal, or copyrighted sample books.
- Use public-domain or dummy text for tests and examples.
- Keep conversion behavior testable.
- Prefer compatibility with KOReader and strict EPUB readers.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

