# PRD: `ultracode-high` — an Ultracode-style orchestration mode for Claude Code on Opus 4.8 High

**Owner:** Brian / Analytics + Engineering Productivity
**Status:** Implemented scaffold v1.1 (merged PRD updated to match the repo configuration we chose)
**Target platform:** Claude Code (≥ v2.1.172)
**Strict model constraint:** Claude Opus 4.8 only, `effort: high` only
**Primary source artifacts:** repo-tracked skills under `skills/` and subagents under `agents/`
**Install target:** copy/link source artifacts into `.claude/skills/` and `.claude/agents/` or the user-global equivalents
**Shared runtime context:** `skills/ultracode-high/references/runtime-context.md`
**Deferred supporting artifacts:** hooks, saved workflows, plugin wrapper, package archives, CI wiring, repo-local conventions in `CLAUDE.md`

---

## 0. How this version was merged (read first)

This document keeps the best of two prior drafts and resolves the places they conflicted.

**Kept from the breadth draft:** S0–S4 scope routing, the full domain-specialist roster (analytics/BI, strategy, writing, security, performance, UX, regression), the output-card schemas, personas, safety/permissions matrix, observability, the per-stack verification matrix, and the phased file-tree packaging.

**Kept from the rigor draft:** the procedural framing (§2), mechanical completion gates over attestation, the plan-critique STOP gate before fan-out, the gated manifest, the on-disk goal-contract, the verifier convergence guard, the confabulation guard, and the known-answer self-test harness.

**Contradictions resolved (the only places "keep both" was impossible):**
1. **Verification model — gates vs attestation.** Resolved as **domain-adaptive**: deterministic `command` gates (exit 0/1) for anything mechanically checkable (code, SQL, build, data reconciliation); **structured attestation with mandatory flagging** for judgment domains (strategy, writing, UX, architecture). Every attested check is labeled as such in the final report. Not a true contradiction once split by domain — it is the honest synthesis.
2. **Routing taxonomy — T1/T2/T3 vs S0–S4.** Kept **S0–S4** (more granular, more operational). The tier concept survives as how much of the protocol each scope runs.
3. **Roster size — ruthless core vs broad roster.** Kept the **broad roster, phased**, and added the rigor draft's verification agents to the MVP core. Breadth is deferred to Phase 2/3, not cut.
4. **Self-test — human rubric vs mechanical KA gates.** Kept **both**: KA-1…5 mechanical CI gates prove the *mechanism* fires; the fixture rubric evaluates *qualitative* product fit. Different jobs.
5. **Model pinning — full ID vs alias.** Pinned the **full ID** `claude-opus-4-8` + `effort: high`, since strict-mode auditability is the point.
6. **Plugin packaging vs frontmatter stripping.** Plugin subagents silently ignore `permissionMode`, `hooks`, and `mcpServers`. Therefore MVP/Phase-2 **install as `.claude/` folders, not a plugin**; read-only enforcement uses `tools`/`disallowedTools` (which survive plugin scope) as the primary mechanism, with `permissionMode: plan` as a belt-and-suspenders that only works pre-packaging. Plugin packaging is Phase 3, and at that point reviewers' read-only guarantee must rest on `tools`, not `permissionMode`.

### 0.1 Ultimate configuration implemented in this repo

The configuration we actually chose is a **repo-source scaffold with runtime-context sharing**, not a direct `.claude/` working tree. Source files live in this repository and can later be copied, linked, packaged, or installed into a Claude Code runtime.

Implemented source layout:

```text
agents/
  ultracode-high-orchestrator.md
  repo-cartographer-high.md
  plan-critic-high.md
  implementation-worker-high.md
  verification-runner-high.md
  test-and-build-runner-high.md
  adversarial-reviewer-high.md
  final-integrator-high.md
  security-reviewer-high.md
  performance-reviewer-high.md
  data-bi-reviewer-high.md
  strategy-critic-high.md
  writing-editor-high.md
  ux-dashboard-reviewer-high.md
  context-compressor-high.md
  regression-guardian-high.md
  migration-operator-high.md
  debug-hypothesis-tester-high.md
  dependency-impact-analyst-high.md
  release-note-writer-high.md
  benchmark-runner-high.md

skills/
  ultracode-high/SKILL.md
  ultracode-high/references/runtime-context.md
  task-intake-contract/SKILL.md
  decomposition-router/SKILL.md
  gate-kit/SKILL.md
  gate-kit/scripts/gate_check.py
  gate-kit/references/gates.schema.json
  gate-kit/references/example-gates.json
  implementation-contract/SKILL.md
  verification-matrix/SKILL.md
  evidence-ledger/SKILL.md
  context-ledger/SKILL.md
  final-report/SKILL.md
  selftest-kit/SKILL.md
  selftest-kit/references/known-answer-tests.md
  analytics-bi-rigor/SKILL.md
  strategy-rigor/SKILL.md
  writing-rigor/SKILL.md
  security-rigor/SKILL.md
  performance-rigor/SKILL.md
  ux-dashboard-rigor/SKILL.md
  high-code-research/SKILL.md
  high-code-review/SKILL.md
  high-code-verify/SKILL.md
  high-code-final-gate/SKILL.md
```

The important implementation decision after the first pass was to avoid anemic prompts by adding one canonical reference:

```text
skills/ultracode-high/references/runtime-context.md
```

Every High-only subagent and every new `ultracode-high` skill now points to that runtime context. It contains the grand scheme, the five procedural failures, S0-S4 routing, the full tool rundown, the skill catalog, the agent roster, gate policy, card schemas, safety rules, and what good orchestration looks like. Individual agents stay focused, but they are no longer context-starved.

The shipped scaffold therefore has:

- **21 High-only subagents**: the MVP spine, the Phase 2 domain specialists, Phase 3 advanced specialists, plus `test-and-build-runner-high` as a narrow verification runner for stack checks.
- **20 new skills**: core orchestration, gate/selftest support, domain rigor, and fork-style workflow skills.
- **One shared runtime reference** used by all of the new High-only agents and orchestration skills.
- **One executable gate helper**, `gate_check.py`, plus a JSON gate schema and runnable example manifest.

What is not yet implemented: package archives for this family, `.claude/` install scripts, hooks, saved workflows, plugin packaging, CI around KA-1...5, and runtime-specific settings files.

### 0.2 Implemented file inventory

This is the configuration of record for the files created from this PRD.

#### Agent files

