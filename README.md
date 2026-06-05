<div align="center">

# 🔬 Researcher

**学术论文调研与阅读助手 | Academic Paper Research & Reading Assistant**

输入主题，输出报告。支持深度调研、引文网络分析、多模态处理和概念教学。

*Input a topic, get a report. Supports deep research, citation network analysis, multimodal processing, and concept teaching.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

> **这是一个 Agent Skill，不是 Python 程序。**
>
> 打开你正在用的 agent（Claude Code、Codex、Cursor、OpenClaw、Hermes、CodeBuddy、Workbuddy、Gemini CLI、OpenCode 等），告诉它：
>
> ```
> 帮我安装这个 skill：git@github.com:zhoucanzong/researcher.git
> ```
>
> 它会自己帮你 clone 并配置好，不需要 `pip install`。

---

## 目录 | Table of Contents

- [功能特性 | Features](#功能特性--features)
- [项目结构 | Project Structure](#项目结构--project-structure)
- [使用方式 | Usage](#使用方式--usage)
- [贡献指南 | Contributing](#贡献指南--contributing)
- [许可证 | License](#许可证--license)

---

## 功能特性 | Features

### 调研模式 | Research Modes

- **快速调研 (`/researcher`)**：输入主题，直接输出结构化报告，最少交互。
- **深度调研 (`/researcher deep`)**：可配置的高级功能菜单，包括逐篇深度阅读、引文网络分析、对比表格、知识图谱等。
- **概念教学 (`/researcher teach`)**：苏格拉底式提问，难度自适应的概念讲解。

### 核心功能 | Core Capabilities

| 功能 | 说明 |
|------|------|
| 📄 逐篇深度阅读 | 结构化提取每篇论文的方法、实验与创新点 |
| 🕸️ 引文网络分析 | 从种子论文沿引用网络发现关联论文（类似 Connected Papers） |
| 📊 对比表格 | Elicit-style 合成数据表，支持多篇论文横向对比 |
| 🧠 知识图谱 | Zettelkasten 风格的概念关联网络 |
| 🖼️ 多模态处理 | 自动路由处理 PDF、Word、图片、网页等多种输入 |
| 👨‍🏫 概念教学 | 苏格拉底式提问，难度自适应的概念讲解 |
| 🌐 HTML 展示 | 将 Markdown 报告转换为精美的 HTML 文件，自适应深色/浅色模式 |

| Feature | Description |
|---------|-------------|
| 📄 Deep Reading | Structured extraction of methods, experiments, and innovations per paper |
| 🕸️ Citation Network | Discover related papers from a seed paper via citation networks |
| 📊 Synthesis Table | Elicit-style comparison tables across multiple papers |
| 🧠 Knowledge Graph | Zettelkasten-style concept linkage networks |
| 🖼️ Multimodal | Auto-routing for PDF, Word, images, web pages, etc. |
| 👨‍🏫 Concept Teaching | Socratic questioning with adaptive difficulty |
| 🌐 HTML Export | Convert Markdown reports to polished HTML with dark/light mode |

---

## 项目结构 | Project Structure

```
researcher/
├── LICENSE                          # MIT License
├── README.md                        # 本文件 | This file
├── requirements.txt                 # Python dependencies (agent auto-installs)
├── .gitignore                       # Git ignore rules
└── skills/
    └── researcher/                  # Skill content
        ├── SKILL.md                 # Skill definition & commands
        ├── assets/                  # Templates & configs
        │   ├── paper-fields.yaml
        │   ├── paper-outline.yaml
        │   └── paper-synthesis-table.md
        ├── references/              # Methodology references
        │   ├── citation-network.md
        │   ├── multimodal-processing.md
        │   ├── paper-reading.md
        │   ├── plan-template.md
        │   ├── report-generation.md
        │   └── teaching-methodology.md
        └── scripts/                 # CLI tools (agent auto-calls)
            ├── extract_multimodal.py
            ├── generate_paper_report.py
            ├── teach_concept.py
            ├── update_knowledge_graph.py
            └── validate_paper_json.py
```

---

## 使用方式 | Usage

安装后，直接在 agent 中使用：

| 用法 | 功能 | 适合场景 |
|------|------|----------|
| `/researcher <主题>` | 快速调研 → 输出报告 | 多数情况 |
| `/researcher deep <主题>` | 深度调研（搜索+阅读+详细报告） | 写论文、做综述 |
| `/researcher teach <概念>` | 讲解概念 | 不懂的地方 |

示例：

```
/researcher RAG最新进展
/researcher deep LLM Reasoning
/researcher teach Attention Mechanism
```

### 深度调研流程

深度模式会通过简单的问答引导你配置：

1. 时间范围偏好？（默认不限）
2. 需要哪些高级功能？（逐篇阅读、引文网络、对比表格、知识图谱等，可多选）
3. 详细程度？（简要/标准/详细，默认标准）

所有问题都有默认值，直接回车即可跳过。

### HTML 导出

报告生成后，agent 会询问是否需要 HTML 版本。确认后自动输出精美的独立 HTML 文件（暖色陶土主题，自适应深色/浅色模式，响应式设计）。

---

<details>
<summary>高级：手动脚本 / Advanced: Manual Script Usage</summary>

### 环境要求

Python 3.8+, PyYAML。

### 手动使用

```bash
# 1. 多模态输入处理
python skills/researcher/scripts/extract_multimodal.py process ./my-research ./paper.pdf

# 2. 生成文献综述报告
python skills/researcher/scripts/generate_paper_report.py my-research.yaml paper-fields.yaml ./papers time 标准

# 3. 验证论文 JSON
python skills/researcher/scripts/validate_paper_json.py -f paper-fields.yaml -j papers/my-paper.json

# 4. 更新知识图谱
python skills/researcher/scripts/update_knowledge_graph.py ./my-research

# 5. 概念教学卡片
python skills/researcher/scripts/teach_concept.py ./my-research "Attention Mechanism" intermediate
```

</details>

---

## 贡献指南 | Contributing

欢迎 Issue 和 PR！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

Issues and PRs are welcome!

---

## 许可证 | License

本项目采用 [MIT License](LICENSE) 开源授权。

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ for researchers.

</div>
