#!/usr/bin/env python3
"""Build the offline-capable Atlas site and Awesome index (standard library only)."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from email.utils import format_datetime

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = [
    {"id": "planning", "label": "推理与规划", "en": "Reasoning & Planning"},
    {"id": "spatial", "label": "空间理解", "en": "Spatial Understanding"},
    {"id": "memory", "label": "记忆与知识", "en": "Memory & Knowledge"},
    {"id": "code", "label": "技能与代码", "en": "Skills & Code"},
    {"id": "recovery", "label": "监控与恢复", "en": "Monitoring & Recovery"},
    {"id": "policies", "label": "VLA / WAM", "en": "VLA & World Models"},
    {"id": "learning", "label": "自我改进", "en": "Self-improvement"},
    {"id": "evaluation", "label": "基准与评测", "en": "Benchmarks & Evaluation"},
]
DEFAULT_STATUS = {"mode": "setup-required", "scheduleEnabled": False, "lastSuccess": None, "lastAttempt": None,
                  "message": "每日更新流程已准备，等待连接 GitHub 仓库"}
ARXIV_RE = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/)?((?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7}))(?:v(\d+))?", re.I)


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def arxiv_identity(value):
    match = ARXIV_RE.search(str(value or ""))
    return (match.group(1).lower(), int(match.group(2) or 1)) if match else (None, None)


def paper_key(paper):
    for value in [paper.get("arxivId"), paper.get("id"), paper.get("links", {}).get("paper")]:
        base, _ = arxiv_identity(value)
        if base:
            return base
    return str(paper["id"]).lower()


def paper_version(paper):
    if paper.get("version"):
        return int(str(paper["version"]).lstrip("v"))
    for value in [paper.get("arxivId"), paper.get("links", {}).get("paper"), paper.get("id")]:
        match = ARXIV_RE.search(str(value or ""))
        if match and match.group(2):
            return int(match.group(2))
    # An unversioned URL resolves to the latest paper, not necessarily v1.
    # Missing editorial version establishes a baseline on first source lookup.
    return None


def load_papers(root=ROOT):
    """Editorial seeds take precedence over discovery; highest versions deduplicate candidates."""
    merged = {}
    candidates = read_json(root / "data/candidates.json", [])
    for original in candidates:
        p = dict(original)
        p.update(curated=False, deepRead=False, review="candidate")
        key = paper_key(p)
        if key not in merged or (paper_version(p) or 0) > (paper_version(merged[key]) or 0):
            merged[key] = p
    for source in sorted((root / "data").glob("seed-*.json")):
        for p in read_json(source, []):
            key = paper_key(p)
            old = merged.get(key)
            if old and old.get("review") != "candidate" and old != p:
                raise ValueError(f"Conflicting editorial seed for {key}: {source.name}")
            merged[key] = dict(p)
    versions = read_json(root / "data/versions.json", {})
    for key, p in merged.items():
        if key in versions:
            p["latestVersion"] = versions[key]["version"]
            p["versionUpdatedAt"] = versions[key].get("updated")
            p["latestPaperUrl"] = versions[key].get("url")
            p["reviewedVersion"] = paper_version(p)
    enrichments = read_json(root / "data/enrichments.json", {})
    for key, p in merged.items():
        enrichment = enrichments.get(key, {})
        version = p.get("latestVersion") or paper_version(p)
        figure = enrichment.get("figure", {})
        if figure and enrichment.get("version") == version:
            relative = str(figure.get("path", ""))
            if relative.startswith("assets/papers/") and ".." not in relative.split("/") and (root / "web" / relative).is_file():
                p["figure"] = dict(figure)
        pdf = enrichment.get("pdf", {})
        if pdf:
            p["pdf"] = {k: v for k, v in pdf.items() if k != "textPath"}
        ai = enrichment.get("ai", {})
        if ai.get("status") == "ready" and ai.get("version", enrichment.get("version")) == version:
            p["aiAnalysis"] = ai
            p["social"] = ai.get("social", {})
            # An automatic draft cannot overwrite a source-checked/editorial reading.
            if p.get("review") == "candidate":
                for field in ["summaryZh", "problem", "method", "findings", "limitations", "role", "evidence"]:
                    if field in ai:
                        p[field] = ai[field]
                p.update(review="ai-draft", curated=False, deepRead=False, reviewedVersion=version)
    return sorted(merged.values(), key=lambda p: (p.get("date", ""), p.get("title", "")), reverse=True)


def safe_url(value):
    value = str(value or "")
    return value if urlparse(value).scheme == "https" and urlparse(value).netloc else ""


def md(value):
    return str(value or "").replace("|", "\\|").replace("\n", " ").replace("[", "\\[").replace("]", "\\]")


def bibtex(papers):
    def escape(value):
        return str(value).replace("\\", "\\textbackslash{}").replace("{", "\\{").replace("}", "\\}").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#")
    entries = []
    for p in papers:
        base, _ = arxiv_identity(p.get("links", {}).get("paper"))
        key = re.sub(r"[^a-zA-Z0-9]", "", p["id"])
        fields = [("title", "{" + escape(p["title"]) + "}"), ("author", escape(p.get("authors") or "Unknown")),
                  ("year", str(p.get("year") or p.get("date", "")[:4])), ("url", safe_url(p.get("links", {}).get("paper")))]
        if base:
            fields += [("eprint", base), ("archivePrefix", "arXiv")]
        # Bibliography exports are metadata; verify full author lists before manuscript submission.
        entries.append("@misc{" + key + ",\n" + ",\n".join("  " + k + " = {" + v + "}" for k, v in fields if v) + "\n}")
    return "\n\n".join(entries) + "\n"


def update_readme(path, papers, english=False, focus_since="2026-09-01"):
    if not path.exists():
        return
    start, end = "<!-- ATLAS:START -->", "<!-- ATLAS:END -->"
    content = path.read_text(encoding="utf-8")
    if start not in content or end not in content:
        raise ValueError(f"Missing generated section markers: {path.name}")
    curated = [p for p in papers if p.get("curated") and p.get("review") != "candidate"]
    candidates = sum(p.get("review") == "candidate" for p in papers)
    checked = sum(p.get("review") == "source-checked" for p in papers)
    reviewed = sum(p.get("review") == "full-review" for p in papers)
    drafts = sum(p.get("review") == "ai-draft" for p in papers)
    counts = (f"{len(papers)} papers · {len(curated)} curated · {checked} source-checked · {reviewed} full-review · {drafts} AI drafts · {candidates} discovery candidates"
              if english else f"共 {len(papers)} 篇 · 精选 {len(curated)} 篇 · 来源核对 {checked} 篇 · 全文核读 {reviewed} 篇 · AI 草稿 {drafts} 篇 · 自动候选 {candidates} 篇")
    lines = [start, "", counts, ""]
    for recent in [True, False]:
        subset = [p for p in curated if ((p.get("date", "") >= focus_since) == recent)]
        if not subset:
            continue
        if recent:
            lines += ["## " + (f"Recent embodied agents · since {focus_since}" if english else f"近期具身 Agent · {focus_since} 起"), ""]
        else:
            lines += ["<details>", "<summary>" + ("Foundations and earlier work" if english else "背景阅读与早期工作（展开）") + "</summary>", ""]
        for cat in CATEGORIES:
            members = [p for p in subset if cat["id"] in p.get("categories", [])]
            if not members:
                continue
            lines += ["### " + (cat["en"] if english else cat["label"]), ""]
            for p in members:
                links = p.get("links", {})
                extra = ""
                for k, label in [("code", "Code"), ("project", "Project")]:
                    if safe_url(links.get(k)):
                        extra += f" · [{label}]({safe_url(links[k])})"
                lines.append(f"- **[{md(p['title'])}]({safe_url(links.get('paper'))})** ({p.get('date') or p.get('year', '')}){extra}")
                if not english:
                    lines.append("  " + md(p.get("summaryZh", "")))
            lines.append("")
        if not recent:
            lines += ["</details>", ""]
    lines.append(end)
    before = content.split(start, 1)[0]
    after = content.split(end, 1)[1]
    path.write_text(before + "\n".join(lines) + after, encoding="utf-8")


def make_rss(papers, events, config, updated):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    home = safe_url(config.get("siteUrl")) or "https://arxiv.org/"
    for key, text in [("title", "Embodied Agent Atlas"), ("link", home), ("description", "具身 Agent 论文发现与版本动态；自动候选不等同于人工精选。"), ("language", "zh-CN")]:
        ET.SubElement(channel, key).text = text
    lookup = {paper_key(p): p for p in papers}
    rss_events = list(events)
    seen = {e.get("paperId") for e in events if e.get("type") == "discovered"}
    for p in papers:
        if paper_key(p) not in seen:
            rss_events.append({"id": "paper-" + paper_key(p), "paperId": paper_key(p), "type": "paper", "date": p.get("date", updated), "title": p["title"], "message": p.get("summaryZh", "")})
    for event in sorted(rss_events, key=lambda e: e.get("date", ""), reverse=True)[:100]:
        p = lookup.get(event.get("paperId"), {})
        link = safe_url(event.get("url")) or safe_url(p.get("links", {}).get("paper")) or home
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = event.get("title") or p.get("title", "论文动态")
        ET.SubElement(item, "link").text = link
        ET.SubElement(item, "description").text = event.get("message") or p.get("summaryZh", "")
        ET.SubElement(item, "guid", isPermaLink="false").text = event.get("id", link)
        try:
            date = dt.datetime.fromisoformat(event.get("date", updated).replace("Z", "+00:00"))
            if date.tzinfo is None:
                date = date.replace(tzinfo=dt.timezone.utc)
            ET.SubElement(item, "pubDate").text = format_datetime(date)
        except ValueError:
            pass
    return ET.tostring(rss, encoding="utf-8", xml_declaration=True)


def build(root=ROOT):
    root = Path(root)
    out = root / "dist"
    out.mkdir(parents=True, exist_ok=True)
    papers = load_papers(root)
    status = read_json(root / "data/update-status.json", DEFAULT_STATUS.copy())
    events = read_json(root / "data/events.json", [])
    config = read_json(root / "config.json", {})
    updated = utc_now()
    result = {"papers": papers, "categories": CATEGORIES, "updatedAt": updated, "updateStatus": status, "events": events, "site": {"title": "Embodied Agent Atlas", "url": config.get("siteUrl", ""), "repository": config.get("repositoryUrl", ""), "focusSince": config.get("focusSince", "2026-09-01")}}
    write_json(out / "data.json", result)
    write_json(out / "papers.json", papers)
    payload = json.dumps(result, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    (out / "data.js").write_text("window.ATLAS_DATA = " + payload + ";\n", encoding="utf-8")
    (out / "papers.bib").write_text(bibtex(papers), encoding="utf-8")
    (out / "feed.xml").write_bytes(make_rss(papers, events, config, updated))
    (out / ".nojekyll").touch()
    for name in ["index.html", "app.js", "styles.css", "cards.js"]:
        if (root / "web" / name).exists():
            shutil.copy2(root / "web" / name, out / name)
    if (root / "web/assets").exists():
        shutil.copytree(root / "web/assets", out / "assets", dirs_exist_ok=True)
    update_readme(root / "README.md", papers, english=True, focus_since=config.get("focusSince", "2026-09-01"))
    update_readme(root / "README.zh-CN.md", papers, focus_since=config.get("focusSince", "2026-09-01"))
    # The public site is a literature collection, not a downloadable project template.
    shutil.rmtree(out / "downloads", ignore_errors=True)
    print(f"Built {len(papers)} papers → {out}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    build(parser.parse_args().root)
