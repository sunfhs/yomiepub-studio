from __future__ import annotations

import re
import warnings
from html import escape

from bs4 import (
    BeautifulSoup,
    Declaration,
    Doctype,
    MarkupResemblesLocatorWarning,
    NavigableString,
    ProcessingInstruction,
    Tag,
)

from jp_ebook_pipeline.furigana import ReadingProvider, add_furigana_to_text
from jp_ebook_pipeline.models import ConvertOptions


KO_READER_CSS_ID = "jp-ebook-pipeline-koreader-css"
XML_DECLARATION_RE = re.compile(r"^\s*xml\s+version\s*=", re.IGNORECASE)


def koreader_css(options: ConvertOptions) -> str:
    writing_mode = "horizontal-tb" if options.horizontal else "inherit"
    return f"""
html, body {{
  writing-mode: {writing_mode} !important;
  -webkit-writing-mode: {writing_mode} !important;
  -epub-writing-mode: {writing_mode} !important;
  font-size: {options.font_size};
  line-height: {options.line_height};
}}
body {{
  margin: 0 0.6em;
}}
p {{
  margin: 0 0 0.85em 0;
}}
ruby {{
  ruby-position: over;
}}
rt {{
  font-size: 0.52em;
  line-height: 1;
}}
"""


def ensure_html_shell(html: str, title: str = "Converted Ebook") -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    for child in list(soup.contents):
        if isinstance(child, (Declaration, Doctype, ProcessingInstruction)):
            child.extract()
        elif isinstance(child, NavigableString) and XML_DECLARATION_RE.match(str(child)):
            child.extract()
    if soup.find("html") is None:
        body = soup.new_tag("body")
        for child in list(soup.contents):
            body.append(child.extract())
        html_tag = soup.new_tag("html")
        head = soup.new_tag("head")
        title_tag = soup.new_tag("title")
        title_tag.string = title
        head.append(title_tag)
        html_tag.append(head)
        html_tag.append(body)
        soup.append(html_tag)
    if soup.find("head") is None:
        head = soup.new_tag("head")
        soup.html.insert(0, head)  # type: ignore[union-attr]
    if soup.find("body") is None:
        body = soup.new_tag("body")
        soup.html.append(body)  # type: ignore[union-attr]
    return soup


def add_css_override(soup: BeautifulSoup, options: ConvertOptions) -> None:
    existing = soup.find("style", id=KO_READER_CSS_ID)
    if existing:
        existing.string = koreader_css(options)
        return
    style = soup.new_tag("style", id=KO_READER_CSS_ID)
    style.string = koreader_css(options)
    head = soup.find("head")
    if isinstance(head, Tag):
        head.append(style)


def add_furigana_to_html(
    html: str, provider: ReadingProvider | None = None
) -> str:
    soup = ensure_html_shell(html)
    blocked = {"script", "style", "ruby", "rt", "rp", "title"}
    text_nodes = [
        node
        for node in soup.find_all(string=True)
        if node.parent and node.parent.name not in blocked and node.strip()
    ]
    for node in text_nodes:
        marked = add_furigana_to_text(str(node), provider)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", MarkupResemblesLocatorWarning)
            fragment = BeautifulSoup(marked, "html.parser")
        replacement = list(fragment.contents)
        if not replacement:
            continue
        for new_node in reversed(replacement):
            node.insert_after(new_node)
        node.extract()
    return str(soup)


def normalize_html(
    html: str,
    options: ConvertOptions,
    provider: ReadingProvider | None = None,
    title: str = "Converted Ebook",
    include_doctype: bool = True,
) -> str:
    if options.furigana:
        html = add_furigana_to_html(html, provider)
    soup = ensure_html_shell(html, title=title)
    add_css_override(soup, options)
    rendered = str(soup)
    if include_doctype:
        return "<!doctype html>\n" + rendered
    return rendered


def text_to_html(text: str, options: ConvertOptions, title: str) -> str:
    paragraphs = [
        f"<p>{escape(line)}</p>"
        for line in text.splitlines()
        if line.strip()
    ]
    html = f"""<html>
<head><meta charset="utf-8"><title>{title}</title></head>
<body>
{''.join(paragraphs)}
</body>
</html>"""
    return normalize_html(html, options, title=title)
