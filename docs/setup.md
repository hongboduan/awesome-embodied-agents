# 维护者运行说明

本文仅记录本仓库的维护方式。公开网站与 README 的主要入口面向文献阅读。

## 本地更新

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/update.py
python scripts/enrich.py
python scripts/build.py
```

- `config.json` 的 `focusSince` 控制首页的默认时间范围，当前为 `2026-09-01`。
- `arxiv.since` 控制新论文首次发表日期下限。首次使用新时间范围或检索式时，回填整个范围；以后增量更新并重叠七天。
- 已收录背景论文仍检查版本变化，不会因一次新版提交而被当作新发表论文。
- `scripts/enrich.py` 下载版本固定的 PDF、提取原图和分页文本；模型精读是可选步骤，详见 [精读配置](enrichment.md)。
- `data/seed-*.json` 保存编辑内容，`data/candidates.json` 保存发现候选，`data/enrichments.json` 保存配图来源与模型草稿。
- `.cache/papers` 保存 PDF 和分页文本，不提交到 Git，也不发布到站点。

## GitHub Actions

现有工作流每日北京时间 08:17 执行，并支持手动运行与相关源码推送触发。GitHub 可能延迟定时任务。

工作流安装 PDF 依赖、测试、发现论文、提取配图/可选精读、构建文献网站，并提交数据与配图。Pages 已启用时发布站点。发现或提取失败保留已有记录；运行情况见 Actions 与 `data/*-status.json`。

维护者如需启用模型，在仓库 Settings → Secrets and variables → Actions 配置 `LLM_API_KEY`（Secret）、`LLM_MODEL`（Variable），以及可选的 `LLM_BASE_URL`（Variable）。没有密钥时只提取 PDF 原图，不执行模型调用。不要把密钥放进配置文件或论文数据。

## 内容审核

模型草稿不会自动获得精选或全文审读标记。核查原文、实验协议、局限和引用后，可将认可的内容整理进 seed 文件。已有编辑解读不会被自动草稿覆盖；模型调用失败时旧内容保留。
