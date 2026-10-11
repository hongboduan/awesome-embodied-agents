# Embodied Agent Atlas · 具身智能体研究地图

一份以来源为依据的 **Awesome 清单 + 论文阅读网站 + 横竖屏卡片工作台**。围绕空间理解、记忆、规划、技能调用、执行恢复和自我改进组织研究工作。

[论文网站](https://hongboduan.github.io/awesome-embodied-agents/) · [更新运行记录](https://github.com/hongboduan/awesome-embodied-agents/actions) · [English](README.md) · [启用自动更新](docs/setup.md) · [贡献指南](CONTRIBUTING.md)

## 已实现

- 精选论文库、能力标签、检索、论文详情与方法对比。
- 同一份论文内容生成 16:9 横版与 3:4 竖版传播卡片，支持 PNG 导出。
- arXiv 分页发现、基础标识符去重、版本变化记录、七天重叠增量更新。
- 每天北京时间 08:17 的 GitHub Actions 工作流，以及手动更新。
- 自动生成 Awesome 清单、JSON、BibTeX 和 RSS。

**仓库已配置源码推送触发、每日北京时间 08:17 与手动更新。** GitHub Pages 首次发布需要在仓库设置中选择 GitHub Actions；论文更新独立运行。 页面明确显示待启用、最近成功抓取或抓取失败状态，不把构建日期当成抓取成功日期。

## 本地预览

需要 Python 3.10+，构建与更新脚本无需安装第三方库。

```bash
python -m unittest discover -s tests -v
python scripts/build.py
python -m http.server 8000 --directory dist
```

浏览器打开 `http://localhost:8000`。实际抓取时运行 `python scripts/update.py`，再构建一次即可。

## 内容与自动化边界

自动程序只产生**待审核候选**，原始英文摘要单独保存。候选不会自动变成中文精读或精选；角色分工、实验结果、局限和代码状态需要编辑核查。无需配置大模型 API Key，此版本没有隐藏的模型调用或模拟翻译。

- `source-checked`：查阅过原始摘要或作者项目页；不代表全文审读。
- `full-review`：有全文阅读、关键结论依据和局限说明。
- `candidate`：自动发现，分类与内容尚待人工审核。

新版论文只更新来源版本记录，不覆盖已经写好的中文解读。失败时保留原有数据并显示失败状态。代码是否发布由人工核查；本版尚不自动监控 GitHub Release、权重或数据上线。

## 精选论文

以下区块由脚本生成。同一论文可属于多个能力分类；不对不同协议下的结果做统一排名。

<!-- ATLAS:START -->

共 144 篇 · 精选 30 篇 · 来源核对 29 篇 · 全文核读 1 篇 · 自动候选 114 篇

### 推理与规划

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
  把探索过程中看到的场景保存为多视角记忆快照，让具身 Agent 在已有记忆和未知区域之间选择下一步。
- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
  在楼宇尺度下，用视觉语言模型组织导航与操作技能，并利用双层记忆支持长时序任务。
- **[AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963)** (2024)
  利用视觉语言模型理解场景，再由语言模型给机器人群提出任务，组织多样化的真实数据采集。
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
  把开放词汇感知、语义记忆、导航和抓取组件组合起来，执行自然语言指定的家庭取放任务。
- **[VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation](https://arxiv.org/abs/2312.03275)** (2023) · [Code](https://github.com/rai-opensource/vlfm) · [Project](https://naoki.io/portfolio/vlfm.html)
  用视觉语言模型评估哪里更可能找到目标，再选择相应探索前沿。
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
  把多视角观测组织为开放词汇三维场景图，为语言查询和机器人规划提供显式空间接口。
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
  语言模型写代码构建三维可供性与约束地图，再由运动规划器生成闭环操作轨迹。
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023) · [Project](https://sayplan.github.io/)
  在分层三维场景图上检索任务相关区域，再结合路径规划与仿真反馈生成长时序计划。
- **[DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329)** (2023) · [Project](https://sites.google.com/view/doremi-paper/)
  持续检查执行是否偏离计划，在物体掉落或其他异常出现时及时重规划。
- **[Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153)** (2023) · [Project](https://sites.google.com/stanford.edu/text2motion)
  在执行前联合检查语义目标与整段技能序列的几何可行性。
- **[PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)** (2023) · [Project](https://palm-e.github.io/)
  把图像、连续状态和文本联合输入语言模型，使它能够进行具身任务规划与多模态推理。
- **[LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088)** (2022) · [Code](https://github.com/OSU-NLP-Group/LLM-Planner/) · [Project](https://dki-lab.github.io/LLM-Planner/)
  利用少量示例和当前观测进行高层规划，并根据已完成子目标和可见物体更新计划。
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
  把视觉语言特征写入三维地图，再把自然语言指令转成具有空间位置的导航目标。
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
  把可用动作、环境对象和示例计划写成程序式提示，让语言模型生成带前置条件检查的任务程序。
- **[Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753)** (2022) · [Project](https://code-as-policies.github.io/)
  把语言指令转换为调用感知和控制接口的程序，用代码表达几何计算、分支和反馈控制。
- **[Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608)** (2022) · [Project](https://innermonologue.github.io/)
  把成功检测、场景描述和人类反馈写进语言上下文，让高层计划随执行结果更新。
- **[LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429)** (2022) · [Code](https://github.com/blazejosinski/lm_nav) · [Project](https://sites.google.com/view/lmnav)
  组合现成的语言、图文和导航模型，让移动机器人根据自然语言完成户外长程导航。
- **[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)** (2022) · [Project](https://say-can.github.io/)
  让语言模型判断下一步是否符合指令，再用技能价值函数判断机器人在当前环境中能否完成。
- **[Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents](https://arxiv.org/abs/2201.07207)** (2022) · [Project](https://huangwl18.github.io/language-planner)
  研究语言模型能否拆解高层任务，再把生成步骤映射到环境允许执行的动作。

### 空间理解

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
  把探索过程中看到的场景保存为多视角记忆快照，让具身 Agent 在已有记忆和未知区域之间选择下一步。
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
  把开放词汇感知、语义记忆、导航和抓取组件组合起来，执行自然语言指定的家庭取放任务。
- **[VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation](https://arxiv.org/abs/2312.03275)** (2023) · [Code](https://github.com/rai-opensource/vlfm) · [Project](https://naoki.io/portfolio/vlfm.html)
  用视觉语言模型评估哪里更可能找到目标，再选择相应探索前沿。
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
  把多视角观测组织为开放词汇三维场景图，为语言查询和机器人规划提供显式空间接口。
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
  语言模型写代码构建三维可供性与约束地图，再由运动规划器生成闭环操作轨迹。
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023) · [Project](https://sayplan.github.io/)
  在分层三维场景图上检索任务相关区域，再结合路径规划与仿真反馈生成长时序计划。
- **[Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153)** (2023) · [Project](https://sites.google.com/stanford.edu/text2motion)
  在执行前联合检查语义目标与整段技能序列的几何可行性。
- **[ConceptFusion: Open-set Multimodal 3D Mapping](https://arxiv.org/abs/2302.07241)** (2023) · [Code](https://github.com/concept-fusion/concept-fusion) · [Project](https://concept-fusion.github.io/)
  把基础模型的开放集合特征融合进三维地图，让语言、图像、音频和几何查询共享空间表示。
- **[OpenScene: 3D Scene Understanding with Open Vocabularies](https://arxiv.org/abs/2211.15654)** (2022) · [Code](https://github.com/pengsongyou/openscene) · [Project](https://pengsongyou.github.io/openscene)
  将三维点特征与语言、图像嵌入对齐，支持不预先固定类别的三维场景查询。
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
  把视觉语言特征写入三维地图，再把自然语言指令转成具有空间位置的导航目标。
- **[CLIPort: What and Where Pathways for Robotic Manipulation](https://arxiv.org/abs/2109.12098)** (2021) · [Code](https://github.com/cliport/cliport) · [Project](https://cliport.github.io/)
  把 CLIP 的语义特征与 Transporter 的空间结构结合，学习语言条件的桌面操作策略。

### 记忆与知识

- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026)
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。
- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
  把探索过程中看到的场景保存为多视角记忆快照，让具身 Agent 在已有记忆和未知区域之间选择下一步。
- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
  在楼宇尺度下，用视觉语言模型组织导航与操作技能，并利用双层记忆支持长时序任务。
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
  把多视角观测组织为开放词汇三维场景图，为语言查询和机器人规划提供显式空间接口。
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023) · [Project](https://sayplan.github.io/)
  在分层三维场景图上检索任务相关区域，再结合路径规划与仿真反馈生成长时序计划。
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
  在 Minecraft 中自动提出探索任务，生成并修复代码，把成功行为积累为可检索的技能库。
- **[ConceptFusion: Open-set Multimodal 3D Mapping](https://arxiv.org/abs/2302.07241)** (2023) · [Code](https://github.com/concept-fusion/concept-fusion) · [Project](https://concept-fusion.github.io/)
  把基础模型的开放集合特征融合进三维地图，让语言、图像、音频和几何查询共享空间表示。

### 技能与代码

- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026)
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。
- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
  由语言模型生成奖励函数代码，再用强化学习训练结果作为反馈，迭代改进奖励。
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
  语言模型写代码构建三维可供性与约束地图，再由运动规划器生成闭环操作轨迹。
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
  在 Minecraft 中自动提出探索任务，生成并修复代码，把成功行为积累为可检索的技能库。
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
  把视觉语言特征写入三维地图，再把自然语言指令转成具有空间位置的导航目标。
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
  把可用动作、环境对象和示例计划写成程序式提示，让语言模型生成带前置条件检查的任务程序。
- **[Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753)** (2022) · [Project](https://code-as-policies.github.io/)
  把语言指令转换为调用感知和控制接口的程序，用代码表达几何计算、分支和反馈控制。

### 监控与恢复

- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026)
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。
- **[DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329)** (2023) · [Project](https://sites.google.com/view/doremi-paper/)
  持续检查执行是否偏离计划，在物体掉落或其他异常出现时及时重规划。
- **[LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088)** (2022) · [Code](https://github.com/OSU-NLP-Group/LLM-Planner/) · [Project](https://dki-lab.github.io/LLM-Planner/)
  利用少量示例和当前观测进行高层规划，并根据已完成子目标和可见物体更新计划。
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
  把可用动作、环境对象和示例计划写成程序式提示，让语言模型生成带前置条件检查的任务程序。
- **[Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608)** (2022) · [Project](https://innermonologue.github.io/)
  把成功检测、场景描述和人类反馈写进语言上下文，让高层计划随执行结果更新。

### VLA / WAM

- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
  在楼宇尺度下，用视觉语言模型组织导航与操作技能，并利用双层记忆支持长时序任务。
- **[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)** (2024) · [Code](https://github.com/openvla/openvla) · [Project](https://openvla.github.io/)
  提供可训练、可微调的视觉语言动作模型，将图像与语言指令映射为机器人控制动作。
- **[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)** (2024) · [Code](https://github.com/octo-models/octo) · [Project](https://octo-models.github.io/)
  提供通用机器人策略初始化，支持用少量目标数据适配新的观测输入和动作空间。
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
  把开放词汇感知、语义记忆、导航和抓取组件组合起来，执行自然语言指定的家庭取放任务。
- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
  由语言模型生成奖励函数代码，再用强化学习训练结果作为反馈，迭代改进奖励。
- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)** (2023) · [Project](https://robotics-transformer2.github.io/)
  把机器人动作写成与文本兼容的符号，使视觉语言模型直接学习控制并利用网络知识。
- **[LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429)** (2022) · [Code](https://github.com/blazejosinski/lm_nav) · [Project](https://sites.google.com/view/lmnav)
  组合现成的语言、图文和导航模型，让移动机器人根据自然语言完成户外长程导航。
- **[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)** (2022) · [Project](https://say-can.github.io/)
  让语言模型判断下一步是否符合指令，再用技能价值函数判断机器人在当前环境中能否完成。
- **[CLIPort: What and Where Pathways for Robotic Manipulation](https://arxiv.org/abs/2109.12098)** (2021) · [Code](https://github.com/cliport/cliport) · [Project](https://cliport.github.io/)
  把 CLIP 的语义特征与 Transporter 的空间结构结合，学习语言条件的桌面操作策略。

### 自我改进

- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026)
  让编码智能体离线改进策略库，机器人执行时只运行固定代码，以显式状态连接感知、决策和恢复。
- **[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)** (2024) · [Code](https://github.com/openvla/openvla) · [Project](https://openvla.github.io/)
  提供可训练、可微调的视觉语言动作模型，将图像与语言指令映射为机器人控制动作。
- **[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)** (2024) · [Code](https://github.com/octo-models/octo) · [Project](https://octo-models.github.io/)
  提供通用机器人策略初始化，支持用少量目标数据适配新的观测输入和动作空间。
- **[AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963)** (2024)
  利用视觉语言模型理解场景，再由语言模型给机器人群提出任务，组织多样化的真实数据采集。
- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
  由语言模型生成奖励函数代码，再用强化学习训练结果作为反馈，迭代改进奖励。
- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)** (2023) · [Project](https://robotics-transformer2.github.io/)
  把机器人动作写成与文本兼容的符号，使视觉语言模型直接学习控制并利用网络知识。
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
  在 Minecraft 中自动提出探索任务，生成并修复代码，把成功行为积累为可检索的技能库。
- **[PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)** (2023) · [Project](https://palm-e.github.io/)
  把图像、连续状态和文本联合输入语言模型，使它能够进行具身任务规划与多模态推理。
- **[OpenScene: 3D Scene Understanding with Open Vocabularies](https://arxiv.org/abs/2211.15654)** (2022) · [Code](https://github.com/pengsongyou/openscene) · [Project](https://pengsongyou.github.io/openscene)
  将三维点特征与语言、图像嵌入对齐，支持不预先固定类别的三维场景查询。

### 基准与评测

- **[BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation](https://arxiv.org/abs/2403.09227)** (2024) · [Code](https://github.com/StanfordVL/BEHAVIOR-1K) · [Project](https://behavior.stanford.edu/)
  以日常生活活动为目标，提供需要长时序决策与复杂交互的具身任务及仿真环境。
- **[Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots](https://arxiv.org/abs/2310.13724)** (2023) · [Code](https://github.com/facebookresearch/habitat-lab) · [Project](https://aihabitat.org/habitat3/)
  面向人与机器人共同生活的场景，提供人形角色、人在环交互和协作任务仿真。

<!-- ATLAS:END -->

## 维护方式

在 `data/seed-*.json` 添加或编辑已核查论文，运行 `python scripts/build.py`；可用 `data/seed-community.json` 接收社区贡献。自动候选位于 `data/candidates.json`，可核查后移入 seed 文件。详情见 [贡献指南](CONTRIBUTING.md)。

所有论文与作者素材归原作者所有；本站提供来源链接。BibTeX 是便捷元数据导出，正式投稿前应核对完整作者列表及最终发表信息。卡片中的编辑提示与论文原文结论应明确区分。
