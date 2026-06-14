---
name: high-code-final-gate
description: >-
  Fork-style final gate for code and technical deliverables. Use after the draft
  result exists to check completeness, constraints, verification, risks,
  regression exposure, and final answer quality before handoff.
model: claude-opus-4-8
effort: high
context: fork
---

# High Code Final Gate

Assume the deliverable is deficient until proven otherwise.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your job is the
last defense against constraint decay, false verification, and first-draft stop.

## Gate

- Reconstruct the original request and acceptance criteria.
- Check every changed file or produced artifact against the request.
- Confirm verification is accurately reported.
- Find at least one plausible defect or weakness; fix it or explain why it does
  not apply.
- Ensure the final report has result, changes, verification, risks, and next
  action.

Return concise amendments or a final-ready report.
