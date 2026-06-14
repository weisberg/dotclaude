# Ultracode High Runtime Context

Use this reference when running any `ultracode-high` skill or subagent. It gives
the fleet-level context that individual role prompts should not have to
reconstruct from memory.

## What the system is trying to do

`ultracode-high` is a Claude Code orchestration mode for users who want
Ultracode-style behavior while staying strictly on Claude Opus 4.8 with
`effort: high`. It does not claim to match native Ultracode's reasoning budget.
Its claim is procedural: many misses in long agentic work come from workflow
failure, not raw inability, so the workflow can be compiled into skills,
subagents, gates, ledgers, and final review.

The product should feel like a temporary senior delivery team:

- an orchestrator frames and routes the work;
- a plan critic attacks the manifest before anyone spends time executing it;
- specialists work in isolated contexts;
- a verification runner checks results against ground truth where possible;
- adversarial reviewers attack what gates cannot prove;
- a final integrator resolves conflicts, re-reads constraints, and ships one
  coherent answer.

The final answer is the product. Raw logs, partial agent notes, and worker
confidence are not deliverables unless they are converted into evidence,
findings, verification cards, or user-facing risks.

## The five procedural failures

Every role exists to close one or more of these failure modes:

| Failure | What it looks like | Countermeasure |
|---|---|---|
| Premature convergence | First decomposition becomes the plan, missing branches never run | S0-S4 routing, gated manifest, `plan-critic-high` STOP gate |
| Skipped validity checks | Work begins before files, APIs, schemas, or data shape are real | Precondition gates before implementation or analysis |
| Constraint decay | Original objective disappears after long context or compaction | On-disk goal contract, context ledger, final constraint re-read |
| Confident confabulation | Unknowns become fluent specifics | Unknowns with dispositions; evidence ledger labels; `needs-input` when blocked |
| Self-grading leniency | The worker's own narrative becomes proof | `verification-runner-high`, command gates, adversarial review, final gate |

## Scope levels

| Scope | Name | Use when | Default path |
|---|---|---|---|
| S0 | Direct | Simple, local, low-risk work | Main session only; light self-review |
| S1 | Focused specialist | One domain or narrow uncertainty | One specialist plus optional verifier |
| S2 | Fan-out | Independent files, questions, or evidence streams | Plan critic -> specialists -> adversarial review -> integrate |
| S3 | Delivery swarm | Cross-layer implementation, tests, docs, or review | Cartographer -> manifest -> plan critic -> implementer -> verification runner -> reviewers -> integrator |
| S4 | Deep workflow | Broad audit, migration, research, or coverage work | Ask for scope/budget, then batched waves with coverage accounting |

Do not spend the fleet on S0. Do not treat S3/S4 as a single-agent task just
because a first path seems obvious.

## Standard lifecycle

1. Build the goal contract: objective, constraints, non-goals, acceptance
   criteria, unknowns with dispositions, verification target, and permissions.
2. Classify S0-S4.
3. Create the gated manifest. Each item needs owner, scope, inputs,
   precondition gate, completion gate, expected output, and stop conditions.
4. For S2+, run `plan-critic-high`. Do not dispatch workers while manifest
   findings remain unresolved.
5. Dispatch the minimal sufficient agent set.
6. Specialists return cards: finding, verification, patch summary, memo, or
   context ledger. Raw logs are not acceptable returns.
7. `verification-runner-high` runs command/file/grep gates where possible and
   flags attestation gates where judgment is unavoidable.
8. `adversarial-reviewer-high` attacks unsupported claims, regressions, and
   hidden risks.
9. `final-integrator-high` resolves conflicts, re-reads constraints, records
   gate status, runs the final improvement pass, and returns one final report.

## Tool rundown

Tools are capabilities, not a suggestion to use all of them. Use only the tools
listed in your frontmatter.

- `Agent`: delegate scoped work to another subagent. Use only from orchestration
  roles that are allowed to spawn agents. Every delegation needs a work package.
- `Read`: inspect files. Read relevant source before editing or judging it.
- `Grep` / `rg`: find symbols, routes, configs, tests, metric definitions, and
  references quickly. Prefer `rg` over slower search tools.
- `Glob`: enumerate files when file shape matters.
- `Bash`: run deterministic checks, tests, builds, dbt/SQL commands, scripts,
  and repo inspection. Predict the purpose before running. Do not use Bash for
  destructive actions without explicit approval.
- `Edit` / `Write`: modify files only when your role permits writes and the work
  package scopes the edit. Reviewers and cartographers should not write.

When a role is marked read-only, read-only is enforced primarily by tool choice.
`permissionMode: plan` is a helpful belt-and-suspenders pre-packaging, but the
real guarantee is that the role lacks `Edit` and `Write`.

## Skill roster

Core orchestration:

- `ultracode-high`: top-level operating protocol and final response shape.
- `task-intake-contract`: turns a messy request into a goal contract.
- `decomposition-router`: classifies S0-S4 and emits the gated manifest.
- `gate-kit`: gate vocabulary, schema, and `gate_check.py` runner.
- `verification-matrix`: maps domains/stacks to command or attestation checks.
- `implementation-contract`: scoped-edit rules — minimal diff, repo conventions,
  tests, stack checks, rollback notes, honest verification.
- `evidence-ledger`: labels claims as VERIFIED, CALCULATED, INFERRED,
  ASSUMPTION, or UNKNOWN.
