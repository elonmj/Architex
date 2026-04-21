---
name: document-validation
description: 'Validate markdown notes, transcripts, PDFs, project briefs, and research documents. Use for source inventory, consistency checks, canonical-source selection, gap analysis, and report writing in documentation-heavy workspaces.'
argument-hint: '[scope, folder, or file list]'
---

# Document Validation

## When To Use

- You need to validate active project documents before planning or implementation.
- You have both a cleaned note and a raw transcript and must decide which one is canonical.
- You need a report that states what was actually verified and what remains unverified.

## Procedure

1. Define the active scope and explicitly exclude archive folders unless the user requests them.
2. Inventory all candidate sources and classify them as text-validated, partially validated, or pending extraction.
3. Compare structured notes against raw sources to detect omissions, contradictions, and wording drift.
4. Extract the operating problem, retained MVP, target users, delivery target, and immediate next actions.
5. Record gaps separately from contradictions. A missing success metric is a gap, not a contradiction.
6. End with a keep, merge, retire, or follow-up decision for each source.

## Output Shape

- Scope
- Sources table
- Aligned points
- Contradictions
- Gaps
- Decisions
- Next actions

## Guardrails

- Never claim a PDF was reviewed textually unless its content was actually extracted.
- Prefer one canonical document plus one evidence source, rather than many competing summaries.
