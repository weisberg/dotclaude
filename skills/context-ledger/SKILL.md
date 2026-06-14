---
name: context-ledger
description: >-
  Compact task-state and handoff ledger for long Opus 4.8 High sessions,
  subagent orchestration, compaction, and resumable workflows. Use to preserve
  decisions, files, commands, evidence, risks, and next actions while dropping
  noisy logs.
model: claude-opus-4-8
effort: high
---

# Context Ledger

Maintain this at phase boundaries, before compaction, and before handoff.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your ledger is
the defense against long-session constraint decay and compaction loss.

```yaml
objective:
constraints:
scope:
files_read:
files_touched:
commands_run:
decisions_made:
assumptions:
verified:
failed_or_skipped_checks:
open_risks:
next_actions:
handoff_prompt:
```

Keep it compact, factual, and restartable. Do not include raw logs unless a
failure cannot be understood without them.
