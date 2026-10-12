# Awesome Embodied Agents · 具身 Agent 文献合集

围绕**基础模型驱动的具身 Agent**整理研究工作，关注推理与规划、工具和代码调用、空间记忆、执行反馈与自我改进。

**重点收录 2026 年 9 月以来首次发表的新工作。** 更早的论文放在折叠的背景阅读区；VLA、WAM 论文主要围绕其在 Agent 系统中的作用与对照价值收录。

[浏览论文合集](https://hongboduan.github.io/awesome-embodied-agents/) · [English](README.md) · [推荐论文](https://github.com/hongboduan/awesome-embodied-agents/issues) · [订阅动态](https://hongboduan.github.io/awesome-embodied-agents/feed.xml)

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

官方项目预览与论文分开列出；首发日期未核实的项目明确显示收录日期，项目原图保留来源署名。

## 阅读标记

- **来源核对**：核对过原始摘要或作者资料，不等同于全文审读。
- **全文精读**：有针对该论文的阅读、关键结论依据与边界说明。
- **AI 草稿**：有原文页码和摘录的机器辅助解读，仍待编辑复核。
- **发现候选**：自动发现的元数据，相关性和具体主张待核查。

自动提取的配图保留 PDF 来源和页码；整页预览会明确标注。不同实验协议下的数值不作为统一排行榜。

<!-- ATLAS:START -->

共 308 条 · 精选 40 条（含 1 个项目）· 来源核对 39 条 · 全文核读 1 篇 · AI 草稿 0 篇 · 自动候选 268 篇

## 项目与系统

- **[LoopROS: A Recursively Self-Evolving Robot Operating System for Agentic Manipulation](https://loopmaster.ai/loopros/)** (收录于 2026-10-12) · 项目预览；论文与代码待公开
  前台用历史观察与动作反馈驱动代码执行，后台把失败和修正整理为跨回合 Skills，让操作经验有机会被后续任务复用。

## 近期具身 Agent · 2026-09-01 起

### 推理与规划

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)** (2026-10-08) · [Code](https://github.com/nssmd/RoboRSI) · [Project](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
  把机器人自我改进组织成分层技能工程：定位负责的分支、局部修复、验证后再复用。
- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)** (2026-10-07) · [Code](https://github.com/metacognitionai/NavGPT-3) · [Project](https://metacognitionai.github.io/NavGPT3/)
  让推理、导航执行和监控拥有各自上下文，由运行时分配运动控制权，连接前沿模型与导航 VLA。
- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)** (2026-10-06) · [Project](https://hyunjung00.github.io/emho/)
  冻结具身模型，把执行轨迹变成改进规划、感知工具和失败恢复逻辑的依据。
- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)** (2026-10-05) · [Code](https://github.com/BWR-hhh/rvicl) · [Project](https://bwr-hhh.github.io/rvicl/)
  把一段任务示范变成可按需查询的层级视频记忆，让 Agent 在接触细节需要时再读取短片。
- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)** (2026-10-04) · [Code](https://github.com/robotuse-team/RobotUse) · [Project](https://robotuse-team.github.io/)
  主 Agent 管目标，子 Agent 在图像中选点和姿态，几何后端执行；跨回合经验沉淀到可更新的操作手册。
- **[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854v1)** (2026-10-01)
  用几何、空间关系、可供性、规划和操作五个维度，检查前沿 VLM 的局部优势能否转化为完整任务成功。
- **[LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507v1)** (2026-09-30) · [Code](https://github.com/dzj441/Libero-Agent)
  让通用 Agent 自己选择观测、处理图像和发出原生机器人命令，拆开评估感知、短程动作与长程组合。
- **[RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261v1)** (2026-09-28) · [Code](https://github.com/Mosi-AI/RoboICL)
  给冻结的 GPT-6 Astra 配上示范和交互记忆，用上下文适应机器人任务，无需训练机器人专用策略。
- **[An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170v1)** (2026-09-21)
  系统测试 GPT-6 Astra 直接充当机器人策略的能力，揭示语义泛化与精细动作之间的明显差距。

### 空间理解

- **[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854v1)** (2026-10-01)
  用几何、空间关系、可供性、规划和操作五个维度，检查前沿 VLM 的局部优势能否转化为完整任务成功。

### 记忆与知识

- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026-10-08)
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。
- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)** (2026-10-07) · [Code](https://github.com/metacognitionai/NavGPT-3) · [Project](https://metacognitionai.github.io/NavGPT3/)
  让推理、导航执行和监控拥有各自上下文，由运行时分配运动控制权，连接前沿模型与导航 VLA。
- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)** (2026-10-05) · [Code](https://github.com/BWR-hhh/rvicl) · [Project](https://bwr-hhh.github.io/rvicl/)
  把一段任务示范变成可按需查询的层级视频记忆，让 Agent 在接触细节需要时再读取短片。
- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)** (2026-10-04) · [Code](https://github.com/robotuse-team/RobotUse) · [Project](https://robotuse-team.github.io/)
  主 Agent 管目标，子 Agent 在图像中选点和姿态，几何后端执行；跨回合经验沉淀到可更新的操作手册。
- **[RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261v1)** (2026-09-28) · [Code](https://github.com/Mosi-AI/RoboICL)
  给冻结的 GPT-6 Astra 配上示范和交互记忆，用上下文适应机器人任务，无需训练机器人专用策略。

### 技能与代码

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)** (2026-10-08) · [Code](https://github.com/nssmd/RoboRSI) · [Project](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
  把机器人自我改进组织成分层技能工程：定位负责的分支、局部修复、验证后再复用。
- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026-10-08)
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。
- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)** (2026-10-06) · [Project](https://hyunjung00.github.io/emho/)
  冻结具身模型，把执行轨迹变成改进规划、感知工具和失败恢复逻辑的依据。
- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)** (2026-10-04) · [Code](https://github.com/robotuse-team/RobotUse) · [Project](https://robotuse-team.github.io/)
  主 Agent 管目标，子 Agent 在图像中选点和姿态，几何后端执行；跨回合经验沉淀到可更新的操作手册。

### 监控与恢复

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)** (2026-10-08) · [Code](https://github.com/nssmd/RoboRSI) · [Project](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
  把机器人自我改进组织成分层技能工程：定位负责的分支、局部修复、验证后再复用。
- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026-10-08)
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。
- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)** (2026-10-07) · [Code](https://github.com/metacognitionai/NavGPT-3) · [Project](https://metacognitionai.github.io/NavGPT3/)
  让推理、导航执行和监控拥有各自上下文，由运行时分配运动控制权，连接前沿模型与导航 VLA。
- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)** (2026-10-06) · [Project](https://hyunjung00.github.io/emho/)
  冻结具身模型，把执行轨迹变成改进规划、感知工具和失败恢复逻辑的依据。
- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)** (2026-10-05) · [Code](https://github.com/BWR-hhh/rvicl) · [Project](https://bwr-hhh.github.io/rvicl/)
  把一段任务示范变成可按需查询的层级视频记忆，让 Agent 在接触细节需要时再读取短片。
- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)** (2026-10-04) · [Code](https://github.com/robotuse-team/RobotUse) · [Project](https://robotuse-team.github.io/)
  主 Agent 管目标，子 Agent 在图像中选点和姿态，几何后端执行；跨回合经验沉淀到可更新的操作手册。
- **[LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507v1)** (2026-09-30) · [Code](https://github.com/dzj441/Libero-Agent)
  让通用 Agent 自己选择观测、处理图像和发出原生机器人命令，拆开评估感知、短程动作与长程组合。
- **[RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261v1)** (2026-09-28) · [Code](https://github.com/Mosi-AI/RoboICL)
  给冻结的 GPT-6 Astra 配上示范和交互记忆，用上下文适应机器人任务，无需训练机器人专用策略。

### VLA / WAM

- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)** (2026-10-07) · [Code](https://github.com/metacognitionai/NavGPT-3) · [Project](https://metacognitionai.github.io/NavGPT3/)
  让推理、导航执行和监控拥有各自上下文，由运行时分配运动控制权，连接前沿模型与导航 VLA。
- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)** (2026-10-05) · [Code](https://github.com/BWR-hhh/rvicl) · [Project](https://bwr-hhh.github.io/rvicl/)
  把一段任务示范变成可按需查询的层级视频记忆，让 Agent 在接触细节需要时再读取短片。
- **[An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170v1)** (2026-09-21)
  系统测试 GPT-6 Astra 直接充当机器人策略的能力，揭示语义泛化与精细动作之间的明显差距。

### 自我改进

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)** (2026-10-08) · [Code](https://github.com/nssmd/RoboRSI) · [Project](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
  把机器人自我改进组织成分层技能工程：定位负责的分支、局部修复、验证后再复用。
- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026-10-08)
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。
- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)** (2026-10-06) · [Project](https://hyunjung00.github.io/emho/)
  冻结具身模型，把执行轨迹变成改进规划、感知工具和失败恢复逻辑的依据。

### 基准与评测

- **[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854v1)** (2026-10-01)
  用几何、空间关系、可供性、规划和操作五个维度，检查前沿 VLM 的局部优势能否转化为完整任务成功。
- **[LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507v1)** (2026-09-30) · [Code](https://github.com/dzj441/Libero-Agent)
  让通用 Agent 自己选择观测、处理图像和发出原生机器人命令，拆开评估感知、短程动作与长程组合。
- **[An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170v1)** (2026-09-21)
  系统测试 GPT-6 Astra 直接充当机器人策略的能力，揭示语义泛化与精细动作之间的明显差距。

<details>
<summary>背景阅读与早期工作（展开）</summary>

### 推理与规划

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024-11-23) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
  把探索过程中看到的场景保存为多视角记忆快照，让具身 Agent 在已有记忆和未知区域之间选择下一步。
- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024-10-08) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
  在楼宇尺度下，用视觉语言模型组织导航与操作技能，并利用双层记忆支持长时序任务。
- **[AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963)** (2024-01-23)
  利用视觉语言模型理解场景，再由语言模型给机器人群提出任务，组织多样化的真实数据采集。
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024-01-22) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
  把开放词汇感知、语义记忆、导航和抓取组件组合起来，执行自然语言指定的家庭取放任务。
- **[VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation](https://arxiv.org/abs/2312.03275)** (2023-12-06) · [Code](https://github.com/rai-opensource/vlfm) · [Project](https://naoki.io/portfolio/vlfm.html)
  用视觉语言模型评估哪里更可能找到目标，再选择相应探索前沿。
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023-09-28) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
  把多视角观测组织为开放词汇三维场景图，为语言查询和机器人规划提供显式空间接口。
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023-07-12) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
  语言模型写代码构建三维可供性与约束地图，再由运动规划器生成闭环操作轨迹。
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023-07-12) · [Project](https://sayplan.github.io/)
  在分层三维场景图上检索任务相关区域，再结合路径规划与仿真反馈生成长时序计划。
- **[DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329)** (2023-07-01) · [Project](https://sites.google.com/view/doremi-paper/)
  持续检查执行是否偏离计划，在物体掉落或其他异常出现时及时重规划。
- **[Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153)** (2023-03-21) · [Project](https://sites.google.com/stanford.edu/text2motion)
  在执行前联合检查语义目标与整段技能序列的几何可行性。
- **[PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)** (2023-03-06) · [Project](https://palm-e.github.io/)
  把图像、连续状态和文本联合输入语言模型，使它能够进行具身任务规划与多模态推理。
- **[LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088)** (2022-12-08) · [Code](https://github.com/OSU-NLP-Group/LLM-Planner/) · [Project](https://dki-lab.github.io/LLM-Planner/)
  利用少量示例和当前观测进行高层规划，并根据已完成子目标和可见物体更新计划。
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022-10-11) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
  把视觉语言特征写入三维地图，再把自然语言指令转成具有空间位置的导航目标。
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022-09-22) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
  把可用动作、环境对象和示例计划写成程序式提示，让语言模型生成带前置条件检查的任务程序。
- **[Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753)** (2022-09-16) · [Project](https://code-as-policies.github.io/)
  把语言指令转换为调用感知和控制接口的程序，用代码表达几何计算、分支和反馈控制。
- **[Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608)** (2022-07-12) · [Project](https://innermonologue.github.io/)
  把成功检测、场景描述和人类反馈写进语言上下文，让高层计划随执行结果更新。
- **[LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429)** (2022-07-10) · [Code](https://github.com/blazejosinski/lm_nav) · [Project](https://sites.google.com/view/lmnav)
  组合现成的语言、图文和导航模型，让移动机器人根据自然语言完成户外长程导航。
- **[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)** (2022-04-04) · [Project](https://say-can.github.io/)
  让语言模型判断下一步是否符合指令，再用技能价值函数判断机器人在当前环境中能否完成。
- **[Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents](https://arxiv.org/abs/2201.07207)** (2022-01-18) · [Project](https://huangwl18.github.io/language-planner)
  研究语言模型能否拆解高层任务，再把生成步骤映射到环境允许执行的动作。

### 空间理解

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024-11-23) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
  把探索过程中看到的场景保存为多视角记忆快照，让具身 Agent 在已有记忆和未知区域之间选择下一步。
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024-01-22) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
  把开放词汇感知、语义记忆、导航和抓取组件组合起来，执行自然语言指定的家庭取放任务。
- **[VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation](https://arxiv.org/abs/2312.03275)** (2023-12-06) · [Code](https://github.com/rai-opensource/vlfm) · [Project](https://naoki.io/portfolio/vlfm.html)
  用视觉语言模型评估哪里更可能找到目标，再选择相应探索前沿。
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023-09-28) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
  把多视角观测组织为开放词汇三维场景图，为语言查询和机器人规划提供显式空间接口。
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023-07-12) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
  语言模型写代码构建三维可供性与约束地图，再由运动规划器生成闭环操作轨迹。
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023-07-12) · [Project](https://sayplan.github.io/)
  在分层三维场景图上检索任务相关区域，再结合路径规划与仿真反馈生成长时序计划。
- **[Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153)** (2023-03-21) · [Project](https://sites.google.com/stanford.edu/text2motion)
  在执行前联合检查语义目标与整段技能序列的几何可行性。
- **[ConceptFusion: Open-set Multimodal 3D Mapping](https://arxiv.org/abs/2302.07241)** (2023-02-14) · [Code](https://github.com/concept-fusion/concept-fusion) · [Project](https://concept-fusion.github.io/)
  把基础模型的开放集合特征融合进三维地图，让语言、图像、音频和几何查询共享空间表示。
- **[OpenScene: 3D Scene Understanding with Open Vocabularies](https://arxiv.org/abs/2211.15654)** (2022-11-28) · [Code](https://github.com/pengsongyou/openscene) · [Project](https://pengsongyou.github.io/openscene)
  将三维点特征与语言、图像嵌入对齐，支持不预先固定类别的三维场景查询。
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022-10-11) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
  把视觉语言特征写入三维地图，再把自然语言指令转成具有空间位置的导航目标。
- **[CLIPort: What and Where Pathways for Robotic Manipulation](https://arxiv.org/abs/2109.12098)** (2021-09-24) · [Code](https://github.com/cliport/cliport) · [Project](https://cliport.github.io/)
  把 CLIP 的语义特征与 Transporter 的空间结构结合，学习语言条件的桌面操作策略。

### 记忆与知识

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024-11-23) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
  把探索过程中看到的场景保存为多视角记忆快照，让具身 Agent 在已有记忆和未知区域之间选择下一步。
- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024-10-08) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
  在楼宇尺度下，用视觉语言模型组织导航与操作技能，并利用双层记忆支持长时序任务。
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023-09-28) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
  把多视角观测组织为开放词汇三维场景图，为语言查询和机器人规划提供显式空间接口。
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023-07-12) · [Project](https://sayplan.github.io/)
  在分层三维场景图上检索任务相关区域，再结合路径规划与仿真反馈生成长时序计划。
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023-05-25) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
  在 Minecraft 中自动提出探索任务，生成并修复代码，把成功行为积累为可检索的技能库。
- **[ConceptFusion: Open-set Multimodal 3D Mapping](https://arxiv.org/abs/2302.07241)** (2023-02-14) · [Code](https://github.com/concept-fusion/concept-fusion) · [Project](https://concept-fusion.github.io/)
  把基础模型的开放集合特征融合进三维地图，让语言、图像、音频和几何查询共享空间表示。

### 技能与代码

- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023-10-19) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
  由语言模型生成奖励函数代码，再用强化学习训练结果作为反馈，迭代改进奖励。
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023-07-12) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
  语言模型写代码构建三维可供性与约束地图，再由运动规划器生成闭环操作轨迹。
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023-05-25) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
  在 Minecraft 中自动提出探索任务，生成并修复代码，把成功行为积累为可检索的技能库。
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022-10-11) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
  把视觉语言特征写入三维地图，再把自然语言指令转成具有空间位置的导航目标。
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022-09-22) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
  把可用动作、环境对象和示例计划写成程序式提示，让语言模型生成带前置条件检查的任务程序。
