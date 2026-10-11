#!/usr/bin/env python3
"""Discover arXiv candidates and record revisions without rewriting editorial seeds."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import ROOT, DEFAULT_STATUS, arxiv_identity, load_papers, paper_key, paper_version, read_json, write_json

ATOM = "{http://www.w3.org/2005/Atom}"
OS = "{http://a9.com/-/spec/opensearch/1.1/}"
CATEGORY_TERMS = {
    "planning": ("planning", "reasoning", "task decomposition", "long-horizon"),
    "spatial": ("spatial", "3d", "scene graph", "grounding", "mapping"),
    "memory": ("memory", "retrieval", "knowledge"),
    "code": ("code", "program", "tool use", "skill composition"),
    "recovery": ("recovery", "failure", "monitor", "replanning", "verification"),
    "policies": ("vision-language-action", "vision language action", "vla", "world model", "world-action"),
    "learning": ("self-improvement", "self improvement", "self-refinement", "continual", "multi-agent"),
    "evaluation": ("benchmark", "evaluation", "dataset"),
}


def clean(value):
    return " ".join(str(value or "").split())


def parse_date(value):
    result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    return result if result.tzinfo else result.replace(tzinfo=dt.timezone.utc)


def parse_feed(xml):
    feed = ET.fromstring(xml)
    if feed.tag != ATOM + "feed":
        raise ValueError("arXiv returned a non-Atom response")
    total_text = feed.findtext(OS + "totalResults")
    entries = []
    for item in feed.findall(ATOM + "entry"):
        full_id = item.findtext(ATOM + "id", "")
        if "/api/errors" in full_id:
            raise ValueError("arXiv API error: " + clean(item.findtext(ATOM + "summary")))
        base, version = arxiv_identity(full_id)
        if not base:
            raise ValueError("arXiv entry missing a valid identifier")
        title = clean(item.findtext(ATOM + "title"))
        updated = item.findtext(ATOM + "updated", "")
        published = item.findtext(ATOM + "published", "")
        if not title or not updated or not published:
            raise ValueError(f"Incomplete arXiv entry: {base}")
        parse_date(updated)
        parse_date(published)
        entries.append({"id": base, "version": version, "title": title,
                        "authors": [clean(a.findtext(ATOM + "name")) for a in item.findall(ATOM + "author")],
                        "abstractEn": clean(item.findtext(ATOM + "summary")),
                        "published": published, "updated": updated,
                        "url": f"https://arxiv.org/abs/{base}v{version}"})
    if total_text is None:
        # Error/incomplete feeds must not advance the incremental watermark.
        raise ValueError("arXiv feed missing totalResults")
    return entries, int(total_text)


class ArxivClient:
    def __init__(self, settings):
        self.settings = settings
        self.last_request = None

    def fetch(self, parameters):
        interval = max(3.0, float(self.settings.get("minRequestIntervalSeconds", 3.1)))
        if self.last_request is not None:
            wait = interval - (time.monotonic() - self.last_request)
            if wait > 0:
                time.sleep(wait)
        url = self.settings.get("endpoint", "https://export.arxiv.org/api/query") + "?" + urlencode(parameters)
        self.last_request = time.monotonic()
        request = Request(url, headers={"User-Agent": self.settings.get("userAgent", "EmbodiedAgentAtlas/1.0"), "Accept": "application/atom+xml"})
        with urlopen(request, timeout=int(self.settings.get("timeoutSeconds", 45))) as response:
            raw = response.read(20_000_001)
        if len(raw) > 20_000_000:
            raise ValueError("Unexpectedly large arXiv response")
        return parse_feed(raw)


def discover(client, settings, cutoff):
    """Traverse lastUpdatedDate descending, so old-paper revisions are included."""
    page_size = max(1, min(1000, int(settings.get("pageSize", 100))))
    collected = []
    for page in range(max(1, int(settings.get("maxPages", 30)))):
        start = page * page_size
        records, total = client.fetch({"search_query": settings["query"], "start": start,
                                       "max_results": page_size, "sortBy": "lastUpdatedDate", "sortOrder": "descending"})
        if not records:
            if start < total:
                raise ValueError("Unexpected empty arXiv page; watermark not advanced")
            return collected
        for record in records:
            if parse_date(record["updated"]) >= cutoff:
                collected.append(record)
        # Every item below the cutoff is a safe stopping point, given server sorting.
        if any(parse_date(r["updated"]) < cutoff for r in records) or start + len(records) >= total:
            return collected
        if len(records) < page_size:
            raise ValueError("Incomplete arXiv page; watermark not advanced")
    raise ValueError("Pagination limit reached before cutoff; increase arxiv.maxPages and rerun")


def relevant(record):
    text = (record["title"] + " " + record["abstractEn"]).lower()
    body = bool(re.search(r"\b(robot\w*|embodied|manipulation|navigation)\b", text))
    agent = bool(re.search(r"\b(agent\w*|planning|reasoning|memory|recovery|replanning|tool.use|code.generation|in.context.learning|self.improvement)\b", text))
    return body and agent


def make_candidate(record, today):
    text = (record["title"] + " " + record["abstractEn"]).lower()
    categories = [key for key, terms in CATEGORY_TERMS.items() if any(term in text for term in terms)] or ["planning"]
    tasks = []
    if "navigat" in text:
        tasks.append("navigation")
    if any(x in text for x in ["manipulat", "grasp", "pick-and-place"]):
        tasks.append("manipulation")
    return {
        "id": record["id"], "arxivId": record["id"], "version": record["version"],
        "title": record["title"], "shortTitle": record["title"].split(":", 1)[0],
        "date": record["published"][:10], "year": int(record["published"][:4]),
        "authors": " and ".join(record["authors"]), "categories": categories,
        "tasks": tasks or ["general"], "environment": [],
        "summaryZh": "自动发现候选；中文解读待审核。", "abstractEn": record["abstractEn"],
        "problem": "未核实", "method": "未核实", "findings": [], "limitations": [],
        "role": {k: "未核实" for k in ["model", "output", "memory", "recovery", "adaptation"]},
        "links": {"paper": record["url"], "project": None, "code": None},
        "evidence": [{"claim": "基础元数据与英文摘要由 arXiv API 获取，尚未进行中文精读。", "source": record["url"], "label": "arXiv 元数据"}],
        "review": "candidate", "codeStatus": "unknown", "lastChecked": today,
        "tags": ["自动候选", "标签待审核"], "curated": False, "deepRead": False,
        "sourceUpdatedAt": record["updated"], "discoveredAt": today,
    }


def merge_discovery(existing, candidates, versions, events, incoming, timestamp, since=None):
    """Return new stores; never mutate input or editorial content."""
    known = {paper_key(p): p for p in existing}
    automatic_states = {"candidate", "ai-draft"}
    discovered = {paper_key(p): dict(p) for p in candidates if paper_key(p) not in {paper_key(x) for x in existing if x.get("review") not in automatic_states}}
    versions = {k: dict(v) for k, v in versions.items()}
    events = list(events)
    event_ids = {e.get("id") for e in events}
    counts = {"newCandidates": 0, "versionChanges": 0}
    latest = {}
    for record in incoming:
        key = record["id"]
        if key not in latest or record["version"] > latest[key]["version"]:
            latest[key] = record
    for key, record in latest.items():
        old = known.get(key)
        # New collection entries use original publication dates, not revision dates.
        if old is None and since and record["published"][:10] < since:
            continue
        if old is None and not relevant(record):
            continue
        previous = versions.get(key, {}).get("version", paper_version(old) if old else None)
        if previous is not None and record["version"] < previous:
            continue
        if old is None or old.get("review") in automatic_states:
            candidate = make_candidate(record, timestamp[:10])
            if key in discovered:
                candidate["discoveredAt"] = discovered[key].get("discoveredAt", timestamp[:10])
            discovered[key] = candidate
        versions[key] = {"version": record["version"], "updated": record["updated"], "url": record["url"], "checkedAt": timestamp}
        event = None
        if old is None:
            counts["newCandidates"] += 1
            event = {"id": f"discovered-{key}", "paperId": key, "type": "discovered", "date": timestamp,
                     "title": record["title"], "message": "发现新论文，已进入待审核候选。", "url": record["url"]}
        elif previous is not None and record["version"] > previous:
            counts["versionChanges"] += 1
            event = {"id": f"version-{key}-v{record['version']}", "paperId": key, "type": "version", "date": timestamp,
                     "title": record["title"], "message": f"arXiv 更新至 v{record['version']}；已有编辑解读保留，待复核新版本。", "fromVersion": previous, "toVersion": record["version"], "url": record["url"]}
        if event and event["id"] not in event_ids:
            events.insert(0, event)
            event_ids.add(event["id"])
    return sorted(discovered.values(), key=lambda p: p["date"], reverse=True), versions, events, counts


def run_update(root=ROOT, client=None, now=None):
    root = Path(root)
    config = read_json(root / "config.json", {})
    settings = config.get("arxiv", {})
    current = now or dt.datetime.now(dt.timezone.utc)
    timestamp = current.isoformat(timespec="seconds").replace("+00:00", "Z")
    status_path = root / "data/update-status.json"
    status = read_json(status_path, DEFAULT_STATUS.copy())
    try:
        previous_success = status.get("lastSuccess")
        cutoff = parse_date(previous_success) - dt.timedelta(days=max(7, int(settings.get("overlapDays", 7)))) if previous_success else current - dt.timedelta(days=int(settings.get("initialLookbackDays", 7)))
        since = settings.get("since")
        if since:
            since_date = parse_date(since)
            # Once per changed scope, backfill the entire requested period.
            if status.get("discoverySince") != since or status.get("discoveryQuery") != settings.get("query"):
                cutoff = min(cutoff, since_date)
        existing = load_papers(root)
        candidates = read_json(root / "data/candidates.json", [])
        versions = read_json(root / "data/versions.json", {})
        events = read_json(root / "data/events.json", [])
        client = client or ArxivClient(settings)
        incoming = discover(client, settings, cutoff)
        # Explicit lookup also checks old curated papers even if changed keywords leave the search query.
        ids = sorted({paper_key(p) for p in existing if arxiv_identity(paper_key(p))[0]})
        for offset in range(0, len(ids), 50):
            batch = ids[offset:offset + 50]
            records, _ = client.fetch({"id_list": ",".join(batch), "start": 0, "max_results": len(batch)})
            if {r["id"] for r in records} != set(batch):
                raise ValueError("Incomplete known-paper version lookup; previous data retained")
            incoming.extend(records)
        new_candidates, new_versions, new_events, counts = merge_discovery(existing, candidates, versions, events, incoming, timestamp, since)
        # Stage only after all network requests and parsing succeed.
        write_json(root / "data/candidates.json", new_candidates)
        write_json(root / "data/versions.json", new_versions)
        write_json(root / "data/events.json", new_events)
        write_json(status_path, {"mode": "active", "scheduleEnabled": os.environ.get("GITHUB_ACTIONS") == "true", "lastSuccess": timestamp, "lastAttempt": timestamp,
                                "message": f"最近发现 {counts['newCandidates']} 篇候选，记录 {counts['versionChanges']} 次版本变化。",
                                "fetched": len({r['id'] for r in incoming}), "discoverySince": since,
                                "discoveryQuery": settings.get("query"), **counts})
        print(f"Update succeeded: {counts['newCandidates']} candidates, {counts['versionChanges']} revisions")
        return True
    except Exception as exc:
        # No empty feed overwrite on network/API/parse failures. Preserve last-success watermark.
        status.update(mode="error", lastAttempt=timestamp, message="本次抓取失败，保留已有论文数据；等待下次重试。", error=f"{type(exc).__name__}: {exc}"[:500])
        write_json(status_path, status)
        print(f"Update failed; existing data retained: {type(exc).__name__}: {exc}", file=sys.stderr)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sys.exit(0 if run_update(parser.parse_args().root) else 1)
