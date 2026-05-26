from __future__ import annotations

import mimetypes
import posixpath
import re
import uuid
import zipfile
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup, Tag

from jp_ebook_pipeline.html_tools import normalize_html, text_to_html
from jp_ebook_pipeline.models import ConvertOptions

CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def _xml_text(element: ET.Element, path: str, namespaces: dict[str, str]) -> str | None:
    found = element.find(path, namespaces)
    return found.text if found is not None else None


def _rootfile_path(zf: zipfile.ZipFile) -> str:
    container = ET.fromstring(zf.read("META-INF/container.xml"))
    ns = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
    rootfile = container.find(".//c:rootfile", ns)
    if rootfile is None:
        raise ValueError("EPUB container has no rootfile")
    path = rootfile.attrib.get("full-path")
    if not path:
        raise ValueError("EPUB rootfile has no full-path")
    return path


def _manifest_html_paths(zf: zipfile.ZipFile, opf_path: str) -> list[str]:
    opf = ET.fromstring(zf.read(opf_path))
    ns = {"opf": "http://www.idpf.org/2007/opf"}
    opf_dir = posixpath.dirname(opf_path)
    item_href_by_id: dict[str, str] = {}
    html_ids: set[str] = set()
    for item in opf.findall(".//opf:manifest/opf:item", ns):
        item_id = item.attrib.get("id")
        href = item.attrib.get("href")
        media = item.attrib.get("media-type", "")
        if not item_id or not href:
            continue
        full_path = posixpath.normpath(posixpath.join(opf_dir, href))
        item_href_by_id[item_id] = full_path
        if media in {"application/xhtml+xml", "text/html"}:
            html_ids.add(item_id)

    ordered: list[str] = []
    for itemref in opf.findall(".//opf:spine/opf:itemref", ns):
        ref = itemref.attrib.get("idref")
        if ref in html_ids and ref in item_href_by_id:
            ordered.append(item_href_by_id[ref])

    if ordered:
        return ordered
    return [item_href_by_id[item_id] for item_id in html_ids]


