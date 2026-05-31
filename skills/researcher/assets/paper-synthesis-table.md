# 合成数据表模板（Elicit-style）

用于多篇论文的结构化对比，从 `papers/*.json` 自动提取。

## 标准列

| 列名 | 来源字段 | 说明 |
|------|----------|------|
| 论文 | `title` | 论文标题（锚点链接） |
| 年份 | `year` | 发表年份 |
| 会议 | `venue` | 会议/期刊 |
| 方法 | `method_overview` | 一句话方法描述 |
| 数据集 | `datasets` | 实验数据集 |
| 关键指标 | `main_results` | 核心性能数字 |
| 创新点 | `innovations` | 主要创新 |
| 局限 | `limitations` | 关键局限 |
| 引用态度 | — | 支持/矛盾/提及 |

## 自定义列

用户可通过 AskUserQuestion 添加：
- 特定领域列（如 "参数量"、"推理速度"、"代码可用性"）
- 评价列（如 "个人评分"、"复现难度"）

## 示例

| 论文 | 年份 | 方法 | 数据集 | 关键指标 | 创新点 | 局限 |
|------|------|------|--------|----------|--------|------|
| [Attention Is All You Need](#) | 2017 | Transformer | WMT 2014 | BLEU 28.4 | 纯注意力机制 | O(n²) 内存 |
| [BERT](#) | 2019 | 双向Transformer | GLUE | GLUE 80.5 | 预训练+微调 | 计算量大 |
| [GPT-3](#) | 2020 | 自回归Transformer | 多种 | Few-shot SOTA | 上下文学习 | 黑盒、偏见 |

## 生成命令

```bash
python scripts/generate_paper_report.py assets/paper-outline.yaml assets/paper-fields.yaml papers/ --table
```

`--table` 标志启用合成表格输出（替代或补充详细报告）。
