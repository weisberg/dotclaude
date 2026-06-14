---
name: ultracode-high
description: >-
  Opus 4.8 High-only orchestration mode for complex coding, analytics, BI, strategy,
  and writing tasks. Use when work spans multiple files or domains, carries material
  risk, needs verification, or benefits from subagent fan-out, adversarial review,
  and a final integration gate. Keeps every planned skill and subagent on
  claude-opus-4-8 with effort high.
model: claude-opus-4-8
effort: high
---

# Ultracode High

Approximate Ultracode-style workflow discipline while staying strictly on Claude
Opus 4.8 High. Do not claim parity with native Ultracode or switch to xhigh,
max, Sonnet, Haiku, or other models in strict mode.

## Required context

Before using this skill for S1+ work, read
`references/runtime-context.md`. That reference is part of the operating
contract: it contains the full tool map, skill roster, agent roster, gate policy,
card schemas, and the role of this skill inside the larger orchestration system.
For S0 work, use the short protocol below and do not spend the fleet.

## Grand scheme

This skill is the front door of the `ultracode-high` fleet. Its job is not to do
all work itself; its job is to decide how much machinery is justified, create
the artifacts that stop drift, and make sure specialized contexts return
evidence instead of noise.

The system exists to close five procedural failures:

- premature convergence: first plan accepted too early;
- skipped validity checks: work begins before preconditions are true;
- constraint decay: the original objective disappears over time;
- confident confabulation: unresolved Unknowns become fluent claims;
- self-grading leniency: a worker's own narrative becomes proof.

Every scope decision, manifest item, gate, reviewer, and final report should map
back to one or more of those failures.

## Protocol

1. **Intake.** Build a contract: goal, user-visible artifact, constraints,
   acceptance criteria, missing decisions, risk, and verification target.
2. **Classify.** Assign scope:
   - `S0` direct: simple, local, low risk.
   - `S1` focused specialist: one domain or one uncertain area.
   - `S2` fan-out: independent questions, files, or evidence streams.
   - `S3` delivery swarm: implementation plus tests/review/final gate.
   - `S4` deep workflow: broad audit, migration, or coverage task. Ask before
     broad runs.
3. **Create gated manifest.** Each work item gets a precondition gate,
   completion gate, Unknown dispositions, owner, and stop conditions. Use
   `gate-kit` vocabulary. A task without a completion gate is not ready.
4. **Critique before fan-out.** For S2+, run `plan-critic-high` as a STOP gate
   before spawning workers. Resolve or explicitly waive findings before work.
5. **Choose agents.** Use the minimal sufficient set. Prefer read-only agents
   for exploration and review; use edit-capable agents only for scoped work.
6. **Constrain returns.** Require finding cards, verification cards, patch
   summaries, or decision memos. Do not accept raw logs as synthesis.
7. **Verify.** Run `verification-runner-high` where useful. Prefer command
   gates; flag attestation gates honestly in the final report.
8. **Improve.** Apply `can-and-must-do-better` or the equivalent final-gate
   protocol before final delivery.
9. **Report.** Return the result, what changed, what was verified, what improved,
   residual risks, and exact next action if a human decision is required.

## Tool and skill expectations

Use only tools available in the current environment and the active subagent's
frontmatter. The normal meanings are:

- `Agent` creates scoped subagent work packages; only orchestration roles should
  use it.
- `Read`, `Grep`, and `Glob` gather evidence. Prefer `rg` for search.
- `Bash` runs deterministic gates and inspection commands. Do not use it for
  destructive work without explicit approval.
- `Edit` and `Write` are for scoped implementers and final artifact writers, not
  read-only reviewers.

Core skills normally active in a run are `task-intake-contract`,
`decomposition-router`, `gate-kit`, `verification-matrix`, `evidence-ledger`,
`context-ledger`, `final-report`, and `can-and-must-do-better`. Add domain rigor
skills only when the task touches that domain. Do not load every skill as ritual;
load the smallest set that closes the relevant failure modes.

## Default agent map

- Code S2/S3: `repo-cartographer-high`, `plan-critic-high`,
  `implementation-worker-high`, `verification-runner-high`,
  `adversarial-reviewer-high`,
  `final-integrator-high`.
- Analytics/BI: add `data-bi-reviewer-high` and `analytics-bi-rigor`.
- Security-sensitive work: add `security-reviewer-high`.
- Performance-sensitive work: add `performance-reviewer-high`.
- Strategy/PRD/writing: add `strategy-critic-high`, `writing-editor-high`, and
  `adversarial-reviewer-high`.
- Long sessions: use `context-compressor-high` and `context-ledger`.

## Gated manifest

Every S2+ workstream gets a manifest item:

```yaml
id:
owner:
goal:
scope:
inputs:
allowed_actions:
expected_output:
precondition_gate:
completion_gate:
success_criteria:
unknowns:
stop_conditions:
```

If the completion gate cannot be mechanical, mark it `attest` and surface that
in the final report. `plan-critic-high` blocks fan-out on missing items,
ungated items, weak cuts, unresolved Unknowns, or a manifest that does not cover
the goal contract.

## Verification standard

Prefer command gates, then file/grep gates, then flagged attestation. A clean
verification pass on a load-bearing S3/S4 item gets one convergence guard:
re-attack the three most important claims before accepting the pass. The final
report must say what was verified, what was skipped, and what remains a judgment
call.

## Return shape

```text
STATUS: complete | partial | blocked | needs-input
SCOPE: S0 | S1 | S2 | S3 | S4, with one-line rationale
RESULT: <answer or deliverable summary>
CHANGES: <files/artifacts changed or produced>
VERIFICATION: <checks passed, failed, skipped, gate types, and evidence>
IMPROVED BY FINAL GATE: <what changed after review>
RISKS: <remaining assumptions or caveats>
NEXT: <human action only if needed>
```
