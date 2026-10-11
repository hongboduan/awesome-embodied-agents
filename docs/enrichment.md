# PDF covers and optional Chinese AI drafts

The daily workflow has two independent enrichment stages. PDF extraction runs
without an LLM key. Chinese close-reading drafts require an explicitly configured
model and API key. The website and browser exports never receive a secret.

## What is generated

- A versioned PDF figure, preferably a framework/overview figure selected using
  its caption and page geometry. If reliable figure extraction is unavailable,
  the result is explicitly labelled a PDF page preview. Automatic selection can
  be imperfect; it is not a claim that a human selected the best framework figure.
- A Chinese summary, problem, method, findings, author-stated limitations and
  model-role fields, plus short WeChat and Xiaohongshu drafts when LLM processing
  is configured. This is a **text-based PDF excerpt analysis**; the model does not
  see the PDF diagrams, and tables with poor text extraction need human checking.
- Page links and short source excerpts for the problem, method, findings and
  limitations. The validator checks the schema, exact quote presence, page
  existence and numerical tokens. It cannot prove semantic entailment or detect
  every mistaken interpretation, so outputs remain `review: "ai-draft"`,
  `curated: false`, `deepRead: false` until manual review.

Existing editorial seed content is preserved. An AI draft does not automatically
become a README recommendation or a human-reviewed paper. No social account is
connected, and generated social copy is never posted automatically.

## Configure a model once

Open the repository **Settings → Secrets and variables → Actions**:

| Kind | Name | Value |
| --- | --- | --- |
| Repository secret | `LLM_API_KEY` | Your chosen provider's API key |
| Repository variable | `LLM_MODEL` | An exact model ID available to your account |
| Repository variable, optional | `LLM_BASE_URL` | API root, default `https://api.openai.com/v1` |

Then use **Actions → Update papers and deploy Atlas → Run workflow**. A ChatGPT
subscription is not an API credential; the runner needs the separately configured
API key. Do not paste credentials into `config.json`, issues, source files or
browser code. If using another compatible provider, its endpoint receives the
selected text of public arXiv PDFs for processing.

The adapter uses `POST /chat/completions`, `response_format: {"type":"json_object"}`
and local validation. The model must support that interface and JSON mode. The
default token-limit parameter is `max_completion_tokens`; providers requiring
`max_tokens` can set `enrichment.llm.tokenParameter` to `max_tokens`.
See the [official API reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).
The project does not silently choose a model or assume that a model mentioned in
a research paper is available through your API provider.

Example configuration:

```json
{
  "enrichment": {
    "enabled": true,
    "since": "2026-09-01",
    "maxPapersPerRun": 12,
    "llm": {
      "enabled": true,
      "maxPapersPerRun": 3,
      "maxInputChars": 45000,
      "maxOutputTokens": 5000,
      "timeoutSeconds": 120,
      "tokenParameter": "max_completion_tokens"
    }
  }
}
```

`since` uses the paper's publication date. Curated recent papers receive covers
first, then papers with explicit agent, reasoning, planning or memory relevance
ahead of generic policy papers, with newer papers first within the priority group. The date preference
does not label older research scientifically invalid.

## Budgets and cache behaviour

Each run attempts at most 12 PDF extractions and 3 model requests by default.
Existing covers do not consume the PDF budget, so the queue advances across runs.
Input is limited to 45,000 **characters**, not tokens: selected pages prioritize
the introduction and pages mentioning evaluation, results or limitations. The
record includes `inputPages`, `inputChars` and `availableChars`, making partial
coverage visible. Output is capped by the model API token parameter; on reasoning
models that limit can also include reasoning tokens.

A successful draft is reused for the same paper version, model, prompt,
generation settings and selected text. Changing those inputs permits another request.
The API key is not part of the fingerprint and is never saved. A failed or invalid
response is not automatically retried for the same fingerprint, because it may
already have incurred charges. To deliberately retry failures:

```bash
python scripts/enrich.py --retry-failed
```

Changing throughput limits or timeouts does not regenerate prior AI drafts.
Changing the figure hint or PDF extraction settings refreshes the image without
requiring a paper version change. A request can still be billed if the runner is terminated before its local attempt
record is committed; no local script can guarantee billing idempotency across a
lost runner. Provider spend limits are the final budget safeguard.

Without both `LLM_API_KEY` and `LLM_MODEL`, the script makes **zero model calls**,
continues PDF extraction and reports `llmMode: "not-configured"`. Setting
`enrichment.llm.enabled` to `false` explicitly disables model processing.
Curated/editorial papers receive PDF covers but do not use the model budget by
default. Set `enrichment.llm.includeCurated` to `true` to generate separate AI
draft records for them too; the build still preserves their editorial fields.

## Storage and review

| Path | Contents |
| --- | --- |
| `web/assets/papers/` | Versioned figure PNGs served by the site |
| `data/enrichments.json` | Figure attribution and optional validated AI drafts, keyed by arXiv base ID |
| `data/enrichment-status.json` | Counts, budget deferrals and explicit model configuration status |
| `.cache/papers/` | Downloaded PDFs, extracted page text and extraction cache; excluded from git/site exports |

Raw provider responses and exception messages are not published. Failures use
short error codes. A failed PDF update retains the previous good artifact; the
version field identifies which version it came from. Per-paper failures do not
stop unrelated papers from receiving covers. Failed PDF attempts wait 24 hours
before retrying (`pdf.retryCooldownHours`) and go behind fresh work, preventing
permanent download failures from consuming every daily slot. A failed same-version
AI refresh preserves the previous successful draft and records the failure in
`lastAiAttempt`; it does not falsely relabel the old draft as the new model's work.
The CLI exits nonzero after partial failures so Actions reports the problem while
the workflow can still publish preserved data.

Before promoting an AI draft, compare its source pages with the original PDF,
check table headers/units and experimental scope, confirm limitations are
author-stated rather than speculation, and edit the social copy. Put the reviewed
record in an appropriate `data/seed-*.json` file with its reviewed version and
review status; editorial seed fields take precedence on the next build.

Local commands (after installing the PDF dependency from `requirements.txt`):

```bash
python scripts/enrich.py
python scripts/build.py
python -m unittest discover -s tests -v
```

Tests mock arXiv and model requests, including missing credentials, invalid
evidence, unsupported numbers, version changes, budgets and failed-request reuse.
Passing tests does not mean the live paid provider connection has been exercised.