| File | Role in the orchestration |
|---|---|
| `agents/ultracode-high-orchestrator.md` | Top-level coordinator for intake, S0-S4 routing, manifest creation, agent selection, synthesis, and final handoff. |
| `agents/repo-cartographer-high.md` | Read-only repository mapper for architecture, dependencies, conventions, tests, risk zones, and implementation context. |
| `agents/plan-critic-high.md` | Pre-dispatch STOP gate that attacks the manifest for missing work, weak decomposition, unresolved Unknowns, and missing/weak gates. |
| `agents/implementation-worker-high.md` | Scoped edit-capable worker that runs precondition gates first, follows repo conventions, changes files, and preserves evidence for verification. |
| `agents/verification-runner-high.md` | Read-only verification owner that authors/runs command/file/grep/attest gates against ground truth and never treats worker reasoning as proof. |
| `agents/test-and-build-runner-high.md` | Narrow stack-check runner for tests, lint, typecheck, build, dbt, and compact verification-card output. |
| `agents/adversarial-reviewer-high.md` | Read-only falsifier for produced work: flaws, regressions, unsupported claims, hidden risks, and missing evidence. |
| `agents/final-integrator-high.md` | Final synthesis owner that resolves conflicts, re-reads the contract, labels gate types, and produces the user-safe final report. |
| `agents/security-reviewer-high.md` | Read-only security/privacy/supply-chain reviewer for auth, permissions, injection, secrets, PII, and dependency risks. |
| `agents/performance-reviewer-high.md` | Read-only performance reviewer for algorithmic, query, rendering, network, caching, concurrency, memory, and benchmark concerns. |
| `agents/data-bi-reviewer-high.md` | Data/BI reviewer for SQL, dbt, semantic layers, dashboards, metric contracts, grain, joins, freshness, lineage, and reconciliation. |
| `agents/strategy-critic-high.md` | Strategy critic for options, criteria, economics, assumptions, risks, execution path, and measurement. |
| `agents/writing-editor-high.md` | Writing editor for PRDs, memos, docs, release notes, executive narrative, evidence, structure, and polish. |
| `agents/ux-dashboard-reviewer-high.md` | UX/dashboard reviewer for operational UI hierarchy, first-screen answers, accessibility, filters, drill paths, and misread risks. |
| `agents/context-compressor-high.md` | Context compressor for restartable state, decisions, evidence, files, commands, risks, and handoff prompts. |
| `agents/regression-guardian-high.md` | Regression guardian for public contracts, downstream consumers, fixtures, snapshots, migrations, and backward compatibility. |
| `agents/migration-operator-high.md` | Edit-capable migration operator for batched repetitive changes with coverage accounting and verification. |
| `agents/debug-hypothesis-tester-high.md` | Single-hypothesis debugger for isolated reproduction, prediction, test, result, and next-hypothesis reporting. |
| `agents/dependency-impact-analyst-high.md` | Read-only blast-radius mapper for packages, modules, services, schemas, public APIs, and downstream consumers. |
| `agents/release-note-writer-high.md` | Release/changelog/PR-summary writer grounded in verified diffs, commits, tests, and implementation notes. |
| `agents/benchmark-runner-high.md` | Read-only benchmark runner/designer for before/after performance evidence, variance, caveats, and conclusions. |

#### Skill files

| File | Role in the orchestration |
|---|---|
| `skills/ultracode-high/SKILL.md` | Top-level orchestration skill: S0-S4 routing, gated manifest, plan critique, delegation, verification, improvement, and final reporting. |
| `skills/task-intake-contract/SKILL.md` | Goal-contract builder: objective, artifact, constraints, scope, acceptance criteria, Unknowns, risk, verification target, and permissions. |
| `skills/decomposition-router/SKILL.md` | Scope router and manifest builder: S0-S4 classification, workstream decomposition, agent selection, gates, and fan-out rules. |
| `skills/gate-kit/SKILL.md` | Gate vocabulary and runner instructions for `command`, `file_exists`, `grep`, and flagged `attest` gates. |
| `skills/implementation-contract/SKILL.md` | Implementation rules for scoped edits, minimal diffs, repo conventions, tests, rollback notes, and honest verification. |
| `skills/verification-matrix/SKILL.md` | Verification-card and stack-check mapping skill for code, analytics, BI, frontend, API, docs, writing, and strategy. |
| `skills/evidence-ledger/SKILL.md` | Claim/evidence ledger skill labeling claims as `VERIFIED`, `CALCULATED`, `INFERRED`, `ASSUMPTION`, or `UNKNOWN`. |
| `skills/context-ledger/SKILL.md` | Compact handoff and phase-boundary ledger for long sessions, compaction, open risks, and next actions. |
| `skills/final-report/SKILL.md` | Final response contract skill for result, changes, verification, final-gate improvements, risks, and next action. |
| `skills/selftest-kit/SKILL.md` | Known-answer self-test skill defining the KA-1...KA-5 mechanism tests for completion, verification, drift, confabulation, and bad plans. |
| `skills/analytics-bi-rigor/SKILL.md` | Domain rigor skill for metrics, SQL/dbt, semantic layers, dashboards, grain, joins, freshness, lineage, and reconciliation. |
| `skills/strategy-rigor/SKILL.md` | Domain rigor skill for diagnosis, options, decision criteria, economics, risks, recommendation, and learning plan. |
| `skills/writing-rigor/SKILL.md` | Domain rigor skill for audience fit, thesis, structure, evidence, terminology, concision, and actionable next steps. |
| `skills/security-rigor/SKILL.md` | Domain rigor skill for auth, authorization, injection, secrets, privacy, permissions, dependencies, and data exposure. |
| `skills/performance-rigor/SKILL.md` | Domain rigor skill for algorithms, database performance, rendering, network, caching, concurrency, memory, and benchmarks. |
| `skills/ux-dashboard-rigor/SKILL.md` | Domain rigor skill for operational UI/dashboard hierarchy, accessibility, filters, drill paths, annotations, and misread risks. |
| `skills/high-code-research/SKILL.md` | Fork-style read-only code research workflow for architecture mapping and isolated repo exploration. |
| `skills/high-code-review/SKILL.md` | Fork-style adversarial code review workflow for current diffs or proposed changes. |
| `skills/high-code-verify/SKILL.md` | Fork-style verification workflow for tests, lint, typecheck, build, dbt, and compact check summaries. |
| `skills/high-code-final-gate/SKILL.md` | Fork-style final gate for completeness, constraints, verification, regression risk, and final answer quality. |

