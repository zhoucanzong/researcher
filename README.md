<div align="center">

# 🔬 Researcher

**学术论文调研与阅读助手 | Academic Paper Research & Reading Assistant**

输入主题，输出报告。支持深度调研、引文网络分析、多模态处理和概念教学。

*Input a topic, get a report. Supports deep research, citation network analysis, multimodal processing, and concept teaching.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>

---

## 目录 | Table of Contents

- [功能特性 | Features](#功能特性--features)
- [项目结构 | Project Structure](#项目结构--project-structure)
- [快速开始 | Quick Start](#快速开始--quick-start)
- [使用说明 | Usage](#使用说明--usage)
- [贡献指南 | Contributing](#贡献指南--contributing)
- [许可证 | License](#许可证--license)

---

## 功能特性 | Features

### 调研模式 | Research Mode
- **快速调研 (`/researcher`)**：输入主题，直接输出结构化报告，最少交互。
- **深度调研 (`/researcher-deep`)**：可配置的高级功能菜单，包括逐篇深度阅读、引文网络分析、对比表格、知识图谱等。

### 核心功能 | Core Capabilities
| 功能 | 说明 |
|------|------|
| 📄 逐篇深度阅读 | 结构化提取每篇论文的方法、实验与创新点 |
| 🕸️ 引文网络分析 | 从种子论文沿引用网络发现关联论文（类似 Connected Papers） |
| 📊 对比表格 | Elicit-style 合成数据表，支持多篇论文横向对比 |
| 🧠 知识图谱 | Zettelkasten 风格的概念关联网络 |
| 🖼️ 多模态处理 | 自动路由处理 PDF、Word、图片、网页等多种输入 |
| 👨‍🏫 概念教学 | 苏格拉底式提问，难度自适应的概念讲解 |

| Feature | Description |
|---------|-------------|
| 📄 Deep Reading | Structured extraction of methods, experiments, and innovations per paper |
| 🕸️ Citation Network | Discover related papers from a seed paper via citation networks |
| 📊 Synthesis Table | Elicit-style comparison tables across multiple papers |
| 🧠 Knowledge Graph | Zettelkasten-style concept linkage networks |
| 🖼️ Multimodal | Auto-routing for PDF, Word, images, web pages, etc. |
| 👨‍🏫 Concept Teaching | Socratic questioning with adaptive difficulty |

---

## 项目结构 | Project Structure

```
researcher/
├── LICENSE                          # MIT License
├── README.md                        # 本文件 | This file
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── skills/
    └── researcher/                  # Skill content
        ├── SKILL.md                 # Skill definition & commands
        ├── assets/                  # Templates & configs
        │   ├── paper-fields.yaml    # Structured reading field definitions
        │   ├── paper-outline.yaml   # Research plan template
        │   └── paper-synthesis-table.md
        ├── references/              # Methodology references
        │   ├── citation-network.md
        │   ├── multimodal-processing.md
        │   ├── paper-reading.md
        │   ├── plan-template.md
        │   ├── report-generation.md
        │   └── teaching-methodology.md
        └── scripts/                 # CLI tools
            ├── extract_multimodal.py
            ├── generate_paper_report.py
            ├── teach_concept.py
            ├── update_knowledge_graph.py
            └── validate_paper_json.py
```

---

## 快速开始 | Quick Start

### 环境要求 | Requirements

- Python 3.8+
- PyYAML

### 安装 | Installation

```bash
# 克隆仓库 | Clone the repo
git clone <repo-url>
cd researcher

# 安装依赖 | Install dependencies
pip install -r requirements.txt
```

### 第一步：准备研究计划 | Step 1: Prepare a Research Plan

复制模板并编辑你的论文列表：

```bash
cp skills/researcher/assets/paper-outline.yaml my-research.yaml
# 编辑 my-research.yaml，填入你的主题和论文列表
```

### 第二步：生成报告 | Step 2: Generate Report

```bash
# 生成文献综述报告
python skills/researcher/scripts/generate_paper_report.py \
  my-research.yaml \
  skills/researcher/assets/paper-fields.yaml \
  ./papers \
  time 标准
```

---

## 使用说明 | Usage

### 1. 多模态输入处理 | Multimodal Input Processing

处理 PDF、图片、Word 等文件，统一提取为 Markdown：

```bash
# 处理单个文件
python skills/researcher/scripts/extract_multimodal.py process \
  ./my-research ./paper.pdf

# 批量处理目录
python skills/researcher/scripts/extract_multimodal.py batch \
  ./my-research ./inputs/

# 查看支持的格式
python skills/researcher/scripts/extract_multimodal.py formats
```

### 2. 论文 JSON 验证 | Paper JSON Validation

验证论文阅读结果是否符合字段规范：

```bash
python skills/researcher/scripts/validate_paper_json.py \
  -f skills/researcher/assets/paper-fields.yaml \
  -j papers/my-paper.json
```

### 3. 知识图谱更新 | Knowledge Graph Update

从论文阅读结果中提取概念，构建 Zettelkasten 风格的知识图谱：

```bash
python skills/researcher/scripts/update_knowledge_graph.py ./my-research
```

### 4. 概念教学卡片 | Concept Teaching Card

为某个概念生成教学卡片并追加到知识图谱：

```bash
python skills/researcher/scripts/teach_concept.py \
  ./my-research "Attention Mechanism" intermediate
```

---

## 贡献指南 | Contributing

欢迎 Issue 和 PR！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

Issues and PRs are welcome!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 许可证 | License

本项目采用 [MIT License](LICENSE) 开源授权。

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ for researchers.

</div>
