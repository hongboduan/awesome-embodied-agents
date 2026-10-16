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


def entry_date(paper):
    """Collection dates order non-paper entries without inventing publication dates."""
    return paper.get("date") or (paper.get("addedAt", "") if paper.get("sourceType") in {"project", "article"} else "")


def load_research_map(root, papers):
    """Publish only well-formed, source-backed editorial relationships."""
    empty = {"version": 1, "routes": [], "resources": [], "relations": [], "teams": []}
    path = Path(root) / "data/research-map.json"
    if not path.exists():
        return empty
    atlas = read_json(path, empty)
    if not isinstance(atlas, dict) or atlas.get("version") != 1:
        raise ValueError("Research map: unsupported schema")
    paper_by_id = {p["id"]: p for p in papers}

    def check_date(value, context):
        try:
            dt.date.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(f"Research map: invalid check date in {context}") from None

    def check_sources(item, context):
        sources = item.get("sources", [])
        if not isinstance(sources, list) or not sources:
            raise ValueError(f"Research map: missing evidence in {context}")
        for source in sources:
            url = urlparse(source.get("url", ""))
            if not source.get("label") or url.scheme != "https" or not url.netloc:
                raise ValueError(f"Research map: invalid evidence source in {context}")
        check_date(item.get("checkedAt"), context)

    def collection(key):
        values = atlas.get(key)
        if not isinstance(values, list):
            raise ValueError(f"Research map: {key} must be a list")
        ids = [item.get("id") for item in values]
        if any(not isinstance(i, str) or not re.fullmatch(r"[a-z0-9-]+", i) for i in ids) or len(ids) != len(set(ids)):
            raise ValueError(f"Research map: invalid or duplicate {key} IDs")
        return values

    def paper_refs(ids, context, curated=False):
        if not isinstance(ids, list) or len(ids) != len(set(ids)):
            raise ValueError(f"Research map: duplicate paper references in {context}")
        for identifier in ids:
            if identifier not in paper_by_id:
                raise ValueError(f"Research map: unknown paper {identifier} in {context}")
            if curated and not paper_by_id[identifier].get("curated"):
                raise ValueError(f"Research map: unreviewed paper {identifier} in {context}")

    check_date(atlas.get("updatedAt"), "map")
    resources = collection("resources")
    resource_ids = {r["id"] for r in resources}
    if resource_ids & paper_by_id.keys():
        raise ValueError("Research map: resource IDs overlap papers")
    for resource in resources:
        url = urlparse(resource.get("url", ""))
        if resource.get("kind") not in {"model", "benchmark", "platform"} or not resource.get("name") or url.scheme != "https" or not url.netloc:
            raise ValueError(f"Research map: invalid resource {resource['id']}")
    for route in collection("routes"):
        if not all(route.get(k) for k in ("title", "question", "summary", "readingQuestion", "paperIds")):
            raise ValueError(f"Research map: incomplete route {route['id']}")
        all_ids = []
        for key in ("paperIds", "backgroundIds", "frontierIds"):
            refs = route.get(key, [])
            paper_refs(refs, route["id"], curated=key != "frontierIds")
            all_ids += refs
        if len(all_ids) != len(set(all_ids)):
            raise ValueError(f"Research map: overlapping reading groups in {route['id']}")
    known = set(paper_by_id) | resource_ids
    seen = set()
    for relation in collection("relations"):
        source, target = relation.get("source"), relation.get("target")
        kind = relation.get("type")
        if source not in paper_by_id or target not in known or source == target:
            raise ValueError(f"Research map: invalid endpoints in {relation['id']}")
        if kind not in {"uses_model", "evaluated_on", "extends", "distills", "comparison"}:
            raise ValueError(f"Research map: invalid relationship type in {relation['id']}")
        if type(relation.get("editorial")) is not bool or relation["editorial"] != (kind == "comparison"):
            raise ValueError(f"Research map: editorial comparison must be distinguished in {relation['id']}")
        if not relation.get("label") or not relation.get("explanation"):
            raise ValueError(f"Research map: missing relationship explanation in {relation['id']}")
        key = (kind, *sorted((source, target))) if kind == "comparison" else (kind, source, target)
        if key in seen:
            raise ValueError(f"Research map: duplicate relationship in {relation['id']}")
        seen.add(key)
        check_sources(relation, relation["id"])
    for team in collection("teams"):
        if not team.get("name") or not team.get("summary") or not team.get("workIds"):
            raise ValueError(f"Research map: incomplete team {team['id']}")
        paper_refs(team["workIds"], team["id"], curated=True)
        check_sources(team, team["id"])
    return atlas


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
        related = p.get("relatedPaper") or {}
        related_id, _ = arxiv_identity(related.get("id") or related.get("url"))
        if related_id in versions:
            latest = versions[related_id]
            p["relatedPaper"] = {**related, "latestVersion": latest["version"],
                                 "latestUrl": latest.get("url"), "latestUpdatedAt": latest.get("updated")}
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
    return sorted(merged.values(), key=lambda p: (entry_date(p), p.get("title", "")), reverse=True)


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
                  ("year", str(p.get("year") or (p.get("date") or "")[:4])),
                  ("url", safe_url(p.get("links", {}).get("paper")) or safe_url(p.get("links", {}).get("article")) or safe_url(p.get("links", {}).get("project")))]
        if p.get("sourceType") == "project" and not p.get("date"):
            fields.append(("note", "Project page; publication date unverified"))
        if p.get("sourceType") == "article":
            fields.append(("note", "Web essay / Perspective"))
        if base:
            fields += [("eprint", base), ("archivePrefix", "arXiv")]
        # Bibliography exports are metadata; verify full author lists before manuscript submission.
        entries.append("@misc{" + key + ",\n" + ",\n".join("  " + k + " = {" + v + "}" for k, v in fields if v) + "\n}")
    return "\n\n".join(entries) + "\n"