#### Supporting files created with the skill family

| File | Role in the orchestration |
|---|---|
| `skills/ultracode-high/references/runtime-context.md` | Canonical shared runtime map loaded by every new High-only agent and orchestration skill. |
| `skills/gate-kit/scripts/gate_check.py` | Executable JSON gate runner for command/file/grep/attest gates. |
| `skills/gate-kit/references/gates.schema.json` | JSON schema for gate manifests. |
| `skills/gate-kit/references/example-gates.json` | Runnable example gate manifest covering file, grep, negated grep, command, and attestation gates. |
| `skills/selftest-kit/references/known-answer-tests.md` | KA-1...KA-5 known-answer definitions. |

---

## 1. Executive summary

`ultracode-high` is a Claude Code operating mode that recreates the practical behavior of native Ultracode while staying strictly on Claude Opus 4.8 High. It does not claim parity with native Ultracode's `xhigh` reasoning budget. It claims something more precise and more defensible: that the gap between High and a stronger setting is mostly *procedural*, not capability-bound (§2), and that the missing procedures can be compiled into an orchestration layer.

The product feels like a temporary senior delivery team inside Claude Code: an orchestrator that classifies and decomposes, a critic that attacks the plan before any work starts, focused specialists that work in isolated contexts, a verification layer that runs deterministic checks where they exist and clearly-flagged judgment where they don't, and a final gate that refuses to hand back unverified work. In the implemented scaffold, that team shares a single runtime map at `skills/ultracode-high/references/runtime-context.md`, so every agent understands its role in the whole system rather than operating from a thin local prompt.

Invocation:
```text
/ultracode-high <task>
```
Persistent main-session mode:
```bash
claude --model claude-opus-4-8 --agent ultracode-high-orchestrator
```
Every agent and skill pins:
```yaml
model: claude-opus-4-8
effort: high
```
No Sonnet, Haiku, Fable, `xhigh`, `max`, or native `/effort ultracode` in strict mode.

---

## 2. Design thesis: the five procedural failures are the spec

Native Ultracode pairs `xhigh` effort with automatic workflow orchestration to fix three failure modes of a single long-lived context: premature stop on enumerable tasks, lenient self-grading, and goal drift after compaction. Per the `fable-thinking` skill (distilled from offline Fable-vs-Opus diffing), the Opus/stronger-model gap "is rarely 'can't do the math' — it is almost always one of five procedural failures." Those three Ultracode failures are three of the five. **So most of Ultracode is reconstructable on High because the deficit is procedural.** A small residue is genuinely capability-bound and is flagged, not faked (Non-Goal 1).

`ultracode-high` enforces each procedure across a fleet of clean-context agents. Every component below exists to discharge a row of this table, and every countermeasure is mechanical wherever a mechanical form exists.

| Procedural failure | How it shows up in a fleet | Countermeasure | Mechanical? |
|---|---|---|---|
| **1. Premature convergence** | Orchestrator commits to the first decomposition; N agents execute the wrong plan | **`plan-critic-high` STOP gate** before any fan-out; no spawn until every manifest item has a disposition + completion gate | Partly (gate presence checkable; cut quality flagged) |
| **2. Skipped validity checks** | Workers act before verifying preconditions (file/API exists, data shape) | **Precondition gates** per manifest item, run before the work | Yes (`command`) |
| **3. Constraint decay** | Original objective/constraints silently dropped after compaction | **Goal-contract on disk**, re-injected into every agent; **constraints re-read and confirmed as a gate at synthesis** | Yes (presence + restatement) |
| **4. Confident confabulation** | A worker invents a result instead of flagging an Unknown | Intake registers **Unknowns with dispositions**; a definite claim for an unresolved Unknown fails verification | Partly |
| **5. Self-grading leniency** | Verification reasons from the worker's narrative and rubber-stamps | **`verification-runner-high` authors/runs gates** against ground truth; **convergence guard** re-attacks a clean pass; judgment checks are attest-flagged | Yes for code/data; flagged attestation for prose |

Mapping to Ultracode's three named failures: premature stop = #1, generous self-grading = #5, goal drift = #3. We additionally cover #2 and #4, which Ultracode gets implicitly from `xhigh` and we must get explicitly.

---

## 3. Problem statement

Opus 4.8 High is strong for complex coding, analytics, BI, strategy, and writing, but used interactively it under-orchestrates when a task deserves independent passes, keeps noisy exploration in the main context, implements before mapping dependencies, runs only one validation path, polishes a final answer without proof that checks were covered, and offloads decomposition onto the user. `ultracode-high` is a reusable orchestration layer that forces High to work as a structured, verifiable multi-agent delivery system — for users capped at High by cost, policy, or rate-limit budget who cannot reach for `xhigh`.

---

## 4. Goals

1. Provide an Ultracode-like experience without native `/effort ultracode`; keep every call on Opus 4.8 High.
2. Discharge each of the five procedural failures (§2) with a named countermeasure — measured by failure incidence, not by "depth."
3. Make verification mechanical where a mechanical check exists (target ≥ 80% `command` gates on code/data tasks) and clearly attested-and-flagged where it does not.
4. Defend the plan, not just the execution: no fan-out until the manifest passes plan critique.
5. Be provably working: ship KA self-tests; block release on regression.
6. Reduce main-context pollution by isolating noisy work; return structured cards, never raw dumps.
7. Right-size the machinery: S0 stays direct; spend the fleet only when scope warrants.
8. Support both interactive use and repeatable team workflows.

**User goals.** Users say `/ultracode-high refactor the auth flow to support passkeys and update tests`, or `/ultracode-high audit this dbt model and dashboard metric`, or `/ultracode-high write a sharper PRD and have critics improve it`, and receive a result that went through plan critique, structured fan-out, domain-adaptive verification, adversarial review, and synthesis.

---

## 5. Non-goals

1. **Closing the capability-bound residue.** A minority of sub-problems are hard for reasons procedure cannot fix and cannot always be decomposed below High's threshold; these are flagged for the user, never faked.
2. Do not reproduce native Ultracode exactly, or beat it on cost/latency — coordination runs in-band and will cost more. Tracked, not optimized.
3. Do not use `xhigh`, `max`, `/effort ultracode`, or any non-Opus model in strict mode.
4. Do not create a hidden autonomous system that edits production, deploys, sends mail, or runs irreversible operations without explicit user permission.
5. Do not spawn agents for trivial tasks where one direct pass is better.
6. Do not trust subagent findings without synthesis and verification; do not let specialists return raw logs.
7. Do not outsource judgment to votes — multiple agents provide evidence; the integrator decides.
8. No unbounded recursion — orchestration is one level deep in v1 (spawn-depth caps respected).

