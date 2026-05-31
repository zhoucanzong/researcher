#!/usr/bin/env python3
"""
Multimodal input processing for researcher skill.
Routes different file types to appropriate extraction tools and produces
unified markdown outputs + sources-index entries.

Usage:
    # Process a single file
    python extract_multimodal.py process <research_dir> <file_path> [--type pdf|word|image|web|text]

    # Batch process a directory of inputs
    python extract_multimodal.py batch <research_dir> <inputs_dir>

    # Update sources-index.md with processed files
    python extract_multimodal.py index <research_dir>

    # List all supported formats
    python extract_multimodal.py formats
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# File extension to type mapping
EXT_MAP = {
    '.pdf': 'pdf',
    '.docx': 'word',
    '.doc': 'word',
    '.md': 'text',
    '.txt': 'text',
    '.json': 'text',
    '.yaml': 'text',
    '.yml': 'text',
    '.png': 'image',
    '.jpg': 'image',
    '.jpeg': 'image',
    '.gif': 'image',
    '.webp': 'image',
    '.bmp': 'image',
    '.svg': 'image',
}

# Template for text extraction output
TEXT_EXTRACT_TEMPLATE = """# Extract: {basename}

> **来源类型**: {file_type}
> **原始文件**: {original_path}
> **提取日期**: {date}
> **提取工具**: {tool}

---

{content}

---

## 处理备注
- 提取状态: {status}
- 完整性评估: {completeness}
- 后续处理建议: {suggestion}
"""

# Template for image analysis output
IMAGE_DESCR_TEMPLATE = """# 图片分析: {basename}

## 来源信息
- **原始文件**: {original_path}
- **分析日期**: {date}
- **文件类型**: {file_type}

## 图片描述
[待通过视觉分析填写]

## 可见内容
- [ ] 图表/示意图
- [ ] 数据表格
- [ ] 数学公式
- [ ] 模型架构图
- [ ] 实验结果图
- [ ] 流程图
- [ ] 其他: ___

## 关键信息提取
| 项目 | 内容 |
|------|------|
| 标题/编号 | |
| 横轴/纵轴 | |
| 数据趋势 | |
| 关键数值 | |
| 图例说明 | |

## 与论文关联
[填写此图在论文中的作用、对应章节]

## 分析备注
- 图片质量: /10
- 信息完整度: /10
- 是否需要重新获取高清版本:
"""

# Template for web clipping output
WEB_CLIP_TEMPLATE = """# Web Clipping: {basename}

> **来源URL**: {url}
> **抓取日期**: {date}
> **抓取工具**: browser_visit

---

{content}

---

