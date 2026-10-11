# Awesome Embodied Agents

A curated reading list on **foundation-model-driven embodied agents**: reasoning, planning, tool use, spatial memory, execution feedback, and self-improvement.

**Focus: papers first published from September 2026 onward.** Earlier papers are kept in a collapsed background-reading section. VLA and world-model work is included when it contributes to an agent system or provides a meaningful comparison.

[Read the paper collection](https://hongboduan.github.io/awesome-embodied-agents/) · [简体中文](README.zh-CN.md) · [Suggest a paper](https://github.com/hongboduan/awesome-embodied-agents/issues) · [RSS](https://hongboduan.github.io/awesome-embodied-agents/feed.xml)

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

## Reading labels

- **Source-checked:** checked against an original abstract or author source; not necessarily a full-paper review.
- **Full review:** a paper-specific reading with evidence and limitations.
- **AI draft:** a machine-assisted reading with page-linked excerpts; still requires editorial verification.
- **Discovery candidate:** automatically discovered metadata; relevance and claims await review.

Automatically extracted illustrations retain their PDF source and page. A page preview is labeled as such. Results from different evaluation protocols are not presented as a common leaderboard.

<!-- ATLAS:START -->

299 papers · 39 curated · 38 source-checked · 1 full-review · 0 AI drafts · 260 discovery candidates

## Recent embodied agents · since 2026-09-01

### Reasoning & Planning

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)** (2026-10-08) · [Code](https://github.com/nssmd/RoboRSI) · [Project](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)** (2026-10-07) · [Code](https://github.com/metacognitionai/NavGPT-3) · [Project](https://metacognitionai.github.io/NavGPT3/)
- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)** (2026-10-06) · [Project](https://hyunjung00.github.io/emho/)
- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)** (2026-10-05) · [Code](https://github.com/BWR-hhh/rvicl) · [Project](https://bwr-hhh.github.io/rvicl/)
- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)** (2026-10-04) · [Code](https://github.com/robotuse-team/RobotUse) · [Project](https://robotuse-team.github.io/)
- **[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854v1)** (2026-10-01)
- **[LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507v1)** (2026-09-30) · [Code](https://github.com/dzj441/Libero-Agent)
- **[RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261v1)** (2026-09-28) · [Code](https://github.com/Mosi-AI/RoboICL)
- **[An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170v1)** (2026-09-21)

### Spatial Understanding

- **[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854v1)** (2026-10-01)

### Memory & Knowledge

- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026-10-08)
- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)** (2026-10-07) · [Code](https://github.com/metacognitionai/NavGPT-3) · [Project](https://metacognitionai.github.io/NavGPT3/)
- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)** (2026-10-05) · [Code](https://github.com/BWR-hhh/rvicl) · [Project](https://bwr-hhh.github.io/rvicl/)
- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)** (2026-10-04) · [Code](https://github.com/robotuse-team/RobotUse) · [Project](https://robotuse-team.github.io/)
- **[RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261v1)** (2026-09-28) · [Code](https://github.com/Mosi-AI/RoboICL)

### Skills & Code

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)** (2026-10-08) · [Code](https://github.com/nssmd/RoboRSI) · [Project](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026-10-08)
- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)** (2026-10-06) · [Project](https://hyunjung00.github.io/emho/)
- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)** (2026-10-04) · [Code](https://github.com/robotuse-team/RobotUse) · [Project](https://robotuse-team.github.io/)

### Monitoring & Recovery

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)** (2026-10-08) · [Code](https://github.com/nssmd/RoboRSI) · [Project](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026-10-08)
- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)** (2026-10-07) · [Code](https://github.com/metacognitionai/NavGPT-3) · [Project](https://metacognitionai.github.io/NavGPT3/)
- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)** (2026-10-06) · [Project](https://hyunjung00.github.io/emho/)
- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)** (2026-10-05) · [Code](https://github.com/BWR-hhh/rvicl) · [Project](https://bwr-hhh.github.io/rvicl/)
- **[RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929v1)** (2026-10-04) · [Code](https://github.com/robotuse-team/RobotUse) · [Project](https://robotuse-team.github.io/)
- **[LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507v1)** (2026-09-30) · [Code](https://github.com/dzj441/Libero-Agent)
- **[RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261v1)** (2026-09-28) · [Code](https://github.com/Mosi-AI/RoboICL)

### VLA & World Models

- **[NavGPT-3: Harnessing Context in a Hierarchical Navigation Runtime](https://arxiv.org/abs/2610.10787v1)** (2026-10-07) · [Code](https://github.com/metacognitionai/NavGPT-3) · [Project](https://metacognitionai.github.io/NavGPT3/)
- **[Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843v1)** (2026-10-05) · [Code](https://github.com/BWR-hhh/rvicl) · [Project](https://bwr-hhh.github.io/rvicl/)
- **[An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170v1)** (2026-09-21)

### Self-improvement

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424v1)** (2026-10-08) · [Code](https://github.com/nssmd/RoboRSI) · [Project](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
- **[Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369v1)** (2026-10-08)
- **[EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432v1)** (2026-10-06) · [Project](https://hyunjung00.github.io/emho/)

### Benchmarks & Evaluation

- **[Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854v1)** (2026-10-01)
- **[LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507v1)** (2026-09-30) · [Code](https://github.com/dzj441/Libero-Agent)
- **[An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170v1)** (2026-09-21)

<details>
<summary>Foundations and earlier work</summary>

### Reasoning & Planning

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024-11-23) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024-10-08) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
- **[AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963)** (2024-01-23)
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024-01-22) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
- **[VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation](https://arxiv.org/abs/2312.03275)** (2023-12-06) · [Code](https://github.com/rai-opensource/vlfm) · [Project](https://naoki.io/portfolio/vlfm.html)
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023-09-28) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023-07-12) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023-07-12) · [Project](https://sayplan.github.io/)
- **[DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329)** (2023-07-01) · [Project](https://sites.google.com/view/doremi-paper/)
- **[Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153)** (2023-03-21) · [Project](https://sites.google.com/stanford.edu/text2motion)
- **[PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)** (2023-03-06) · [Project](https://palm-e.github.io/)
- **[LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088)** (2022-12-08) · [Code](https://github.com/OSU-NLP-Group/LLM-Planner/) · [Project](https://dki-lab.github.io/LLM-Planner/)
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022-10-11) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022-09-22) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
- **[Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753)** (2022-09-16) · [Project](https://code-as-policies.github.io/)
- **[Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608)** (2022-07-12) · [Project](https://innermonologue.github.io/)
- **[LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429)** (2022-07-10) · [Code](https://github.com/blazejosinski/lm_nav) · [Project](https://sites.google.com/view/lmnav)
- **[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)** (2022-04-04) · [Project](https://say-can.github.io/)
- **[Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents](https://arxiv.org/abs/2201.07207)** (2022-01-18) · [Project](https://huangwl18.github.io/language-planner)

### Spatial Understanding

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024-11-23) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024-01-22) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
- **[VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation](https://arxiv.org/abs/2312.03275)** (2023-12-06) · [Code](https://github.com/rai-opensource/vlfm) · [Project](https://naoki.io/portfolio/vlfm.html)
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023-09-28) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023-07-12) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023-07-12) · [Project](https://sayplan.github.io/)
- **[Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153)** (2023-03-21) · [Project](https://sites.google.com/stanford.edu/text2motion)
- **[ConceptFusion: Open-set Multimodal 3D Mapping](https://arxiv.org/abs/2302.07241)** (2023-02-14) · [Code](https://github.com/concept-fusion/concept-fusion) · [Project](https://concept-fusion.github.io/)
- **[OpenScene: 3D Scene Understanding with Open Vocabularies](https://arxiv.org/abs/2211.15654)** (2022-11-28) · [Code](https://github.com/pengsongyou/openscene) · [Project](https://pengsongyou.github.io/openscene)
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022-10-11) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
- **[CLIPort: What and Where Pathways for Robotic Manipulation](https://arxiv.org/abs/2109.12098)** (2021-09-24) · [Code](https://github.com/cliport/cliport) · [Project](https://cliport.github.io/)

### Memory & Knowledge

- **[3D-Mem: 3D Scene Memory for Embodied Exploration and Reasoning](https://arxiv.org/abs/2411.17735)** (2024-11-23) · [Code](https://github.com/UMass-Embodied-AGI/3D-Mem) · [Project](https://umass-embodied-agi.github.io/3D-Mem/)
- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024-10-08) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
- **[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](https://arxiv.org/abs/2309.16650)** (2023-09-28) · [Code](https://github.com/concept-graphs/concept-graphs) · [Project](https://concept-graphs.github.io/)
- **[SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135)** (2023-07-12) · [Project](https://sayplan.github.io/)
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023-05-25) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
- **[ConceptFusion: Open-set Multimodal 3D Mapping](https://arxiv.org/abs/2302.07241)** (2023-02-14) · [Code](https://github.com/concept-fusion/concept-fusion) · [Project](https://concept-fusion.github.io/)

### Skills & Code

- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023-10-19) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
- **[VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973)** (2023-07-12) · [Code](https://github.com/huangwl18/VoxPoser) · [Project](https://voxposer.github.io/)
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023-05-25) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
- **[Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714)** (2022-10-11) · [Code](https://github.com/vlmaps/vlmaps) · [Project](https://vlmaps.github.io/)
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022-09-22) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
- **[Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753)** (2022-09-16) · [Project](https://code-as-policies.github.io/)

### Monitoring & Recovery

- **[DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329)** (2023-07-01) · [Project](https://sites.google.com/view/doremi-paper/)
- **[LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088)** (2022-12-08) · [Code](https://github.com/OSU-NLP-Group/LLM-Planner/) · [Project](https://dki-lab.github.io/LLM-Planner/)
- **[ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302)** (2022-09-22) · [Code](https://github.com/NVlabs/progprompt-vh) · [Project](https://progprompt.github.io/)
- **[Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608)** (2022-07-12) · [Project](https://innermonologue.github.io/)

### VLA & World Models

- **[BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237)** (2024-10-08) · [Code](https://github.com/UT-Austin-RobIn/BUMBLE) · [Project](https://robin-lab.cs.utexas.edu/BUMBLE/)
- **[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)** (2024-06-13) · [Code](https://github.com/openvla/openvla) · [Project](https://openvla.github.io/)
- **[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)** (2024-05-20) · [Code](https://github.com/octo-models/octo) · [Project](https://octo-models.github.io/)
- **[OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics](https://arxiv.org/abs/2401.12202)** (2024-01-22) · [Code](https://github.com/ok-robot/ok-robot) · [Project](https://ok-robot.github.io/)
- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023-10-19) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)** (2023-07-28) · [Project](https://robotics-transformer2.github.io/)
- **[LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429)** (2022-07-10) · [Code](https://github.com/blazejosinski/lm_nav) · [Project](https://sites.google.com/view/lmnav)
- **[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)** (2022-04-04) · [Project](https://say-can.github.io/)
- **[CLIPort: What and Where Pathways for Robotic Manipulation](https://arxiv.org/abs/2109.12098)** (2021-09-24) · [Code](https://github.com/cliport/cliport) · [Project](https://cliport.github.io/)

### Self-improvement

- **[OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)** (2024-06-13) · [Code](https://github.com/openvla/openvla) · [Project](https://openvla.github.io/)
- **[Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)** (2024-05-20) · [Code](https://github.com/octo-models/octo) · [Project](https://octo-models.github.io/)
- **[AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963)** (2024-01-23)
- **[Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931)** (2023-10-19) · [Code](https://github.com/eureka-research/Eureka) · [Project](https://eureka-research.github.io/)
- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)** (2023-07-28) · [Project](https://robotics-transformer2.github.io/)
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023-05-25) · [Code](https://github.com/MineDojo/Voyager) · [Project](https://voyager.minedojo.org/)
- **[PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)** (2023-03-06) · [Project](https://palm-e.github.io/)
- **[OpenScene: 3D Scene Understanding with Open Vocabularies](https://arxiv.org/abs/2211.15654)** (2022-11-28) · [Code](https://github.com/pengsongyou/openscene) · [Project](https://pengsongyou.github.io/openscene)

### Benchmarks & Evaluation

- **[BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation](https://arxiv.org/abs/2403.09227)** (2024-03-14) · [Code](https://github.com/StanfordVL/BEHAVIOR-1K) · [Project](https://behavior.stanford.edu/)
- **[Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots](https://arxiv.org/abs/2310.13724)** (2023-10-19) · [Code](https://github.com/facebookresearch/habitat-lab) · [Project](https://aihabitat.org/habitat3/)

</details>

<!-- ATLAS:END -->

## Contributing

Suggestions and corrections are welcome via [Issues](https://github.com/hongboduan/awesome-embodied-agents/issues) or pull requests. Please include the paper link, first publication date, author project/code links when available, and a short explanation of its relevance to embodied agents. See [contribution guidance](CONTRIBUTING.md).

Paper figures and paper content belong to their respective authors. Please cite the original work. BibTeX exports are reading aids; verify complete author names and publication metadata before submission.