- **[Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753)** (2022-09-16) · [Project](https://code-as-policies.github.io/)
  把语言指令转换为调用感知和控制接口的程序，用代码表达几何计算、分支和反馈控制。

### 监控与恢复

- **[DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329)** (2023-07-01) · [Project](https://sites.google.com/view/doremi-paper/)
  持续检查执行是否偏离计划，在物体掉落或其他异常出现时及时重规划。
- **[LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088)** (2022-12-08) · [Code](https://github.com/OSU-NLP-Group/LLM-Planner/) · [Project](https://dki-lab.github.io/LLM-Planner/)
  利用少量示例和当前观测进行高层规划，并根据已完成子目标和可见物体更新计划。
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022-09-22) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
  把可用动作、环境对象和示例计划写成程序式提示，让语言模型生成带前置条件检查的任务程序。
- **[Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608)** (2022-07-12) · [Project](https://innermonologue.github.io/)
  把成功检测、场景描述和人类反馈写进语言上下文，让高层计划随执行结果更新。

### VLA / WAM

- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024-10-08) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
  在楼宇尺度下，用视觉语言模型组织导航与操作技能，并利用双层记忆支持长时序任务。
- **[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)** (2024-06-13) · [Code](https://github.com/openvla/openvla) · [Project](https://openvla.github.io/)
  提供可训练、可微调的视觉语言动作模型，将图像与语言指令映射为机器人控制动作。
- **[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)** (2024-05-20) · [Code](https://github.com/octo-models/octo) · [Project](https://octo-models.github.io/)
  提供通用机器人策略初始化，支持用少量目标数据适配新的观测输入和动作空间。
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024-01-22) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
  把开放词汇感知、语义记忆、导航和抓取组件组合起来，执行自然语言指定的家庭取放任务。
- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023-10-19) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
  由语言模型生成奖励函数代码，再用强化学习训练结果作为反馈，迭代改进奖励。
- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)** (2023-07-28) · [Project](https://robotics-transformer2.github.io/)
  把机器人动作写成与文本兼容的符号，使视觉语言模型直接学习控制并利用网络知识。
- **[LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429)** (2022-07-10) · [Code](https://github.com/blazejosinski/lm_nav) · [Project](https://sites.google.com/view/lmnav)
  组合现成的语言、图文和导航模型，让移动机器人根据自然语言完成户外长程导航。
- **[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)** (2022-04-04) · [Project](https://say-can.github.io/)
  让语言模型判断下一步是否符合指令，再用技能价值函数判断机器人在当前环境中能否完成。
- **[CLIPort: What and Where Pathways for Robotic Manipulation](https://arxiv.org/abs/2109.12098)** (2021-09-24) · [Code](https://github.com/cliport/cliport) · [Project](https://cliport.github.io/)
  把 CLIP 的语义特征与 Transporter 的空间结构结合，学习语言条件的桌面操作策略。

### 自我改进

- **[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)** (2024-06-13) · [Code](https://github.com/openvla/openvla) · [Project](https://openvla.github.io/)
  提供可训练、可微调的视觉语言动作模型，将图像与语言指令映射为机器人控制动作。
- **[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)** (2024-05-20) · [Code](https://github.com/octo-models/octo) · [Project](https://octo-models.github.io/)
  提供通用机器人策略初始化，支持用少量目标数据适配新的观测输入和动作空间。
- **[AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963)** (2024-01-23)
  利用视觉语言模型理解场景，再由语言模型给机器人群提出任务，组织多样化的真实数据采集。
- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023-10-19) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
  由语言模型生成奖励函数代码，再用强化学习训练结果作为反馈，迭代改进奖励。
- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)** (2023-07-28) · [Project](https://robotics-transformer2.github.io/)
  把机器人动作写成与文本兼容的符号，使视觉语言模型直接学习控制并利用网络知识。
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023-05-25) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
  在 Minecraft 中自动提出探索任务，生成并修复代码，把成功行为积累为可检索的技能库。
- **[PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)** (2023-03-06) · [Project](https://palm-e.github.io/)
  把图像、连续状态和文本联合输入语言模型，使它能够进行具身任务规划与多模态推理。
- **[OpenScene: 3D Scene Understanding with Open Vocabularies](https://arxiv.org/abs/2211.15654)** (2022-11-28) · [Code](https://github.com/pengsongyou/openscene) · [Project](https://pengsongyou.github.io/openscene)
  将三维点特征与语言、图像嵌入对齐，支持不预先固定类别的三维场景查询。

### 基准与评测

- **[BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation](https://arxiv.org/abs/2403.09227)** (2024-03-14) · [Code](https://github.com/StanfordVL/BEHAVIOR-1K) · [Project](https://behavior.stanford.edu/)
  以日常生活活动为目标，提供需要长时序决策与复杂交互的具身任务及仿真环境。
- **[Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots](https://arxiv.org/abs/2310.13724)** (2023-10-19) · [Code](https://github.com/facebookresearch/habitat-lab) · [Project](https://aihabitat.org/habitat3/)
  面向人与机器人共同生活的场景，提供人形角色、人在环交互和协作任务仿真。

</details>

<!-- ATLAS:END -->

## 推荐与纠错

欢迎通过 [Issues](https://github.com/hongboduan/awesome-embodied-agents/issues) 或 Pull Request 推荐论文、补充代码链接和纠正解读。请提供论文链接、首次发表日期、作者项目/代码链接，以及与具身 Agent 的关联。详见[贡献说明](CONTRIBUTING.md)。

论文图片与内容归原作者所有，请引用原始工作。BibTeX 用于辅助整理，正式投稿前请核对完整作者与发表信息。