## 元数据
- **页面标题**:
- **作者/发布者**:
- **发布日期**:
- **可信度评估**:
- **相关度评分**: /10
"""


def ensure_dirs(research_dir):
    """Create required subdirectories."""
    for sub in ['raw-extracts', 'image-descriptions', 'papers']:
        (Path(research_dir) / sub).mkdir(parents=True, exist_ok=True)


def detect_file_type(file_path):
    """Detect file type from extension."""
    ext = Path(file_path).suffix.lower()
    return EXT_MAP.get(ext, 'unknown')


def slugify(text):
    text = re.sub(r'[^\w\s]', '', text).lower().replace(' ', '_')
    return text[:80]  # Limit length


def process_pdf(research_dir, file_path):
    """Process PDF: extract text via read_file."""
    basename = Path(file_path).stem
    slug = slugify(basename)
    output_path = Path(research_dir) / 'raw-extracts' / f"pdf-{slug}.md"

    content = TEXT_EXTRACT_TEMPLATE.format(
        basename=basename,
        file_type='PDF',
        original_path=file_path,
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        tool='read_file (PDF→Markdown)',
        content=f'[通过read_file提取的PDF内容，见原始文件: {file_path}]\n\n'
                f'**重要提醒**: 检查以下内容是否完整提取：\n'
                f'- [ ] 论文标题、作者、摘要\n'
                f'- [ ] 所有章节正文\n'
                f'- [ ] 表格数据\n'
                f'- [ ] 参考文献列表\n'
                f'- [ ] 附录\n\n'
                f'**图片处理**: PDF中的图片需单独截图上传进行视觉分析。',
        status='待通过read_file提取',
        completeness='未知（需执行read_file后评估）',
        suggestion='1. 使用read_file读取PDF全文\n'
                   '2. 对关键插图截图并上传进行视觉分析\n'
                   '3. 检查公式是否正确提取'
    )

    output_path.write_text(content, encoding='utf-8')
    print(f"[PDF] Created extraction template: {output_path}")
    return str(output_path)


def process_word(research_dir, file_path):
    """Process Word document: extract text via read_file."""
    basename = Path(file_path).stem
    slug = slugify(basename)
    output_path = Path(research_dir) / 'raw-extracts' / f"word-{slug}.md"

    content = TEXT_EXTRACT_TEMPLATE.format(
        basename=basename,
        file_type='Word (.docx)',
        original_path=file_path,
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        tool='read_file (DOCX→Markdown)',
        content=f'[通过read_file提取的Word内容，见原始文件: {file_path}]\n\n'
                f'**检查清单**: \n'
                f'- [ ] 标题和章节结构\n'
                f'- [ ] 正文内容\n'
                f'- [ ] 表格数据\n'
                f'- [ ] 图片说明（图片本身需单独处理）',
        status='待通过read_file提取',
        completeness='未知',
        suggestion='使用read_file读取DOCX全文'
    )

    output_path.write_text(content, encoding='utf-8')
    print(f"[Word] Created extraction template: {output_path}")
    return str(output_path)


def process_image(research_dir, file_path):
    """Process image: create analysis template for visual analysis."""
    basename = Path(file_path).stem
    slug = slugify(basename)
    output_path = Path(research_dir) / 'image-descriptions' / f"img-{slug}.md"

    file_type = detect_file_type(file_path).upper()

    content = IMAGE_DESCR_TEMPLATE.format(
        basename=basename,
        original_path=file_path,
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        file_type=file_type
    )

    output_path.write_text(content, encoding='utf-8')
    print(f"[Image] Created analysis template: {output_path}")
    print(f"  -> 上传 {file_path} 进行视觉分析，将结果填入模板")
    return str(output_path)


def process_web(research_dir, url):
    """Process web URL: create clipping template."""
    slug = slugify(url.replace('https://', '').replace('http://', '').replace('/', '_'))
    output_path = Path(research_dir) / 'raw-extracts' / f"web-{slug}.md"

    content = WEB_CLIP_TEMPLATE.format(
        basename=slug,
        url=url,
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        content=f'[通过browser_visit抓取的内容，见: {url}]\n\n'
                f'**抓取步骤**: \n'
                f'1. 使用browser_visit访问URL\n'
                f'2. 滚动页面确保完整加载\n'
                f'3. 提取关键文本内容\n'
                f'4. 如有重要图片，单独下载分析'
    )

    output_path.write_text(content, encoding='utf-8')
    print(f"[Web] Created clipping template: {output_path}")
    return str(output_path)


def process_text(research_dir, file_path):
    """Process text/markdown file: direct copy."""
    basename = Path(file_path).stem
    slug = slugify(basename)
    output_path = Path(research_dir) / 'raw-extracts' / f"text-{slug}.md"

    try:
        original = Path(file_path).read_text(encoding='utf-8')
        content = TEXT_EXTRACT_TEMPLATE.format(
            basename=basename,
            file_type='Text/Markdown',
            original_path=file_path,
            date=datetime.now().strftime('%Y-%m-%d %H:%M'),
            tool='direct read',
            content=original,
            status='已直接复制',
            completeness='完整（原始文本）',
            suggestion='无需额外处理'
        )
    except Exception as e:
        content = TEXT_EXTRACT_TEMPLATE.format(
            basename=basename,
            file_type='Text',
            original_path=file_path,
            date=datetime.now().strftime('%Y-%m-%d %H:%M'),
            tool='direct read',
            content=f'[读取失败: {e}]',
            status='失败',
            completeness='无法评估',
            suggestion=f'检查文件编码或权限: {e}'
        )

    output_path.write_text(content, encoding='utf-8')
    print(f"[Text] Copied to: {output_path}")
    return str(output_path)


def process_file(research_dir, file_path, forced_type=None):
    """Route a single file to the appropriate processor."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return None

    ftype = forced_type or detect_file_type(file_path)
    ensure_dirs(research_dir)

    router = {
        'pdf': process_pdf,
        'word': process_word,
        'image': process_image,
        'text': process_text,
    }

    handler = router.get(ftype)
    if handler:
        return handler(research_dir, file_path)
    else:
        print(f"[Unknown] Unsupported file type: {ftype} ({file_path})")
        # Create a generic template
        basename = path.stem
        slug = slugify(basename)
        output_path = Path(research_dir) / 'raw-extracts' / f"unknown-{slug}.md"
        output_path.write_text(
            f"# Unknown File: {basename}\n\n"
            f"- **路径**: {file_path}\n"
            f"- **检测类型**: {ftype}\n"
            f"- **处理建议**: 手动检查并决定处理方式\n",
            encoding='utf-8'
        )
        return str(output_path)


def process_url(research_dir, url):
    """Process a web URL."""
    ensure_dirs(research_dir)
    return process_web(research_dir, url)


