#!/usr/bin/env python3
"""
Update knowledge graph from paper reading results with Zettelkasten-style dynamic linking.
Usage: python update_knowledge_graph.py <research_dir> [--link-mode auto|manual]
"""

import argparse, json, re, sys
from pathlib import Path
from datetime import datetime

KNOWLEDGE_GRAPH = "knowledge-graph.md"
LEARNING_JOURNAL = "learning-journal.md"

# Common concept patterns for ML papers
CONCEPT_PATTERNS = [
    r'Attention|Transformer|BERT|GPT|LLM|VAE|GAN|Diffusion|CNN|RNN|LSTM|GRU',
    r'Reinforcement Learning|RLHF|Fine-tuning|Pre-training|Self-supervised',
    r'Optimization|Gradient Descent|Adam|SGD|Backpropagation',
    r'Generalization|Overfitting|Regularization|Dropout|Batch Normalization',
    r'Federated Learning|Meta-learning|Transfer Learning|Few-shot|Zero-shot',
    r'Contrastive Learning|Siamese|Triplet|InfoNCE|CLIP',
    r'Multi-modal|Vision-Language|Cross-modal',
    r'Graph Neural Network|GNN|Graph Convolution|Message Passing',
    r'Generative AI|Large Language Model|Foundation Model',
    r'Prompt Engineering|Chain-of-Thought|In-context Learning',
    r'Retrieval-Augmented Generation|RAG|Vector Database',
    r'Knowledge Distillation|Model Compression|Quantization|Pruning',
]


def load_papers(papers_dir):
    papers = []
    for f in Path(papers_dir).glob("*.json"):
        try:
            papers.append(json.loads(f.read_text(encoding='utf-8')))
        except:
            pass
    return papers


def extract_concepts(paper):
    """Extract key concepts from a paper reading result."""
    concepts = set()
    cats = paper.get('内容摘要', paper)
    kw = cats.get('keywords', []) if isinstance(cats, dict) else paper.get('keywords', [])
    if isinstance(kw, list):
        for k in kw:
            concepts.add(k.strip())
    title = paper.get('基本信息', {}).get('title', paper.get('title', ''))
    for pat in CONCEPT_PATTERNS:
        for m in re.finditer(pat, title, re.IGNORECASE):
            concepts.add(m.group(0))
    return list(concepts)


def find_citation_relationships(papers):
    """Find citation-like relationships between papers based on title mentions."""
    relationships = []  # [(paper_a, paper_b, relation_type)]
    for i, pa in enumerate(papers):
        title_a = pa.get('基本信息', {}).get('title', pa.get('title', ''))
        for j, pb in enumerate(papers):
            if i == j:
                continue
            title_b = pb.get('基本信息', {}).get('title', pb.get('title', ''))
            # Check if paper A mentions paper B in related_work
            rw = pa.get('研究背景', {}).get('related_work', '') if isinstance(pa.get('研究背景'), dict) else ''
            if title_b.split()[0] in rw if len(title_b.split()) > 0 else False:
                relationships.append((title_a, title_b, 'cites'))
            # Check year-based prior/derivative
            year_a = pa.get('基本信息', {}).get('year', 0) if isinstance(pa.get('基本信息'), dict) else 0
            year_b = pb.get('基本信息', {}).get('year', 0) if isinstance(pb.get('基本信息'), dict) else 0
            try:
                ya, yb = int(year_a), int(year_b)
                if ya > yb and title_b.split()[0] in str(rw):
                    relationships.append((title_a, title_b, 'prior_work'))
            except:
                pass
    return relationships


def find_concept_links(concepts_list):
    """Find links between concepts based on co-occurrence in papers."""
    links = {}
    for concepts in concepts_list:
        for i, ca in enumerate(concepts):
            for j, cb in enumerate(concepts):
                if i < j:
                    pair = tuple(sorted([ca, cb]))
                    links[pair] = links.get(pair, 0) + 1
    # Return pairs that co-occur in 2+ papers
    return [pair for pair, count in links.items() if count >= 2]


