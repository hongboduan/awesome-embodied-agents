"""Budget, provenance and failure tests. These tests never call a model or arXiv."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from enrich import EnrichmentError, run_enrichment, select_text_pages, validate_analysis


PAGES = [{"page": 1, "text": "The robot plans actions. The method uses explicit memory. " * 20},
         {"page": 2, "text": "Results: success reaches 70.24% on 42 simulated tasks. Only simulation is evaluated. " * 15}]


def draft():
    return {
        "summaryZh": "用显式记忆规划机器人动作，在仿真任务上验证。",
        "problem": {"text": "机器人需要规划动作。", "evidence": [{"page": 1, "quote": "The robot plans actions."}]},
        "method": {"text": "方法使用显式记忆。", "evidence": [{"page": 1, "quote": "The method uses explicit memory."}]},
        "findings": [{"text": "42项仿真任务上成功率为70.24%。", "evidence": [{"page": 2, "quote": "success reaches 70.24% on 42 simulated tasks."}]}],
        "limitations": [{"text": "仅验证了仿真环境。", "evidence": [{"page": 2, "quote": "Only simulation is evaluated."}]}],
        "role": {key: "文中未说明" for key in ["model", "output", "memory", "recovery", "adaptation"]},
        "social": {"xiaohongshu": {"title": "机器人如何记住任务状态", "body": "这项工作通过显式记忆规划动作，结果来自仿真环境。", "tags": ["具身智能"]},
                   "wechat": {"title": "用显式记忆组织机器人规划", "body": "论文展示了显式记忆在机器人规划中的用途，验证范围为仿真任务。"}}
    }


class EvidenceTests(unittest.TestCase):
    def test_valid_claims_keep_page_and_quote_and_draft_label(self):
        value = validate_analysis(draft(), PAGES, "https://arxiv.org/pdf/2610.12345v1")
        self.assertEqual(value["review"], "ai-draft")
        self.assertFalse(value["curated"])
        self.assertFalse(value["deepRead"])
        self.assertIn("#page=2", value["evidence"][2]["source"])
        self.assertIn("AI 辅助草稿", value["social"]["wechat"]["body"])

    def test_made_up_quote_rejected(self):
        value = draft()
        value["findings"][0]["evidence"][0]["quote"] = "We achieve perfect results in the real world."
        with self.assertRaisesRegex(EnrichmentError, "quote-not-in-source"):
            validate_analysis(value, PAGES, "https://arxiv.org/pdf/2610.12345v1")

    def test_false_numeric_value_rejected_even_next_to_chinese(self):
        value = draft()
        value["findings"][0]["text"] = "在42项仿真任务上取得99.99%成功率。"
        with self.assertRaisesRegex(EnrichmentError, "unsupported-numerical"):
            validate_analysis(value, PAGES, "https://arxiv.org/pdf/2610.12345v1")

    def test_missing_evidence_and_fake_page_rejected(self):
        for evidence in [[], [{"page": 9, "quote": "Only simulation is evaluated."}]]:
            value = draft()
            value["limitations"][0]["evidence"] = evidence
            with self.assertRaises(EnrichmentError):
                validate_analysis(value, PAGES, "https://arxiv.org/pdf/2610.12345v1")

    def test_schema_and_social_number_checked(self):
        value = draft()
        value["social"]["wechat"]["body"] += "性能提升100%。"
        with self.assertRaisesRegex(EnrichmentError, "unsupported-social"):
            validate_analysis(value, PAGES, "https://arxiv.org/pdf/2610.12345v1")
        value = draft()
        value["code"] = "https://example.com/invented"
        with self.assertRaisesRegex(EnrichmentError, "invalid-schema"):
            validate_analysis(value, PAGES, "https://arxiv.org/pdf/2610.12345v1")

    def test_input_is_bounded_and_records_original_page_numbers(self):
        selected = select_text_pages(PAGES, 1700)
        self.assertLessEqual(sum(len(p["text"]) for p in selected), 1700)
        self.assertEqual(selected[0]["page"], 1)


class OrchestrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "data").mkdir()
        self.config = {"enrichment": {"enabled": True, "since": "2026-09-01", "maxPapersPerRun": 12,
                                      "llm": {"enabled": True, "maxPapersPerRun": 3, "maxInputChars": 45000}}}
        self.papers = [{"id": "2610.12345", "arxivId": "2610.12345", "version": 1,
                        "title": "Robot Agent with Memory", "date": "2026-10-08",
                        "links": {"paper": "https://arxiv.org/abs/2610.12345v1"}}]
        self.pdf_calls = []
        self.model_calls = []
        self.write("config.json", self.config)
        self.write("data/candidates.json", self.papers)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, data):
        (self.root / name).write_text(json.dumps(data), encoding="utf-8")

    def extract(self, paper, root, config):
        self.pdf_calls.append(paper["id"])
        path = f"assets/papers/{paper['id']}-v{paper['version']}.png"
        full = root / "web" / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(b"fake-cover")
        return {"pdf": {"status": "extracted", "version": paper["version"], "sourceUrl": f"https://arxiv.org/pdf/{paper['id']}v{paper['version']}"},
                "figure": {"path": path, "page": 2, "version": paper["version"]}}

    def model(self, paper, pages, config, env):
        self.model_calls.append(paper["id"])
        return draft(), {"total_tokens": 100}

    def run_pipeline(self, **kwargs):
        return run_enrichment(self.root, extractor=kwargs.pop("extractor", self.extract),
                              text_reader=lambda record, root: copy.deepcopy(PAGES),
                              llm_call=kwargs.pop("llm_call", self.model),
                              environ=kwargs.pop("environ", {"LLM_API_KEY": "test-not-real", "LLM_MODEL": "test-model"}), **kwargs)

    def test_no_key_still_extracts_pdf_and_never_calls_model(self):
        result = self.run_pipeline(environ={})
        self.assertEqual(result["pdfExtracted"], 1)
        self.assertEqual(result["llmMode"], "not-configured")
        self.assertEqual(self.model_calls, [])

    def test_selected_earlier_paper_gets_cover_without_widening_discovery_scope(self):
        selected = dict(self.papers[0], id="2606.19980", arxivId="2606.19980", date="2026-06-18",
                        links={"paper": "https://arxiv.org/abs/2606.19980v1"},
                        curated=True, review="source-checked", featuredBackground=True)
        ordinary = dict(selected, id="2606.10001", arxivId="2606.10001",
                        links={"paper": "https://arxiv.org/abs/2606.10001v1"}, featuredBackground=False)
        self.write("data/candidates.json", [])
        self.write("data/seed-selected.json", [selected, ordinary])
        result = self.run_pipeline(environ={})
        self.assertEqual(result["eligible"], 1)
        self.assertEqual(self.pdf_calls, ["2606.19980"])
        self.assertEqual(self.model_calls, [])
        result = self.run_pipeline(environ={})
        self.assertEqual(len(self.pdf_calls), 1)

    def test_project_previews_are_not_sent_to_pdf_or_model_pipeline(self):
        self.write("data/seed-projects.json", [{"id": "loopros", "title": "LoopROS",
                   "sourceType": "project", "date": None, "addedAt": "2026-10-12",
                   "curated": True, "links": {"paper": None, "project": "https://loopmaster.ai/loopros/"}}])
        result = self.run_pipeline()
        self.assertEqual(result["eligible"], 1)
        self.assertEqual(self.pdf_calls, ["2610.12345"])
        self.assertEqual(self.model_calls, ["2610.12345"])

    def test_successful_request_is_cached_and_new_version_is_reanalyzed(self):
        self.run_pipeline()
        self.run_pipeline()
        self.assertEqual(len(self.model_calls), 1)
        self.papers[0]["version"] = 2
        self.write("data/candidates.json", self.papers)
        self.run_pipeline()
        self.assertEqual(len(self.model_calls), 2)
        records = json.loads((self.root / "data/enrichments.json").read_text())
        self.assertEqual(records["2610.12345"]["ai"]["version"], 2)

    def test_failed_model_is_not_automatically_rebilled_and_secrets_not_saved(self):
        def fail(*args):
            self.model_calls.append("failed")
            raise RuntimeError("a secret token must never reach public JSON")
        result = self.run_pipeline(llm_call=fail)
        self.assertEqual(result["aiFailed"], 1)
        self.run_pipeline(llm_call=fail)
        self.assertEqual(len(self.model_calls), 1)
        text = (self.root / "data/enrichments.json").read_text()
        self.assertNotIn("secret token", text)
        self.run_pipeline(llm_call=fail, retry_failed=True)
        self.assertEqual(len(self.model_calls), 2)

    def test_recent_filter_and_per_run_budgets(self):
        self.papers += [{**self.papers[0], "id": "2610.12346", "arxivId": "2610.12346"},
                        {**self.papers[0], "id": "2401.12345", "arxivId": "2401.12345", "date": "2024-01-01"}]
        self.config["enrichment"]["llm"]["maxPapersPerRun"] = 1
        self.write("config.json", self.config)
        self.write("data/candidates.json", self.papers)
        result = self.run_pipeline()
        self.assertEqual(result["eligible"], 2)
        self.assertEqual(len(self.pdf_calls), 2)
        self.assertEqual(len(self.model_calls), 1)
        self.run_pipeline()
        self.assertEqual(len(self.model_calls), 2)

    def test_pdf_budget_advances_beyond_cached_covers(self):
        self.papers += [{**self.papers[0], "id": "2610.12346", "arxivId": "2610.12346"}]
        self.config["enrichment"]["maxPapersPerRun"] = 1
        self.write("config.json", self.config)
        self.write("data/candidates.json", self.papers)
        self.run_pipeline(environ={})
        self.run_pipeline(environ={})
        self.assertEqual(len(self.pdf_calls), 2)

    def test_pdf_failure_keeps_previous_good_version(self):
        self.run_pipeline()
        self.papers[0]["version"] = 2
        self.write("data/candidates.json", self.papers)
        def fail(*args):
            raise RuntimeError("network failed")
        self.run_pipeline(extractor=fail)
        record = json.loads((self.root / "data/enrichments.json").read_text())["2610.12345"]
        self.assertEqual(record["version"], 1)
        self.assertEqual(record["ai"]["status"], "ready")
        self.assertEqual(record["lastPdfAttempt"]["version"], 2)

    def test_curated_editorial_is_not_sent_to_model(self):
        paper = {**self.papers[0], "review": "full-review", "curated": True, "summaryZh": "人工核读内容"}
        self.write("data/seed-test.json", [paper])
        self.run_pipeline()
        self.assertEqual(len(self.pdf_calls), 1)
        self.assertEqual(self.model_calls, [])

    def test_figure_hint_and_extraction_configuration_refresh_cover(self):
        self.run_pipeline(environ={})
        self.papers[0]["figureHint"] = {"label": "Figure 3", "page": 6}
        self.write("data/candidates.json", self.papers)
        self.run_pipeline(environ={})
        self.assertEqual(len(self.pdf_calls), 2)
        self.config["pdf"] = {"renderScale": 3}
        self.write("config.json", self.config)
        self.run_pipeline(environ={})
        self.assertEqual(len(self.pdf_calls), 3)

    def test_recent_curated_paper_gets_cover_before_generic_candidates(self):
        paper = {**self.papers[0], "id": "2609.11111", "arxivId": "2609.11111", "date": "2026-09-10",
                 "links": {"paper": "https://arxiv.org/abs/2609.11111v1"}, "review": "source-checked", "curated": True}
        self.write("data/seed-test.json", [paper])
        self.config["enrichment"]["maxPapersPerRun"] = 1
        self.write("config.json", self.config)
        self.run_pipeline(environ={})
        self.assertEqual(self.pdf_calls, ["2609.11111"])

    def test_pdf_failure_cooldown_and_fresh_queue_precedence(self):
        self.papers += [{**self.papers[0], "id": "2610.12346", "arxivId": "2610.12346", "date": "2026-10-07"}]
        self.config["enrichment"]["maxPapersPerRun"] = 1
        self.write("config.json", self.config)
        self.write("data/candidates.json", self.papers)
        failures = []
        def fail_first(paper, root, config):
            if paper["id"] == "2610.12345":
                failures.append(paper["id"])
                raise RuntimeError("permanent failure")
            return self.extract(paper, root, config)
        self.run_pipeline(environ={}, extractor=fail_first)
        self.run_pipeline(environ={}, extractor=fail_first)
        self.assertEqual(len(failures), 1)
        self.assertEqual(self.pdf_calls, ["2610.12346"])
        # After cooldown, fresh work still receives the only extraction slot first.
        self.config["pdf"] = {"retryCooldownHours": 0}
        self.papers += [{**self.papers[0], "id": "2610.12347", "arxivId": "2610.12347", "date": "2026-10-06"}]
        self.write("config.json", self.config)
        self.write("data/candidates.json", self.papers)
        self.run_pipeline(environ={}, extractor=fail_first)
        # A PDF settings change refreshes the previously valid 12346 cover first.
        self.run_pipeline(environ={}, extractor=fail_first)
        self.assertIn("2610.12347", self.pdf_calls)
        self.assertEqual(len(failures), 1)

    def test_refresh_failure_preserves_previous_ready_draft_and_is_not_rebilled(self):
        self.run_pipeline()
        self.config["enrichment"]["llm"]["maxOutputTokens"] = 6000
        self.write("config.json", self.config)
        def fail(*args):
            self.model_calls.append("failed")
            raise RuntimeError("provider failure")
        self.run_pipeline(llm_call=fail)
        record = json.loads((self.root / "data/enrichments.json").read_text())["2610.12345"]
        self.assertEqual(record["ai"]["status"], "ready")
        self.assertEqual(record["lastAiAttempt"]["status"], "failed")
        self.run_pipeline(llm_call=fail)
        self.assertEqual(len(self.model_calls), 2)

    def test_throughput_change_does_not_regenerate_paid_drafts(self):
        self.run_pipeline()
        self.config["enrichment"]["llm"]["maxPapersPerRun"] = 5
        self.write("config.json", self.config)
        self.run_pipeline()
        self.assertEqual(len(self.model_calls), 1)


if __name__ == "__main__":
    unittest.main()