---

## 6. Personas

- **Senior engineer / tech lead** — large refactors, migrations, debugging, feature builds, reviews. Values correctness, minimal regressions, test evidence.
- **Analytics / BI developer** — validating SQL, dbt models, dashboards, metric definitions, lineage, grain, joins, reconciliation. Values traceability and data quality.
- **Product / strategy operator** — turning messy inputs into PRDs, memos, launch plans, competitive analyses. Values options, risks, decision logic, polish.
- **Documentation / writing owner** — drafts improved via structure, evidence checks, voice consistency, adversarial editing.

---

## 7. Product principles

1. **High-only honesty.** State plainly that this emulates Ultracode-style behavior, not its `xhigh` reasoning budget.
2. **Critique the plan before parallelism.** Classify and decompose, then attack the decomposition before fan-out.
3. **Mechanical where possible, flagged where not.** A scripted check is a judge that does not degrade with the model; an opinion is labeled as one.
4. **Right isolation.** Named subagents for fresh-context specialist work; `/fork` when the worker needs full parent context.
5. **No noisy returns.** Subagents return finding/verification/decision cards, not raw dumps.
6. **Adversarial by default for S2+.** Every S2+ task includes a reviewer whose job is falsification.
7. **Verification is a product feature.** Final output distinguishes verified facts, attested judgments, unverified assumptions, failed checks, and remaining risks.
8. **Context is a budget.** Summarize aggressively; maintain a compact ledger.
9. **Stop when enough.** Avoid over-orchestrating small or sequential tasks.
10. **Business value matters.** For analytics and strategy, correctness is necessary but outputs must connect to decisions, stakeholders, and next actions.

---

## 8. Scope levels and routing

The `ultracode-high` skill classifies every request S0–S4. The plan-critique STOP gate (§14) runs before fan-out on every S2+ task.

| Scope | Name | Trigger | Default execution |
|---|---|---|---|
| S0 | Direct | Single-file / simple / no material risk | Main session only; light self-review |
| S1 | Focused specialist | One domain, limited uncertainty, moderate risk | 1 specialist + optional verification |
| S2 | Fan-out | Multiple independent files/domains/questions | plan-critic → 2–5 specialists in parallel → adversarial review → integrate |
| S3 | Delivery swarm | Cross-layer implementation, tests, docs, review | cartographer → plan → plan-critic → implementer(s) → verification-runner → reviewers → final gate |
| S4 | Deep workflow | Repo-scale audit/migration/research, dozens of units | confirm scope/budget → batched subagent waves with coverage tracking → cross-check → synthesize |

**Fan-out limits** (High-only relies on structure, not brute force):

| Scope | Default concurrent | Max per wave |
|---|---:|---:|
| S1 | 1 | 2 |
| S2 | 2–4 | 5 |
| S3 | 3–6 | 8 |
| S4 | 4–8 per wave | 12 (confirm first) |

---

## 9. Core user experience

**Main invocation** `/ultracode-high <task>` →
1. Parse request; 2. Build the **goal-contract** (intake); 3. Classify S0–S4; 4. Decompose into a **gated manifest**; 5. **Plan critique (STOP gate)** for S2+; 6. Spawn the minimal sufficient agent set; 7. Verify (domain-adaptive); 8. Adversarial review; 9. Synthesize + constraint re-read; 10. `can-and-must-do-better` improvement pass; 11. Final report with verification ledger. Phase-boundary updates throughout. Clarifying questions only when a missing decision blocks safe progress.

**Context-rich second opinion** `/fork Run can-and-must-do-better on the current work; improve materially, report what changed, verify what can be verified.` — use when the deliverable depends heavily on prior conversation.

**Direct specialist** `Use the data-bi-reviewer-high agent to audit this SQL and dashboard definition.`

**Source and install** Source files live under repo `skills/` and `agents/`. Install by copying or linking them into project-local `.claude/skills/…`, `.claude/agents/…`, or the user-global equivalents. Package archives and install scripts are deferred.

---

## 10. Subagents

All pin `model: claude-opus-4-8`, `effort: high`. Read-only enforcement is via `tools`/`disallowedTools` first (survives plugin scope), with `permissionMode: plan` as a pre-packaging extra.

### 10.1 MVP core (the verification spine + delivery loop)

| Agent | Purpose | Tools | Writes? |
|---|---|---|---:|
| `ultracode-high-orchestrator` | Scope classification, decomposition, fan-out, synthesis, handoff | Agent, Read, Grep, Glob, Bash | Optional |
| `repo-cartographer-high` | Read-only repo mapping: architecture, deps, files, risk zones | Read, Grep, Glob, Bash | No |
| `plan-critic-high` | **(spine)** Attacks the manifest before fan-out: missing items, wrong cuts, ungated items, undisposed Unknowns | Read, Grep, Glob, Bash | No |
| `implementation-worker-high` | Scoped code changes, minimal patches, repo conventions | Read, Edit, Write, Grep, Glob, Bash | Yes |
| `verification-runner-high` | **(spine)** Authors & runs `command` gates against ground truth; runs tests/lint/build/data checks; emits verification cards; flags any attest fallback | Read, Grep, Glob, Bash | No |
| `test-and-build-runner-high` | Narrow runner for stack-specific test/build/lint/typecheck/dbt checks, returning compact verification cards | Read, Grep, Glob, Bash | No |
| `adversarial-reviewer-high` | Finds flaws, regressions, edge cases, unsupported claims — the judgment layer for what gates can't catch (esp. prose/strategy) | Read, Grep, Glob, Bash | No |
| `final-integrator-high` | Merges findings, resolves conflicts, **re-reads contract constraints as a gate**, produces final result + verification ledger | Read, Grep, Glob, Bash, Edit, Write | Optional |

`verification-runner-high` owns gate semantics and claim verification; `test-and-build-runner-high` exists as a narrower utility role for ordinary stack checks when the orchestrator wants compact test/build output without invoking the full claim-verification pass.

### 10.2 Phase-2 domain specialists

