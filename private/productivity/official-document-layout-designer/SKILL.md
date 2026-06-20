---
name: official-document-layout-designer
description: Use when Codex needs to format, clean up, or visually QA Chinese official-document-style Word files, government/enterprise report drafts, PPT speaking outlines in .docx, or materials that should follow gongwen layout conventions. Trigger when the user asks for 公文排版, 公文格式, 按公文排版, 汇报稿排版, Word排版核对, 主逻辑红色, 总结句蓝色, or asks to fix document layout after editing a Chinese report.
---

# Official Document Layout Designer

## Source Of Truth

Prefer the user's existing Hermes skill for official Chinese document formatting:

- Core quick reference: `/tmp/公文排版核心规则.md`
- Full Hermes skill: `/Users/chenkang/.hermes/skills/productivity/chinese-formal-documents/SKILL.md`

When available, read `/tmp/公文排版核心规则.md` first and follow it over this file. If deeper examples, scripts, or templates are needed, read the full Hermes skill. This Codex skill is only a trigger and bridge so that requests like "公文排版" use the same rules the user already established in Hermes.

## Core Behavior

Format Chinese `.docx` report drafts as serious official-document-style working materials. Preserve the user's content and structure unless they explicitly ask for rewriting. Treat layout consistency, color rules, and render verification as part of the task, not optional polish.

When working with `.docx`, also use the Documents skill if available.

## Workflow

1. Identify the active target document from the user's wording and current workspace.
2. Make a timestamped or clearly named backup before editing.
3. Inspect the document structure: page markers such as `P13`, headings, `主逻辑：`, `总结句：`, action items, and body paragraphs.
4. Apply formatting rules consistently across the whole document, especially newly inserted sections.
5. Render the document to page images in a temporary directory and inspect representative pages, including changed pages and pages after the changed region.
6. Reopen or point to the final document. Mention any skipped verification only if rendering fails.

## Formatting Rules

Use these defaults unless `/tmp/公文排版核心规则.md` or the full Hermes skill says otherwise:

- Page: A4 portrait.
- Page margins: top 3.7 cm, bottom 3.5 cm, left 2.8 cm, right 2.6 cm.
- Body Chinese font: `仿宋_GB2312` or `仿宋` if the former is unavailable.
- English and numbers: `Times New Roman` via `w:ascii` and `w:hAnsi`; Chinese via `w:eastAsia`.
- Body size: 16 pt, equivalent to 三号 in many Word setups.
- Line spacing: fixed 30 pt.
- Alignment: justified.
- Paragraph spacing: 0 pt before and after.
- Body paragraphs: first-line indent 2 Chinese characters.
- Page markers such as `P13`: small bold marker, usually 14 pt.
- Section/page titles: `黑体`, 16 pt, not bold unless the Hermes rule says otherwise.
- Body text: not bold.
- Do not leave newly inserted text in default Calibri/Times styling.

## Color Rules

These rules are strict for the user's report-outline workflow:

- For `主逻辑：...`, the label `主逻辑` is black and bold; the content after the label is red.
- For `总结句：...`, the label `总结句` is black and bold; the content after the label is blue.
- Body text should normally be black unless the user asks for emphasis.
- Checklist helper lines such as `【问题】【行动】【效果】` should follow the body font unless the surrounding document intentionally uses another convention.

## Content Hygiene

- Do not rewrite substance while formatting.
- If a newly split page lacks a `总结句：`, add a concise one only when the surrounding structure clearly requires every page to have one.
- Keep page-marker sequencing coherent after inserting or splitting sections.
- When a Word page count differs from internal PPT page markers like `P13`, preserve the internal markers and explain only if relevant.
- Avoid adding output folders in the user's workspace. Use `/tmp` for render checks unless the user asks to keep rendered previews.

## Verification Checklist

Before final response, check:

- Changed pages and following pages have consistent font, size, spacing, and indentation.
- `主逻辑` label is black and bold; its content is red.
- `总结句` label is black and bold; its content is blue.
- Newly inserted sections do not use default fonts.
- Page markers and headings remain in order.
- Rendered pages are readable and not obviously clipped or garbled.
