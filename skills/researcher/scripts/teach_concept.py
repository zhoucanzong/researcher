#!/usr/bin/env python3
"""
Generate concept card and teaching plan.
Usage: python teach_concept.py <research_dir> <concept_name> <difficulty> [related_papers]
  difficulty: beginner | intermediate | advanced | expert
"""

import json, re, sys
from pathlib import Path
from datetime import datetime

CONCEPT_CARD_TEMPLATE = """## {concept}
- **难度级别**: {difficulty}
- **定义**: {definition}
- **类比**: {analogy}
- {math_section}
- **直观理解**: {intuition}
- **关联概念**: {related}
- **典型应用**: {applications}
- **常见误区**: {misconceptions}
- **首次学习**: {date}
- **最后复习**: {date}
- **用户理解度**: /10

### 教学计划
{teaching_plan}

### 检查清单
- [ ] 能用自己的话解释定义
- [ ] 能画出示意图/流程图
- [ ] 能举例说明应用场景
- [ ] 能识别常见错误
- [ ] 能关联到其他概念
"""


def get_analogy(concept):
    """Return a default analogy for common ML concepts."""
    analogies = {
        "attention": "就像你在嘈杂餐厅里专注于朋友的声音，忽略周围噪音",
        "transformer": "像是一个高效的翻译团队，每个成员同时查看所有原文，决定关注哪些部分",
        "gradient descent": "就像一个盲人在山上找最低点，用脚感受坡度方向，一步步往下走",
        "backpropagation": "像是一个成绩反馈系统，从最终考试分数倒推，找出每个知识点需要改进的地方",
        "neural network": "像大脑中的神经元网络，每个节点接收信号，处理后传递给下一个节点",
        "convolution": "就像是一个扫描窗口，在图片上滑动寻找特定模式（如边缘、纹理）",
        "regularization": "像是给模型戴上手铐，限制它的自由度，防止它过度拟合训练数据",
        "dropout": "像是团队训练中随机让部分成员休息，强迫剩余成员独立承担责任",
        "batch normalization": "像是考试前把所有学生的成绩标准化，让不同班级的学生公平比较",
        "embedding": "像是给每个单词分配一个独特的坐标，意思相近的词在空间中距离也近",
        "fine-tuning": "像是学会骑自行车后学骑摩托车，基础技能通用，只需微调适应新场景",
        "transfer learning": "像是学会弹钢琴后学大提琴，音乐理论基础通用，只需学习新乐器特性",
    }
    c = concept.lower().replace(' ', '_')
    return analogies.get(c, "待补充（根据具体概念构造生活类比）")


def get_misconceptions(concept):
    """Return common misconceptions for common ML concepts."""
    myths = {
        "attention": '- 误以为注意力权重就是"重要性"排名\n- 忽略多头注意力的多样性',
        "gradient descent": "- 以为梯度下降总能找到全局最优\n- 忽略学习率的选择对结果影响巨大",
        "neural network": "- 以为层数越多越好\n- 把神经网络当黑盒，不理解内部机制",
        "overfitting": "- 以为训练集准确率100%是好事\n- 不清楚如何判断是否过拟合",
        "regularization": "- 以为正则化强度越大越好\n- 混淆L1和L2正则化的作用",
    }
    return myths.get(concept.lower().replace(' ', '_'), "- 待补充")


def generate_card(concept, difficulty, research_dir, related_papers=None):
    rd = Path(research_dir)
    kg_path = rd / "knowledge-graph.md"

    # Try to find definition from existing papers
    definition = "待补充"
    if related_papers:
        for p in related_papers:
            abst = p.get('内容摘要', {}).get('abstract', '') if isinstance(p.get('内容摘要'), dict) else ''
            if abst and concept.lower() in abst.lower():
                # Extract a sentence containing the concept
                for sent in abst.split('。'):
                    if concept.lower() in sent.lower() and len(sent) > 20:
                        definition = sent.strip() + "。"
                        break

    math_section = "- **数学表达**: 待补充" if difficulty in ('intermediate', 'advanced', 'expert') else ""
    analogy = get_analogy(concept)
    misconceptions = get_misconceptions(concept)
    date = datetime.now().strftime('%Y-%m-%d')

    # Generate teaching plan based on difficulty
    if difficulty == 'beginner':
        plan = f"""1. 用"{analogy}"建立直觉
2. 展示一个具体例子
3. 让用户用自己的话解释
4. 指出常见误区"""
    elif difficulty == 'intermediate':
        plan = f"""1. 正式定义 + 数学表达
2. 为什么需要这个概念（动机）
3. 与已知概念的对比
4. 实际代码演示
5. 让用户实现一个简单版本"""
    elif difficulty == 'advanced':
        plan = f"""1. 严格数学定义 + 证明
2. 不同变体的比较
3. 最新研究进展
4. 开放问题讨论
5. 前沿应用案例"""
    else:  # expert
        plan = f"""1. 论文级深度讨论
2. 与相关工作的细微差别
3. 未解决问题与研究机会
4. 引导用户思考可能的改进方向"""

    card = CONCEPT_CARD_TEMPLATE.format(
        concept=concept,
        difficulty=difficulty,
        definition=definition,
        analogy=analogy,
        math_section=math_section,
        intuition="待补充",
        related="待补充",
        applications="待补充",
        misconceptions=misconceptions,
        date=date,
        teaching_plan=plan
    )

    # Append to knowledge graph
    if kg_path.exists():
        content = kg_path.read_text(encoding='utf-8')
        if f"## {concept}" not in content:
            kg_path.write_text(content.rstrip() + "\n\n" + card + "\n", encoding='utf-8')
        else:
            print(f"Concept '{concept}' already exists in knowledge graph.")
    else:
        kg_path.write_text(f"# 知识图谱\n\n{card}\n", encoding='utf-8')

    print(f"\nConcept card for '{concept}' generated.")
    print(f"Location: {kg_path}")
    return card


def main():
    if len(sys.argv) < 4:
        print("Usage: python teach_concept.py <research_dir> <concept> <difficulty> [paper1.json ...]")
        sys.exit(1)

    rd, concept, diff = sys.argv[1], sys.argv[2], sys.argv[3]
    papers = []
    for pf in sys.argv[4:]:
        p = Path(pf)
        if p.exists():
            papers.append(json.loads(p.read_text(encoding='utf-8')))

    generate_card(concept, diff, rd, papers)


if __name__ == '__main__':
    main()
