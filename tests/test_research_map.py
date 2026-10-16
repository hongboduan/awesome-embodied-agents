"""Keep editorial comparisons separate from evidenced relationships at publication."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build


class ResearchMapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.papers = [{"id": "paper-a", "curated": True},
                       {"id": "paper-b", "curated": True},
                       {"id": "candidate", "curated": False}]
        source = {"label": "Original project", "url": "https://example.org/source"}
        self.data = {
            "version": 1, "updatedAt": "2026-10-16",
            "routes": [{"id": "code-policy", "title": "Code", "question": "When?",
                        "summary": "Read the designs", "readingQuestion": "How?",
                        "paperIds": ["paper-a"], "backgroundIds": ["paper-b"],
                        "frontierIds": ["candidate"]}],
            "resources": [{"id": "resource-model", "kind": "model", "name": "Model",
                           "url": "https://example.org/model"}],
            "relations": [{"id": "a-uses-model", "source": "paper-a", "target": "resource-model",
                           "type": "uses_model", "editorial": False, "label": "Uses model",
                           "explanation": "The project documents this backend.",
                           "sources": [source], "checkedAt": "2026-10-16"}],
            "teams": [{"id": "team", "name": "Team", "summary": "Research line",
                       "workIds": ["paper-a"], "sources": [source], "checkedAt": "2026-10-16"}],
        }

    def load(self):
        build.write_json(self.root / "data/research-map.json", self.data)
        return build.load_research_map(self.root, self.papers)

    def test_valid_route_preserves_candidate_as_separate_frontier(self):
        result = self.load()
        self.assertEqual(result, self.data)
        self.assertFalse(self.papers[-1]["curated"])

    def test_missing_map_is_backward_compatible(self):
        self.assertEqual(build.load_research_map(self.root, self.papers)["relations"], [])

    def test_unknown_endpoints_and_self_edges_cannot_publish(self):
        for target in ["missing-paper", "paper-a"]:
            with self.subTest(target=target):
                self.data["relations"][0]["target"] = target
                with self.assertRaisesRegex(ValueError, "endpoints"):
                    self.load()

    def test_relation_requires_evidence_and_verified_date(self):
        original = copy.deepcopy(self.data["relations"][0])
        for change in [{"sources": []}, {"sources": [{"label": "Bad", "url": "javascript:alert(1)"}]},
                       {"checkedAt": "not-a-date"}]:
            self.data["relations"][0] = original | change
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.load()

    def test_comparison_cannot_be_presented_as_factual_inheritance(self):
        for kind, editorial in [("comparison", False), ("extends", True), ("uses_model", "false")]:
            self.data["relations"][0].update(type=kind, editorial=editorial)
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "editorial"):
                self.load()

    def test_reverse_comparisons_are_deduplicated(self):
        relation = self.data["relations"][0]
        relation.update(type="comparison", editorial=True, target="paper-b")
        self.data["relations"].append(relation | {"id": "reverse", "source": "paper-b", "target": "paper-a"})
        with self.assertRaisesRegex(ValueError, "duplicate relationship"):
            self.load()

    def test_candidates_cannot_silently_enter_curated_route_or_team(self):
        self.data["routes"][0]["paperIds"] = ["candidate"]
        with self.assertRaisesRegex(ValueError, "unreviewed"):
            self.load()
        self.data["routes"][0]["paperIds"] = ["paper-a"]
        self.data["teams"][0]["workIds"] = ["candidate"]
        with self.assertRaisesRegex(ValueError, "unreviewed"):
            self.load()

    def test_build_includes_map_and_enrichment_status_without_rewriting_sources(self):
        self.load()
        build.write_json(self.root / "data/seed-fixture.json", [p | {"title": p["id"]} for p in self.papers[:2]])
        build.write_json(self.root / "data/candidates.json", [{"id": "candidate", "title": "Candidate"}])
        build.write_json(self.root / "data/enrichment-status.json", {"llmMode": "not-configured"})
        original = (self.root / "data/research-map.json").read_bytes()
        result = build.build(self.root)
        self.assertEqual(result["researchMap"], self.data)
        self.assertEqual(result["enrichmentStatus"]["llmMode"], "not-configured")
        self.assertEqual((self.root / "data/research-map.json").read_bytes(), original)
        self.assertEqual(json.loads((self.root / "dist/data.json").read_text())["researchMap"], self.data)


if __name__ == "__main__":
    unittest.main()
