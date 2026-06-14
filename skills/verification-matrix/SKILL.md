---
name: verification-matrix
description: >-
  Standard verification gates for code, analytics, BI, writing, strategy, and
  documentation deliverables. Use before final delivery and inside review or
  test-runner subagents to record passed, failed, skipped, and not-applicable
  checks with evidence.
model: claude-opus-4-8
effort: high
---

# Verification Matrix

Verification is evidence, not confidence.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your job is to
turn "looks good" into passed, failed, skipped, or attested checks with evidence.

Prefer `command` gates from `gate-kit` for mechanically checkable work. Use
`attest` only where no command/file/grep gate is realistic, and label those
checks as attestation in the final report.

## Verification card

```yaml
check:
command_or_method:
gate_type: command | file_exists | grep | attest
status: passed | failed | skipped | not-applicable
summary:
evidence:
failure_details:
next_action:
```

## Common checks

- JavaScript/TypeScript: package manager detection, lint, typecheck, tests, build.
- Python: pytest, ruff, mypy/pyright when configured.
- SQL/dbt: compile, tests, row counts, freshness, reconciliation queries.
- Frontend: build, component tests, accessibility states, snapshot checks,
  responsive smoke check.
- APIs: unit tests, contract tests, route coverage, auth and error-path checks.
- Analytics/BI: grain, joins, filters, nulls, freshness, metric definition, totals.
- Writing/docs: structure and consistency (attest), factual support (attest,
  flagged), link checks when feasible.
- Strategy: customer/problem/decision clarity, options, evidence, risks, and
  success metrics (attest, flagged).
- UX/dashboard: first-screen answer, hierarchy, accessibility, filter defaults,
  and misread risks (attest, flagged).

Never hide unavailable checks. Mark them skipped and state the blocker.
