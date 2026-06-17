---
name: gongwen-paiban
description: "中国公文排版规范（7条铁律）：字体、字号、页面设置、行距、页边距等全套规范。用户提到'公文'、'排版'、'正式文件'、'红头文件'时自动加载。"
version: 1.1.0
author: Hermes Agent
license: MIT
---

# 公文排版规范

当用户要求**生成公文、报告、正式文件**时，必须严格遵循以下规范。

## 一、字体与字号

| # | 元素 | 字体 | 字号 | 加粗 | 对齐/缩进 |
|---|------|------|------|------|-----------|
| 1 | 公文标题 | 方正小标宋简体 | 22pt | ❌ 不加粗 | **居中** |
| 2 | 一级标题（一、） | 黑体 | 16pt | ❌ 不加粗 | 首行缩进2字符 |
| 3 | 二级标题（（一）） | 楷体_GB2312 | 16pt | ✅ **加粗** | 首行缩进2字符 |
| 4 | 正文 | 仿宋_GB2312 | 16pt | — | 首行缩进2字符 |
| 5 | 西文/数字 | Times New Roman | 随中文 | — | — |
| 6 | 引号 | 中文全角 `"…"` | — | — | — |
| 7 | 系统字体 | 已安装（除黑体用文泉驿正黑替代） | — | — | — |

> **本服务器字体状态：** 方正小标宋简体 ✅ / 仿宋_GB2312 ✅ / 楷体_GB2312 ✅ / 黑体 ❌ 用文泉驿正黑 (wqy-zenhei.ttc) 替代 / Times New Roman ✅。详见 `references/公文排版规范.md`

## 二、页面设置

- **纸张：** A4（21.0 × 29.7 cm）
- **页边距：** 上 3.7cm / 下 3.5cm / 左 2.8cm / 右 2.6cm
- **行距：** **28 磅固定值**
- **首行缩进：** **32pt**（= 2 字符 @ 16pt）

## 三、其他元素格式

| 元素 | 字体 | 字号 | 对齐 |
|------|------|------|------|
| 署名 | 仿宋_GB2312 | 16pt | **右对齐** |
| 日期 | 仿宋_GB2312 | 16pt | **右对齐** |
| 分送 | 仿宋_GB2312 | 16pt | 左对齐，顶格 |
| 附件标签 | 仿宋_GB2312 | 16pt | 左对齐 |

## 四、生成方式

有两种方式生成公文，按需选择：

### 方式 A：python-docx（生成 .docx）

适用于用户需要可编辑的 Word 文档。使用 python-docx 库设置中西文分设字体。

```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn

def set_run_font(run, western="Times New Roman", eastern="仿宋_GB2312", size=16, bold=False):
    """中西文分设字体"""
    run.font.name = western
    run.font.size = Pt(size)
    run.bold = bold
    run.element.rPr.rFonts.set(qn('w:eastAsia'), eastern)

def set_page_margins(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3.7)
    section.bottom_margin = Cm(3.5)
    section.left_margin = Cm(2.8)
    section.right_margin = Cm(2.6)

def set_line_spacing(paragraph, spacing_pt=28):
    pf = paragraph.paragraph_format
    pf.line_spacing = Pt(spacing_pt)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY

def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_line_spacing(p)
    run = p.add_run(text)
    set_run_font(run, eastern="方正小标宋简体", size=22)

def add_heading1(doc, text):
    p = doc.add_paragraph()
    set_line_spacing(p)
    p.paragraph_format.first_line_indent = Pt(32)
    run = p.add_run(text)
    set_run_font(run, eastern="黑体", bold=False)

def add_heading2(doc, text):
    p = doc.add_paragraph()
    set_line_spacing(p)
    p.paragraph_format.first_line_indent = Pt(32)
    run = p.add_run(text)
    set_run_font(run, eastern="楷体_GB2312", bold=True)

def add_body(doc, text):
    p = doc.add_paragraph()
    set_line_spacing(p)
    p.paragraph_format.first_line_indent = Pt(32)
    run = p.add_run(text)
    set_run_font(run, eastern="仿宋_GB2312")

def add_signature(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_line_spacing(p)
    run = p.add_run(text)
    set_run_font(run, eastern="仿宋_GB2312")
```

### 方式 B：reportlab（生成 .pdf）

适用于直接输出 PDF。使用 `scripts/gongwen_pdf.py` 脚本（本 skill 自带）。

```python
# 快速使用
from scripts.gongwen_pdf import title, h1, h2, body, signature, spacer, build_pdf

content = [
    title("公文标题"),
    spacer(),
    h1("一、章节"),
    body("正文内容..."),
    h2("（一）小节"),
    body("正文内容..."),
    signature("署名"),
    signature("日期"),
]
build_pdf(content, "/tmp/output.pdf")
```

也可直接运行脚本生成示例：
```bash
python3 ~/.hermes/skills/productivity/gongwen-paiban/scripts/gongwen_pdf.py -o /tmp/公文.pdf
```

> ⚠️ **重要：** 本服务器已安装方正小标宋简体、仿宋_GB2312、楷体_GB2312 字体，位于 `/usr/share/fonts/truetype/gongwen/`。黑体缺失，使用文泉驿正黑 (wqy-zenhei.ttc) 替代。详见 `references/公文排版规范.md` 的字体映射表。重装字体流程见 `references/字体安装流程.md`。

## 五、重要提醒

1. **字体已安装：** 方正小标宋简体、仿宋_GB2312、楷体_GB2312 均已从用户提供的字体包安装。**黑体** 缺失，使用文泉驿正黑 (wqy-zenhei.ttc) 替代。
2. **生成 PDF 时：** 使用 reportlab，先通过 `fc-list` 确认字体路径后注册，用映射表中的实际字体名。
3. **reportlab TTC 兼容性陷阱：** Noto Sans CJK 系列 (.ttc) 使用 PostScript 轮廓，**reportlab 不支持**。遇到 `TTFError: postscript outlines are not supported` 时，改用文泉驿正黑 (wqy-zenhei.ttc) 或文泉驿微米黑 (wqy-microhei.ttc) 替代。单个 .ttf 文件（方正小标宋、仿宋、楷体）无此问题。
4. 斜体/倾斜：公文中**一律不使用**斜体。
5. 用户说"公文排版"、"正式文件"、"红头文件"、"写公文"、"生成报告"等关键词时，**必须加载本 skill**。
6. **已整合：** 本 skill 已合并原 `gongwen-format` 的内容（reportlab PDF 生成脚本）。
