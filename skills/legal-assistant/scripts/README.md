# 案例检索工具使用说明

## 工具位置

`/root/clawd/skills/legal-assistant/scripts/search_cases.py`

## 功能特性

- 在本地案例库中搜索案例
- 支持多关键词搜索
- 支持按分类筛选
- 支持多种输出格式（文本/JSON）
- 按相关性排序结果

## 使用方法

### 1. 基本搜索

```bash
# 搜索单个关键词
python3 search_cases.py 违约

# 搜索多个关键词
python3 search_cases.py 合同 质量 瑕疵
```

### 2. 按分类搜索

```bash
# 先查看可用分类
python3 search_cases.py --list-categories

# 在特定分类中搜索
python3 search_cases.py --category 劳动争议 双倍工资
python3 search_cases.py -c 民事纠纷 格式条款
```

### 3. JSON 格式输出

```bash
python3 search_cases.py --format json 侵权
python3 search_cases.py -f json 诽谤
```

### 4. 限制结果数量

```bash
# 只显示前 3 个结果
python3 search_cases.py --limit 3 劳动
python3 search_cases.py -n 3 解除合同
```

### 5. 组合使用

```bash
# 在劳动争议分类中搜索，JSON 格式，只显示前 2 个结果
python3 search_cases.py --category 劳动争议 --format json --limit 2 赔偿
```

### 6. 查看帮助

```bash
python3 search_cases.py --help
```

## 可用分类

| 分类 | 案例数量 |
|------|----------|
| 民事纠纷案例 | 3 |
| 劳动争议案例 | 2 |
| 侵权纠纷案例 | 2 |
| 合同解除案例 | 1 |
| 诉讼时效案例 | 1 |

## 示例输出

### 文本格式

```bash
$ python3 search_cases.py 劳动合同

找到 2 个匹配案例（显示前 2 个）

============================================================
案例 4: 未签书面劳动合同双倍工资案
============================================================
分类: 劳动争议案例

案情简介：张某入职某公司工作，公司未与张某签订书面劳动合同，工作6个月后张某离职。张某要求公司支付未签书面劳动合同的双倍工资差额。

争议焦点：未签书面劳动合同是否应支付双倍工资？

裁判观点：根据《劳动合同法》第八十二条，用人单位自用工之日起超过一个月不满一年未与劳动者订立书面劳动合同的，应当向劳动者每月支付二倍的工资。公司应向张某支付第2个月至第6个月的双倍工资差额。

法律依据：- 《劳动合同法》第八十二条 - 《劳动合同法实施条例》第六条、第七条

实务要点：1. 用人单位应自用工之日起一个月内与劳动者签订书面劳动合同 2. 双倍工资最多支持11个月（第2个月至第12个月） 3. 劳动者需保留工资发放记录、工作证、考勤记录等证据
```

### JSON 格式

```bash
$ python3 search_cases.py -f json -n 1 格式条款

[
  {
    "number": "1",
    "title": "格式条款无效案",
    "category": "民事纠纷案例",
    "facts": "张某与某健身公司签订健身会员合同，合同中约定\"会员卡一经售出，概不退换\"。后因健身公司经营不善倒闭，张某要求退还剩余费用，健身公司以合同条款为由拒绝。",
    "issue": "格式条款中\"概不退换\"的约定是否有效？",
    "view": "根据《民法典》第四百九十七条，格式条款中提供方不合理地免除其责任、排除对方主要权利的，该条款无效。\"概不退换\"条款排除了消费者的主要权利，应当认定无效。健身公司应退还张某剩余费用。",
    "basis": "- 《民法典》第四百九十七条 - 《消费者权益保护法》第二十六条",
    "points": "1. 遇到不公平格式条款，可主张无效 2. 重点关注\"最终解释权\"、\"概不退换\"等排除消费者权利的条款 3. 格式条款的提供方有提示和说明义务"
  }
]
```

## 注意事项

1. 案例库位于 `references/case-studies.md`
2. 搜索不区分大小写
3. 关键词匹配会根据字段给予不同权重（标题 > 焦点/观点 > 其他内容）
4. 如需添加新案例，请编辑 `references/case-studies.md` 文件

## 在 Agent 中使用

```python
# 示例：在 Agent 代码中调用案例检索
import subprocess
import json

def search_case(query, category=None):
    """搜索相关案例"""
    cmd = ['python3', 'search_cases.py', '--format', 'json']
    if category:
        cmd.extend(['--category', category])
    cmd.append(query)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        cases = json.loads(result.stdout)
        return cases
    return []
```