def update_graph(research_dir, link_mode='auto'):
    rd = Path(research_dir)
    papers_dir = rd / "papers"
    kg_path = rd / KNOWLEDGE_GRAPH
    lj_path = rd / LEARNING_JOURNAL

    papers = load_papers(papers_dir) if papers_dir.exists() else []
    if not papers:
        print("No papers found.")
        return

    # Parse existing graph
    existing_concepts = {}
    existing_links = []
    if kg_path.exists():
        content = kg_path.read_text(encoding='utf-8')
        for m in re.finditer(r'### (.+?)\n', content):
            existing_concepts[m.group(1).strip()] = True
        for m in re.finditer(r'- \*\*链接\*\*: `(.+?)` ↔ `(.+?)`', content):
            existing_links.append((m.group(1), m.group(2)))

    # Extract concepts per paper
    paper_concepts = [extract_concepts(p) for p in papers]
    all_concepts = set()
    for cs in paper_concepts:
        all_concepts.update(cs)

    # Find relationships
    paper_rels = find_citation_relationships(papers)
    concept_links = find_concept_links(paper_concepts)

    # Build graph
    lines = ["# 知识图谱", "",
             f"> 最后更新: {datetime.now().strftime('%Y-%m-%d')}",
             f"> 论文数: {len(papers)} | 概念数: {len(all_concepts)} | 链接数: {len(concept_links)}",
             ""]

    # Paper nodes with citation relationships
    lines.extend(["## 论文节点", ""])
    for p in papers:
        info = p.get('基本信息', p)
        title = info.get('title', 'Unknown')
        year = info.get('year', '-')
        venue = info.get('venue', '-')
        concepts = extract_concepts(p)
        lines.append(f"- **{title}** ({year}, {venue})")
        if concepts:
            lines.append(f"  - 概念: {', '.join(concepts)}")
        method = p.get('核心方法', {}).get('method_overview', '') if isinstance(p.get('核心方法'), dict) else ''
        if method:
            lines.append(f"  - 方法: {method[:80]}...")
        # Add citation relations
        rels = [r for r in paper_rels if r[0] == title]
        for _, target, rel_type in rels[:3]:
            lines.append(f"  - {rel_type}: {target}")
        lines.append("")

    # Concept nodes with Zettelkasten-style links
    new_concepts = [c for c in sorted(all_concepts) if c not in existing_concepts]

    if all_concepts:
        lines.extend(["## 概念节点（Zettelkasten）", "",
                      "> 每个概念是一个「原子笔记」，通过链接形成知识网络。", ""])

        for c in sorted(all_concepts):
            is_new = c in new_concepts
            # Find linked concepts
            linked = []
            for ca, cb in concept_links:
                if ca == c:
                    linked.append(cb)
                elif cb == c:
                    linked.append(ca)

            lines.append(f"### {c}")
            if is_new:
                lines.append("- **状态**: 🆕 新发现")
            else:
                lines.append("- **状态**: 📌 已存在")

            lines.append(f"- **定义**: 待补充")
            lines.append(f"- **关联论文**: 待补充")

            if linked:
                lines.append(f"- **链接（共现）**: {', '.join([f'[[{x}]]' for x in linked])}")
            else:
                lines.append(f"- **链接**: 待建立")

            # Find related papers
            related_papers = []
            for pi, pcs in enumerate(paper_concepts):
                if c in pcs:
                    t = papers[pi].get('基本信息', {}).get('title', f'Paper {pi}')
                    related_papers.append(t)
            if related_papers:
                lines.append(f"- **来源论文**: {', '.join(related_papers[:3])}")

            lines.append(f"- **理解度**: /10")
            lines.append("")

    # Zettelkasten index
    if concept_links:
        lines.extend(["## 链接索引", ""])
        for ca, cb in concept_links:
            lines.append(f"- `[[{ca}]]` ↔ `[[{cb}]]`")
        lines.append("")

    kg_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"Knowledge graph updated: {kg_path}")
    print(f"Papers: {len(papers)} | Concepts: {len(all_concepts)} | New concepts: {len(new_concepts)} | Links: {len(concept_links)}")

    # Update learning journal
    if not lj_path.exists():
        lj_path.write_text(
            f"# 学习日志\n\n> 创建日期: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            "## 已学习概念\n\n## 理解度追踪\n\n## 复习计划\n\n",
            encoding='utf-8'
        )
        print(f"Learning journal created: {lj_path}")


def main():
    parser = argparse.ArgumentParser(description='Update knowledge graph with Zettelkasten linking')
    parser.add_argument('research_dir', help='Research project directory')
    parser.add_argument('--link-mode', choices=['auto', 'manual'], default='auto',
                        help='Link creation mode (auto=co-occurrence based, manual=user confirmed)')
    args = parser.parse_args()
    update_graph(args.research_dir, args.link_mode)


if __name__ == '__main__':
    main()