def update_index(research_dir):
    """Update sources-index.md with all processed files."""
    rd = Path(research_dir)
    index_path = rd / 'sources-index.md'

    entries = []

    # Scan raw-extracts
    extracts_dir = rd / 'raw-extracts'
    if extracts_dir.exists():
        for f in sorted(extracts_dir.glob('*.md')):
            ftype = f.stem.split('-')[0] if '-' in f.stem else 'unknown'
            entries.append({
                'type': ftype,
                'title': f.stem,
                'path': str(f.relative_to(rd)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })

    # Scan image-descriptions
    img_dir = rd / 'image-descriptions'
    if img_dir.exists():
        for f in sorted(img_dir.glob('*.md')):
            entries.append({
                'type': 'image',
                'title': f.stem,
                'path': str(f.relative_to(rd)),
                'date': datetime.now().strftime('%Y-%m-%d')
            })

    # Write index
    lines = ["# 来源索引 (Sources Index)", "",
             f"> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
             f"> 总条目: {len(entries)}", ""]

    # Group by type
    by_type = {}
    for e in entries:
        by_type.setdefault(e['type'], []).append(e)

    for ttype, items in sorted(by_type.items()):
        lines.append(f"## {ttype.upper()}")
        lines.append("")
        for item in items:
            lines.append(f"- [{item['title']}]({item['path']}) — {item['date']}")
        lines.append("")

    index_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"Sources index updated: {index_path} ({len(entries)} entries)")
    return str(index_path)


def batch_process(research_dir, inputs_dir):
    """Process all files in a directory."""
    inputs_path = Path(inputs_dir)
    if not inputs_path.exists():
        print(f"Error: Directory not found: {inputs_dir}")
        return []

    results = []
    for f in sorted(inputs_path.iterdir()):
        if f.is_file():
            print(f"\nProcessing: {f.name}")
            result = process_file(research_dir, str(f))
            if result:
                results.append(result)

    # Update index
    update_index(research_dir)
    print(f"\nBatch complete: {len(results)} files processed")
    return results


def list_formats():
    """Display supported formats."""
    print("=" * 60)
    print("Researcher Skill - Supported Input Formats")
    print("=" * 60)
    print()
    print("TEXT DOCUMENTS:")
    print("  .pdf       -> raw-extracts/pdf-{slug}.md")
    print("  .docx      -> raw-extracts/word-{slug}.md")
    print("  .doc       -> raw-extracts/word-{slug}.md")
    print("  .md        -> raw-extracts/text-{slug}.md")
    print("  .txt       -> raw-extracts/text-{slug}.md")
    print()
    print("IMAGES (require visual analysis):")
    print("  .png       -> image-descriptions/img-{slug}.md")
    print("  .jpg       -> image-descriptions/img-{slug}.md")
    print("  .jpeg      -> image-descriptions/img-{slug}.md")
    print("  .gif       -> image-descriptions/img-{slug}.md")
    print("  .webp      -> image-descriptions/img-{slug}.md")
    print("  .svg       -> image-descriptions/img-{slug}.md")
    print()
    print("WEB:")
    print("  URL        -> raw-extracts/web-{slug}.md")
    print()
    print("CODE/DATA:")
    print("  .json      -> raw-extracts/text-{slug}.md")
    print("  .yaml      -> raw-extracts/text-{slug}.md")
    print("  .yml       -> raw-extracts/text-{slug}.md")
    print()
    print("OUTPUT DIRECTORIES:")
    print("  {research_dir}/raw-extracts/       - 文本提取结果")
    print("  {research_dir}/image-descriptions/ - 图片分析结果")
    print("  {research_dir}/sources-index.md    - 统一索引文件")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Multimodal input processor for researcher skill')
    subparsers = parser.add_subparsers(dest='command', help='Command')

    # process command
    p_process = subparsers.add_parser('process', help='Process a single file')
    p_process.add_argument('research_dir', help='Research project directory')
    p_process.add_argument('file_path', help='File to process')
    p_process.add_argument('--type', choices=['pdf', 'word', 'image', 'web', 'text'],
                           help='Force file type (auto-detect if not set)')

    # batch command
    p_batch = subparsers.add_parser('batch', help='Batch process a directory')
    p_batch.add_argument('research_dir', help='Research project directory')
    p_batch.add_argument('inputs_dir', help='Directory containing input files')

    # index command
    p_index = subparsers.add_parser('index', help='Update sources-index.md')
    p_index.add_argument('research_dir', help='Research project directory')

    # formats command
    subparsers.add_parser('formats', help='List supported formats')

    args = parser.parse_args()

    if args.command == 'process':
        process_file(args.research_dir, args.file_path, args.type)
        update_index(args.research_dir)
    elif args.command == 'batch':
        batch_process(args.research_dir, args.inputs_dir)
    elif args.command == 'index':
        update_index(args.research_dir)
    elif args.command == 'formats':
        list_formats()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