def _write_epub_zip(files: dict[str, bytes], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w") as zout:
        info = zipfile.ZipInfo("mimetype")
        info.compress_type = zipfile.ZIP_STORED
        info.external_attr = 0o644 << 16
        zout.writestr(info, b"application/epub+zip")

        for name in sorted(files):
            if name == "mimetype" or name.endswith("/"):
                continue
            info = zipfile.ZipInfo(name)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zout.writestr(info, files[name])


def convert_epub(input_path: Path, output_path: Path, options: ConvertOptions) -> Path:
    with zipfile.ZipFile(input_path, "r") as zin:
        files = {
            name: zin.read(name)
            for name in zin.namelist()
            if not name.endswith("/")
        }
        opf_path = _rootfile_path(zin)
        html_paths = set(_manifest_html_paths(zin, opf_path))

    for name in html_paths:
        if name in files:
            html = files[name].decode("utf-8", errors="ignore")
            if options.horizontal:
                html = _switch_to_horizontal_stylesheets(html, name, files)
            files[name] = normalize_html(
                html,
                options,
                title=input_path.stem,
                include_doctype=False,
            ).encode("utf-8")

    if opf_path in files:
        files[opf_path] = _force_ltr_spine(files[opf_path], options)

    _write_epub_zip(files, output_path)
    return output_path


def _switch_to_horizontal_stylesheets(
    html: str,
    html_path: str,
    files: dict[str, bytes],
) -> str:
    soup = BeautifulSoup(html, "html.parser")
    base_dir = posixpath.dirname(html_path)
    changed = False
    for link in soup.find_all("link", href=True):
        if not isinstance(link, Tag):
            continue
        href = str(link.get("href", ""))
        candidates = []
        if "_v_" in href:
            candidates.append(href.replace("_v_", "_h_"))
        if href.endswith("_v.css"):
            candidates.append(href[:-6] + "_h.css")
        if href == "nav_v.css":
            candidates.append("nav_h.css")

        for candidate in candidates:
            candidate_path = posixpath.normpath(posixpath.join(base_dir, candidate))
            if candidate_path in files:
                link["href"] = candidate
                classes = [
                    "horizontal" if css_class == "vertical" else css_class
                    for css_class in link.get("class", [])
                ]
                if classes:
                    link["class"] = classes
                changed = True
                break
    return str(soup) if changed else html


def _force_ltr_spine(opf_bytes: bytes, options: ConvertOptions) -> bytes:
    if not options.horizontal:
        return opf_bytes
    text = opf_bytes.decode("utf-8", errors="ignore")
    spine_re = re.compile(
        r"(<(?:[A-Za-z_][\w.-]*:)?spine\b)([^>]*)(/?>)",
        re.IGNORECASE,
    )
    direction_re = re.compile(
        r"(page-progression-direction\s*=\s*)([\"']).*?\2",
        re.IGNORECASE,
    )

    def replace_spine(match: re.Match[str]) -> str:
        start, attrs, end = match.groups()

        def replace_direction(direction: re.Match[str]) -> str:
            quote = direction.group(2)
            return f"{direction.group(1)}{quote}ltr{quote}"

        if direction_re.search(attrs):
            attrs = direction_re.sub(replace_direction, attrs, count=1)
        else:
            attrs = f'{attrs} page-progression-direction="ltr"'
        return f"{start}{attrs}{end}"

    updated = spine_re.sub(replace_spine, text, count=1)
    return updated.encode("utf-8")


def build_epub_from_text(
    input_path: Path, output_path: Path, options: ConvertOptions
) -> Path:
    title = input_path.stem
    text = input_path.read_text(encoding="utf-8", errors="ignore")
    chapter = text_to_html(text, options, title=title).encode("utf-8")
    uid = f"urn:uuid:{uuid.uuid4()}"
    files = {
        "META-INF/container.xml": CONTAINER_XML.encode("utf-8"),
        "OEBPS/nav.xhtml": _nav_html(title).encode("utf-8"),
        "OEBPS/chapter_001.xhtml": chapter,
        "OEBPS/package.opf": _package_opf(title, uid).encode("utf-8"),
    }
    _write_epub_zip(files, output_path)
    return output_path


def build_epub_from_html(
    input_path: Path, output_path: Path, options: ConvertOptions
) -> Path:
    title = input_path.stem
    html = input_path.read_text(encoding="utf-8", errors="ignore")
    chapter = normalize_html(html, options, title=title).encode("utf-8")
    uid = f"urn:uuid:{uuid.uuid4()}"
    files = {
        "META-INF/container.xml": CONTAINER_XML.encode("utf-8"),
        "OEBPS/nav.xhtml": _nav_html(title).encode("utf-8"),
        "OEBPS/chapter_001.xhtml": chapter,
        "OEBPS/package.opf": _package_opf(title, uid).encode("utf-8"),
    }
    _write_epub_zip(files, output_path)
    return output_path


def _nav_html(title: str) -> str:
    safe = escape(title)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{safe}</title></head>
<body>
<nav epub:type="toc" id="toc">
  <ol><li><a href="chapter_001.xhtml">{safe}</a></li></ol>
</nav>
</body>
</html>
"""


def _package_opf(title: str, uid: str) -> str:
    safe = escape(title)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<package version="3.0" unique-identifier="pub-id" xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{escape(uid)}</dc:identifier>
    <dc:title>{safe}</dc:title>
    <dc:language>ja</dc:language>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="chapter-001" href="chapter_001.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine page-progression-direction="ltr">
    <itemref idref="chapter-001"/>
  </spine>
</package>
"""


def guess_input_kind(input_path: Path) -> str:
    suffix = input_path.suffix.lower()
    if suffix == ".epub":
        return "epub"
    if suffix == ".txt":
        return "txt"
    if suffix in {".html", ".xhtml", ".htm"}:
        return "html"
    guessed, _ = mimetypes.guess_type(input_path.name)
    if guessed == "application/epub+zip":
        return "epub"
    raise ValueError(f"Unsupported input type: {input_path}")