`security-reviewer-high`, `performance-reviewer-high`, `data-bi-reviewer-high`, `strategy-critic-high`, `writing-editor-high`, `ux-dashboard-reviewer-high`, `context-compressor-high`, `regression-guardian-high`. Each read-only by default (except where a domain writes its own artifact), each preloaded with its rigor skill (§12).

### 10.3 Phase-3 advanced

`migration-operator-high` (prefer `isolation: worktree`), `debug-hypothesis-tester-high` (run several in parallel for hard failures), `dependency-impact-analyst-high`, `release-note-writer-high`, `benchmark-runner-high`.

### 10.4 Representative frontmatter

Read-only critic/verifier (note read-only is enforced by `disallowedTools`, not only `permissionMode`):
```yaml
---
name: plan-critic-high
description: Opus 4.8 High plan critic. Attacks a ultracode-high manifest BEFORE any work begins — missing items, wrong decomposition, items lacking a checkable completion gate, Unknowns without dispositions. Receives the contract and manifest but not the orchestrator's reasoning. Rewards finding flaws, not approving.
model: claude-opus-4-8
effort: high
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
permissionMode: plan
maxTurns: 20
color: red
skills: [evidence-ledger]
---
```

### 10.5 Shared runtime context

All High-only subagents include a fleet-context preamble directing them to load `skills/ultracode-high/references/runtime-context.md` before substantive work when available. That reference is the canonical source for:

- why the system exists and which procedural failures each role closes;
- the S0-S4 lifecycle;
- tool semantics and write/read-only boundaries;
- the full skill and agent roster;
- gate policy and card schemas;
- safety and escalation rules.

The prompt pattern is intentional: individual agents remain role-focused, while the shared reference prevents them from being anemic or blind to the larger orchestration.
```yaml
---
name: verification-runner-high
description: Opus 4.8 High verification runner. For each claim, authors and runs a deterministic check (exit 0/1) against ground truth where one exists; falls back to attestation only when none is possible, and flags it. Runs tests, lint, typecheck, build, and data checks; returns verification cards, never raw logs. Never cites the worker's own reasoning as evidence. On a clean pass for an S3/S4 item, re-attacks the three most load-bearing claims once.
model: claude-opus-4-8
effort: high
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
permissionMode: plan
maxTurns: 30
color: cyan
skills: [verification-matrix, gate-kit, evidence-ledger]
---
```
```yaml
---
name: implementation-worker-high
description: Opus 4.8 High implementation worker for scoped code changes. Runs its precondition gate first; on failure, flags and stops rather than inventing a result. Minimal diffs, repo conventions, updates tests.
model: claude-opus-4-8
effort: high
tools: Read, Edit, Write, Grep, Glob, Bash
permissionMode: acceptEdits
maxTurns: 40
color: green
skills: [implementation-contract, verification-matrix, context-ledger]
---
```

---

## 11. The gated manifest and goal-contract

The decomposition router (§12) emits two artifacts that make the rest of the system mechanical.

**Goal-contract** — `.claude/ultracode-high/<run-id>/CONTRACT.md`, written at intake, re-read every iteration, injected into every subagent, and **persisted on disk so it survives main-context compaction**. Holds objective verbatim, constraints, acceptance criteria, non-goals, Unknowns-with-dispositions (`search | compute | ask | flag`), and decisions-with-rationale appended as the run proceeds. Workers never receive conversation history — only the contract plus their one item — so they cannot drift.

In the current repo scaffold, this contract path is the **runtime install target** rather than a source-controlled file. The source prompt that describes how to create and use it lives in `skills/task-intake-contract/SKILL.md`, and the shared runtime context documents how every subagent should treat the contract.

**Gated manifest** — each work item is a triple:
```yaml
- id: path-12
  task: "Classify query path cashplus.attribution.v2 for PII leakage"
  precondition_gate:                       # validity check, run BEFORE work (failure #2)
    type: command
    cmd: "test -f src/cashplus/attribution_v2.sql"
  completion_gate:                         # how 'done' is proven (failures #1, #5)
    type: command
    cmd: "python scripts/check_pii.py --path attribution_v2 --require-evidence"
  unknowns:                                # failure #4
    - q: "Does v2 inherit v1's masking CTE?"
      disposition: compute
```
**Hard rule (from the rigor draft):** a manifest item without a checkable completion criterion is a wish, not a step — `plan-critic-high` rejects it. Where no `command` is possible (strategy, writing, UX), the completion gate is `type: attest` with a binary question, and **every attest gate appears in the final report**. Target ≤ 20% attest gates on code/data S3 runs; a higher ratio is itself a flag that the task was under-specified.

---

## 12. Skills

### 12.1 MVP skills

| Skill | Purpose | Context |
|---|---|---|
| `ultracode-high` | Top-level orchestration protocol (§14) | Inline |
| `ultracode-high/references/runtime-context.md` | Canonical shared runtime map: grand scheme, tools, skills, agents, gates, cards, safety | Reference |
| `task-intake-contract` | Builds the on-disk goal-contract: goal, constraints, acceptance criteria, Unknowns+dispositions, blocking decisions | Inline |
| `decomposition-router` | Classifies S0–S4 and emits the **gated manifest** (rejects ungated items) | Inline |
| `gate-kit` | **(spine)** Gate vocabulary, `gate_check.py` (exit 0/1 runner), `gates.json` schema; domain gate packs are deferred | Inline / referenced by runner |
| `verification-matrix` | Maps domain → checks: which stack → which `command` gates; which judgment domain → which structured-attestation checklist | Preloaded by runner/reviewers |
| `evidence-ledger` | Evidence / facts / assumptions format | Preloaded broadly |
| `context-ledger` | Compact task state + handoff format | Preloaded broadly |
| `final-report` | Final format: result, changes, **gate-results table (command vs attest-flagged)**, risks, follow-ups | Preloaded by integrator |
| `selftest-kit` | **(spine)** KA-1…5 definitions now; seeded fixture files and CI release gate deferred (§13) | Standalone |
| `can-and-must-do-better` | Second-pass improvement demand before final response | Inline or fork |

### 12.2 Phase-2 domain rigor skills

`analytics-bi-rigor`, `strategy-rigor`, `writing-rigor`, `security-rigor`, `performance-rigor`, `ux-dashboard-rigor`.

### 12.3 Optional workflow skills (`context: fork`)

`high-code-research`, `high-code-review`, `high-code-verify`, `high-code-final-gate`. Use inline skills for standing guidance, `context: fork` skills for self-contained tasks, and `/fork` directly when the reviewer must inherit full parent context.

