#!/usr/bin/env python3
"""Extract attributable cover images and page text from versioned arXiv PDFs.

Public API::

    result = extract_paper(paper, repository_root, config)
    pages = read_text_pages(result, repository_root)

``config`` is the complete site configuration; optional controls live under
``pdf``. The result is safe to store publicly: ``figure.path`` is relative to
``web/``, and page numbers are one-based PDF pages. Raw PDFs and extracted text
stay in ``.cache/papers``. No model, API key, or generated imagery is involved.
Automatic figure selection is heuristic, not a claim that a figure was reviewed.
If no credible caption/graphic pair exists, the result explicitly says
``kind: page-preview``. Errors raise; callers should retain previous good data.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import time
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

try:
    import pymupdf as fitz
except ImportError:
    import fitz


EXTRACTOR_VERSION = 5
ARXIV_ID = re.compile(r"(?<![\w.])((?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7}))(?:v([1-9]\d*))?(?:\.pdf)?(?=$|[?#/])")
CAPTION = re.compile(r"^(?i:Figure|Fig\.?)\s*(\d+)(?:\s*[:.|\-–—]\s*|\s+(?=[A-Z]))(.*)")
FRAMEWORK_WORDS = re.compile(r"\b(framework|architecture|overview|pipeline|workflow|interaction grammar)\b", re.I)
_last_request = None


def _atomic_bytes(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _atomic_json(path, data):
    _atomic_bytes(path, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())


def _identity(paper):
    values = [paper.get("arxivId"), paper.get("latestPaperUrl"),
              paper.get("links", {}).get("paper"), paper.get("id")]
    matched = [(value, ARXIV_ID.search(str(value or ""))) for value in values]
    matched = [(value, match) for value, match in matched if match]
    if not matched:
        raise ValueError("PDF extraction requires a canonical arXiv identifier")
    identifier = matched[0][1].group(1)
    if any(match.group(1) != identifier for _, match in matched):
        raise ValueError("Conflicting arXiv identifiers in paper record")
    version = paper.get("latestVersion") or paper.get("version")
    if not version:
        versions = [int(match.group(2)) for _, match in matched if match.group(2)]
        version = max(versions) if versions else None
    if isinstance(version, bool) or not str(version or "").isdigit() or int(version) < 1:
        raise ValueError("PDF extraction requires an explicit arXiv version; refresh metadata first")
    return identifier, int(version)


def _check_arxiv_url(url):
    parsed = urlparse(url)
    if (parsed.scheme != "https" or parsed.hostname not in {"arxiv.org", "export.arxiv.org"}
            or parsed.username or parsed.password or parsed.port not in {None, 443}):
        raise ValueError("PDF download may only use HTTPS arxiv.org URLs")
    return url


class _ArxivRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _check_arxiv_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_pdf(source_url, destination, settings):
    """Bounded serial download, validating every redirect and the PDF signature.

    Cached version-specific PDFs do not cause a network request. A 429/503 ends
    this attempt instead of multiplying server load; the next run may retry.
    """
    global _last_request
    _check_arxiv_url(source_url)
    maximum = min(80_000_000, max(1024, int(settings.get("maxDownloadBytes", 25_000_000))))
    destination = Path(destination)
    if destination.exists():
        if destination.stat().st_size > maximum:
            raise ValueError("Cached PDF exceeds configured size limit")
        with destination.open("rb") as cached:
            if not cached.read(1024).lstrip().startswith(b"%PDF-"):
                raise ValueError("Cached file is not a PDF")
        return destination
    interval = max(3.1, float(settings.get("minRequestIntervalSeconds", 3.1)))
    if _last_request is not None:
        delay = interval - (time.monotonic() - _last_request)
        if delay > 0:
            time.sleep(delay)
    _last_request = time.monotonic()
    request = Request(source_url, headers={
        "User-Agent": settings.get("userAgent", "EmbodiedAgentAtlas/1.0 (arXiv paper cards)"),
        "Accept": "application/pdf", "Accept-Encoding": "identity",
    })
    timeout = min(90, max(5, float(settings.get("timeoutSeconds", 45))))
    deadline = time.monotonic() + max(timeout, min(240, float(settings.get("maxDownloadSeconds", 120))))
    try:
        with build_opener(_ArxivRedirects()).open(request, timeout=timeout) as response:
            _check_arxiv_url(response.geturl())
            length = response.headers.get("Content-Length")
            if length and int(length) > maximum:
                raise ValueError("PDF exceeds configured download size limit")
            chunks, count = [], 0
            while True:
                if time.monotonic() > deadline:
                    raise TimeoutError("PDF download exceeded total time budget")
                chunk = response.read(min(262144, maximum + 1 - count))
                if not chunk:
                    break
                chunks.append(chunk)
                count += len(chunk)
                if count > maximum:
                    raise ValueError("PDF exceeds configured download size limit")
            payload = b"".join(chunks)
    except HTTPError as error:
        if error.code in {429, 503}:
            raise RuntimeError(f"arXiv is rate limited/unavailable ({error.code}); retry on a later run") from error
        raise
    if not payload[:1024].lstrip().startswith(b"%PDF-"):
        raise ValueError("arXiv returned a non-PDF response")
    _atomic_bytes(destination, payload)
    return destination


def _text_blocks(page):
    return [(fitz.Rect(block[:4]), " ".join(block[4].split()), block[4])
            for block in page.get_text("blocks") if block[6] == 0 and block[4].strip()]


def find_captions(page):
    """Return candidate captions with geometry, including vector-figure captions."""
    result = []
    for block in page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]:
        if block.get("type") != 0:
            continue
        lines = block.get("lines", [])
        for index, line in enumerate(lines):
            text = "".join(span["text"] for span in line.get("spans", [])).strip()
            match = CAPTION.match(text)
            if not match:
                continue
            remaining = lines[index:]
            caption = " ".join("".join(span["text"] for span in ln.get("spans", [])).strip() for ln in remaining)
            rectangle = fitz.Rect(line["bbox"])
            for ln in remaining[1:]:
                rectangle |= fitz.Rect(ln["bbox"])
            number = int(match.group(1))
            # Match the description, not generic 'method' in a benchmark's long
            # discussion. Body sentences such as 'Figure 2 shows' are not captions.
            description = CAPTION.sub(r"\2", caption).split(". ", 1)[0]
            score = (120 if FRAMEWORK_WORDS.search(description) else 0) + max(0, 24 - number * 4)
            result.append({"rect": rectangle, "caption": caption[:2000], "number": number,
                           "figureLabel": f"Figure {number}", "score": score})
    return result


def _graphics(page):
    """Image + vector bounds; raster-only extraction loses composite diagrams."""
    bounds = []
    for item in page.get_image_info():
        bounds.append(fitz.Rect(item["bbox"]))
    for drawing in page.get_drawings():
        bounds.append(fitz.Rect(drawing["rect"]))
    # Drop full-page background fills, invisible/degenerate marks, and rules.
    area = page.rect.width * page.rect.height
    return [rect for rect in bounds if rect.width > 2 and rect.height > 2
            and rect.width * rect.height < area * 0.88 and rect.intersects(page.rect)]


def figure_rectangle(page, caption, all_captions=None):
    """Locate the graphic cluster immediately above a caption, conservatively.

    Render the complete native page region (vectors, embedded images and labels),
    never a single embedded image that might be one panel of a composite figure.
    """
    box = caption["rect"]
    page_box = page.rect
    if box.width > page_box.width * 0.46:
        # A one-line caption may be shorter than the full-width diagram.
        left, right = 16, page_box.width - 16
    elif box.x0 >= page_box.width * 0.47:
        left, right = page_box.width * 0.48, page_box.width - 16
    else:
        left, right = 16, page_box.width * 0.52
    upper = max(16, box.y0 - page_box.height * 0.70)
    for other in all_captions or []:
        previous = other["rect"]
        if previous.y1 < box.y0 and previous.x1 > left and previous.x0 < right:
            upper = max(upper, previous.y1 + 4)
    graphics = [r for r in _graphics(page) if r.y1 <= box.y0 + 2 and r.y0 >= upper
                and r.x1 > left + 8 and r.x0 < right - 8]
    if not graphics:
        return None
    anchor = max(graphics, key=lambda r: r.y1)
    if box.y0 - anchor.y1 > 80:
        return None
    selected = [anchor]
    top = anchor.y0
    # Merge the nearest visual band upward. A large blank gap is a boundary.
    for rect in sorted(graphics, key=lambda r: r.y1, reverse=True):
        if rect.y1 >= top - 38:
            selected.append(rect)
            top = min(top, rect.y0)
    region = fitz.Rect(selected[0])
    for rect in selected[1:]:
        region |= rect
    if region.height < 35 or region.width < 65:
        return None
    # Include nearby figure labels, while excluding paragraphs and the caption.
    for rect, text, raw in _text_blocks(page):
        if (rect.y1 <= box.y0 + 1 and rect.y0 >= region.y0 - 18
                and rect.x1 >= region.x0 - 18 and rect.x0 <= region.x1 + 18
                and len(text) < 350 and rect.height < 80):
            region |= rect
    region = fitz.Rect(max(left, region.x0 - 6), max(upper, region.y0 - 6),
                       min(right, region.x1 + 6), min(box.y0 - 3, region.y1 + 6))
    if region.is_empty or region.height < 40 or region.width < 80:
        return None
    return region & page.rect


def select_cover(document, settings=None, figure_hint=None):
    """Return page index, clipping rectangle, and honest figure provenance."""
    settings = settings or {}
    figure_hint = figure_hint or {}
    hint_page = figure_hint.get("page")
    hint_label = figure_hint.get("figureLabel")
    inspect_count = min(len(document), max(1, int(settings.get("maxPagesToInspect", 12))))
    indices = set(range(inspect_count))
    if isinstance(hint_page, int) and 1 <= hint_page <= len(document):
        indices.add(hint_page - 1)
    candidates = []
    for index in sorted(indices):
        page = document[index]
        captions = find_captions(page)
        for caption in captions:
            rectangle = figure_rectangle(page, caption, captions)
            if rectangle is not None:
                # Favor early figures; caption semantics dominate this tie break.
                hinted = bool(hint_label and caption["figureLabel"].lower() == str(hint_label).lower()
                              and (not hint_page or index + 1 == hint_page))
                score = caption["score"] - index * 0.75 + (1000 if hinted else 0)
                candidates.append((score, index, rectangle, caption, hinted))
    if candidates:
        _, index, rectangle, caption, hinted = max(candidates, key=lambda item: item[0])
        return index, rectangle, {"kind": "figure", "caption": caption["caption"],
                                  "figureLabel": caption["figureLabel"],
                                  "selection": "source-hint" if hinted else "automatic"}
    return 0, document[0].rect, {"kind": "page-preview", "caption": "论文 PDF 第 1 页预览；未自动定位可靠框架图。",
                               "figureLabel": None, "selection": "automatic-fallback"}


def read_text_pages(result, root):
    """Read private text cache for evidence-grounded summarization."""
    path = Path(root) / result["pdf"]["textPath"]
    return json.loads(path.read_text(encoding="utf-8"))["pages"]


def extract_paper(paper, root, config=None):
    """Download a versioned source, cache page text, and write its native cover.

    The input record and editorial fields are never mutated. Version-specific
    cache metadata avoids repeating parsing or rendering on unchanged sources.
    """
    root = Path(root)
    settings = (config or {}).get("pdf", {})
    identifier, version = _identity(paper)
    key = f"{identifier.replace('/', '_')}-v{version}"
    cache = root / ".cache" / "papers"
    source_url = f"https://arxiv.org/pdf/{identifier}v{version}"
    pdf_path = cache / f"{key}.pdf"
    text_path = cache / f"{key}.text.json"
    metadata_path = cache / f"{key}.asset.json"
    image_path = root / "web" / "assets" / "papers" / f"{key}.png"
    figure_hint = paper.get("figureHint", {})
    fingerprint = hashlib.sha256(json.dumps({"version": EXTRACTOR_VERSION, "settings": settings, "figureHint": figure_hint}, sort_keys=True).encode()).hexdigest()[:16]
    if metadata_path.exists() and text_path.exists() and image_path.exists():
        previous = json.loads(metadata_path.read_text(encoding="utf-8"))
        if previous.get("fingerprint") == fingerprint:
            return previous["result"]
    download_pdf(source_url, pdf_path, settings)
    with fitz.open(pdf_path) as document:
        if document.needs_pass or not len(document):
            raise ValueError("PDF is encrypted or has no pages")
        page_count = len(document)
        maximum_pages = min(300, max(1, int(settings.get("maxTextPages", 120))))
        pages = [{"page": i + 1, "text": document[i].get_text("text", sort=True)[:80000]}
                 for i in range(min(page_count, maximum_pages))]
        index, rectangle, figure = select_cover(document, settings, figure_hint)
        scale = min(3, max(1, float(settings.get("renderScale", 2))))
        # Bound raster memory even for unusually large PDF page dimensions.
        scale = min(scale, 2200 / max(rectangle.width, rectangle.height))
        pixmap = document[index].get_pixmap(matrix=fitz.Matrix(scale, scale), clip=rectangle, alpha=False, colorspace=fitz.csRGB)
        image_payload = pixmap.tobytes("png")
        figure.update({"path": f"assets/papers/{key}.png", "sourceUrl": source_url,
                       "page": index + 1, "version": version,
                       "width": pixmap.width, "height": pixmap.height,
                       "crop": [round(v, 2) for v in rectangle]})
    extracted_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    result = {"pdf": {"status": "extracted", "arxivId": identifier, "sourceUrl": source_url,
                      "version": version, "pageCount": page_count,
                      "textPages": len(pages), "textTruncated": len(pages) < page_count,
                      "textPath": text_path.relative_to(root).as_posix(), "extractedAt": extracted_at},
              "figure": figure}
    _atomic_json(text_path, {"sourceUrl": source_url, "version": version, "pages": pages})
    _atomic_bytes(image_path, image_payload)
    _atomic_json(metadata_path, {"fingerprint": fingerprint, "result": result})
    return result
