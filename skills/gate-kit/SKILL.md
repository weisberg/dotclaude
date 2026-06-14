---
name: gate-kit
description: >-
  Gate vocabulary and runner support for ultracode-high. Use to define
  precondition and completion gates, prefer deterministic command/file/grep
  gates where possible, flag attestation gates honestly, and run gates with the
  bundled gate_check.py helper.
model: claude-opus-4-8
effort: high
---

# Gate Kit

A manifest item without a checkable completion criterion is a wish, not a step.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your gates are
the mechanical spine that keeps workers and verifiers from self-grading.

## Gate types

- `command`: shell command must exit 0. Best for tests, builds, SQL/dbt checks,
  data reconciliation, file validation, and scripts.
- `file_exists`: required path must exist.
- `grep`: pattern must appear in the target file. Set `"negate": true` to assert
  the pattern must NOT appear (for example, no leftover secret or `TODO`).
- `attest`: structured judgment. Use only when no mechanical gate exists, and
  surface every attestation gate in the final report.

## Gate row

```json
{
  "id": "unit-test",
  "type": "command",
  "cmd": "npm test -- --runInBand",
  "description": "Unit test suite passes"
}
```

See `references/gates.schema.json` for the schema and run gates with:

```bash
python skills/gate-kit/scripts/gate_check.py path/to/gates.json
```

A runnable example covering every gate type (including a negated grep) lives at
`references/example-gates.json`; from the repo root it passes with exit 0 and
doubles as a smoke test for the runner:

```bash
python skills/gate-kit/scripts/gate_check.py skills/gate-kit/references/example-gates.json
```

Exit codes: `0` all gates passed; `1` at least one gate genuinely failed (the
work did not meet a gate, including an attestation gate without an explicit
passing answer); `2` the manifest or a gate is malformed (a configuration or
runner problem, reported with gate status `error`). The runner fails closed, so a
typo in a gate can never read as a clean pass.
