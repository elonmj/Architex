---
description: 'Validate active workspace documents and produce a keep or merge or retire decision report.'
name: validate-active-docs
argument-hint: '[scope, folder, or file list]'
agent: agent
---

Validate the active documents for: ${input:scope:workspace root}

Use [documentation rules](../instructions/documentation.instructions.md).

Requirements:

- Treat `Arch Noé/` as archive unless explicitly requested.
- Classify each source as text-validated, partially validated, or pending extraction.
- Compare cleaned notes against raw sources when both exist.
- Produce: scope, source table, aligned points, contradictions, gaps, decisions, next actions.
- Never claim a PDF was reviewed textually unless its content was actually extracted.
