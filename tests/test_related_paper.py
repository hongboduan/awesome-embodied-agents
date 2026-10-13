"""Project-linked papers remain watched without duplicate cards or seed edits."""
import copy
import datetime as dt
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build
import update


NOW = dt.datetime(2026, 10, 13, 0, 17, tzinfo=dt.timezone.utc)
STAMP = "2026-10-13T00:17:00Z"
PAPER_ID = "2607.08448"


def project(identifier="rpent", version=5):
    return {"id": identifier, "title": "RPent", "shortTitle": "RPent", "sourceType": "project",
            "date": None, "addedAt": "2026-10-13", "review": "source-checked", "curated": True,
            "summaryZh": "编辑核对的项目解读", "links": {"project": "https://github.com/RLinf/RPent"},
            "relatedPaper": {"id": PAPER_ID, "version": version,
                             "url": f"https://arxiv.org/abs/{PAPER_ID}v{version}"}}


def record(version=6):
    return {"id": PAPER_ID, "version": version, "title": "Harness VLA",
            "authors": ["A. Author"], "abstractEn": "Robot agents use memory and planning.",
            "published": "2026-07-09T13:08:54Z", "updated": "2026-10-12T10:00:00Z",
            "url": f"https://arxiv.org/abs/{PAPER_ID}v{version}"}


class RelatedPaperTests(unittest.TestCase):
    def merge(self, projects, versions=None, events=None, incoming=None):
        return update.merge_discovery(projects, [], versions or {}, events or [],
                                      incoming or [record()], STAMP, since="2026-09-01")

    def test_pre_scope_related_revision_updates_project_once_without_candidate(self):
        original = [project()]
        before = copy.deepcopy(original)
        candidates, versions, events, counts = self.merge(original)
        self.assertEqual(original, before)
        self.assertEqual(candidates, [])
        self.assertEqual(counts, {"newCandidates": 0, "versionChanges": 1})
        self.assertEqual(versions[PAPER_ID]["version"], 6)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["paperId"], "rpent")
        self.assertEqual(events[0]["relatedPaperId"], PAPER_ID)
        self.assertEqual((events[0]["fromVersion"], events[0]["toVersion"]), (5, 6))
        self.assertIn("关联论文", events[0]["title"])
        again = self.merge(original, versions, events)
        self.assertEqual(again[0], [])
        self.assertEqual(again[2], events)
        self.assertEqual(again[3], {"newCandidates": 0, "versionChanges": 0})

    def test_old_source_response_cannot_regress_reviewed_or_observed_version(self):
        candidates, versions, events, counts = self.merge([project()], incoming=[record(4)])
        self.assertEqual((candidates, versions, events), ([], {}, []))
        self.assertEqual(counts["versionChanges"], 0)
        prior = {PAPER_ID: {"version": 7, "url": f"https://arxiv.org/abs/{PAPER_ID}v7"}}
        result = self.merge([project()], versions=prior)
        self.assertEqual(result[1], prior)
        self.assertEqual(result[2], [])

    def test_unchanged_or_unversioned_link_establishes_no_false_revision(self):
        unchanged = self.merge([project()], incoming=[record(5)])
        self.assertEqual(unchanged[1][PAPER_ID]["version"], 5)
        self.assertEqual(unchanged[2], [])
        unversioned = project()
        unversioned["relatedPaper"] = {"id": PAPER_ID, "url": f"https://arxiv.org/abs/{PAPER_ID}"}
        result = self.merge([unversioned])
        self.assertEqual(result[1][PAPER_ID]["version"], 6)
        self.assertEqual(result[2], [])
        self.assertEqual(result[3]["newCandidates"], 0)

    def test_shared_paper_notifies_each_project_but_counts_one_source_revision(self):
        result = self.merge([project(), project("another-project")])
        self.assertEqual({e["paperId"] for e in result[2]}, {"rpent", "another-project"})
        self.assertEqual(len({e["id"] for e in result[2]}), 2)
        self.assertEqual(result[3], {"newCandidates": 0, "versionChanges": 1})

    def test_existing_paper_entry_keeps_normal_revision_identity(self):
        paper = {"id": PAPER_ID, "title": "Harness VLA", "version": 5,
                 "date": "2026-07-09", "review": "source-checked", "curated": True}
        result = self.merge([project(), paper])
        self.assertEqual(result[0], [])
        self.assertEqual(len(result[2]), 1)
        self.assertEqual(result[2][0]["paperId"], PAPER_ID)
        self.assertNotIn("relatedPaperId", result[2][0])

    def test_explicit_lookup_tracks_link_even_when_discovery_is_empty(self):
        class Client:
            def __init__(self):
                self.calls = []

            def fetch(self, parameters):
                self.calls.append(parameters)
                return ([record()], 1) if "id_list" in parameters else ([], 0)

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            seed = root / "data/seed-projects.json"
            build.write_json(seed, [project()])
            original = seed.read_bytes()
            build.write_json(root / "config.json", {"arxiv": {"query": "all:robot", "since": "2026-09-01"}})
            client = Client()
            self.assertTrue(update.run_update(root, client, NOW))
            self.assertEqual([c["id_list"] for c in client.calls if "id_list" in c], [PAPER_ID])
            self.assertEqual(seed.read_bytes(), original)
            self.assertEqual(build.read_json(root / "data/candidates.json", []), [])
            self.assertEqual(build.read_json(root / "data/versions.json", {})[PAPER_ID]["version"], 6)
            self.assertEqual(build.read_json(root / "data/events.json", [])[0]["paperId"], "rpent")

    def test_invalid_or_nonproject_related_ids_are_not_requested(self):
        invalid = project()
        invalid["relatedPaper"]["id"] = "not-an-arxiv-id"
        article = project("essay")
        article["sourceType"] = "article"
        self.assertEqual(update.related_paper_projects([invalid, article]), {})

    def test_loading_latest_link_metadata_preserves_project_identity_and_review(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = project()
            seed = root / "data/seed-projects.json"
            build.write_json(seed, [original])
            before = seed.read_bytes()
            latest = {"version": 6, "url": f"https://arxiv.org/abs/{PAPER_ID}v6",
                      "updated": "2026-10-12T10:00:00Z"}
            build.write_json(root / "data/versions.json", {PAPER_ID: latest})
            loaded = build.load_papers(root)
            self.assertEqual(len(loaded), 1)
            entry = loaded[0]
            self.assertEqual((entry["id"], entry["sourceType"], entry["date"], entry["review"]),
                             ("rpent", "project", None, "source-checked"))
            self.assertEqual(entry["summaryZh"], original["summaryZh"])
            self.assertEqual(entry["relatedPaper"]["version"], 5)
            self.assertEqual(entry["relatedPaper"]["latestVersion"], 6)
            self.assertEqual(entry["relatedPaper"]["latestUrl"], latest["url"])
            self.assertEqual(entry["relatedPaper"]["latestUpdatedAt"], latest["updated"])
            self.assertNotIn("latestVersion", entry)
            self.assertEqual(seed.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
