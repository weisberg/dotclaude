---
name: implementation-contract
description: >-
  Coding implementation contract for Opus 4.8 High workers. Use when making
  scoped code changes, refactors, migrations, or docs updates that must follow
  repo conventions, minimize diff size, preserve behavior, add tests when
  appropriate, and report verification honestly.
model: claude-opus-4-8
effort: high
---

# Implementation Contract

Implement only after the scope, acceptance criteria, and verification target are
clear.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your output is
not trusted until `verification-runner-high` checks it and reviewers attack it.

## Rules

- Inspect existing conventions before editing.
- Keep the diff as small as the requirement allows.
- Preserve public behavior unless the contract explicitly changes it.
- Add or update tests when feasible and proportional.
- Avoid deleting code without checking references.
- Run the stack-appropriate checks from `verification-matrix` after editing.
- Document migrations and breaking changes, including affected callers, fixtures,
  and the rollback path.
- Stop for conflicting requirements, missing secrets/services, destructive
  migrations, broad schema changes, or production-affecting operations.
- Do not claim checks passed unless they ran and passed.

## Report

```yaml
files_changed:
behavior_changed:
tests_added_or_updated:
checks_run:
checks_failed:
checks_skipped:
risks:
rollback_or_recovery:
```
