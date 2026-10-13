"""Reading-list navigation and source labels survive the daily rebuild."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build


class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "README.md"
        self.path.write_text("Intro\n<!-- ATLAS:START -->\n<!-- ATLAS:END -->\nFooter\n")
        build.write_json(self.root / "config.json", {"siteUrl": "https://example.org/collection/"})

    def paper(self, **changes):
        result = {"id": "2610.10409", "title": "A robot benchmark", "date": "2026-10-07",
                  "curated": True, "review": "source-checked", "categories": ["evaluation", "spatial"],
                  "summaryZh": "基准和评测协议", "links": {"paper": "https://arxiv.org/abs/2610.10409v1",
                  "code": "https://github.com/robotworldai/robotworld", "project": "https://robotworldai.github.io/"}}
        result.update(changes)
        return result

    def test_primary_topic_lists_each_paper_once_and_old_work_is_collapsed(self):
        old = self.paper(id="old-paper", title="An earlier paper", date="2024-01-01")
        candidate = self.paper(id="candidate", title="Unreviewed candidate", review="candidate", curated=False)
        build.update_readme(self.path, [old, candidate, self.paper()], english=True)
        text = self.path.read_text()
        self.assertEqual(text.count("**[A robot benchmark]"), 1)
        self.assertIn("[Benchmarks & Evaluation · 1](#recent-evaluation)", text)
        self.assertIn('<a id="recent-evaluation"></a>', text)
        self.assertIn("Benchmarks & Evaluation · Spatial Understanding", text)
        self.assertGreater(text.index("**[An earlier paper]"), text.index("<details>"))
        self.assertNotIn("Unreviewed candidate", text)
        self.assertIn("1 discovery candidates", text)
        build.update_readme(self.path, [old, candidate, self.paper()], english=True)
        self.assertEqual(text, self.path.read_text())

    def test_article_has_its_own_section_and_no_invented_paper_or_code_links(self):
        article = self.paper(id="isola-essay", title="Robot-Use Agents", sourceType="article",
                             authors="Phillip Isola", date="2026-09-07", categories=["planning"],
                             links={"article": "https://web.mit.edu/phillipi/www/writing/robot-use-agents.html"})
        build.update_readme(self.path, [article, self.paper()], english=True)
        text = self.path.read_text()
        self.assertIn("2 curated entries · 1 paper · 0 projects · 1 perspective", text)
        section = text.split("## Perspectives and essays", 1)[1]
        self.assertIn("Phillip Isola · Perspective / essay", section)
        self.assertIn("[![Read the original article]", section)
        self.assertNotIn("logo=arxiv", section)
        self.assertNotIn("logo=github", section)
        self.assertNotIn("]()", text)

    def test_selected_earlier_papers_remain_visible_with_original_dates(self):
        featured = self.paper(id="enpire", title="ENPIRE", date="2026-06-18", featuredBackground=True)
        featured_later = self.paper(id="emerge", title="EMERGE", date="2026-08-30", featuredBackground=True)
        old = self.paper(id="old-paper", title="Background paper", date="2024-01-01")
        recent = self.paper(featuredBackground=True)
        candidate = self.paper(id="candidate", title="Unreviewed candidate", date="2026-08-01",
                               featuredBackground=True, review="candidate", curated=False)
        project = self.paper(id="project", title="Project preview", sourceType="project", date="2026-08-01",
                             featuredBackground=True, links={"project": "https://example.org/project/"})
        for english in (True, False):
            with self.subTest(english=english):
                build.update_readme(self.path, [featured, old, candidate, recent, featured_later, project], english=english)
                text = self.path.read_text()
                label = "Selected earlier foundations" if english else "重点补充 · 早期首发"
                self.assertIn(f"[{label}](#selected-earlier)", text)
                self.assertIn('<a id="selected-earlier"></a>', text)
                selected = text.split("## " + label, 1)[1].split('<a id="projects">', 1)[0]
                for title, date in (("ENPIRE", "2026-06-18"), ("EMERGE", "2026-08-30")):
                    self.assertIn(f"**[{title}]", selected)
                    self.assertIn(date, selected)
                    self.assertEqual(text.count(f"**[{title}]"), 1)
                    self.assertLess(text.index(f"**[{title}]"), text.index("<details>"))
                self.assertLess(selected.index("**[EMERGE]"), selected.index("**[ENPIRE]"))
                self.assertLess(text.index("**[A robot benchmark]"), text.index("## " + label))
                self.assertNotIn("Project preview", selected)
                self.assertNotIn("Unreviewed candidate", text)
                self.assertGreater(text.index("**[Background paper]"), text.index("<details>"))

    def test_badges_link_to_supplied_sources_and_reading_card(self):
        build.update_readme(self.path, [self.paper()], english=False)
        text = self.path.read_text()
        self.assertIn("[![arXiv: 2610.10409]", text)
        self.assertIn("logo=arxiv&logoColor=white", text)
        self.assertIn("[![GitHub source code]", text)
        self.assertIn("logo=github&logoColor=white", text)
        self.assertIn("](https://arxiv.org/abs/2610.10409v1)", text)
        self.assertIn("](https://example.org/collection/#paper=2610.10409)", text)
        self.assertNotIn("github/stars", text)
        invalid = self.paper(links={"paper": "javascript:alert(1)", "code": "http://example.org/code"}, categories=[])
        build.update_readme(self.path, [invalid])
        text = self.path.read_text()
        self.assertIn("其他 Agent 研究", text)
        self.assertIn("**A robot benchmark**", text)
        self.assertNotIn("javascript:", text)
        self.assertNotIn("logo=github", text)


if __name__ == "__main__":
    unittest.main()
