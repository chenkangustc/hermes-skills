#!/usr/bin/env python3
"""
公文PDF生成器 — 按用户提供的7条铁律排版规范生成PDF。
使用 reportlab，注册已安装的公文字体。

Usage:
    python3 gongwen_pdf.py -o output.pdf  # 交互式输入内容
    # 或作为模块导入使用
"""
import sys, os, argparse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 注册公文字体（本服务器路径） ──────────────────────────
FONT_DIR = "/usr/share/fonts/truetype/gongwen"

# 方正小标宋简体 — 公文标题用
pdfmetrics.registerFont(TTFont(
    "FZXiaoBiaoSong",
    os.path.join(FONT_DIR, "方正小标宋体.TTF")
))
# 仿宋_GB2312 — 正文用
pdfmetrics.registerFont(TTFont(
    "FangSong_GB2312",
    os.path.join(FONT_DIR, "SIMFANG_0.TTF")
))
# 楷体_GB2312 — 二级标题用
pdfmetrics.registerFont(TTFont(
    "KaiTi_GB2312",
    os.path.join(FONT_DIR, "SIMKAI_0.TTF")
))
# 黑体替代（Noto Sans CJK SC Bold）
pdfmetrics.registerFont(TTFont(
    "HeiTi",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
))
# Times New Roman
pdfmetrics.registerFont(TTFont(
    "TimesNewRoman",
    "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"
))

# ── 页面设置（GB/T 9704-2012） ────────────────────────────
LM, RM, TM, BM = 28*mm, 26*mm, 37*mm, 35*mm  # 左/右/上/下

# ── 样式定义 ──────────────────────────────────────────────

def _make_style(name, font, size, leading, align=TA_JUSTIFY, indent=0, bold=False):
    return ParagraphStyle(
        name, fontName=font, fontSize=size, leading=leading,
        alignment=align, firstLineIndent=indent,
        spaceBefore=0, spaceAfter=0,
    )

S_TITLE = _make_style("title", "FZXiaoBiaoSong", 22, 38, align=TA_CENTER)  # 公文标题 22pt 居中
S_H1    = _make_style("h1", "HeiTi", 16, 30, indent=32)                   # 一级标题 黑体 16pt 缩进2字符
S_H2    = _make_style("h2", "KaiTi_GB2312", 16, 28, indent=32)             # 二级标题 楷体 16pt 加粗
S_BODY  = _make_style("body", "FangSong_GB2312", 16, 28, indent=32)        # 正文 仿宋 16pt 缩进2字符
S_SIGN  = _make_style("sign", "FangSong_GB2312", 16, 28, align=TA_RIGHT)   # 署名/日期 右对齐
S_LABEL = _make_style("label", "FangSong_GB2312", 16, 28)                   # 分送/附件 左对齐顶格

# ── 辅助函数 ──────────────────────────────────────────────

def title(text):
    """公文标题"""
    return Paragraph(text, S_TITLE)

def h1(text):
    """一级标题（一、）"""
    return Paragraph(f"<b>{text}</b>", S_H1)

def h2(text):
    """二级标题（（一））"""
    return Paragraph(f"<b>{text}</b>", S_H2)

def body(text):
    """正文"""
    return Paragraph(text, S_BODY)

def signature(text):
    """署名/日期"""
    return Paragraph(text, S_SIGN)

def label(text):
    """分送/附件标签"""
    return Paragraph(text, S_LABEL)

def spacer(pt=14):
    """间距（公文中用行距控制，一般不需要额外间距）"""
    return Spacer(1, pt)


def build_pdf(content, output_path, title_meta=""):
    """
    生成公文PDF。

    Args:
        content: list of flowables (Paragraph, Spacer, Table, etc.)
        output_path: 输出PDF路径
        title_meta: PDF元数据标题
    """
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
        title=title_meta or "公文",
    )
    doc.build(content)
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="公文PDF生成器")
    parser.add_argument("-o", "--output", default="/tmp/公文.pdf", help="输出PDF路径")
    args = parser.parse_args()

    # 示例：生成一份测试文档
    content = [
        title("关于XXXX工作的报告"),
        spacer(),
        h1("一、工作背景"),
        body("根据上级部门工作部署，我单位深入开展相关工作，现将有关情况报告如下。"),
        h1("二、主要工作"),
        h2("（一）组织管理"),
        body("建立健全工作机制，成立专项工作领导小组，明确职责分工。"),
        h2("（二）工作成效"),
        body("各项工作稳步推进，取得了阶段性成果。"),
        h1("三、下一步计划"),
        body("继续加大工作力度，确保各项任务按期完成。"),
        spacer(28),
        signature("XXXX单位"),
        signature("2025年6月17日"),
    ]
    build_pdf(content, args.output)
    print(f"✅ 公文PDF已生成: {args.output}")
