#!/usr/bin/env python3
"""
Generate literature review report from paper reading JSONs.
Usage: python generate_paper_report.py paper-outline.yaml paper-fields.yaml papers_dir [organization] [detail]
  organization: time | score | topic (default: time)
  detail: 简要 | 标准 | 详细 (default: 标准)
"""

import json, sys, re
from pathlib import Path
from datetime import datetime
try:
    import yaml
except ImportError:
    print("Error: pyyaml required. pip install pyyaml")
    sys.exit(1)

CATEGORY_MAP = {
    "基本信息": ["basic_info", "基本信息"],
    "内容摘要": ["abstract_info", "内容摘要", "summary"],
    "研究背景": ["background", "研究背景", "context"],
    "核心方法": ["method", "核心方法", "approach"],
    "实验与结果": ["experiments", "实验与结果", "results"],
    "分析与讨论": ["analysis", "分析与讨论", "discussion"],
    "个人评价": ["evaluation", "个人评价", "personal"],
}


def slugify(t):
    return re.sub(r'[^\w\-]', '', t.lower().replace(' ', '-'))


def to_stars(s):
    try:
        n = int(round(float(s) / 2))
        return '★' * n + '☆' * (5 - n) + f" ({s}/10)"
    except:
        return str(s)


def find_field(data, names):
    for n in names:
        if n in data:
            v = data[n]
            if v is not None and v != "" and "[不确定]" not in str(v):
                return v
    for cn, fv in data.items():
        if isinstance(fv, dict):
            for n in names:
                if n in fv:
                    v = fv[n]
                    if v is not None and v != "" and "[不确定]" not in str(v):
                        return v
    return None


def get_field(data, name):
    keys = []
    for cat, variants in CATEGORY_MAP.items():
        if name in variants:
            keys.extend(variants)
            break
    if not keys:
        keys = [name]
    if '_unread' in data:
        return data.get('_meta', {}).get(name, "[未阅读]")
    val = find_field(data, keys)
    if val is not None:
        return val
    return data.get('_meta', {}).get(name, "")


def fmt(v):
    if v is None:
        return "*未记录*"
    if isinstance(v, list):
        if not v:
            return "*无*"
        if isinstance(v[0], dict):
            return "\n".join(f"- {' | '.join(f'**{k}**: {xv}' for k, xv in item.items())}" for item in v)
        return ", ".join(str(x) for x in v)
    if isinstance(v, dict):
        return " | ".join(f"**{k}**: {fmt(xv)}" for k, xv in v.items())
    if isinstance(v, str) and len(v) > 200:
        return v[:200] + "..."
    return str(v)


def collect_papers(outline, papers_dir):
    papers, dp = [], Path(papers_dir)
    for p in outline.get('papers', []):
        title = p.get('title', '')
        slug = re.sub(r'[^\w\s]', '', title).replace(' ', '_').lower()
        jp = dp / f"{slug}.json"
        if jp.exists():
            d = json.loads(jp.read_text(encoding='utf-8'))
            d['_meta'], d['_source'] = p, str(jp)
            papers.append(d)
        else:
            papers.append({'_meta': p, '_unread': True, **p})
    return papers


