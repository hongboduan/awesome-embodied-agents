# Paper data contract

Each data/seed-*.json is a JSON array of records. scripts/build.py merges these and data/candidates.json into dist/data.json and dist/data.js (window.ATLAS_DATA). Stable identity: arXiv base ID, otherwise lowercase slug. All UI strings Chinese except official titles.

Required fields: id, title, shortTitle, date (YYYY-MM-DD), year (integer), authors (string), categories (array of keys planning/spatial/memory/code/recovery/policies/learning/evaluation), tasks (array of navigation/manipulation/mobile/qa/general), environment (array of real/simulation/virtual), summaryZh, problem, method, findings (string array), limitations (string array), role ({model,output,memory,recovery,adaptation}: strings), links ({paper,project,code}: strings or null), evidence (array of {claim,source,label}), review (source-checked/full-review/candidate/ai-draft), codeStatus (unknown/announced/repository/code), lastChecked (YYYY-MM-DD), tags (string array), curated (boolean), deepRead (boolean).

Use null/unknown or Chinese 未核实 for unavailable information. Never invent results, exact adaptation requirements or code availability. source-checked means original abstract/project checked, not full-paper peer review. Limitations not author-stated must explicitly begin 编辑提示：. All records have at least one evidence source. Only COAP is full-review/deepRead initially. Frontend must use safe text escaping and HTTPS URL validation. Candidate records are never curated automatically.

Build output ATLAS_DATA: {papers:[...], categories:[{id,label,en}], updatedAt:ISO timestamp, updateStatus:{mode:"setup-required",lastSuccess:null,lastAttempt:null,message:"每日更新流程已准备，等待连接 GitHub 仓库"}, events:[]}. categories may be created by build.py. Frontend must handle missing optional fields defensively.


## Enrichment

`data/enrichments.json` is a dictionary keyed by base arXiv ID. Each entry records `version`, `pdf`, `figure`, and optional `ai`. PDF/text caches stay in `.cache/papers` and are not published. The model output is a draft, never automatic curation.

`figure` has `path` (relative to `web`, under `assets/papers/`), `sourceUrl`, one-based PDF `page`, original `caption`, `figureLabel`, `kind` (`figure` or `page-preview`), `selection`, and `version`. Only existing local images for the current observed version are attached by the build. Figures retain complete aspect ratio in both card formats.

A ready `ai` contains `summaryZh`, `problem`, `method`, `findings`, `limitations`, `role`, `evidence`, `social`, plus model/prompt/version/coverage metadata. Findings and limitations require literal source excerpts and page numbers. The evidence check confirms excerpt presence; it does not prove the model's interpretation. Full details in `docs/enrichment.md`.

The build attaches ready current-version drafts as `aiAnalysis` and social drafts as `social`. For automatic candidates it also fills reading fields and changes the display label to `ai-draft`, with `curated=false` and `deepRead=false`. Existing source-checked/full-review fields remain authoritative. New arXiv versions hide outdated AI drafts until regenerated.

`site.focusSince` controls the default first-publication window (`2026-09-01`). The public library opens with recent curated works; background reading and discovery candidates remain separately accessible. No source ZIP is generated or linked on the website.
