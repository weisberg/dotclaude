---
name: final-report
description: >-
  Final response contract for ultracode-high and high-rigor subagent workflows.
  Use to synthesize work into a relayable result with changes, verification,
  final-gate improvements, risks, and next actions.
model: claude-opus-4-8
effort: high
---

# Final Report

The final answer is the product. Lead with the answer, not the process.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your output is
the only thing the user can safely act on, so carry verification, caveats, and
attestation labels forward.

## Shape

```text
RESULT: <answer, recommendation, or deliverable summary>
CHANGES: <files/artifacts changed or produced>
VERIFICATION: <checks passed, failed, skipped, gate types, with evidence>
IMPROVED BY FINAL GATE: <specific changes made after critique>
RISKS: <decision-changing assumptions, caveats, or unknowns>
NEXT: <only if human action is required>
```

## Gate-results table

For S2+ work, render `VERIFICATION` as a table so measured and judged checks are
distinguishable at a glance, with every attestation row flagged:

| check | gate_type | status | evidence |
|---|---|---|---|
| unit tests | command | passed | `npm test` exit 0 |
| metric reconciles to source of truth | command | passed | recon query diff = 0 |
| narrative reads clearly for the audience | attest (flagged) | passed | editor judgment |

A high attestation ratio on code/data work is a signal that the task was
under-specified, not that it was thoroughly verified.

## Rules

- Do not claim verification that did not run.
- Surface the command-vs-attest gate mix for S2+ work. Attestation is allowed,
  but it must not masquerade as mechanical verification.
- Distinguish result from remaining risk.
- Include file paths when artifacts were created or edited.
- Keep raw logs out unless the user asked for them.
- For blocked work, include the smallest concrete question or artifact needed.
