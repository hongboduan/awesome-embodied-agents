# Awesome Embodied Agents

A curated reading list on **foundation-model-driven embodied agents**: reasoning, planning, tool use, spatial memory, execution feedback, and self-improvement.

**Focus: papers first published from September 2026 onward.** Earlier papers are kept in a collapsed background-reading section. VLA and world-model work is included when it contributes to an agent system or provides a meaningful comparison.

[Read the paper collection](https://hongboduan.github.io/awesome-embodied-agents/) · [简体中文](README.zh-CN.md) · [Suggest a paper](https://github.com/hongboduan/awesome-embodied-agents/issues) · [RSS](https://hongboduan.github.io/awesome-embodied-agents/feed.xml)

<!-- ATLAS:START -->

**47 curated entries · 44 papers · 2 projects · 1 perspective**

46 source-checked · 1 full-review · 0 AI drafts · 263 discovery candidates

## Contents

- [Recent papers](#recent-papers)
  - [Reasoning & Planning · 3](#recent-planning)
  - [Memory & Knowledge · 3](#recent-memory)
  - [Skills & Code · 4](#recent-code)
  - [Self-improvement · 1](#recent-learning)
  - [Benchmarks & Evaluation · 4](#recent-evaluation)
- [Projects and systems](#projects)
- [Perspectives and essays](#perspectives)
- [Foundations and earlier work](#earlier-work)

Each paper appears once under its primary topic; secondary topics remain visible as tags. English titles link to original sources; Chinese notes and reading cards are available alongside them.

<a id="recent-papers"></a>

## Recent embodied agents · since 2026-09-01

<a id="recent-planning"></a>

### Reasoning & Planning

- **[BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation](https://arxiv.org/abs/2610.13862v1)**<br>
  2026-10-09 · Reasoning & Planning · Monitoring & Recovery · Benchmarks & Evaluation · Memory & Knowledge<br>
  让机载小模型选择行为树技能，由本地检查及时中断异常执行，并用结构化反馈支持重试。<br>
  [![arXiv: 2610.13862](https://img.shields.io/badge/arXiv-2610.13862-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.13862v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.13862)

- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)**<br>
  2026-10-07 · Reasoning & Planning · Monitoring & Recovery · Memory & Knowledge · VLA & World Models<br>
  让推理、导航执行和监控拥有各自上下文，由运行时分配运动控制权，连接前沿模型与导航 VLA。<br>
  [![arXiv: 2610.10787](https://img.shields.io/badge/arXiv-2610.10787-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.10787v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/metacognitionai/NavGPT-3) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://metacognitionai.github.io/NavGPT3/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.10787)

- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)**<br>
  2026-10-04 · Reasoning & Planning · Memory & Knowledge · Monitoring & Recovery · Skills & Code<br>
  主 Agent 管目标，子 Agent 在图像中选点和姿态，几何后端执行；跨回合经验沉淀到可更新的操作手册。<br>
  [![arXiv: 2610.04929](https://img.shields.io/badge/arXiv-2610.04929-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.04929v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/robotuse-team/RobotUse) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robotuse-team.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.04929)

<a id="recent-memory"></a>

### Memory & Knowledge

- **[REMM: Revisable Embodied Memory for Manipulation](https://arxiv.org/abs/2610.12710v1)**<br>
  2026-10-08 · Memory & Knowledge · Reasoning & Planning · Monitoring & Recovery · VLA & World Models<br>
  给冻结 VLA 加一层可撤销的任务记忆：证据变了，依赖它的“已完成”状态也必须重审。<br>
  [![arXiv: 2610.12710](https://img.shields.io/badge/arXiv-2610.12710-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.12710v1) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://revanthsenthil.github.io/remm/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.12710)

- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)**<br>
  2026-10-05 · Memory & Knowledge · Reasoning & Planning · VLA & World Models · Monitoring & Recovery<br>
  把一段任务示范变成可按需查询的层级视频记忆，让 Agent 在接触细节需要时再读取短片。<br>
  [![arXiv: 2610.06843](https://img.shields.io/badge/arXiv-2610.06843-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.06843v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/BWR-hhh/rvicl) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://bwr-hhh.github.io/rvicl/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.06843)

- **[RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261v1)**<br>
  2026-09-28 · Memory & Knowledge · Monitoring & Recovery · Reasoning & Planning<br>
  给冻结的 GPT-6 Astra 配上示范和交互记忆，用上下文适应机器人任务，无需训练机器人专用策略。<br>
  [![arXiv: 2609.34261](https://img.shields.io/badge/arXiv-2609.34261-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.34261v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Mosi-AI/RoboICL) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2609.34261)

<a id="recent-code"></a>

### Skills & Code

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)**<br>
  2026-10-08 · Skills & Code · Self-improvement · Monitoring & Recovery · Reasoning & Planning<br>
  把机器人自我改进组织成分层技能工程：定位负责的分支、局部修复、验证后再复用。<br>
  [![arXiv: 2610.12424](https://img.shields.io/badge/arXiv-2610.12424-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.12424v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/nssmd/RoboRSI) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://lab.noematrix.ai/blog/2-roborsi-research-preview/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.12424)

- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)**<br>
  2026-10-08 · Skills & Code · Memory & Knowledge · Monitoring & Recovery · Self-improvement<br>
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。<br>
  [![arXiv: 2610.12369](https://img.shields.io/badge/arXiv-2610.12369-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.12369v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.12369)

- **[PhysEvo: Astra Can Act, Let It](https://arxiv.org/abs/2610.08995v1)**<br>
  2026-10-06 · Skills & Code · Self-improvement · Monitoring & Recovery · Spatial Understanding<br>
  冻结 Astra，让执行 Agent 行动、元 Agent 根据轨迹修订工具和技能，连诊断工具本身也能迭代。<br>
  [![arXiv: 2610.08995](https://img.shields.io/badge/arXiv-2610.08995-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.08995v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.08995)

- **[Make Code as Policy Great Again: Frontier Agents Write, Call, and Evolve Robot Tools](https://arxiv.org/abs/2609.39018v1)**<br>
  2026-09-30 · Skills & Code · Reasoning & Planning · Monitoring & Recovery · Self-improvement<br>
  把多阶段动作封装成可执行工具，每次工具运行后再由 Agent 根据反馈决定下一步。<br>
  [![arXiv: 2609.39018](https://img.shields.io/badge/arXiv-2609.39018-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.39018v1) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://hexafuture.ai/blog/urai/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2609.39018)

<a id="recent-learning"></a>

### Self-improvement

- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)**<br>
  2026-10-06 · Self-improvement · Monitoring & Recovery · Reasoning & Planning · Skills & Code<br>
  冻结具身模型，把执行轨迹变成改进规划、感知工具和失败恢复逻辑的依据。<br>
  [![arXiv: 2610.08432](https://img.shields.io/badge/arXiv-2610.08432-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.08432v1) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://hyunjung00.github.io/emho/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.08432)

<a id="recent-evaluation"></a>

### Benchmarks & Evaluation

- **[RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](https://arxiv.org/abs/2610.10409v1)**<br>
  2026-10-07 · Benchmarks & Evaluation · Spatial Understanding · Monitoring & Recovery<br>
  An 84-task simulation benchmark of multimodal robot-use agents across five domains, with trajectory-level diagnosis of state tracking and recovery failures.<br>
  [![arXiv: 2610.10409](https://img.shields.io/badge/arXiv-2610.10409-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.10409v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/robotworldai/robotworld) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robotworldai.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.10409)

- **[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854v1)**<br>
  2026-10-01 · Benchmarks & Evaluation · Spatial Understanding · Reasoning & Planning<br>
  用几何、空间关系、可供性、规划和操作五个维度，检查前沿 VLM 的局部优势能否转化为完整任务成功。<br>
  [![arXiv: 2610.00854](https://img.shields.io/badge/arXiv-2610.00854-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2610.00854v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2610.00854)

- **[LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507v1)**<br>
  2026-09-30 · Benchmarks & Evaluation · Reasoning & Planning · Monitoring & Recovery<br>
  让通用 Agent 自己选择观测、处理图像和发出原生机器人命令，拆开评估感知、短程动作与长程组合。<br>
  [![arXiv: 2609.39507](https://img.shields.io/badge/arXiv-2609.39507-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.39507v1) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/dzj441/Libero-Agent) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2609.39507)

- **[An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170v1)**<br>
  2026-09-21 · Benchmarks & Evaluation · Reasoning & Planning · VLA & World Models<br>
  系统测试 GPT-6 Astra 直接充当机器人策略的能力，揭示语义泛化与精细动作之间的明显差距。<br>
  [![arXiv: 2609.24170](https://img.shields.io/badge/arXiv-2609.24170-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2609.24170v1) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2609.24170)

<a id="projects"></a>

## Projects and systems

Project previews; collection dates are labeled when publication dates are unverified.

- **[Physical RSI 1.0: Recursive Self-Harness for Scaling Embodied Skills](https://mmlab.hk/research/PhysicalRSI)**<br>
  added 2026-10-12 · Project preview<br>
  A preview system for embodied self-harness: propose changes to skills, memory and tools, evaluate frozen candidates on fresh paired cases, select a survivor and preserve evidence and lineage.<br>
  [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/PhysicalRSI/PhysicalRSI) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://mmlab.hk/research/PhysicalRSI) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=physicalrsi)

- **[LoopROS: A Recursively Self-Evolving Robot Operating System for Agentic Manipulation](https://loopmaster.ai/loopros/)**<br>
  added 2026-10-12 · Project preview<br>
  An agentic robot runtime combining within-episode observation and action feedback with background consolidation of reusable cross-episode Skills. The official project reports 82/100 successes on a selected ten-task simulation subset; component ablations are ongoing.<br>
  [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://loopmaster.ai/loopros/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=loopros)

<a id="perspectives"></a>

## Perspectives and essays

Author perspectives and essays, listed separately from experimental papers.

- **[Robot-Use Agents](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html)**<br>
  2026-09-07 · Phillip Isola · Perspective / essay<br>
  Phillip Isola considers robot use as a tool capability of general-purpose agents and its implications for how capabilities spread across robots.<br>
  [![Read the original article](https://img.shields.io/badge/Article-7C3AED?style=flat-square)](https://web.mit.edu/phillipi/www/writing/robot-use-agents.html) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=robot-use-agents-isola)

<a id="earlier-work"></a>

<details>
<summary>Foundations and earlier work (29 papers)</summary>

### Reasoning & Planning

- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)**<br>
  2024-10-08 · Reasoning & Planning · Memory & Knowledge · VLA & World Models<br>
  [![arXiv: 2410.06237](https://img.shields.io/badge/arXiv-2410.06237-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2410.06237) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/UT-Austin-RobIn/BUMBLE) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robin-lab.cs.utexas.edu/BUMBLE/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2410.06237)

- **[AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963)**<br>
  2024-01-23 · Reasoning & Planning · Self-improvement<br>
  [![arXiv: 2401.12963](https://img.shields.io/badge/arXiv-2401.12963-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2401.12963) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2401.12963)

- **[VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation](https://arxiv.org/abs/2312.03275)**<br>
  2023-12-06 · Reasoning & Planning · Spatial Understanding<br>
  [![arXiv: 2312.03275](https://img.shields.io/badge/arXiv-2312.03275-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2312.03275) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/rai-opensource/vlfm) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://naoki.io/portfolio/vlfm.html) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2312.03275)

- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)**<br>
  2023-07-12 · Reasoning & Planning · Spatial Understanding · Memory & Knowledge<br>
  [![arXiv: 2307.06135](https://img.shields.io/badge/arXiv-2307.06135-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2307.06135) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://sayplan.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2307.06135)

- **[Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153)**<br>
  2023-03-21 · Reasoning & Planning · Spatial Understanding<br>
  [![arXiv: 2303.12153](https://img.shields.io/badge/arXiv-2303.12153-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2303.12153) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://sites.google.com/stanford.edu/text2motion) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2303.12153)

- **[PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)**<br>
  2023-03-06 · Reasoning & Planning · Self-improvement<br>
  [![arXiv: 2303.03378](https://img.shields.io/badge/arXiv-2303.03378-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2303.03378) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://palm-e.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2303.03378)

- **[LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088)**<br>
  2022-12-08 · Reasoning & Planning · Monitoring & Recovery<br>
  [![arXiv: 2212.04088](https://img.shields.io/badge/arXiv-2212.04088-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2212.04088) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OSU-NLP-Group/LLM-Planner/) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://dki-lab.github.io/LLM-Planner/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2212.04088)

- **[Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608)**<br>
  2022-07-12 · Reasoning & Planning · Monitoring & Recovery<br>
  [![arXiv: 2207.05608](https://img.shields.io/badge/arXiv-2207.05608-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2207.05608) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://innermonologue.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2207.05608)

- **[LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429)**<br>
  2022-07-10 · Reasoning & Planning · VLA & World Models<br>
  [![arXiv: 2207.04429](https://img.shields.io/badge/arXiv-2207.04429-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2207.04429) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/blazejosinski/lm_nav) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://sites.google.com/view/lmnav) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2207.04429)

- **[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)**<br>
  2022-04-04 · Reasoning & Planning · VLA & World Models<br>
  [![arXiv: 2204.01691](https://img.shields.io/badge/arXiv-2204.01691-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2204.01691) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://say-can.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2204.01691)

- **[Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents](https://arxiv.org/abs/2201.07207)**<br>
  2022-01-18 · Reasoning & Planning<br>
  [![arXiv: 2201.07207](https://img.shields.io/badge/arXiv-2201.07207-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2201.07207) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://huangwl18.github.io/language-planner) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2201.07207)

### Spatial Understanding

- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)**<br>
  2023-09-28 · Spatial Understanding · Reasoning & Planning · Memory & Knowledge<br>
  [![arXiv: 2309.16650](https://img.shields.io/badge/arXiv-2309.16650-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2309.16650) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/concept-graphs/concept-graphs) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://concept-graphs.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2309.16650)

- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)**<br>
  2023-07-12 · Spatial Understanding · Skills & Code · Reasoning & Planning<br>
  [![arXiv: 2307.05973](https://img.shields.io/badge/arXiv-2307.05973-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2307.05973) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/huangwl18/VoxPoser) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://voxposer.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2307.05973)

- **[ConceptFusion: Open-set Multimodal 3D Mapping](https://arxiv.org/abs/2302.07241)**<br>
  2023-02-14 · Spatial Understanding · Memory & Knowledge<br>
  [![arXiv: 2302.07241](https://img.shields.io/badge/arXiv-2302.07241-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2302.07241) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/concept-fusion/concept-fusion) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://concept-fusion.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2302.07241)

- **[OpenScene: 3D Scene Understanding with Open Vocabularies](https://arxiv.org/abs/2211.15654)**<br>
  2022-11-28 · Spatial Understanding · Self-improvement<br>
  [![arXiv: 2211.15654](https://img.shields.io/badge/arXiv-2211.15654-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2211.15654) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/pengsongyou/openscene) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://pengsongyou.github.io/openscene) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2211.15654)

- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)**<br>
  2022-10-11 · Spatial Understanding · Skills & Code · Reasoning & Planning<br>
  [![arXiv: 2210.05714](https://img.shields.io/badge/arXiv-2210.05714-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2210.05714) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/vlmaps/vlmaps) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://vlmaps.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2210.05714)

### Memory & Knowledge

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)**<br>
  2024-11-23 · Memory & Knowledge · Spatial Understanding · Reasoning & Planning<br>
  [![arXiv: 2411.17735](https://img.shields.io/badge/arXiv-2411.17735-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2411.17735) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/UMass-Embodied-AGI/3D-Mem) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://umass-embodied-agi.github.io/3D-Mem/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2411.17735)

### Skills & Code

- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)**<br>
  2023-10-19 · Skills & Code · Self-improvement · VLA & World Models<br>
  [![arXiv: 2310.12931](https://img.shields.io/badge/arXiv-2310.12931-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2310.12931) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/eureka-research/Eureka) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://eureka-research.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2310.12931)

- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)**<br>
  2023-05-25 · Skills & Code · Memory & Knowledge · Self-improvement<br>
  [![arXiv: 2305.16291](https://img.shields.io/badge/arXiv-2305.16291-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2305.16291) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/MineDojo/Voyager) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://voyager.minedojo.org/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2305.16291)

- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)**<br>
  2022-09-22 · Skills & Code · Reasoning & Planning · Monitoring & Recovery<br>
  [![arXiv: 2209.11302](https://img.shields.io/badge/arXiv-2209.11302-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2209.11302) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/NVlabs/progprompt-vh) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://progprompt.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2209.11302)

- **[Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753)**<br>
  2022-09-16 · Skills & Code · Reasoning & Planning<br>
  [![arXiv: 2209.07753](https://img.shields.io/badge/arXiv-2209.07753-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2209.07753) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://code-as-policies.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2209.07753)

### Monitoring & Recovery

- **[DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329)**<br>
  2023-07-01 · Monitoring & Recovery · Reasoning & Planning<br>
  [![arXiv: 2307.00329](https://img.shields.io/badge/arXiv-2307.00329-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2307.00329) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://sites.google.com/view/doremi-paper/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2307.00329)

### VLA & World Models

- **[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)**<br>
  2024-06-13 · VLA & World Models · Self-improvement<br>
  [![arXiv: 2406.09246](https://img.shields.io/badge/arXiv-2406.09246-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2406.09246) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/openvla/openvla) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://openvla.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2406.09246)

- **[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)**<br>
  2024-05-20 · VLA & World Models · Self-improvement<br>
  [![arXiv: 2405.12213](https://img.shields.io/badge/arXiv-2405.12213-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2405.12213) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/octo-models/octo) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://octo-models.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2405.12213)

- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)**<br>
  2024-01-22 · VLA & World Models · Spatial Understanding · Reasoning & Planning<br>
  [![arXiv: 2401.12202](https://img.shields.io/badge/arXiv-2401.12202-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2401.12202) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/ok-robot/ok-robot) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://ok-robot.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2401.12202)

- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)**<br>
  2023-07-28 · VLA & World Models · Self-improvement<br>
  [![arXiv: 2307.15818](https://img.shields.io/badge/arXiv-2307.15818-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2307.15818) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://robotics-transformer2.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2307.15818)

- **[CLIPort: What and Where Pathways for Robotic Manipulation](https://arxiv.org/abs/2109.12098)**<br>
  2021-09-24 · VLA & World Models · Spatial Understanding<br>
  [![arXiv: 2109.12098](https://img.shields.io/badge/arXiv-2109.12098-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2109.12098) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/cliport/cliport) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://cliport.github.io/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2109.12098)

### Benchmarks & Evaluation

- **[BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation](https://arxiv.org/abs/2403.09227)**<br>
  2024-03-14 · Benchmarks & Evaluation<br>
  [![arXiv: 2403.09227](https://img.shields.io/badge/arXiv-2403.09227-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2403.09227) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/StanfordVL/BEHAVIOR-1K) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://behavior.stanford.edu/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2403.09227)

- **[Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots](https://arxiv.org/abs/2310.13724)**<br>
  2023-10-19 · Benchmarks & Evaluation<br>
  [![arXiv: 2310.13724](https://img.shields.io/badge/arXiv-2310.13724-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2310.13724) [![GitHub source code](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/facebookresearch/habitat-lab) [![Project website](https://img.shields.io/badge/Project-2563EB?style=flat-square)](https://aihabitat.org/habitat3/) [![中文阅读与横竖屏卡片](https://img.shields.io/badge/Reading%20card-0F766E?style=flat-square)](https://hongboduan.github.io/awesome-embodied-agents/#paper=2310.13724)

</details>

<!-- ATLAS:END -->

<details>
<summary>Reading guide and editorial labels</summary>

## Reading map

| Question | Research direction |
| --- | --- |
| How does a model turn a goal into an executable plan? | Reasoning, planning, code and tools |
| How does an agent retain and use observations? | Spatial state, memory and retrieval |
| How does execution adapt to failures? | Monitoring, feedback and recovery |
| What improves through interaction? | In-context learning and self-improvement |
| How do agents work with learned policies? | Agent–VLA/WAM interfaces |
| What does an experiment actually demonstrate? | Benchmarks, protocols and real-robot evidence |

The website includes source-linked reading notes, original paper figures, method comparison, and landscape/portrait cards for reading and sharing. Publication dates refer to the first arXiv submission; revisions are tracked separately.

Opinion essays are labeled separately and do not count as experimental evidence. Official project previews are listed separately from papers. When a release date is unverified, the website labels the collection date instead; project images retain their original source attribution.

## Reading labels

- **Source-checked:** checked against an original abstract or author source; not necessarily a full-paper review.
- **Full review:** a paper-specific reading with evidence and limitations.
- **AI draft:** a machine-assisted reading with page-linked excerpts; still requires editorial verification.
- **Discovery candidate:** automatically discovered metadata; relevance and claims await review.

Automatically extracted illustrations retain their PDF source and page. A page preview is labeled as such. Results from different evaluation protocols are not presented as a common leaderboard.

</details>

## Contributing

Suggestions and corrections are welcome via [Issues](https://github.com/hongboduan/awesome-embodied-agents/issues) or pull requests. Please include the paper link, first publication date, author project/code links when available, and a short explanation of its relevance to embodied agents. See [contribution guidance](CONTRIBUTING.md).

Paper figures and paper content belong to their respective authors. Please cite the original work. BibTeX exports are reading aids; verify complete author names and publication metadata before submission.
