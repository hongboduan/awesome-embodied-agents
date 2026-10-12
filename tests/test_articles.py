"""Keep non-paper perspectives distinct in citations, feeds, and PDF discovery."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build
import enrich


class ArticleTests(unittest.TestCase):
    def test_article_citation_feed_and_pdf_exclusion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            article = {
                "id": "robot-use-agents-isola", "sourceType": "article",
                "title": "Robot-Use Agents", "authors": "Phillip Isola",
                "date": "2026-09-07", "year": 2026, "addedAt": "2026-10-12",
                "review": "source-checked", "curated": True,
                "links": {"article": "https://web.mit.edu/phillipi/www/writing/robot-use-agents.html"},
            }
            build.write_json(root / "data/seed-articles.json", [article])
            papers = build.load_papers(root)
            self.assertEqual(build.entry_date(papers[0]), "2026-09-07")
            citation = build.bibtex(papers)
            self.assertIn(article["links"]["article"], citation)
            self.assertIn("year = {2026}", citation)
            self.assertIn("Web essay / Perspective", citation)
            self.assertNotIn("eprint", citation)
            feed = build.make_rss(papers, [], {}, "2026-10-12T00:00:00Z").decode()
            self.assertIn("<link>" + article["links"]["article"] + "</link>", feed)
            self.assertIn("07 Sep 2026", feed)

            def no_pdf(*args):
                self.fail("An opinion essay must not enter PDF extraction")

            result = enrich.run_enrichment(root, environ={}, extractor=no_pdf, text_reader=no_pdf)
            self.assertEqual(result["eligible"], 0)
            self.assertEqual(result["pdfExtracted"], 0)


if __name__ == "__main__":
    unittest.main()
