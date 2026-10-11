"""Native PDF cover selection, attribution and bounded download behavior."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from io import BytesIO

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
try:
    import pdf_assets
except ImportError:
    pdf_assets = None


@unittest.skipIf(pdf_assets is None, "PyMuPDF not installed")
class PdfAssetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def make_pdf(self, framework=True):
        doc = pdf_assets.fitz.open()
        first = doc.new_page(width=600, height=800)
        first.insert_text((50, 60), "A Robot Agent Paper", fontsize=22)
        first.insert_text((50, 110), "Abstract: our agent plans robot actions.", fontsize=11)
        if framework:
            # All-vector composite: an image-only extractor would find nothing.
            page = doc.new_page(width=600, height=800)
            page.draw_rect((50, 140, 210, 245), color=(0, 0.4, 0.2), fill=(0.9, 0.95, 0.9))
            page.draw_rect((340, 140, 530, 245), color=(0, 0.4, 0.2), fill=(0.9, 0.95, 0.9))
            page.draw_line((210, 190), (340, 190), color=(0, 0, 0), width=2)
            page.insert_text((75, 185), "Observation", fontsize=14)
            page.insert_text((365, 185), "Agent policy", fontsize=14)
            page.insert_text((50, 280), "Figure 2: Overview of the proposed framework and action pipeline.", fontsize=10)
            page.insert_text((50, 350), "This body paragraph must not appear inside the extracted figure.", fontsize=10)
        target = self.root / ".cache/papers/2610.00001-v2.pdf"
        target.parent.mkdir(parents=True)
        doc.save(target)
        doc.close()
        return target

    def test_vector_framework_is_rendered_with_provenance(self):
        self.make_pdf()
        paper = {"arxivId": "2610.00001", "latestVersion": 2, "method": "editorial"}
        before = dict(paper)
        result = pdf_assets.extract_paper(paper, self.root, {})
        self.assertEqual(paper, before)
        figure = result["figure"]
        self.assertEqual(figure["kind"], "figure")
        self.assertEqual(figure["figureLabel"], "Figure 2")
        self.assertEqual(figure["page"], 2)
        self.assertEqual(figure["sourceUrl"], "https://arxiv.org/pdf/2610.00001v2")
        self.assertLess(figure["crop"][3], 280)
        self.assertGreater(figure["width"], 800)
        self.assertTrue((self.root / "web" / figure["path"]).exists())
        pages = pdf_assets.read_text_pages(result, self.root)
        self.assertEqual([p["page"] for p in pages], [1, 2])
        self.assertIn("Abstract:", pages[0]["text"])
        with patch.object(pdf_assets, "download_pdf", side_effect=AssertionError("cache should avoid work")):
            self.assertEqual(pdf_assets.extract_paper(paper, self.root, {}), result)

    def test_captionless_pdf_is_honestly_labeled_page_preview(self):
        self.make_pdf(framework=False)
        result = pdf_assets.extract_paper({"arxivId": "2610.00001", "version": 2}, self.root, {})
        self.assertEqual(result["figure"]["kind"], "page-preview")
        self.assertIsNone(result["figure"]["figureLabel"])
        self.assertEqual(result["figure"]["selection"], "automatic-fallback")
        self.assertEqual(result["figure"]["page"], 1)

    def test_requires_version_and_rejects_conflicting_source_ids(self):
        with self.assertRaisesRegex(ValueError, "explicit arXiv version"):
            pdf_assets.extract_paper({"arxivId": "2610.00001"}, self.root, {})
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            pdf_assets.extract_paper({"arxivId": "2610.00001", "links": {"paper": "https://arxiv.org/abs/2610.00002v1"}}, self.root, {})

    def test_download_rejects_arbitrary_hosts_and_oversized_cache(self):
        for url in ["http://arxiv.org/pdf/2610.00001v1", "https://arxiv.org.evil.test/a", "https://user:pass@arxiv.org/a", "https://localhost/a"]:
            with self.assertRaises(ValueError):
                pdf_assets.download_pdf(url, self.root / "download.pdf", {})
        cached = self.root / "large.pdf"
        cached.write_bytes(b"%PDF-" + b"a" * 2000)
        with self.assertRaisesRegex(ValueError, "size limit"):
            pdf_assets.download_pdf("https://arxiv.org/pdf/2610.00001v1", cached, {"maxDownloadBytes": 1024})

    def test_redirects_and_streamed_download_limits_are_enforced(self):
        with self.assertRaises(ValueError):
            pdf_assets._ArxivRedirects().redirect_request(None, None, 302, "Found", {}, "https://example.com/file.pdf")
        class Response(BytesIO):
            headers = {}
            def geturl(self): return "https://arxiv.org/pdf/2610.00001v1"
        class Opener:
            def open(self, *args, **kwargs): return Response(b"%PDF-" + b"x" * 2000)
        target = self.root / "bounded.pdf"
        with patch.object(pdf_assets, "build_opener", return_value=Opener()), patch.object(pdf_assets, "_last_request", None):
            with self.assertRaisesRegex(ValueError, "size limit"):
                pdf_assets.download_pdf("https://arxiv.org/pdf/2610.00001v1", target, {"maxDownloadBytes": 1024})
        self.assertFalse(target.exists())

    def test_caption_without_nearby_graphics_is_not_called_a_figure(self):
        doc = pdf_assets.fitz.open()
        page = doc.new_page()
        page.insert_text((50, 400), "Figure 1: Architecture of our agent.")
        _, _, figure = pdf_assets.select_cover(doc)
        self.assertEqual(figure["kind"], "page-preview")
        doc.close()

    def test_source_checked_hint_wins_and_body_references_are_not_captions(self):
        doc = pdf_assets.fitz.open()
        page = doc.new_page(width=600, height=800)
        page.draw_rect((50, 100, 520, 210), fill=(0.8, 0.9, 0.8))
        page.insert_text((50, 240), "Figure 1: Overview of the framework.", fontsize=12)
        page.draw_rect((50, 400, 520, 510), fill=(0.8, 0.9, 0.8))
        page.insert_text((50, 540), "Figure 2 A shared interaction grammar.", fontsize=12)
        page.insert_text((50, 600), "Figure 3 describes our experimental results.", fontsize=12)
        self.assertEqual(len(pdf_assets.find_captions(page)), 2)
        _, _, chosen = pdf_assets.select_cover(doc, {}, {"figureLabel": "Figure 2", "page": 1})
        self.assertEqual(chosen["figureLabel"], "Figure 2")
        self.assertEqual(chosen["selection"], "source-hint")
        doc.close()

    def test_text_limit_is_visible_in_metadata(self):
        self.make_pdf()
        result = pdf_assets.extract_paper({"arxivId": "2610.00001", "version": 2}, self.root, {"pdf": {"maxTextPages": 1}})
        self.assertTrue(result["pdf"]["textTruncated"])
        self.assertEqual(result["pdf"]["pageCount"], 2)
        self.assertEqual(result["pdf"]["textPages"], 1)

    def test_centered_caption_does_not_clip_wider_figure(self):
        doc = pdf_assets.fitz.open()
        page = doc.new_page(width=600, height=800)
        page.draw_rect((45, 100, 555, 250), fill=(0.8, 0.9, 0.8))
        page.insert_text((100, 280), "Figure 1 Overview of our agent-native framework and benchmark.", fontsize=10)
        _, rectangle, figure = pdf_assets.select_cover(doc)
        self.assertEqual(figure["kind"], "figure")
        self.assertLess(rectangle.x0, 45)
        self.assertGreater(rectangle.x1, 555)
        doc.close()


if __name__ == "__main__":
    unittest.main()
