---
name: high-code-review
description: >-
  Fork-style adversarial review workflow for the current diff or a proposed code
  change. Use to find correctness, regression, security, performance,
  maintainability, test, and documentation issues before final delivery.
model: claude-opus-4-8
effort: high
context: fork
---

# High Code Review

Review as a code reviewer. Findings first, summaries second.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your findings
are not prose polish; they are candidate blockers with mechanisms and checks.

## Finding card

```yaml
severity: critical | high | medium | low | suggestion
file:
line:
mechanism:
impact:
recommendation:
verification:
```

Prefer fewer, verified findings over broad speculation. If no issues are found,
say so and name residual test gaps.
