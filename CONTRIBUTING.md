# Contributing / 贡献指南

We welcome paper suggestions, corrections, source checks, and improvements to the card layouts. Please keep research claims attributable to their original source.

## Review a candidate

1. Open the original paper and author project. Confirm title, authors, identifier, version and task scope.
2. Copy the candidate to `data/seed-community.json` (a JSON array), or edit an existing seed file. Remove any duplicate seed record with the same base arXiv identifier.
3. Write a short Chinese summary. Fill the model role, output, memory, recovery, and adaptation fields only when supported by a source. Use `未核实` for missing information.
4. Add `evidence` items linking claims to the paper, relevant table/page, or author project. State evaluation conditions alongside numbers.
5. Set `review: "source-checked"` after checking the abstract/project, or `"full-review"` after a full reading. Set `curated: true` only after deciding the paper belongs in the collection. Set `deepRead: true` only for a complete paper-specific reading.
6. Run the commands below, inspect the website and both card orientations, then open a pull request.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/build.py
python -m http.server 8000 --directory dist
```

Seeds override automatic candidates during builds, so an old candidate entry cannot overwrite reviewed work. New source versions are shown separately and require editorial rechecking. An arXiv revision does not prove that a result improved.

## Accuracy requirements

- Label interpretation with `编辑提示：`; do not attribute it to the authors.
- Keep raw English abstracts under `abstractEn`. Do not place unreviewed English text in `summaryZh` and label it a Chinese reading.
- Record code status separately: `unknown`, `announced`, `repository`, or `code`. A project link is not evidence of released code or reproducibility.
- Avoid comparing headline numbers across incompatible benchmarks or test protocols.
- Use HTTPS source links. Do not add tracking scripts or third-party credentials.
- Complete schema: [docs/data-contract.md](docs/data-contract.md).

## Corrections

For a correction, include the paper ID, affected text, original-source link, and proposed replacement. Correct the seed record and rebuild; do not edit generated README sections or `dist/data.js` directly.

Prioritize embodied-agent papers first published from September 2026 onward. Earlier papers belong to background reading. Automatic PDF covers and optional AI drafts are separate from editorial curation; an AI draft must not promote itself to a reviewed or curated paper. Automated code-release monitoring is not implemented.
