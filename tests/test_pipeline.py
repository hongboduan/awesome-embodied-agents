"""Behavioral tests: source identity, review preservation, and safe failed updates."""
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import build
import update

NOW = dt.datetime(2026, 10, 11, 0, 17, tzinfo=dt.timezone.utc)


def paper(version=1, curated=True):
    return {"id": "sample-agent", "title": "Robot Agent with Memory", "shortTitle": "Sample",
            "date": "2026-10-01", "year": 2026, "authors": "A. Author and B. Author",
            "categories": ["memory"], "summaryZh": "人工精读：经过检查的解释", "method": "编辑写作不能被覆盖",
            "review": "full-review" if curated else "candidate", "curated": curated, "deepRead": curated,
            "version": version, "links": {"paper": f"https://arxiv.org/abs/2610.00001v{version}"}}


def source(version=2, identifier="2610.00001"):
    return {"id": identifier, "version": version, "title": "Robot Agent with Memory revised",
            "authors": ["A. Author", "B. Author"], "abstractEn": "We introduce an embodied robot agent with planning and memory.",
            "published": "2026-10-01T00:00:00Z", "updated": "2026-10-10T10:00:00Z",
            "url": f"https://arxiv.org/abs/{identifier}v{version}"}


class FakeClient:
    def __init__(self, pages):
        self.pages = iter(pages)
        self.calls = []

    def fetch(self, params):
        self.calls.append(params)
        result = next(self.pages)
        if isinstance(result, Exception):
            raise result
        return result


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "data").mkdir()
        (self.root / "web").mkdir()
        build.write_json(self.root / "config.json", {"arxiv": {"query": "all:robot", "pageSize": 2, "maxPages": 3}})
        self.addCleanup(self.temp.cleanup)

    def put(self, name, value):
        build.write_json(self.root / "data" / name, value)

    def test_base_id_dedup_and_editorial_precedence(self):
        self.put("seed-a.json", [paper()])
        automatic = update.make_candidate(source(), "2026-10-11")
        automatic["curated"] = True  # Erroneous auto data must never promote itself.
        self.put("candidates.json", [automatic, update.make_candidate(source(1), "2026-10-10")])
        result = build.load_papers(self.root)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["summaryZh"], paper()["summaryZh"])
        self.assertEqual(result[0]["review"], "full-review")
        self.assertEqual(build.arxiv_identity("https://arxiv.org/pdf/2610.00001v3.pdf"), ("2610.00001", 3))

    def test_candidate_never_auto_curated(self):
        p = update.make_candidate(source(), "2026-10-11")
        p.update(curated=True, deepRead=True, review="full-review")
        self.put("candidates.json", [p])
        loaded = build.load_papers(self.root)[0]
        self.assertFalse(loaded["curated"])
        self.assertFalse(loaded["deepRead"])
        self.assertEqual(loaded["review"], "candidate")
        self.assertNotEqual(loaded["summaryZh"], loaded["abstractEn"])

    def test_project_without_publication_date_builds_without_fabricated_citation(self):
        project = {"id": "loopros", "title": "LoopROS", "sourceType": "project", "date": None,
                   "year": None, "addedAt": "2026-10-12", "review": "source-checked", "curated": True,
                   "links": {"paper": None, "project": "https://loopmaster.ai/loopros/", "code": None}}
        self.put("seed-projects.json", [project])
        self.put("seed-papers.json", [paper()])
        self.assertEqual(build.load_papers(self.root)[0]["id"], "loopros")
        citation = build.bibtex([project])
        self.assertIn("https://loopmaster.ai/loopros/", citation)
        self.assertNotIn("year =", citation)
        self.assertNotIn("eprint =", citation)
        readme = self.root / "README.md"
        readme.write_text("<!-- ATLAS:START -->\n<!-- ATLAS:END -->")
        result = build.build(self.root)
        self.assertIsNone(result["papers"][0]["date"])
        text = readme.read_text()
        self.assertIn("Projects and systems", text)
        self.assertIn("added 2026-10-12", text)
        self.assertNotIn("]()", text)
        rss = (self.root / "dist/feed.xml").read_text()
        self.assertIn("<link>https://loopmaster.ai/loopros/</link>", rss)

    def test_unversioned_seed_establishes_baseline_without_false_revision(self):
        editorial = paper()
        editorial.pop("version")
        editorial["links"]["paper"] = "https://arxiv.org/abs/2610.00001"
        self.assertIsNone(build.paper_version(editorial))
        self.assertEqual(build.paper_version({"id": "coap", "links": {"paper": "https://arxiv.org/pdf/2610.12369v1"}}), 1)
        self.put("seed-a.json", [editorial])
        with patch.dict(update.os.environ, {"GITHUB_ACTIONS": "false"}):
            self.assertTrue(update.run_update(self.root, FakeClient([([source(2)], 1), ([source(2)], 1)]), NOW))
        self.assertEqual(build.read_json(self.root / "data/events.json", []), [])
        status = build.read_json(self.root / "data/update-status.json", {})
        self.assertEqual(status["versionChanges"], 0)
        self.assertFalse(status["scheduleEnabled"])
        loaded = build.load_papers(self.root)[0]
        self.assertIsNone(loaded["reviewedVersion"])
        self.assertEqual(loaded["latestVersion"], 2)
        with patch.dict(update.os.environ, {"GITHUB_ACTIONS": "true"}):
            self.assertTrue(update.run_update(self.root, FakeClient([([source(3)], 1), ([source(3)], 1)]), NOW))
        events = build.read_json(self.root / "data/events.json", [])
        self.assertEqual(len(events), 1)
        self.assertEqual((events[0]["fromVersion"], events[0]["toVersion"]), (2, 3))
        self.assertTrue(build.read_json(self.root / "data/update-status.json", {})["scheduleEnabled"])

    def test_revision_does_not_rewrite_seed_and_event_is_idempotent(self):
        original = paper()
        self.put("seed-a.json", [original])
        initial_bytes = (self.root / "data/seed-a.json").read_bytes()
        client = FakeClient([([source()], 1), ([source()], 1)])
        self.assertTrue(update.run_update(self.root, client, NOW))
        self.assertEqual((self.root / "data/seed-a.json").read_bytes(), initial_bytes)
        loaded = build.load_papers(self.root)[0]
        self.assertEqual(loaded["method"], original["method"])
        self.assertEqual(loaded["reviewedVersion"], 1)
        self.assertEqual(loaded["latestVersion"], 2)
        self.assertEqual(len(build.read_json(self.root / "data/events.json", [])), 1)
        again = FakeClient([([source()], 1), ([source()], 1)])
        self.assertTrue(update.run_update(self.root, again, NOW))
        self.assertEqual(len(build.read_json(self.root / "data/events.json", [])), 1)

    def test_partial_fetch_failure_preserves_all_content_and_watermark(self):
        self.put("seed-a.json", [paper()])
        self.put("candidates.json", [update.make_candidate(source(1, "2610.00002"), "2026-10-10")])
        self.put("versions.json", {"2610.00001": {"version": 1}})
        self.put("events.json", [{"id": "old"}])
        self.put("update-status.json", {"mode": "active", "lastSuccess": "2026-10-10T00:17:00Z"})
        protected = ["seed-a.json", "candidates.json", "versions.json", "events.json"]
        before = {name: (self.root / "data" / name).read_bytes() for name in protected}
        client = FakeClient([([source(2), source(1, "2610.00003")], 4), TimeoutError("network timeout")])
        self.assertFalse(update.run_update(self.root, client, NOW))
        self.assertEqual(before, {name: (self.root / "data" / name).read_bytes() for name in protected})
        status = build.read_json(self.root / "data/update-status.json", {})
        self.assertEqual(status["lastSuccess"], "2026-10-10T00:17:00Z")
        self.assertEqual(status["mode"], "error")
        self.assertIn("lastAttempt", status)

    def test_pagination_and_boundary_keep_old_revisions(self):
        first = [source(2), source(1, "2610.00002")]
        second = [source(1, "2610.00003")]
        second[0]["updated"] = "2026-09-01T00:00:00Z"
        client = FakeClient([(first, 8), (second, 8)])
        result = update.discover(client, {"query": "all:robot", "pageSize": 2, "maxPages": 3}, NOW - dt.timedelta(days=7))
        self.assertEqual(len(result), 2)
        self.assertEqual([p["start"] for p in client.calls], [0, 2])
        self.assertTrue(all(p["sortBy"] == "lastUpdatedDate" for p in client.calls))

    def test_page_limit_and_truncated_feed_fail_instead_of_skipping(self):
        client = FakeClient([([source()], 100)])
        with self.assertRaisesRegex(ValueError, "Pagination limit"):
            update.discover(client, {"query": "all:robot", "pageSize": 1, "maxPages": 1}, NOW - dt.timedelta(days=7))
        with self.assertRaisesRegex(ValueError, "totalResults"):
            update.parse_feed('<feed xmlns="http://www.w3.org/2005/Atom"></feed>')

    def test_serial_rate_limit_cannot_be_configured_below_three_seconds(self):
        payload = b'<feed xmlns="http://www.w3.org/2005/Atom" xmlns:os="http://a9.com/-/spec/opensearch/1.1/"><os:totalResults>0</os:totalResults></feed>'
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return payload
        client = update.ArxivClient({"minRequestIntervalSeconds": 0})
        with patch.object(update, "urlopen", return_value=Response()), patch.object(update.time, "monotonic", side_effect=[100.0, 101.0, 103.0]), patch.object(update.time, "sleep") as sleep:
            client.fetch({"id_list": "2610.00001"})
            client.fetch({"id_list": "2610.00002"})
            sleep.assert_called_once_with(2.0)

    def test_build_preserves_readme_prose_and_safe_data_script(self):
        p = paper()
        p["title"] = "Robot </script><script>alert(1)</script>"
        self.put("seed-a.json", [p])
        readme = "Custom intro\n<!-- ATLAS:START -->\nstale\n<!-- ATLAS:END -->\nCustom footer\n"
        (self.root / "README.md").write_text(readme)
        (self.root / "web/index.html").write_text('<script src="./data.js"></script>')
        built = build.build(self.root)
        self.assertEqual(built["updateStatus"]["mode"], "setup-required")
        updated = (self.root / "README.md").read_text()
        self.assertTrue(updated.startswith("Custom intro\n"))
        self.assertTrue(updated.endswith("\nCustom footer\n"))
        self.assertNotIn("</script>", (self.root / "dist/data.js").read_text())
        for file in ["data.json", "papers.json", "papers.bib", "feed.xml", "index.html"]:
            self.assertTrue((self.root / "dist" / file).exists())

    def test_source_checked_not_counted_as_automatic_candidate(self):
        checked = paper(curated=False)
        checked["review"] = "source-checked"
        self.put("seed-a.json", [checked])
        (self.root / "README.md").write_text("<!-- ATLAS:START -->\n<!-- ATLAS:END -->")
        build.build(self.root)
        content = (self.root / "README.md").read_text()
        self.assertIn("1 source-checked", content)
        self.assertIn("0 discovery candidates", content)

    def test_public_build_does_not_ship_source_archive(self):
        stale = self.root / "dist/downloads/awesome-embodied-agents.zip"
        stale.parent.mkdir(parents=True)
        stale.write_bytes(b"old source archive")
        build.build(self.root)
        self.assertFalse(stale.exists())

    def test_new_old_paper_revision_does_not_enter_recent_discovery(self):
        old = source()
        old["published"] = "2024-01-01T00:00:00Z"
        candidate, versions, events, counts = update.merge_discovery([], [], {}, [], [old], "2026-10-11T00:00:00Z", since="2026-09-01")
        self.assertEqual(candidate, [])
        self.assertEqual(counts["newCandidates"], 0)
        # Existing background papers still get revision tracking.
        candidate, versions, events, counts = update.merge_discovery([paper()], [], {}, [], [old], "2026-10-11T00:00:00Z", since="2026-09-01")
        self.assertEqual(counts["versionChanges"], 1)

    def test_enrichment_draft_does_not_overwrite_editorial(self):
        self.put("seed-a.json", [paper()])
        ai = {"status": "ready", "version": 1, "summaryZh": "模型草稿", "social": {"wechat": {"title": "草稿"}}}
        self.put("enrichments.json", {"2610.00001": {"version": 1, "ai": ai}})
        loaded = build.load_papers(self.root)[0]
        self.assertEqual(loaded["summaryZh"], paper()["summaryZh"])
        self.assertEqual(loaded["review"], "full-review")
        self.assertEqual(loaded["social"]["wechat"]["title"], "草稿")

    def test_discovery_preserves_candidate_that_has_an_ai_draft(self):
        candidate = update.make_candidate(source(1), "2026-10-11")
        display_record = dict(candidate, review="ai-draft")
        result, versions, events, counts = update.merge_discovery([display_record], [candidate], {}, [], [source(2)], "2026-10-11T00:00:00Z")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["version"], 2)
        self.assertEqual(result[0]["review"], "candidate")

    def test_current_ai_draft_is_visible_but_never_curated(self):
        self.put("candidates.json", [update.make_candidate(source(1), "2026-10-11")])
        self.put("enrichments.json", {"2610.00001": {"version": 1, "ai": {"status": "ready", "version": 1, "summaryZh": "模型草稿"}}})
        loaded = build.load_papers(self.root)[0]
        self.assertEqual(loaded["review"], "ai-draft")
        self.assertFalse(loaded["curated"])
        self.assertFalse(loaded["deepRead"])
        self.put("versions.json", {"2610.00001": {"version": 2}})
        self.assertEqual(build.load_papers(self.root)[0]["review"], "candidate")


if __name__ == "__main__":
    unittest.main()
