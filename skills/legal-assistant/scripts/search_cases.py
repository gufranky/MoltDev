#!/usr/bin/env python3
"""
案例检索工具 - Legal Agent Case Search Tool

功能：
1. 在本地案例库中搜索案例
2. 支持关键词搜索、分类搜索
3. 返回匹配的案例摘要

使用方法：
    python3 search_cases.py 关键词
    python3 search_cases.py --category 劳动争议
    python3 search_cases.py --list-categories
"""

import re
import sys
import argparse
from pathlib import Path

# 案例库路径
CASES_FILE = Path(__file__).parent.parent / "references" / "case-studies.md"


def load_cases():
    """加载案例库"""
    with open(CASES_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    return parse_cases(content)


def parse_cases(content):
    """解析案例内容"""
    cases = []

    # 按分类分割
    # 分类格式：## XXX案例
    lines = content.split('\n')

    current_category = ''
    current_case = None
    current_section = None

    for line in lines:
        line_stripped = line.strip()

        # 检测分类标题
        if line_stripped.startswith('## ') and '案例' in line_stripped:
            current_category = line_stripped[3:].strip()
            continue

        # 检测案例标题
        match = re.match(r'### 案例(\d+)[:：](.*)', line_stripped)
        if match:
            # 保存上一个案例
            if current_case:
                cases.append(current_case)

            # 创建新案例
            num = match.group(1)
            title = match.group(2)
            current_case = {
                'number': num,
                'title': title,
                'category': current_category,
                'facts': '',
                'issue': '',
                'view': '',
                'basis': '',
                'points': ''
            }
            current_section = None
            continue

        # 检测各部分标题
        if line_stripped.startswith('**案情简介：**'):
            current_section = 'facts'
            continue
        elif line_stripped.startswith('**争议焦点：**'):
            current_section = 'issue'
            continue
        elif line_stripped.startswith('**裁判观点：**'):
            current_section = 'view'
            continue
        elif line_stripped.startswith('**法律依据：**'):
            current_section = 'basis'
            continue
        elif line_stripped.startswith('**实务要点：**'):
            current_section = 'points'
            continue

        # 收集内容
        if current_case and current_section and line_stripped and line_stripped != '---':
            if current_case[current_section]:
                current_case[current_section] += ' '
            current_case[current_section] += line_stripped

    # 保存最后一个案例
    if current_case:
        cases.append(current_case)

    return cases


def search_cases(cases, keywords, category=None):
    """搜索案例"""
    results = []

    for case in cases:
        # 分类过滤
        if category and category.lower() not in case['category'].lower():
            continue

        # 关键词匹配
        score = 0
        content = ' '.join([
            case['title'],
            case['facts'],
            case['issue'],
            case['view'],
            case['basis'],
            case['points']
        ]).lower()

        for keyword in keywords:
            keyword_lower = keyword.lower()
            # 标题匹配权重最高
            if keyword_lower in case['title'].lower():
                score += 10
            # 焦点和观点匹配权重高
            elif keyword_lower in case['issue'].lower() or keyword_lower in case['view'].lower():
                score += 5
            # 其他内容匹配
            elif keyword_lower in content:
                score += 1

        if score > 0:
            results.append((case, score))

    # 按分数排序
    results.sort(key=lambda x: x[1], reverse=True)

    return [case for case, score in results]


def format_case(case):
    """格式化案例输出"""
    output = []
    output.append(f"{'='*60}")
    output.append(f"案例 {case['number']}: {case['title']}")
    output.append(f"{'='*60}")
    output.append(f"分类: {case['category']}")
    output.append("")
    output.append(f"案情简介：{case['facts']}")
    output.append("")
    output.append(f"争议焦点：{case['issue']}")
    output.append("")
    output.append(f"裁判观点：{case['view']}")
    output.append("")
    output.append(f"法律依据：{case['basis']}")
    output.append("")
    output.append(f"实务要点：{case['points']}")
    output.append("")
    return '\n'.join(output)


def list_categories(cases):
    """列出所有案例分类"""
    categories = {}
    for case in cases:
        cat = case['category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1

    print("\n案例分类：")
    print("="*40)
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} 个案例")
    print("="*40)
    print(f"  总计: {len(cases)} 个案例\n")


def main():
    parser = argparse.ArgumentParser(
        description='案例检索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 search_cases.py 违约合同
  python3 search_cases.py --category 劳动争议 双倍工资
  python3 search_cases.py --list-categories
  python3 search_cases.py --format json 盗窃罪
        """
    )

    parser.add_argument(
        'keywords',
        nargs='*',
        help='搜索关键词（多个关键词空格分隔）'
    )
    parser.add_argument(
        '-c', '--category',
        help='按分类筛选（如：民事纠纷、劳动争议、侵权纠纷）'
    )
    parser.add_argument(
        '-l', '--list-categories',
        action='store_true',
        help='列出所有案例分类'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json'],
        default='text',
        help='输出格式（默认: text）'
    )
    parser.add_argument(
        '-n', '--limit',
        type=int,
        default=5,
        help='最多显示结果数（默认: 5）'
    )

    args = parser.parse_args()

    # 检查案例库文件
    if not CASES_FILE.exists():
        print(f"错误：案例库文件不存在: {CASES_FILE}")
        sys.exit(1)

    # 加载案例
    cases = load_cases()

    # 列出分类
    if args.list_categories:
        list_categories(cases)
        return

    # 搜索案例
    if not args.keywords:
        print("请提供搜索关键词，或使用 --list-categories 查看分类")
        print("使用 --help 查看帮助信息")
        sys.exit(1)

    results = search_cases(cases, args.keywords, args.category)

    # 输出结果
    if not results:
        print(f"\n未找到匹配 '{' '.join(args.keywords)}' 的案例")
        if args.category:
            print(f"（分类: {args.category}）")
        sys.exit(0)

    print(f"\n找到 {len(results)} 个匹配案例（显示前 {min(args.limit, len(results))} 个）\n")

    if args.format == 'json':
        import json
        output = []
        for case in results[:args.limit]:
            output.append(case)
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        for i, case in enumerate(results[:args.limit], 1):
            print(format_case(case))


if __name__ == '__main__':
    main()