def update_readme(path, papers, english=False, focus_since="2026-09-01"):
    """Generate a navigable reading list: one primary section per editorial entry."""
    from urllib.parse import quote

    if not path.exists():
        return
    start, end = "<!-- ATLAS:START -->", "<!-- ATLAS:END -->"
    content = path.read_text(encoding="utf-8")
    if start not in content or end not in content:
        raise ValueError(f"Missing generated section markers: {path.name}")
    curated = sorted((p for p in papers if p.get("curated") and p.get("review") != "candidate"),
                     key=lambda p: (entry_date(p), p.get("title", "")), reverse=True)
    candidates = sum(p.get("review") == "candidate" for p in papers)
    checked = sum(p.get("review") == "source-checked" for p in papers)
    reviewed = sum(p.get("review") == "full-review" for p in papers)
    drafts = sum(p.get("review") == "ai-draft" for p in papers)
    projects = [p for p in curated if p.get("sourceType") == "project"]
    articles = [p for p in curated if p.get("sourceType") == "article"]
    research = [p for p in curated if p.get("sourceType") not in {"project", "article"}]
    recent = [p for p in research if entry_date(p) >= focus_since]
    earlier = [p for p in research if entry_date(p) < focus_since]
    selected_earlier = [p for p in earlier if p.get("featuredBackground") is True and entry_date(p)]
    earlier = [p for p in earlier if p not in selected_earlier]
    counts = (f"{len(curated)} curated entries · {len(research)} paper{'s' if len(research) != 1 else ''} · {len(projects)} project{'s' if len(projects) != 1 else ''} · {len(articles)} perspective{'s' if len(articles) != 1 else ''}"
              if english else f"精选 {len(curated)} 条 · 论文 {len(research)} 篇 · 项目 {len(projects)} 个 · 观点 {len(articles)} 篇")
    status = (f"{checked} source-checked · {reviewed} full-review · {drafts} AI drafts · {candidates} discovery candidates"
              if english else f"来源核对 {checked} 条 · 全文核读 {reviewed} 篇 · AI 草稿 {drafts} 篇 · 自动候选 {candidates} 篇")
    home = safe_url(read_json(path.parent / "config.json", {}).get("siteUrl"))
    category_names = {c["id"]: c["en"] if english else c["label"] for c in CATEGORIES}
    categories = CATEGORIES + [{"id": "other", "en": "Other agent research", "label": "其他 Agent 研究"}]

    def primary(p):
        return next((c for c in p.get("categories", []) if c in category_names), "other")

    def badge(label, target, color, logo=None, message=None, alt=None):
        target = safe_url(target)
        if not target:
            return ""
        parts = [quote(label.replace("-", "--"), safe="")]
        if message:
            parts.append(quote(str(message).replace("-", "--"), safe=""))
        parts.append(color)
        image = "https://img.shields.io/badge/" + "-".join(parts) + "?style=flat-square"
        if logo:
            image += "&logo=" + logo + "&logoColor=white"
        return f"[![{md(alt or label)}]({image})]({target})"

    def entry(p, detailed=True):
        links = p.get("links", {})
        kind = p.get("sourceType", "paper")
        target = next((safe_url(links.get(k)) for k in ("paper", "article", "project", "code") if safe_url(links.get(k))), "")
        title = f"[{md(p['title'])}]({target})" if target else md(p["title"])
        date = p.get("date") or (("added " if english else "收录于 ") + p.get("addedAt", ""))
        meta = [md(date)] if date else []
        if kind == "project":
            meta.append("Project preview" if english else "项目预览")
        elif kind == "article":
            meta += [md(p.get("authors", "")), "Perspective / essay" if english else "观点文章"]
        else:
            meta.extend(category_names[c] for c in p.get("categories", []) if c in category_names)
        result = [f"- **{title}**<br>", "  " + " · ".join(v for v in meta if v) + "<br>"]
        summary = (p.get("summaryEn") or p.get("summaryZh")) if english else p.get("summaryZh")
        if detailed and summary:
            result.append("  " + md(summary) + "<br>")
        badges = []
        paper_url = safe_url(links.get("paper")) or safe_url((p.get("relatedPaper") or {}).get("url"))
        if paper_url:
            base, _ = arxiv_identity(paper_url)
            badges.append(badge("arXiv" if base else "Paper", paper_url, "B31B1B", "arxiv" if base else None,
                                base, "arXiv: " + base if base else "Read the paper"))
        if safe_url(links.get("code")):
            github = urlparse(links["code"]).netloc.lower() == "github.com"
            badges.append(badge("GitHub" if github else "Code", links["code"], "181717", "github" if github else None,
                                alt="GitHub source code" if github else "Source code"))
        if safe_url(links.get("project")):
            badges.append(badge("Project", links["project"], "2563EB", alt="Project website"))
        if safe_url(links.get("article")):
            badges.append(badge("Article", links["article"], "7C3AED", alt="Read the original article"))
        if home:
            badges.append(badge("Reading card", home + "#paper=" + quote(str(p["id"]), safe=""), "0F766E", alt="中文阅读与横竖屏卡片"))
        if badges:
            result.append("  " + " ".join(badges))
        return result + [""]

    lines = [start, "", "**" + counts + "**", "", status, "", "## " + ("Contents" if english else "目录"), ""]
    if recent:
        lines.append("- [" + ("Recent papers" if english else "近期论文") + "](#recent-papers)")
        for cat in categories:
            members = [p for p in recent if primary(p) == cat["id"]]
            if members:
                label = cat["en"] if english else cat["label"]
                lines.append(f"  - [{label} · {len(members)}](#recent-{cat['id']})")
    if selected_earlier:
        lines.append("- [" + ("Selected earlier foundations" if english else "重点补充 · 早期首发") + "](#selected-earlier)")
    if projects:
        lines.append("- [" + ("Projects and systems" if english else "项目与系统") + "](#projects)")
    if articles:
        lines.append("- [" + ("Perspectives and essays" if english else "观点与讨论") + "](#perspectives)")
    if earlier:
        lines.append("- [" + ("Foundations and earlier work" if english else "背景阅读与早期工作") + "](#earlier-work)")
    lines += ["", ("Each paper appears once under its primary topic; secondary topics remain visible as tags. English titles link to original sources; Chinese notes and reading cards are available alongside them."
                    if english else "每篇论文只列在一个主分类下，其他研究方向保留为标签；点击徽章可直接打开原文、代码、项目主页或阅读卡片。"), ""]
    if recent:
        lines += ['<a id="recent-papers"></a>', "", "## " + (f"Recent embodied agents · since {focus_since}" if english else f"近期具身 Agent · {focus_since} 起"), ""]
        for cat in categories:
            members = [p for p in recent if primary(p) == cat["id"]]
            if members:
                lines += [f'<a id="recent-{cat["id"]}"></a>', "", "### " + (cat["en"] if english else cat["label"]), ""]
                for p in members:
                    lines += entry(p)
    if selected_earlier:
        lines += ['<a id="selected-earlier"></a>', "", "## " + ("Selected earlier foundations" if english else "重点补充 · 早期首发"), "",
                  "Selected earlier work relevant to current embodied-agent research. Original publication dates are retained." if english else "与当前具身 Agent 议题直接相关的早期工作，保留真实首发日期。", ""]
        for p in selected_earlier:
            lines += entry(p)
    if projects:
        lines += ['<a id="projects"></a>', "", "## " + ("Projects and systems" if english else "项目与系统"), "",
                  "Project previews; collection dates are labeled when publication dates are unverified." if english else "官方项目预览；首发日期未核实时，明确标注收录日期。", ""]
        for p in projects:
            lines += entry(p)
    if articles:
        lines += ['<a id="perspectives"></a>', "", "## " + ("Perspectives and essays" if english else "观点与讨论"), "",
                  "Author perspectives and essays, listed separately from experimental papers." if english else "作者观点与研究随笔，和报告实验结果的论文分开列出。", ""]
        for p in articles:
            lines += entry(p)
    if earlier:
        lines += ['<a id="earlier-work"></a>', "", "<details>", "<summary>" + (f"Foundations and earlier work ({len(earlier)} papers)" if english else f"背景阅读与早期工作（{len(earlier)} 篇，展开）") + "</summary>", ""]
        for cat in categories:
            members = [p for p in earlier if primary(p) == cat["id"]]
            if members:
                lines += ["### " + (cat["en"] if english else cat["label"]), ""]
                for p in members:
                    lines += entry(p, detailed=False)
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
            rss_events.append({"id": "paper-" + paper_key(p), "paperId": paper_key(p), "type": "paper", "date": entry_date(p) or updated, "title": p["title"], "message": p.get("summaryZh", "")})
    for event in sorted(rss_events, key=lambda e: e.get("date", ""), reverse=True)[:100]:
        p = lookup.get(event.get("paperId"), {})
        link = safe_url(event.get("url")) or safe_url(p.get("links", {}).get("paper")) or safe_url(p.get("links", {}).get("article")) or safe_url(p.get("links", {}).get("project")) or home
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
    result = {"papers": papers, "categories": CATEGORIES, "updatedAt": updated, "updateStatus": status,
              "enrichmentStatus": read_json(root / "data/enrichment-status.json", {}),
              "researchMap": load_research_map(root, papers), "events": events,
              "site": {"title": "Embodied Agent Atlas", "url": config.get("siteUrl", ""), "repository": config.get("repositoryUrl", ""), "focusSince": config.get("focusSince", "2026-09-01")}}
    write_json(out / "data.json", result)
    write_json(out / "papers.json", papers)
    payload = json.dumps(result, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    (out / "data.js").write_text("window.ATLAS_DATA = " + payload + ";\n", encoding="utf-8")
    (out / "papers.bib").write_text(bibtex(papers), encoding="utf-8")
    (out / "feed.xml").write_bytes(make_rss(papers, events, config, updated))
    (out / ".nojekyll").touch()
    for name in ["index.html", "app.js", "styles.css", "cards.js", "map.js", "map.css", "updates.js", "updates.css"]:
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