---

## 13. Known-answer self-test harness (proves the mechanism fires)

`selftest-kit` ships seeded tasks with mechanically-graded expected properties, one per failure mode. Release ships only if KA-1…5 pass via `gate_check.py`; a regression means the orchestration text is broken, not the test.

Current scaffold status: `selftest-kit` includes the KA-1...5 definitions and `gate-kit` includes `gate_check.py`; CI wiring and full seeded fixture files are deferred.

- **KA-1 planted-50** — input with exactly 50 enumerable items; pass iff all 50 close. *(premature stop, #1)*
- **KA-2 planted-bug** — worker output contains a claim contradicted by ground truth; pass iff the runner's gate flips it to fail. *(self-grading, #5)*
- **KA-3 drift-trap** — long run with a constraint stated once and violated only late; pass iff the synthesis constraint-gate catches it. *(constraint decay, #3)*
- **KA-4 confab-bait** — an item unanswerable from inputs; pass iff the worker flags the Unknown instead of inventing. *(confabulation, #4)*
- **KA-5 bad-plan** — manifest with a missing item and an ungated item; pass iff `plan-critic-high` blocks dispatch. *(premature convergence, #1)*

This complements (does not replace) the qualitative fixture rubric in §22.

---

## 14. Orchestration algorithm

```text
on /ultracode-high(task):
  contract = build_goal_contract(task)            # task-intake-contract → CONTRACT.md
  scope    = classify_scope(contract)             # decomposition-router, S0–S4

  if scope == S0:
      do_direct_work(); self_review_light(); return final_report()

  manifest = decompose_into_gated_items(contract) # each item: precondition + completion gate
  if scope >= S2:
      findings = run(plan-critic-high, contract, manifest)   # STOP gate
      if findings.open: resolve_or_waive_with_rationale(); halt_until_clear()

  # S1: single specialist + optional verification
  # S2: parallel specialists → adversarial review → integrate
  # S3:
  map  = run(repo-cartographer-high)
  plan = create_plan(map, manifest)
  impl = run(implementation-worker-high, plan)            # runs precondition gates first
  tests = run(test-and-build-runner-high, impl)           # optional narrow stack checks
  ver  = run(verification-runner-high, impl + tests)      # command gates; flag attest fallbacks
  rev  = run_parallel([adversarial-reviewer-high,
                       security/data-bi/performance/... if relevant])
  fix_blockers()
  final = run(final-integrator-high)                      # re-reads contract constraints (gate)
  improve(final)                                          # can-and-must-do-better
  return final_report()                                   # result + gate-results table + risks

  # S4: confirm budget → batched waves with coverage tracking → cross-check → synthesize
```
Verifier **convergence guard:** an S3/S4 item passing with zero findings triggers exactly one re-attack on its three most load-bearing claims before the pass stands.

---

## 15. Output contracts

**Work-package card** (every delegation): `id, owner, goal, scope, inputs, allowed_actions, expected_output, precondition_gate, completion_gate, success_criteria, stop_conditions`.

**Finding card** (every reviewer finding): `finding_id, severity {critical|high|medium|low|suggestion}, confidence, category, evidence {file/line, command, data check, quote}, impact, recommendation, verification`.

**Verification card** (every check): `check, method, gate_type {command|file_exists|grep|attest}, status {passed|failed|skipped|n/a}, evidence, failure_details, next_action`. **`gate_type` is mandatory** — it is how the final report distinguishes measured from judged.

**Context ledger** (phase boundaries): objective, constraints, files touched/read, commands run, decisions, assumptions, verified, failed/skipped checks, open risks, next actions.

**Final report:** result/deliverable; what changed; **gate-results table (command vs attest-flagged)**; how the `can-and-must-do-better` pass improved it; verification performed; remaining risks/assumptions; required human next step.

---

## 16. Domain requirements

**Analytics/BI** (use `analytics-bi-rigor` → `data-bi-reviewer-high`): metric definition (numerator/denominator/filters/window/dimensionality); grain (source/join/output/dashboard); join safety (cardinality, fanout, duplicates, missing keys); filter logic (date inclusivity, timezone, status, test rows); null/zero behavior; **reconciliation against a source of truth (command gate where possible)**; freshness; lineage; BI semantics (filters, drill paths, totals, RLS); decision relevance. Output: metric contract, model changes, data checks run, reconciliation results, caveats, recommended interpretation, what *not* to conclude.

**Code** (`implementation-worker-high` + `verification-runner-high`): inspect conventions before editing; minimal diff; preserve public behavior unless required; add/update tests; document migrations/breaking changes; run the stack-appropriate checks; stop if tests need unavailable secrets/services. Per-stack `command` gates:

| Stack | Checks |
|---|---|
| JS/TS | package-manager detect, lint, typecheck, tests, build |
| Python | pytest, ruff, mypy/pyright when configured |
| SQL/dbt | dbt compile, dbt test, targeted query checks |
| Frontend | build, component tests, a11y review, snapshot check |
| APIs | unit, contract, route coverage, auth checks |
| Docs/writing | link check, structure/consistency (attest), factual support (attest, flagged) |

Never invent a verification result; an unrunnable check is `skipped`/`n/a` with reason.

**Writing/strategy** (`strategy-critic-high`, `writing-editor-high`, `adversarial-reviewer-high`, `final-integrator-high`): strategy checks — customer, problem, decision, options, tradeoffs, assumptions, evidence, risks/mitigations, success criteria, execution path. Writing checks — audience fit, thesis, structure, no unsupported claims, concision, consistent terminology, next steps, exec summary/TLDR when useful. These domains are **attestation-heavy by nature**; the verifier flags them as such — that is honest, not a gap.

---

## 17. Context, safety, observability

**Context** — main session gets summaries not logs; subagents return cards; long tasks keep a context ledger; run `context-compressor-high` before compaction or after major phases; named subagents for fresh-context work, `/fork` for full-context review, worktrees for high-risk parallel edits. Return budgets: ≤ 10–20 bullets for maps, 3–7 finding cards for reviews, 1 verification table per runner, no raw log > 50 lines unless requested. The source-controlled scaffold centralizes fleet context in `skills/ultracode-high/references/runtime-context.md`; every new High-only agent and new `ultracode-high` skill references it.

**Safety/permissions** — reviewers/cartographers read-only (`tools` first, `permissionMode: plan` second); implementers `acceptEdits` only when scoped; migration operators `acceptEdits` + `isolation: worktree`; block destructive shell commands without approval; never expose secrets; require plan approval before schema/auth changes, destructive migrations, or broad rewrites; document any skipped verification. Optional hooks (deferred): `PreToolUse` block dangerous Bash, `PostToolUse` summarize huge output, `SubagentStop` reject cards missing required sections. **Note:** hooks and `permissionMode` do not survive plugin packaging — keep them in `.claude/settings.json` / repo scripts.

**Observability** — phase-boundary updates for S2+ (intake/scope → plan → checkpoint → verification → synthesis); internal trace as structured JSON (`.claude/ultracode-high/*/trace.json`) when installed into a runtime: agents used, files read/edited, commands run, checks passed/failed/skipped, **gate_type ratio**, unresolved risks, whether the final answer changed after `can-and-must-do-better`, user follow-up corrections. Trace writing is deferred in the repo scaffold; the context-ledger skill provides the manual contract for now.

---

## 18. Functional requirements

FR1 **High-only enforcement** — every artifact pins `claude-opus-4-8` + `effort: high`; no instruction to switch to `xhigh`/`max`/`ultracode`. Verified by config lint in CI.
FR2 **Goal-contract** — orchestrator produces the on-disk contract with goal, constraints, acceptance criteria, Unknowns+dispositions, blocking decisions.
FR3 **Scope classification** — S0–S4, briefly explained for S2+.
FR4 **Gated decomposition** — manifest items each carry precondition + completion gates; ungated items rejected.
FR5 **Plan-critique STOP gate** — no S2+ fan-out until `plan-critic-high` findings are resolved or waived with logged rationale.
FR6 **Minimal agent set** — orchestrator selects the smallest sufficient set.
FR7 **Context isolation** — noisy search/logs/tests/broad review run outside the main context.
FR8 **Structured returns** — subagents return cards, never raw dumps; `gate_type` is mandatory on verification cards.
FR9 **Domain-adaptive verification** — `command` gates where checkable (target ≥ 80% on code/data); attestation elsewhere, always flagged.
FR10 **Convergence guard** — a clean S3/S4 pass triggers one re-attack before standing.
FR11 **Constraint-decay gate** — integrator re-reads contract constraints and confirms each before returning.
FR12 **Confabulation guard** — a definite claim for an unresolved Unknown fails verification.
FR13 **Adversarial review** — required before delivery on S2+.
FR14 **Improvement loop** — final answer passes `can-and-must-do-better`.
FR15 **Final report** — result, changes, gate-results table, verification, risks, what improved.
FR16 **Domain specialization** — analytics tasks run data/grain checks; writing/strategy run structure/evidence/decision checks.
FR17 **Safety prompts** — explicit confirmation before destructive/production/broad-schema/sensitive operations.
FR18 **KA self-test** — KA-1…5 definitions exist; `gate_check.py` exists; full seeded fixtures and CI blocking are next work.
FR19 **Installability** — source lives under repo `skills/` + `agents/`; runtime install copies/links to `.claude/skills/` + `.claude/agents/`; plugin packaging deferred to Phase 3 (frontmatter-stripping caveat applies).

---

## 19. Non-functional requirements

| Requirement | Target |
|---|---|
| Reliability | Never claims tests passed unless a `command` gate ran and passed |
| Latency | S0 direct; S2+ trades speed for verified quality |
| Cost | Fan-out bounded by §8 caps |
| Security | Read-only-by-`tools` default for reviewers/cartographers |
| Maintainability | Focused, reusable, version-controlled agents |
| Portability | Project-local and user-global installs |
| Auditability | Verification ledger + gate_type ratio in every S2+ output |
| Provability | KA-1…5 defined now; CI release gate still to wire |
| Human control | User can approve/cancel broad runs |

---

## 20. Implemented packaging and remaining phases

**Implemented repo-source scaffold**:
```text
skills/ ultracode-high (+ references/runtime-context.md),
        task-intake-contract, decomposition-router, gate-kit,
        implementation-contract, verification-matrix, evidence-ledger,
        context-ledger, final-report, selftest-kit,
        analytics-bi-rigor, strategy-rigor, writing-rigor, security-rigor,
        performance-rigor, ux-dashboard-rigor,
        high-code-research, high-code-review, high-code-verify,
        high-code-final-gate
agents/ ultracode-high-orchestrator, repo-cartographer-high, plan-critic-high,
        implementation-worker-high, verification-runner-high,
        test-and-build-runner-high, adversarial-reviewer-high,
        final-integrator-high,
        security-reviewer-high, performance-reviewer-high,
        data-bi-reviewer-high, strategy-critic-high, writing-editor-high,
        ux-dashboard-reviewer-high, context-compressor-high,
        regression-guardian-high,
        migration-operator-high, debug-hypothesis-tester-high,
        dependency-impact-analyst-high, release-note-writer-high,
        benchmark-runner-high
```

Implemented acceptance baseline: reliable S0-S4 protocol text; no subagents for trivial tasks; plan critic and verification runner exist; every High-only agent and orchestration skill pins `claude-opus-4-8` + `effort: high`; every new High-only agent and orchestration skill references `runtime-context.md`; `gate_check.py` smoke-tested against `example-gates.json`; `git diff --check` clean. Full KA-1...5 fixture execution remains pending.

**Install phase** — copy/link repo source into `.claude/skills/` and `.claude/agents/`, add runtime settings, and verify Claude Code recognizes all skills/subagents.

**Test phase** — create seeded KA fixture files, wire `selftest-kit` and `gate_check.py` into CI or a local release script, and run the qualitative fixtures in §22.

**Packaging phase** — create zip/package artifacts, optional hooks, saved JS workflows, agent teams for direct specialist messaging, and plugin packaging. If packaging as a plugin, migrate read-only enforcement off `permissionMode` onto `tools`, and relocate hooks to settings.

---

## 21. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Verifier collusion (the existential risk) | Self-grading returns | Separate context + read-only `tools` + gate-first; tripwires: gate_type ratio, overturn rate, KA-2 |
| Gate authoring is the new ceiling | Bad gates pass bad work | `plan-critic-high` inspects gate quality; attest gates capped + flagged; promote recurring attests to commands over time |
| Mechanical gates scarce in prose | Over-claimed verification on strategy/writing | Domain-adaptive model; attestation flagged, never disguised as measured |
| Over-orchestration on small tasks | Slower than plain High | S0 direct path; conservative scope thresholds; `/ultracode-high` opt-in |
| Capability-bound residue mis-handled | Confident wrong answer | Flag below "would stake the deliverable on it"; never synthesize over it |
| Agents conflict on file edits | Broken tree | One implementer by default; worktrees for parallel edits |
| Plugin packaging strips permissionMode/hooks | Reviewers silently gain write access | Read-only via `tools`; defer packaging to Phase 3; relocate hooks to settings |
| Subagents return verbose logs | Context pollution | Output contracts + optional SubagentStop hook |
| Depth caps (bg subagents stop at depth 5; forks can't fork) | Deep decomposition stalls | One-level orchestration in v1 |

---

## 22. Test plan

**Fixtures** (route + behavior expectations): single-file bug (S0/S1); multi-file feature (S3); SQL metric bug (data/BI review + reconciliation gate); dashboard spec review (UX + analytics); PRD rewrite (strategy + writing critics, attest-flagged); hard debugging (parallel hypothesis testers); repo-wide audit (S4, confirm first).

**Rubric** (per task): correct scope; appropriate agent set; **plan-critic caught planted plan flaw**; relevant evidence; output correctness; **verification accuracy and correct gate_type labeling**; context efficiency; report clarity; whether `can-and-must-do-better` materially improved the result.

This qualitative rubric runs alongside the mechanical KA harness (§13).

---

## 23. Success metrics

**Mechanism health (precondition for trusting outcomes):** KA-1…5 = 5/5 every release; mechanical-gate ratio ≥ 80% on code/data S3 runs.
**Leading:** coverage closure rate ≥ 95% (stretch ≥ 99%); verifier overturn rate 5–15% (~0% = rubber-stamping, investigate); plan-critic catch rate > 0.
**Lagging:** ≥ 50% reduction in "you missed X" follow-ups vs single-agent-High baseline; ≥ 40% of previously-`xhigh`/`ultracode` tasks now acceptable on `ultracode-high` within a quarter; overhead vs native Ultracode tracked, not minimized.
**Analytics/BI:** % metric changes with explicit grain; % dashboard audits with reconciliation; join/cardinality issues caught pre-delivery; freshness/filter caveats documented.
**Blocking dependency [data]:** establish the single-agent-High baseline first, or rework-rate has no comparator.

---

## 24. Resolved decisions and remaining questions

### Resolved in the implemented scaffold

1. **Source layout:** repo `skills/` and `agents/` are the source of truth; `.claude/` is an install target.
2. **Shared context:** add `skills/ultracode-high/references/runtime-context.md` and point all new High-only agents and orchestration skills to it.
3. **Plan critic vs adversarial reviewer:** keep separate. `plan-critic-high` attacks the manifest before fan-out; `adversarial-reviewer-high` attacks produced work.
4. **Verification runner vs test/build runner:** keep both. `verification-runner-high` owns gate semantics and claim verification; `test-and-build-runner-high` is a narrower stack-check utility.
5. **Scope of implementation:** build the MVP spine, Phase 2 domain specialists, and Phase 3 specialist definitions now; defer hooks, workflows, package archives, and CI.

### Still open

1. Should strict mode forbid built-in Claude Code agents (Explore/Plan) that may run non-Opus models? This affects FR1 purity.
2. Should plan critique run on some S1 tasks, or only S2+? Cost and failure data should decide.
3. Should implementation workers default to `isolation: worktree` for all edits, or only risky edits?
4. What attest-gate cap should trigger "task under-specified" in practice? The working target remains 20% for code/data S3 runs, pending real data.
5. Should attest-to-command gate promotion feed the same offline improvement loop as `fable-thinking`?
6. How much phase-boundary progress reporting is useful before it becomes noise?

---

## 25. Implemented sequence and next build order

### Implemented sequence

1. Created the core orchestration skills: `ultracode-high`, `task-intake-contract`, `decomposition-router`, `gate-kit`, `verification-matrix`, `evidence-ledger`, `context-ledger`, `final-report`, `selftest-kit`.
2. Created the MVP spine agents: orchestrator, cartographer, plan critic, implementation worker, verification runner, test/build runner, adversarial reviewer, final integrator.
3. Created the Phase 2 domain skills and agents: analytics/BI, strategy, writing, security, performance, UX/dashboard, context compression, regression.
4. Created the Phase 3 specialist agents and fork-style workflow skills: migration, debugging hypotheses, dependency impact, release notes, benchmarks, code research/review/verify/final gate.
5. Added `runtime-context.md` and updated all new High-only agents and orchestration skills to reference it.
6. Added `gate_check.py`, `gates.schema.json`, and KA-1...5 definitions.
7. Updated README to expose the scaffold.

### Next build order

1. Add install/copy scripts for `.claude/skills/` and `.claude/agents/`.
2. Create the seeded KA fixture files and run KA-1...5 through `gate_check.py`.
3. Add CI or a local release script for frontmatter/model pinning, gate tests, and package integrity.
4. Create package archives under `skills/_packages/` if archive-based distribution is needed.
5. Add optional hooks and saved workflows once the folder-install path is stable.
6. Run the qualitative fixtures in §22 and tune scope thresholds, attest-gate caps, and progress-update cadence.

---

## 26. TLDR

| Area | Recommendation |
|---|---|
| Name | `ultracode-high` |
| Constraint | Opus 4.8 only, `effort: high` only |
| Design frame | Compile the five `fable-thinking` procedural failures into a fleet (§2) |
| Implemented agents | 21 High-only agents: MVP spine, domain specialists, advanced specialists, plus test/build runner |
| Implemented skills | 20 new skills: orchestration, gate/selftest, domain rigor, and fork-style workflow skills |
| Runtime context | `skills/ultracode-high/references/runtime-context.md`, referenced by every new High-only agent and orchestration skill |
| Verification | **Domain-adaptive**: `command` gates for code/data; flagged attestation for prose; `gate_check.py` scaffolded |
| Plan defense | `plan-critic-high` STOP gate before every S2+ fan-out |
| Provability | KA-1...5 definitions exist; seeded fixtures and CI remain next work |
| Context | named subagents for isolation, `/fork` for full-context review, runtime-context reference + on-disk goal-contract pattern |
| Safety | read-only via `tools`; confirmations for destructive ops; plugin packaging deferred (frontmatter caveat) |
| Success target | complex tasks produce verified, provably-orchestrated outputs without `xhigh` or native Ultracode |
