# Paper data contract

Each data/seed-*.json is a JSON array of records. scripts/build.py merges these and data/candidates.json into dist/data.json and dist/data.js (window.ATLAS_DATA). Stable identity: arXiv base ID, otherwise lowercase slug. All UI strings Chinese except official titles.

Required fields: id, title, shortTitle, date (YYYY-MM-DD), year (integer), authors (string), categories (array of keys planning/spatial/memory/code/recovery/policies/learning/evaluation), tasks (array of navigation/manipulation/mobile/qa/general), environment (array of real/simulation/virtual), summaryZh, problem, method, findings (string array), limitations (string array), role ({model,output,memory,recovery,adaptation}: strings), links ({paper,project,code}: strings or null), evidence (array of {claim,source,label}), review (source-checked/full-review/candidate), codeStatus (unknown/announced/repository/code), lastChecked (YYYY-MM-DD), tags (string array), curated (boolean), deepRead (boolean).

Use null/unknown or Chinese 未核实 for unavailable information. Never invent results, exact adaptation requirements or code availability. source-checked means original abstract/project checked, not full-paper peer review. Limitations not author-stated must explicitly begin 编辑提示：. All records have at least one evidence source. Only COAP is full-review/deepRead initially. Frontend must use safe text escaping and HTTPS URL validation. Candidate records are never curated automatically.

Build output ATLAS_DATA: {papers:[...], categories:[{id,label,en}], updatedAt:ISO timestamp, updateStatus:{mode:"setup-required",lastSuccess:null,lastAttempt:null,message:"每日更新流程已准备，等待连接 GitHub 仓库"}, events:[]}. categories may be created by build.py. Frontend must handle missing optional fields defensively.
