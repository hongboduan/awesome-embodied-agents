# Awesome Embodied Agents · 具身 Agent 文献合集

围绕**基础模型驱动的具身 Agent**整理研究工作，关注推理与规划、工具和代码调用、空间记忆、执行反馈与自我改进。

**重点收录 2026 年 9 月以来首次发表的新工作。** 更早的论文放在折叠的背景阅读区；VLA、WAM 论文主要围绕其在 Agent 系统中的作用与对照价值收录。

[浏览论文合集](https://hongboduan.github.io/awesome-embodied-agents/) · [English](README.md) · [推荐论文](https://github.com/hongboduan/awesome-embodied-agents/issues) · [订阅动态](https://hongboduan.github.io/awesome-embodied-agents/feed.xml)

[梳理研究脉络](https://hongboduan.github.io/awesome-embodied-agents/#map) · [查看团队研究线](https://hongboduan.github.io/awesome-embodied-agents/#teams) · [最近七天更新](https://hongboduan.github.io/awesome-embodied-agents/#updates?range=7)

<!-- ATLAS:START -->

**精选 55 条 · 论文 49 篇 · 项目 5 个 · 观点 1 篇**

来源核对 54 条 · 全文核读 1 篇 · AI 草稿 0 篇 · 自动候选 367 篇

## 目录

- [近期论文](#recent-papers)
  - [推理与规划 · 4](#recent-planning)
  - [记忆与知识 · 3](#recent-memory)
  - [技能与代码 · 5](#recent-code)
  - [自我改进 · 1](#recent-learning)
  - [基准与评测 · 4](#recent-evaluation)
- [重点补充 · 早期首发](#selected-earlier)
- [项目与系统](#projects)
- [观点与讨论](#perspectives)
- [背景阅读与早期工作](#earlier-work)

每篇论文只列在一个主分类下，其他研究方向保留为标签；点击徽章可直接打开原文、代码、项目主页或阅读卡片。

<a id="recent-papers"></a>

## 近期具身 Agent · 2026-09-01 起

<a id="recent-planning"></a>

### 推理与规划

- **[Agentic World Action Models](https://arxiv.org/abs/2610.30136v1)**<br>
  2026-10-21 · 推理与规划 · 技能与代码 · VLA / WAM · 自我改进 · 基准与评测<br>
  AW-0 把代码计划、未来视频预测和机器人动作放进同一个世界动作模型，用自动代码标注与技能库连接长程规划、物理预测和执行。<br>
  [![arXiv: 2610.30136](https://img.shields.io/badge/arXiv-2610.30136-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.30136v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/ZhuoyangLiu2005/agentic-wam) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://agentic-wam.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.30136)

- **[BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation](https://arxiv.org/abs/2610.13862v1)**<br>
  2026-10-09 · 推理与规划 · 监控与恢复 · 基准与评测 · 记忆与知识<br>
  让机载小模型选择行为树技能，由本地检查及时中断异常执行，并用结构化反馈支持重试。<br>
  [![arXiv: 2610.13862](https://img.shields.io/badge/arXiv-2610.13862-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.13862v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.13862)

- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)**<br>
  2026-10-07 · 推理与规划 · 监控与恢复 · 记忆与知识 · VLA / WAM<br>
  让推理、导航执行和监控拥有各自上下文，由运行时分配运动控制权，连接前沿模型与导航 VLA。<br>
  [![arXiv: 2610.10787](https://img.shields.io/badge/arXiv-2610.10787-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.10787v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/metacognitionai/NavGPT-3) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://metacognitionai.github.io/NavGPT3/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.10787)

- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)**<br>
  2026-10-04 · 推理与规划 · 记忆与知识 · 监控与恢复 · 技能与代码<br>
  主 Agent 管目标，子 Agent 在图像中选点和姿态，几何后端执行；跨回合经验沉淀到可更新的操作手册。<br>
  [![arXiv: 2610.04929](https://img.shields.io/badge/arXiv-2610.04929-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.04929v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/robotuse-team/RobotUse) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robotuse-team.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.04929)

<a id="recent-memory"></a>

### 记忆与知识

- **[REMM: Revisable Embodied Memory for Manipulation](https://arxiv.org/abs/2610.12710v1)**<br>
  2026-10-08 · 记忆与知识 · 推理与规划 · 监控与恢复 · VLA / WAM<br>
  给冻结 VLA 加一层可撤销的任务记忆：证据变了，依赖它的“已完成”状态也必须重审。<br>
  [![arXiv: 2610.12710](https://img.shields.io/badge/arXiv-2610.12710-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.12710v1) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://revanthsenthil.github.io/remm/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.12710)

- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)**<br>
  2026-10-05 · 记忆与知识 · 推理与规划 · VLA / WAM · 监控与恢复<br>
  把一段任务示范变成可按需查询的层级视频记忆，让 Agent 在接触细节需要时再读取短片。<br>
  [![arXiv: 2610.06843](https://img.shields.io/badge/arXiv-2610.06843-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.06843v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/BWR-hhh/rvicl) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://bwr-hhh.github.io/rvicl/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.06843)

- **[RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261v1)**<br>
  2026-09-28 · 记忆与知识 · 监控与恢复 · 推理与规划<br>
  给冻结的 GPT-6 Astra 配上示范和交互记忆，用上下文适应机器人任务，无需训练机器人专用策略。<br>
  [![arXiv: 2609.34261](https://img.shields.io/badge/arXiv-2609.34261-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.34261v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Mosi-AI/RoboICL) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2609.34261)

<a id="recent-code"></a>

### 技能与代码

- **[HexaShell: A Thin Harness for Exploring the Limits of VLM Agents as Robot Coding Agents](https://arxiv.org/abs/2610.23479v2)**<br>
  2026-10-16 · 技能与代码 · 自我改进 · 监控与恢复 · 基准与评测<br>
  在线 Coding Agent 通过薄命令行接口操作机器人，开发时由另一个 Agent 把失败修成可复用工具；用 RGB 几何测量支撑动作，在 RoboDojo 官方隐藏种子评测中取得 46.85% 加权成功率。<br>
  [![arXiv: 2610.23479](https://img.shields.io/badge/arXiv-2610.23479-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.23479v2) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/HexaFuture/HexaShell) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://hexafuture.ai/blog/hexashell/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.23479)

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)**<br>
  2026-10-08 · 技能与代码 · 自我改进 · 监控与恢复 · 推理与规划<br>
  把机器人自我改进组织成分层技能工程：定位负责的分支、局部修复、验证后再复用。<br>
  [![arXiv: 2610.12424](https://img.shields.io/badge/arXiv-2610.12424-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.12424v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/nssmd/RoboRSI) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://lab.noematrix.ai/blog/2-roborsi-research-preview/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.12424)

- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)**<br>
  2026-10-08 · 技能与代码 · 记忆与知识 · 监控与恢复 · 自我改进<br>
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。<br>
  [![arXiv: 2610.12369](https://img.shields.io/badge/arXiv-2610.12369-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.12369v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.12369)

- **[PhysEvo: Astra Can Act, Let It](https://arxiv.org/abs/2610.08995v1)**<br>
  2026-10-06 · 技能与代码 · 自我改进 · 监控与恢复 · 空间理解<br>
  冻结 Astra，让执行 Agent 行动、元 Agent 根据轨迹修订工具和技能，连诊断工具本身也能迭代。<br>
  [![arXiv: 2610.08995](https://img.shields.io/badge/arXiv-2610.08995-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.08995v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.08995)

- **[Make Code as Policy Great Again: Frontier Agents Write, Call, and Evolve Robot Tools](https://arxiv.org/abs/2609.39018v1)**<br>
  2026-09-30 · 技能与代码 · 推理与规划 · 监控与恢复 · 自我改进<br>
  把多阶段动作封装成可执行工具，每次工具运行后再由 Agent 根据反馈决定下一步。<br>
  [![arXiv: 2609.39018](https://img.shields.io/badge/arXiv-2609.39018-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.39018v1) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://hexafuture.ai/blog/urai/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2609.39018)

<a id="recent-learning"></a>

### 自我改进

- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)**<br>
  2026-10-06 · 自我改进 · 监控与恢复 · 推理与规划 · 技能与代码<br>
  冻结具身模型，把执行轨迹变成改进规划、感知工具和失败恢复逻辑的依据。<br>
  [![arXiv: 2610.08432](https://img.shields.io/badge/arXiv-2610.08432-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.08432v1) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://hyunjung00.github.io/emho/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.08432)

<a id="recent-evaluation"></a>

### 基准与评测

- **[RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](https://arxiv.org/abs/2610.10409v1)**<br>
  2026-10-07 · 基准与评测 · 空间理解 · 监控与恢复<br>
  用 84 项仿真任务检验多模态 Agent 能否闭环使用机器人，并追踪空间判断、状态保持和失败恢复的断点。<br>
  [![arXiv: 2610.10409](https://img.shields.io/badge/arXiv-2610.10409-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.10409v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/robotworldai/robotworld) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robotworldai.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.10409)

- **[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854v1)**<br>
  2026-10-01 · 基准与评测 · 空间理解 · 推理与规划<br>
  用几何、空间关系、可供性、规划和操作五个维度，检查前沿 VLM 的局部优势能否转化为完整任务成功。<br>
  [![arXiv: 2610.00854](https://img.shields.io/badge/arXiv-2610.00854-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.00854v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.00854)

- **[LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507v1)**<br>
  2026-09-30 · 基准与评测 · 推理与规划 · 监控与恢复<br>
  让通用 Agent 自己选择观测、处理图像和发出原生机器人命令，拆开评估感知、短程动作与长程组合。<br>
  [![arXiv: 2609.39507](https://img.shields.io/badge/arXiv-2609.39507-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.39507v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/dzj441/Libero-Agent) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2609.39507)

- **[An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170v1)**<br>
  2026-09-21 · 基准与评测 · 推理与规划 · VLA / WAM<br>
  系统测试 GPT-6 Astra 直接充当机器人策略的能力，揭示语义泛化与精细动作之间的明显差距。<br>
  [![arXiv: 2609.24170](https://img.shields.io/badge/arXiv-2609.24170-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.24170v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2609.24170)

<a id="selected-earlier"></a>

## 重点补充 · 早期首发

与当前具身 Agent 议题直接相关的早期工作，保留真实首发日期。

- **[EMERGE-Policy: A Robot Mind Emerges Beyond a Single Policy](https://arxiv.org/abs/2608.29896v2)**<br>
  2026-08-30 · VLA / WAM · 推理与规划 · 记忆与知识 · 监控与恢复<br>
  主 Agent 统筹任务，子 Agent 分工处理感知与验证，把 VLA、世界模型和控制器作为可组合技能。<br>
  [![arXiv: 2608.29896](https://img.shields.io/badge/arXiv-2608.29896-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2608.29896v2) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/EMERGE-Policy/EMERGE-Policy) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://emerge-policy.github.io/EMERGE-Policy/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2608.29896)

- **[ASPIRE: Agentic /Skills Discovery for Robotics](https://arxiv.org/abs/2607.00272v1)**<br>
  2026-06-30 · 自我改进 · 技能与代码 · 记忆与知识 · 监控与恢复<br>
  让 Coding Agent 从执行证据中诊断失败、修复程序，并把验证有效的经验积累为跨任务可检索技能；10 月项目更新扩展了模型与真机演示。<br>
  [![arXiv: 2607.00272](https://img.shields.io/badge/arXiv-2607.00272-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2607.00272v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/NVlabs/ASPIRE) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://research.nvidia.com/labs/gear/aspire/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2607.00272)

- **[ENPIRE: Agentic Robot Policy Self-Improvement in the Real World](https://arxiv.org/abs/2606.19980v2)**<br>
  2026-06-18 · 自我改进 · 技能与代码 · 基准与评测 · 监控与恢复<br>
  先把真机任务变成可复位、可判分的实验环境，再让 Coding Agent 改策略、跑实验、分析失败，持续改进代码或学习算法。<br>
  [![arXiv: 2606.19980](https://img.shields.io/badge/arXiv-2606.19980-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2606.19980v2) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/NVlabs/ENPIRE) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://research.nvidia.com/labs/gear/enpire/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2606.19980)

<a id="projects"></a>

## 项目与系统

官方项目预览；首发日期未核实时，明确标注收录日期。

- **[Preliminary Indicators for Robotics Progress](https://robocurve.org/rci/)**<br>
  2026-10-15 · 项目预览<br>
  用真机任务进度拟合 RCI 能力指数，检验通用能力与空间推理榜单能否预测机器人表现。<br>
  [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robocurve.org/rci/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=robocurve-rci)

- **[RPent: Agentic Infrastructure for the Physical World](https://rpent.readthedocs.io/en/latest/)**<br>
  收录于 2026-10-13 · 项目预览<br>
  把规划器、记忆、感知与动作原语组织成可组合的机器人运行框架，让通用 Agent 调用冻结 VLA 和解析控制，并依据执行反馈调整操作。<br>
  [![arXiv: 2607.08448](https://img.shields.io/badge/arXiv-2607.08448-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2607.08448v5) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/RLinf/RPent) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://rpent.readthedocs.io/en/latest/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=rpent)

- **[Frontier Models for Every Robot: Announcing our API beta](https://www.pi.website/blog/api-beta)**<br>
  2026-10-13 · 项目预览<br>
  将机器人模型的微调与推理做成托管 API，让开发者用自己的数据和真机反馈迭代策略。<br>
  [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://www.pi.website/blog/api-beta) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=pi-api-beta)

- **[Physical RSI 1.0: Recursive Self-Harness for Scaling Embodied Skills](https://mmlab.hk/research/PhysicalRSI)**<br>
  收录于 2026-10-12 · 项目预览<br>
  让大模型依据执行证据修改技能、记忆与工具，再用新场景成对评测，选择下一轮继承的控制程序。<br>
  [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/PhysicalRSI/PhysicalRSI) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://mmlab.hk/research/PhysicalRSI) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=physicalrsi)

- **[LoopROS: A Recursively Self-Evolving Robot Operating System for Agentic Manipulation](https://loopmaster.ai/loopros/)**<br>
  收录于 2026-10-12 · 项目预览<br>
  前台用历史观察与动作反馈驱动代码执行，后台把失败和修正整理为跨回合 Skills，让操作经验有机会被后续任务复用。<br>
  [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://loopmaster.ai/loopros/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=loopros)

<a id="perspectives"></a>

## 观点与讨论

作者观点与研究随笔，和报告实验结果的论文分开列出。

- **[Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html)**<br>
  2026-09-07 · Phillip Isola · 观点文章<br>
  Phillip Isola 讨论：当机器人能被通用 Agent 调用，智能的扩散方式可能怎样改变。<br>
  [![Read the original article](https://img.shields.io/badge/Article-7C3AED?style=flat-square)](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=robot-use-agents-isola)

<a id="earlier-work"></a>

<details>
<summary>背景阅读与早期工作（29 篇，展开）</summary>

### 推理与规划

- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)**<br>
  2024-10-08 · 推理与规划 · 记忆与知识 · VLA / WAM<br>
  [![arXiv: 2410.06237](https://img.shields.io/badge/arXiv-2410.06237-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2410.06237) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/UT-Austin-RobIn/BUMBLE) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robin-lab.cs.utexas.edu/BUMBLE/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2410.06237)

- **[AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963)**<br>
  2024-01-23 · 推理与规划 · 自我改进<br>
  [![arXiv: 2401.12963](https://img.shields.io/badge/arXiv-2401.12963-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2401.12963) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2401.12963)

- **[VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation](https://arxiv.org/abs/2312.03275)**<br>
  2023-12-06 · 推理与规划 · 空间理解<br>
  [![arXiv: 2312.03275](https://img.shields.io/badge/arXiv-2312.03275-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2312.03275) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/rai-opensource/vlfm) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://naoki.io/portfolio/vlfm.html) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2312.03275)

- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)**<br>
  2023-07-12 · 推理与规划 · 空间理解 · 记忆与知识<br>
  [![arXiv: 2307.06135](https://img.shields.io/badge/arXiv-2307.06135-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2307.06135) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://sayplan.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2307.06135)

- **[Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153)**<br>
  2023-03-21 · 推理与规划 · 空间理解<br>
  [![arXiv: 2303.12153](https://img.shields.io/badge/arXiv-2303.12153-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2303.12153) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://sites.google.com/stanford.edu/text2motion) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2303.12153)

- **[PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)**<br>
  2023-03-06 · 推理与规划 · 自我改进<br>
  [![arXiv: 2303.03378](https://img.shields.io/badge/arXiv-2303.03378-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2303.03378) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://palm-e.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2303.03378)

- **[LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088)**<br>
  2022-12-08 · 推理与规划 · 监控与恢复<br>
  [![arXiv: 2212.04088](https://img.shields.io/badge/arXiv-2212.04088-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2212.04088) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OSU-NLP-Group/LLM-Planner/) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://dki-lab.github.io/LLM-Planner/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2212.04088)

- **[Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608)**<br>
  2022-07-12 · 推理与规划 · 监控与恢复<br>
  [![arXiv: 2207.05608](https://img.shields.io/badge/arXiv-2207.05608-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2207.05608) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://innermonologue.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2207.05608)

- **[LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429)**<br>
  2022-07-10 · 推理与规划 · VLA / WAM<br>
  [![arXiv: 2207.04429](https://img.shields.io/badge/arXiv-2207.04429-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2207.04429) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/blazejosinski/lm_nav) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://sites.google.com/view/lmnav) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2207.04429)

- **[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)**<br>
  2022-04-04 · 推理与规划 · VLA / WAM<br>
  [![arXiv: 2204.01691](https://img.shields.io/badge/arXiv-2204.01691-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2204.01691) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://say-can.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2204.01691)

- **[Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents](https://arxiv.org/abs/2201.07207)**<br>
  2022-01-18 · 推理与规划<br>
  [![arXiv: 2201.07207](https://img.shields.io/badge/arXiv-2201.07207-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2201.07207) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://huangwl18.github.io/language-planner) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2201.07207)

### 空间理解

- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)**<br>
  2023-09-28 · 空间理解 · 推理与规划 · 记忆与知识<br>
  [![arXiv: 2309.16650](https://img.shields.io/badge/arXiv-2309.16650-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2309.16650) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/concept-graphs/concept-graphs) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://concept-graphs.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2309.16650)

- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)**<br>
  2023-07-12 · 空间理解 · 技能与代码 · 推理与规划<br>
  [![arXiv: 2307.05973](https://img.shields.io/badge/arXiv-2307.05973-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2307.05973) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/huangwl18/VoxPoser) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://voxposer.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2307.05973)

- **[ConceptFusion: Open-set Multimodal 3D Mapping](https://arxiv.org/abs/2302.07241)**<br>
  2023-02-14 · 空间理解 · 记忆与知识<br>
  [![arXiv: 2302.07241](https://img.shields.io/badge/arXiv-2302.07241-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2302.07241) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/concept-fusion/concept-fusion) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://concept-fusion.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2302.07241)

- **[OpenScene: 3D Scene Understanding with Open Vocabularies](https://arxiv.org/abs/2211.15654)**<br>
  2022-11-28 · 空间理解 · 自我改进<br>
  [![arXiv: 2211.15654](https://img.shields.io/badge/arXiv-2211.15654-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2211.15654) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/pengsongyou/openscene) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://pengsongyou.github.io/openscene) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2211.15654)

- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)**<br>
  2022-10-11 · 空间理解 · 技能与代码 · 推理与规划<br>
  [![arXiv: 2210.05714](https://img.shields.io/badge/arXiv-2210.05714-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2210.05714) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/vlmaps/vlmaps) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://vlmaps.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2210.05714)

### 记忆与知识

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)**<br>
  2024-11-23 · 记忆与知识 · 空间理解 · 推理与规划<br>
  [![arXiv: 2411.17735](https://img.shields.io/badge/arXiv-2411.17735-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2411.17735) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/UMass-Embodied-AGI/3D-Mem) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://umass-embodied-agi.github.io/3D-Mem/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2411.17735)

### 技能与代码

- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)**<br>
  2023-10-19 · 技能与代码 · 自我改进 · VLA / WAM<br>
  [![arXiv: 2310.12931](https://img.shields.io/badge/arXiv-2310.12931-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2310.12931) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/eureka-research/Eureka) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://eureka-research.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2310.12931)

- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)**<br>
  2023-05-25 · 技能与代码 · 记忆与知识 · 自我改进<br>
  [![arXiv: 2305.16291](https://img.shields.io/badge/arXiv-2305.16291-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2305.16291) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/MineDojo/Voyager) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://voyager.minedojo.org/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2305.16291)

- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)**<br>
  2022-09-22 · 技能与代码 · 推理与规划 · 监控与恢复<br>
  [![arXiv: 2209.11302](https://img.shields.io/badge/arXiv-2209.11302-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2209.11302) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/NVlabs/progprompt-vh) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://progprompt.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2209.11302)

- **[Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753)**<br>
  2022-09-16 · 技能与代码 · 推理与规划<br>
  [![arXiv: 2209.07753](https://img.shields.io/badge/arXiv-2209.07753-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2209.07753) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://code-as-policies.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2209.07753)

### 监控与恢复

- **[DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329)**<br>
  2023-07-01 · 监控与恢复 · 推理与规划<br>
  [![arXiv: 2307.00329](https://img.shields.io/badge/arXiv-2307.00329-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2307.00329) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://sites.google.com/view/doremi-paper/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2307.00329)

### VLA / WAM

- **[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)**<br>
  2024-06-13 · VLA / WAM · 自我改进<br>
  [![arXiv: 2406.09246](https://img.shields.io/badge/arXiv-2406.09246-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2406.09246) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/openvla/openvla) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://openvla.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2406.09246)

- **[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)**<br>
  2024-05-20 · VLA / WAM · 自我改进<br>
  [![arXiv: 2405.12213](https://img.shields.io/badge/arXiv-2405.12213-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2405.12213) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/octo-models/octo) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://octo-models.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2405.12213)

- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)**<br>
  2024-01-22 · VLA / WAM · 空间理解 · 推理与规划<br>
  [![arXiv: 2401.12202](https://img.shields.io/badge/arXiv-2401.12202-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2401.12202) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/ok-robot/ok-robot) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://ok-robot.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2401.12202)

- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)**<br>
  2023-07-28 · VLA / WAM · 自我改进<br>
  [![arXiv: 2307.15818](https://img.shields.io/badge/arXiv-2307.15818-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2307.15818) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robotics-transformer2.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2307.15818)

- **[CLIPort: What and Where Pathways for Robotic Manipulation](https://arxiv.org/abs/2109.12098)**<br>
  2021-09-24 · VLA / WAM · 空间理解<br>
  [![arXiv: 2109.12098](https://img.shields.io/badge/arXiv-2109.12098-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2109.12098) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/cliport/cliport) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://cliport.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2109.12098)

### 基准与评测

- **[BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation](https://arxiv.org/abs/2403.09227)**<br>
  2024-03-14 · 基准与评测<br>
  [![arXiv: 2403.09227](https://img.shields.io/badge/arXiv-2403.09227-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2403.09227) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/StanfordVL/BEHAVIOR-1K) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://behavior.stanford.edu/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2403.09227)

- **[Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots](https://arxiv.org/abs/2310.13724)**<br>
  2023-10-19 · 基准与评测<br>
  [![arXiv: 2310.13724](https://img.shields.io/badge/arXiv-2310.13724-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2310.13724) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/facebookresearch/habitat-lab) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://aihabitat.org/habitat3/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2310.13724)

</details>

<!-- ATLAS:END -->

<details>
<summary>阅读线索与收录标记</summary>

## 阅读线索

| 关心的问题 | 对应研究方向 |
| --- | --- |
| 模型怎样把目标变成可执行计划？ | 推理、规划、代码与工具 |
| 怎样保存并利用已经观察过的信息？ | 空间状态、记忆与检索 |
| 执行偏离预期时怎么办？ | 监控、反馈与失败恢复 |
| 哪些能力可以从交互中改善？ | 上下文学习与自我改进 |
| Agent 怎样调用学习策略？ | Agent 与 VLA/WAM 的接口 |
| 实验到底验证了什么？ | 评测协议、基准与真机证据 |

网站提供有原始来源的阅读笔记、论文原图、方法对照，以及适合阅读和传播的横屏/竖屏卡片。发表时间按 arXiv 首次提交日期计算，版本更新单独记录。

观点文章单独标注，不作为实验证据。官方项目预览与论文分开列出；首发日期未核实的项目明确显示收录日期，项目原图保留来源署名。

## 阅读标记

- **来源核对**：核对过原始摘要或作者资料，不等同于全文审读。
- **全文精读**：有针对该论文的阅读、关键结论依据与边界说明。
- **AI 草稿**：有原文页码和摘录的机器辅助解读，仍待编辑复核。
- **发现候选**：自动发现的元数据，相关性和具体主张待核查。

自动提取的配图保留 PDF 来源和页码；整页预览会明确标注。不同实验协议下的数值不作为统一排行榜。

</details>

## 推荐与纠错

欢迎通过 [Issues](https://github.com/hongboduan/awesome-embodied-agents/issues) 或 Pull Request 推荐论文、补充代码链接和纠正解读。请提供论文链接、首次发表日期、作者项目/代码链接，以及与具身 Agent 的关联。详见[贡献说明](CONTRIBUTING.md)。

论文图片与内容归原作者所有，请引用原始工作。BibTeX 用于辅助整理，正式投稿前请核对完整作者与发表信息。
