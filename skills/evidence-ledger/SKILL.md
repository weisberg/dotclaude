---
name: evidence-ledger
description: >-
  Evidence, claim, assumption, and uncertainty ledger for high-rigor agent work.
  Use when synthesizing research, analytics, code review, strategy, or writing so
  important claims are labeled as verified, calculated, inferred, assumed, or
  unknown with source evidence.
model: claude-opus-4-8
effort: high
---

# Evidence Ledger

Track the status of important claims before they enter the final answer.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your ledger is
how the integrator separates facts from assumptions and decides what must be
relayed to the user.

## Claim labels

- `VERIFIED`: directly observed in a file, command output, source, test, or doc.
- `CALCULATED`: computed from inspected inputs with reproducible logic.
- `INFERRED`: best interpretation from evidence, not directly proven.
- `ASSUMPTION`: accepted default or user-provided premise not verified.
- `UNKNOWN`: material fact not resolved.

## Ledger row

```yaml
claim:
label:
evidence:
source_path_or_method:
confidence:
decision_impact:
needs_relay_to_user: true | false
```

Surface high-impact assumptions and unknowns in the final answer.
