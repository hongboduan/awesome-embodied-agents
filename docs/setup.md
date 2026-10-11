# 启用 GitHub 自动更新与 Pages

本仓库已配置真实源码推送触发、每日北京时间 08:17 和手动触发。首次启用网站时，在 Settings → Pages 选择 GitHub Actions；论文发现与数据提交不依赖 Pages 开关。

## 1. 新建仓库并上传源码

建议仓库名 `awesome-embodied-agents`，默认分支设为 `main`。选择仓库可见性后上传本目录中的源码；包括 `.github/workflows/update-and-deploy.yml`。不要上传密钥或 `.env`。`dist/` 由工作流生成，不必提交。

## 2. 配置网址

编辑根目录 `config.json`：

```json
{
  "siteUrl": "https://hongboduan.github.io/awesome-embodied-agents/",
  "repositoryUrl": "https://github.com/hongboduan/awesome-embodied-agents"
}
```

保留现有 `arxiv` 对象。请把 `arxiv.userAgent` 中的联系信息替换为维护者公开联系页面或邮箱。网站资源使用相对路径，支持 GitHub Pages 的项目子目录；RSS 使用 `siteUrl` 生成站点链接。

## 3. 打开 Pages 和工作流权限

- 仓库 **Settings → Pages → Build and deployment → Source**，选 **GitHub Actions**。
- 在 **Settings → Actions → General** 允许运行此仓库的工作流及官方 `actions/*` actions。
- 工作流的构建 job 需要 `contents: write`，用于提交候选与运行状态；部署 job 只申请 `pages: write` 和 `id-token: write`。组织策略若禁止写入，应先按组织规则配置。
- 默认 `main` 如有禁止 bot 直接推送的分支保护，需要为该流程配置允许的更新方式；不要把工作流报错误认为抓取成功。此模板未自动绕过保护或替你修改策略。

## 4. 第一次手动运行

进入 **Actions → Update papers and deploy Atlas → Run workflow**。保留 `refresh=true` 会抓取 arXiv；第一次以最近 7 天为范围，同时检查已收录论文的最新版本。

工作流依次测试、抓取、构建、提交数据和上传站点产物。只有 Pages 已配置时才部署；未配置时在运行摘要显示设置入口，不妨碍论文数据更新。部署地址显示在运行页面及 Pages 设置中。网站更新指示器只有在真实抓取成功后才显示成功时间。

每天计划时间为 **北京时间 08:17（UTC 00:17）**。GitHub 定时任务可能延迟，不保证精确到分钟；公共仓库长期无活动时也可能停用计划任务。保留手动触发用于补跑。仅 `main` 分支配置本工作流；若改默认分支，请同步修改 YAML 中的分支和提交条件。

## 5. 日常编辑

`data/seed-*.json` 为人工编辑区；`data/candidates.json` 为自动候选。把审核后的候选复制到 seed 文件，填写中文解读和来源，再提交。构建时人工记录优先，已有解读不会被候选或新版摘要覆盖。

状态文件说明：

| 文件 | 用途 |
| --- | --- |
| `data/update-status.json` | 最近尝试、最近成功和错误状态 |
| `data/versions.json` | 已观察到的 arXiv 版本与检查时间 |
| `data/events.json` | 首次发现和版本更新事件 |
| `dist/feed.xml` | RSS 动态，构建生成 |
| `dist/papers.bib` | BibTeX 元数据导出，构建生成 |
| `dist/papers.json` | 论文 JSON 导出，构建生成 |

## 抓取策略与失败处理

- 按最后更新时间倒序分页；成功时间前再回溯七天，减少延迟索引造成的遗漏。
- 以 arXiv 基础 ID 去重，版本单独保存。另按 ID 检查全部已收录论文，避免关键词变化漏掉旧论文的新版本。人工记录未注明版本时，首次检查只建立版本基线，不记作新变化；只有后续观察到版本提升才产生动态。
- 请求串行，间隔至少三秒。每次分页响应都必须通过检查。
- 达到分页上限但尚未抵达时间边界时，本轮报错，保留旧数据；提高 `arxiv.maxPages` 后重跑，不悄悄截断结果。
- 抓取失败不会清空旧数据。工作流继续发布可用内容与失败状态，最后标记失败，方便 GitHub 通知维护者。
- 更新和部署处于同一工作流。无需依赖 `GITHUB_TOKEN` 创建的提交再次触发另一个工作流。

无需模型密钥。候选保留英文摘要且标为待审，不生成未经核查的中文精读。关键词发现有漏检与误报可能，精选仍依赖编辑判断。

## 当前范围

本版自动化包括 arXiv 候选发现和版本变化。代码/权重发布监控、自动全文分析、定时公众号发布没有实现，也不会在后台假运行。扩展这些功能时，应分别增加真实数据来源、凭据配置、运行日志与人工审核环节。

## 官方参考

- [GitHub Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub Actions 定时触发说明](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [actions/checkout](https://github.com/actions/checkout)
- [actions/setup-python](https://github.com/actions/setup-python)
- [arXiv API 手册](https://info.arxiv.org/help/api/user-manual.html)

工作流使用官方 action 主版本：checkout v6、setup-python v7、configure-pages v5、upload-pages-artifact v4、deploy-pages v4。首次部署失败时请先检查 Pages 来源、默认分支、组织权限和 action 日志。
