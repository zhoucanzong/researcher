# 结构化阅读规范（/researcher-read 的权威参考）

本文档是 Phase 3（结构化阅读）的完整规范，包含字段定义、agent prompt 模板、断点续传逻辑、并发策略和阅读质量自检清单。

## 为什么按类别组织字段

论文信息天然分块：基本信息是元数据，内容摘要是入口，研究背景交代动机，核心方法是创新所在，实验与结果提供证据，分析与讨论是作者反思，个人评价是读者思考。按类别而非扁平排列，agent 阅读时有层次，用户后续查阅时也有结构。

## 字段定义模板

完整模板见 `assets/paper-fields.yaml`。以下是类别说明和关键字段的注意事项：

| 类别 | 字段数 | 阅读重点 |
|------|--------|----------|
| 基本信息 | 6 | 元数据，优先填写 url 和 citations |
| 内容摘要 | 3 | **tl_dr 是核心**，用一句话概括论文贡献 |
| 研究背景 | 3 | problem 和 motivation 帮助判断论文价值 |
| 核心方法 | 3 | method_overview 讲思路，key_technique 讲细节，innovations 列创新点 |
| 实验与结果 | 4 | main_results 必须包含关键数字（BLEU、F1、准确率等） |
| 分析与讨论 | 3 | limitations 帮助识别研究缺口 |
| 个人评价 | 3 | relevance/quality 1-10 分，insights 写真实思考 |

### 不确定值规范

- 无法确认的字段值标注 `[不确定]`
- JSON 末尾添加 `uncertain` 数组，列出所有不确定字段名
- 宁可标注不确定，也不猜测填充

## paper-outline.yaml 结构

模板见 `assets/paper-outline.yaml`。执行配置说明：

| 字段 | 作用 |
|------|------|
| `batch_size` | 每批启动的并行 agent 数 |
| `papers_per_agent` | 每个 agent 同时阅读几篇（>1 时减少深度，适合快速扫描） |
| `output_dir` | JSON 输出目录，默认 `papers/` |

## Agent Prompt 模板

以下 prompt 硬约束：**严格复述，仅替换 {xxx} 变量，禁止改写结构或措辞**。

```python
prompt = f"""## 任务
深度阅读论文并输出结构化 JSON。

## 论文信息
标题: {paper_title}
作者: {authors}
年份: {year}
会议/期刊: {venue}
论文链接: {paper_url or "通过搜索找到可访问版本"}

## 阅读要求
1. 优先直接阅读论文 PDF 全文（arXiv / Google Scholar）
2. 若无法获取全文，基于摘要、介绍和结论进行阅读
3. 查阅引用情况了解影响力
4. 查找官方代码仓库（如有）

## 字段定义
读取 {fields_path} 获取所有字段定义。

## 输出要求
1. 按 paper-fields.yaml 字段输出 JSON，类别嵌套结构
2. 不确定字段标注 [不确定]
3. JSON 末尾添加 uncertain 数组
4. 所有字段值使用中文
5. tl_dr 一句话概括核心贡献
6. main_results 列出关键性能指标数字
7. relevance/quality 为 1-10 分评分

## 输出路径
{output_path}

## 验证
python scripts/validate_paper_json.py -f {fields_path} -j {output_path}
验证通过后才算完成任务。
"""
```

## 断点续传逻辑

1. 读取 `paper-outline.yaml` 获取论文列表
2. 扫描 `output_dir` 下已有 `.json` 文件
3. 以论文 slug 名匹配：已完成论文跳过
4. 显示进度：已完成 / 总数
5. 分批执行，每批完成需用户确认才继续下一批

## 并发策略

| 场景 | batch_size | papers_per_agent | 说明 |
|------|-----------|------------------|------|
| 深度阅读 | 3 | 1 | 每篇精读，默认配置 |
| 快速扫描 | 5 | 3 | 快速了解全貌，牺牲深度 |
| 核心论文优先 | 2 | 1 | 先深度读核心，再批量扫补充 |

## 阅读质量自检清单

每篇论文阅读后确认：
- [ ] 基本信息完整（标题、作者、年份、会议）
- [ ] tl_dr 能独立传达核心贡献
- [ ] main_results 包含关键数字（非模糊描述）
- [ ] innovations 至少列出 1 个（无创新 = 很可能是方法迁移论文）
- [ ] limitations 已填写（帮助识别研究缺口）
- [ ] uncertain 数组已标注不确定字段
- [ ] validate_paper_json.py 验证通过
