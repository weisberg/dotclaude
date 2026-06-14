---
name: high-code-verify
description: >-
  Fork-style verification workflow for running or planning lint, typecheck,
  tests, builds, dbt checks, and other project validation commands. Use to return
  compact verification cards without polluting the main context with logs.
model: claude-opus-4-8
effort: high
context: fork
---

# High Code Verify

Run the narrowest useful checks. Do not claim success for skipped commands.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your output
should be compact enough for the main context and precise enough to reproduce.

## Output

```yaml
checks:
  - command_or_method:
    gate_type: command | file_exists | grep | attest
    status: passed | failed | skipped | not-applicable
    evidence:
    failure_summary:
    next_action:
overall_status:
```

Summarize failures. Include raw logs only when needed to reproduce the issue.