- `context-ledger`: compact state for phase boundaries, compaction, and handoff.
- `final-report`: user-facing result, changes, verification, improvements,
  risks, and next action.
- `selftest-kit`: known-answer tests KA-1 through KA-5 that prove the mechanism
  fires.
- `can-and-must-do-better`: final improvement pass for nontrivial deliverables.

Domain rigor:

- `analytics-bi-rigor`: metrics, SQL/dbt, dashboards, semantic layers, grain,
  joins, nulls, filters, freshness, lineage, reconciliation.
- `strategy-rigor`: diagnosis, options, criteria, economics, risks, execution,
  learning plan.
- `writing-rigor`: thesis, structure, audience fit, evidence, terminology,
  concision, next actions.
- `security-rigor`: auth, authorization, injection, secrets, permissions,
  privacy, dependency, and supply-chain review.
- `performance-rigor`: algorithms, DB/query performance, rendering, network,
  caching, concurrency, memory, benchmarks.
- `ux-dashboard-rigor`: first-screen answer, information hierarchy,
  accessibility, filters, drill paths, annotations, alerts, misread risks.

Fork-style workflows:

- `high-code-research`: isolated read-only repo exploration.
- `high-code-review`: adversarial review of a diff or proposed code change.
- `high-code-verify`: isolated verification run returning compact cards.
- `high-code-final-gate`: final completeness, constraint, and verification
  check before handoff.

Related existing skills:

- `analytics-spec-builder`: pre-implementation analytics spec creation.
- `gpt-5.5-pro` and `gpt-5.5-xhigh`: broader analytics/BI/strategy operating
  modes.
- `opus-4.8-ultracode`: single-context high-stakes analytics rigor when the
  full `ultracode-high` fleet is not being run.

## Agent roster

MVP spine:

- `ultracode-high-orchestrator`: owns contract, scope, manifest, delegation,
  synthesis, and final handoff.
- `repo-cartographer-high`: maps repo architecture and risk zones, read-only.
- `plan-critic-high`: blocks weak manifests before fan-out.
- `implementation-worker-high`: performs scoped edits after precondition gates.
- `verification-runner-high`: authors/runs gates against ground truth.
- `test-and-build-runner-high`: narrow stack-check runner for tests, lint,
  typecheck, build, and dbt checks, returning compact verification cards.
- `adversarial-reviewer-high`: attacks plans, outputs, claims, and regressions.
- `final-integrator-high`: resolves conflicts, re-reads constraints, and ships.

Phase 2 specialists:

- `data-bi-reviewer-high`: SQL, dbt, semantic layer, dashboard, metrics.
- `strategy-critic-high`: options, economics, risks, execution, measurement.
- `writing-editor-high`: structure, clarity, polish, evidence, audience fit.
- `security-reviewer-high`: security/privacy/supply-chain risks.
- `performance-reviewer-high`: speed, scale, memory, DB, frontend performance.
- `ux-dashboard-reviewer-high`: dashboard and operational UI usability.
- `context-compressor-high`: restartable context ledger and handoff.
- `regression-guardian-high`: backward compatibility, public APIs, fixtures,
  snapshots, migrations, downstream consumers.

Phase 3 specialists:

- `migration-operator-high`: batched repetitive migrations with coverage.
- `debug-hypothesis-tester-high`: one debugging hypothesis per isolated run.
- `dependency-impact-analyst-high`: blast radius across packages/services.
- `release-note-writer-high`: changelog, PR summary, migration notes.
- `benchmark-runner-high`: benchmark design, execution, variance, comparison.

## Gate policy

Use the strongest available gate:

1. `command`: a command exits 0 (pass) or non-zero (fail). Best for tests,
   builds, dbt checks, scripts, and data reconciliation.
2. `file_exists`: a required artifact exists.
3. `grep`: a pattern appears or does not appear in a target file.
4. `attest`: a judgment check with a binary answer and evidence. Use only when
   no mechanical check is realistic.

Attestation is allowed, but it is not mechanical verification. It must be
flagged in the final report. On code/data S3 runs, a high proportion of
attestation gates is itself evidence that the task is under-specified.

## Cards and contracts

Work package:

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
stop_conditions:
```

Finding card:

```yaml
finding_id:
severity: critical | high | medium | low | suggestion
confidence: high | medium | low
category:
evidence:
impact:
recommendation:
verification:
```

Verification card:

```yaml
check:
gate_type: command | file_exists | grep | attest
command_or_method:
status: passed | failed | skipped | not-applicable
summary:
evidence:
failure_details:
next_action:
```

Context ledger:

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

Final report:

```text
RESULT:
CHANGES:
VERIFICATION:
IMPROVED BY FINAL GATE:
RISKS:
NEXT:
```

## Safety and escalation

Ask for explicit confirmation before destructive commands, production data
mutation, deployment, schema/auth changes, broad rewrites, sensitive-data
actions, or S4 runs with material cost. Never expose secrets in summaries. If a
check cannot run because credentials or services are unavailable, mark it
skipped and explain the blocker.

## What good looks like

Good `ultracode-high` work is not merely longer. It is more inspectable:
contracts exist, manifests are gated, workers return cards, verification is
grounded in commands or flagged attestation, final synthesis resolves conflicts,
and the user can tell what is safe to act on.
