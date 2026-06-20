---
name: fixed-official-document-writer
description: Use when Codex needs to draft,整理, rewrite, standardize, or format fixed Chinese work-document types such as 事项跟踪单, 会议纪要, fixed-format internal reports, Word-ready official materials, or recurring enterprise/government-style templates with stable fields, structure, tone, and layout.
---

# Fixed Official Document Writer

## Purpose

Create or整理 fixed-format Chinese work documents where the document type is stable and the expected structure matters more than free-form writing. Keep the user-facing material practical, concise, and Word-ready.

This skill is for recurring document types such as:

- 事项跟踪单
- 会议纪要
- Other fixed templates the user later adds

When the task also needs `.docx` creation, editing, or visual layout verification, use the Documents skill and the user's official-document layout skill as needed.

## Workflow

1. Identify the document type from the user's request or source material.
2. Read only the matching reference file:
   - 事项跟踪单: `references/matters-tracking-sheet.md`
   - 会议纪要: `references/meeting-minutes.md`
3. Extract or ask for only missing high-impact facts: meeting time, participants, matter owner, deadlines, decisions, next steps.
4. Draft in the fixed structure. Do not invent concrete facts such as dates, attendees,责任人, or deadlines.
5. Normalize wording into concise Chinese office style:
   - Prefer clear subject-verb-object sentences.
   - Use numbered items for actions and follow-ups.
   - Avoid empty slogans, rhetorical flourishes, and vague praise.
6. If outputting Word, apply official-document-style formatting:
   - A4 portrait, suitable margins, Chinese body font, fixed line spacing.
   - Keep fields, tables, and numbered items scannable.
   - Render-check the final document when feasible.

## Decision Rules

- If source facts are incomplete but the structure is clear, leave bracketed placeholders such as `【责任人】` or `【完成时限】` instead of fabricating.
- If the user provides rough notes, reorganize them into the target format while preserving substance.
- If the user asks only for text, return clean Markdown or plain text ready to paste into Word.
- If the user asks for a Word file, create `.docx` and verify the layout.
- If the user asks to "按模板" and provides a file, treat that file as the source of truth over the references.

## Output Quality Checklist

Before responding, check:

- The document type matches the requested fixed format.
- Required fields are present or clearly marked as placeholders.
- Matters, decisions, owners, and deadlines are not mixed together.
- Language is concise, specific, and suitable for internal official work materials.
- Formatting is Word-ready, with no casual chat phrasing left in the final text.
