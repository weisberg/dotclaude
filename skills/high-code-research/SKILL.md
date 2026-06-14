---
name: high-code-research
description: >-
  Fork-style read-only repository exploration workflow for Opus 4.8 High. Use
  when a task needs isolated codebase research, architecture mapping, dependency
  tracing, or risk discovery without editing files.
model: claude-opus-4-8
effort: high
context: fork
---

# High Code Research

Explore without editing. Return a compact map, not raw search logs.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your output
usually feeds the orchestrator, implementer, plan critic, or final integrator.

## Output

```yaml
objective:
files_read:
architecture_map:
relevant_paths:
dependencies:
risks:
unknowns:
recommended_next_steps:
```

Use `rg`/`rg --files` first. Cite file paths and line numbers when useful.