def generate(outline, papers, org='time', detail='标准'):
    topic = outline.get('topic', '论文综述')
    if org == 'time':
        papers.sort(key=lambda p: str(get_field(p, 'year') or '0'))
    elif org == 'score':
        papers.sort(key=lambda p: float(get_field(p, 'quality') or 0), reverse=True)

    lines = [f"# {topic} - 文献综述报告", "",
             f"> **生成日期**: {datetime.now().strftime('%Y-%m-%d')}",
             f"> **论文数量**: {len(papers)}篇", ""]

    # Overview table
    lines.extend(["## 论文概览", "", "| 序号 | 论文 | 年份 | 会议 | TL;DR | 质量 |",
                  "|------|------|------|------|-------|------|"])
    for i, p in enumerate(papers, 1):
        t = get_field(p, 'title')
        y = get_field(p, 'year') or '-'
        v = get_field(p, 'venue') or '-'
        tl = get_field(p, 'tl_dr') or get_field(p, 'abstract') or '-'
        if len(str(tl)) > 50:
            tl = str(tl)[:50] + '...'
        q = get_field(p, 'quality')
        lines.append(f"| {i} | [{t}](#{slugify(str(t))}) | {y} | {v} | {tl} | {to_stars(q) if q else '-'} |")
    lines.append("")

    # Statistics
    lines.extend(["## 统计摘要", ""])
    qs = [float(get_field(p, 'quality') or 0) for p in papers if get_field(p, 'quality')]
    if qs:
        lines.append(f"- **平均质量评分**: {sum(qs) / len(qs):.1f}/10")
    yrs = [str(get_field(p, 'year')) for p in papers if get_field(p, 'year')]
    if yrs:
        lines.append(f"- **时间跨度**: {min(yrs)} - {max(yrs)}")
    venues = {}
    for p in papers:
        vn = str(get_field(p, 'venue') or 'Unknown')
        venues[vn] = venues.get(vn, 0) + 1
    if venues:
        top = sorted(venues.items(), key=lambda x: x[1], reverse=True)[:5]
        lines.append(f"- **主要会议**: {', '.join(f'{v}({c})' for v, c in top)}")
    lines.append("")

    # Detailed notes
    lines.extend(["## 论文详细阅读笔记", ""])
    for p in papers:
        t = get_field(p, 'title')
        a = get_field(p, 'authors')
        y = get_field(p, 'year')
        v = get_field(p, 'venue')
        lines.extend([f"### {t}",
                      f"**作者**: {a or '-'} | **年份**: {y or '-'} | **会议**: {v or '-'}" , ""])
        if '_unread' in p:
            lines.extend(["*[尚未完成深度阅读]*", "", "---", ""])
            continue
        tl = get_field(p, 'tl_dr')
        if tl:
            lines.extend([f"**一句话总结**: {tl}", ""])

        sections = [('研究问题', ['problem']), ('研究动机', ['motivation']),
                    ('核心方法', ['method_overview', 'key_technique']), ('创新点', ['innovations']),
                    ('实验数据', ['datasets']), ('主要结果', ['main_results']),
                    ('主要贡献', ['contributions']), ('局限性', ['limitations']), ('未来工作', ['future_work'])]
        if detail == '简要':
            sections = [s for s in sections if s[0] in ('核心方法', '创新点', '主要结果')]
        elif detail == '标准':
            sections = [s for s in sections if s[0] not in ('研究动机', '实验数据')]

        for sn, keys in sections:
            val = find_field(p, keys) if not any(k in p for k in keys) else None
            if not val:
                for k in keys:
                    val = get_field(p, k)
                    if val and str(val).strip() and "[不确定]" not in str(val):
                        break
            if val and str(val).strip() and "[不确定]" not in str(val):
                lines.extend([f"**{sn}**: {fmt(val)}", ""])

        rel = get_field(p, 'relevance')
        qua = get_field(p, 'quality')
        ins = get_field(p, 'insights')
        if rel or qua:
            lines.append(f"**评分**: 相关度 {to_stars(rel)} | 质量 {to_stars(qua)}")
            lines.append("")
        if ins and "[不确定]" not in str(ins):
            lines.extend([f"**个人启发**: {ins}", ""])
        unc = p.get('uncertain', [])
        if unc:
            lines.append(f"*[未确认: {', '.join(unc)}]*")
            lines.append("")
        lines.extend(["---", ""])

    # Trends
    lines.extend(["## 研究趋势与展望", ""])
    inns = [str(get_field(p, 'innovations')) for p in papers if '_unread' not in p and get_field(p, 'innovations')]
    fws = [str(get_field(p, 'future_work')) for p in papers if '_unread' not in p and get_field(p, 'future_work')]
    if inns:
        lines.extend(["### 主要创新方向"] + [f"- {x[:150]}{'...' if len(x) > 150 else ''}" for x in inns[:5]] + [""])
    if fws:
        lines.extend(["### 未来方向"] + [f"- {x[:150]}{'...' if len(x) > 150 else ''}" for x in fws[:5]] + [""])

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_paper_report.py outline.yaml fields.yaml papers_dir [org] [detail]")
        sys.exit(1)
    outline = yaml.safe_load(open(sys.argv[1], encoding='utf-8'))
    papers = collect_papers(outline, sys.argv[3])
    org = sys.argv[4] if len(sys.argv) > 4 else 'time'
    detail = sys.argv[5] if len(sys.argv) > 5 else '标准'
    report = generate(outline, papers, org, detail)
    rp = Path(sys.argv[1]).parent / 'report.md'
    rp.write_text(report, encoding='utf-8')
    print(f"\nReport: {rp} | Papers: {len(papers)} | Org: {org} | Detail: {detail}")


if __name__ == '__main__':
    main()
