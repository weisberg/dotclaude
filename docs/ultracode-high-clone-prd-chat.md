# PRD: `ultracode-high` — an Ultracode-style orchestration clone for Claude Code using only Claude Opus 4.8 High

**Owner:** Brian / Analytics + Engineering Productivity  
**Status:** Superseded draft v0.1
**Target platform:** Claude Code  
**Strict model constraint:** Claude Opus 4.8 only, `effort: high` only  
**Primary artifacts to create:** Claude Code skills under `.claude/skills/` and subagents under `.claude/agents/`  
**Optional supporting artifacts:** hooks, saved workflows, plugin wrapper, repo-local conventions in `CLAUDE.md`

---

## Supersession note

The implemented configuration is captured in [`ultracode-high-clone-prd-merged.md`](ultracode-high-clone-prd-merged.md). The final scaffold we went with is repo-source first: skills live under `skills/`, subagents live under `agents/`, install into `.claude/` is a later copy/link step, and every new High-only agent plus orchestration skill points to `skills/ultracode-high/references/runtime-context.md` for the full fleet map.

The merged PRD is the configuration of record because it adds the verification spine that this draft did not fully specify: `plan-critic-high`, `verification-runner-high`, `gate-kit`, `selftest-kit`, gated manifests, command-vs-attest verification, and known-answer tests.

---

## 1. Executive summary

`ultracode-high` is a Claude Code operating mode that approximates the practical benefits of Ultracode while staying strictly on Claude Opus 4.8 High. The goal is not to claim parity with native Ultracode, because native Ultracode combines extra-high reasoning with automatic workflow orchestration. Instead, this clone recreates the behaviors that matter most in day-to-day work:

1. deliberate task triage,
2. automatic decomposition,
3. parallel subagent fan-out when warranted,
4. isolated context windows for noisy exploration,
5. adversarial review,
6. verification before final output,
7. concise synthesis back to the main session,
8. context-window protection through summaries, ledgers, and forked review passes.

The product should feel like a temporary senior delivery team inside Claude Code: one orchestrator, several focused specialists, and a final gatekeeper that refuses to hand back weak work.

The mode will be invoked primarily through a top-level skill:

```text
/ultracode-high <task>
```

For a more persistent experience, it can also be launched with a main-session agent:

```bash
claude --model claude-opus-4-8 --agent ultracode-high-orchestrator
```

All agents and skills in this PRD must pin:

```yaml
model: claude-opus-4-8
effort: high
```

No Sonnet, Haiku, Fable, `xhigh`, `max`, or native `/effort ultracode` may be used in strict mode.

---

## 2. Research basis and design implications

Native Claude Code Ultracode is a session setting that combines `xhigh` reasoning effort with automatic workflow orchestration. The official Claude Code workflow docs describe dynamic workflows as JavaScript scripts that orchestrate many subagents, keep intermediate results in script variables, and use workflows for large migrations, codebase audits, and cross-checked research. They also state that Ultracode makes Claude plan a workflow for each substantive task in the session. The high-only clone must therefore approximate automatic orchestration without relying on `xhigh`.

Claude Opus 4.8 defaults to `high` effort across Claude API and Claude Code. Anthropic recommends starting with `xhigh` for coding and agentic work, while `high` is the default quality/cost balance. Because this product is high-only, it needs compensating structure: explicit routing, decomposition, quality gates, and adversarial review.

Claude Code subagents are specialized assistants with isolated contexts, custom prompts, model settings, tool permissions, and optional preloaded skills. They are useful for preserving main-session context by moving verbose operations such as repository search, tests, logs, and independent investigations into separate windows. Forks inherit the full parent conversation, while named subagents start fresh from their definition and delegation prompt. This PRD uses both: named subagents for reusable specialist work, and forks for context-heavy second opinions.

Claude Code skills are lazily loaded `SKILL.md` procedures. They can be invoked directly with slash commands, can run inline, can run in a forked subagent context, and can include dynamic shell context. Skills are the right primitive for reusable operating procedures and quality checklists; subagents are the right primitive for isolated work and context management.

Agent teams are a possible optional layer for collaborative parallel exploration, but they are experimental, token-expensive, and disabled by default. This PRD treats agent teams as a Phase 3 enhancement, not an MVP dependency.

---

## 3. Problem statement

Claude Opus 4.8 High is strong enough for complex coding, analytics, and writing tasks, but High alone does not always behave like native Ultracode. Common gaps when using High interactively:

- it may under-orchestrate when a task deserves multiple independent passes;
- it may keep too much noisy exploration in the main context;
- it may prematurely implement before fully mapping dependencies;
- it may perform only one validation path;
- it may produce a polished final answer without enough proof that tests, data checks, citations, or edge cases were covered;
- it may ask the user to manually manage task decomposition and agent selection.

`ultracode-high` solves this by creating a reusable orchestration layer that forces Opus 4.8 High to work as a structured multi-agent delivery system.

---

## 4. Goals

### 4.1 Product goals

1. Provide an Ultracode-like experience without using native `/effort ultracode`.
2. Keep every model call on Claude Opus 4.8 High.
3. Improve completion quality for complex coding, analytics, BI, strategy, and writing tasks.
4. Reduce main-context pollution by isolating noisy exploration, logs, and review passes.
5. Make verification explicit and auditable.
6. Produce final outputs that include what changed, what was verified, what improved, and what remains risky.
7. Support both interactive use and repeatable team workflows.

### 4.2 User goals

Users should be able to say:

```text
/ultracode-high refactor the auth flow to support passkeys and update tests
```

or:

```text
/ultracode-high audit this dbt model and dashboard metric for correctness
```

or:

```text
/ultracode-high write a sharper PRD for this feature and have critics improve it
```

and receive a result that has gone through structured fan-out, synthesis, and verification.

---

## 5. Non-goals

1. Do not reproduce native Ultracode exactly.
2. Do not use `xhigh`, `max`, or `/effort ultracode` in strict mode.
3. Do not use Haiku, Sonnet, Fable, or non-Claude models in strict mode.
4. Do not create a hidden autonomous system that edits production, deploys, sends emails, or executes irreversible operations without explicit user permission.
5. Do not spawn agents for trivial tasks where one direct pass is better.
6. Do not optimize for lowest token cost; optimize for quality under a High-only constraint.
7. Do not trust subagent findings without synthesis and verification.
8. Do not let every specialist return full logs; every subagent must return a structured summary.

---

## 6. Target users and personas

### 6.1 Primary persona: senior engineer / technical lead

Needs help with large refactors, migrations, debugging, feature implementation, and code reviews. Values correctness, minimal regressions, and test evidence.

### 6.2 Primary persona: analytics specialist / BI developer

Needs help validating SQL, dbt models, dashboards, metric definitions, data contracts, lineage, grain, joins, and reconciliation. Values traceability and data quality.

### 6.3 Secondary persona: product / strategy operator

Needs help turning messy inputs into PRDs, strategy memos, launch plans, competitive analyses, and executive-ready writing. Values clarity, options, risks, decision logic, and polished narrative.

### 6.4 Secondary persona: documentation and writing owner

Needs drafts improved through structure, evidence checks, voice consistency, and adversarial editing.

---

## 7. Product principles

1. **High-only honesty.** The product must state that it emulates Ultracode-style workflow behavior but does not equal native Ultracode’s `xhigh` reasoning budget.
2. **Plan before parallelism.** Do not fan out blindly. First classify the task and identify independent workstreams.
3. **Use the right isolation.** Use named subagents for domain-specific work. Use `/fork` or fork-style review when the worker needs the full conversation context.
4. **No noisy returns.** Subagents must return finding cards, verification cards, or decision memos, not raw dumps.
5. **Adversarial by default for complex work.** Any S2+ task must include at least one reviewer whose job is to find flaws.
6. **Verification is a product feature.** Final output must distinguish verified facts, unverified assumptions, failed checks, and remaining risks.
7. **Do not outsource judgment to votes.** Multiple agents provide evidence; the integrator makes a decision.
8. **Context is a budget.** Every phase must summarize aggressively and maintain a compact context ledger.
9. **Stop when enough.** The router must avoid over-orchestrating small or sequential tasks.
10. **Business value matters.** For analytics and strategy, correctness is not enough; outputs must connect to decisions, stakeholders, and next actions.

---

## 8. Scope levels and routing model

The `ultracode-high` skill should classify every request into one of five scope levels.

| Scope | Name | Trigger | Default execution |
|---|---|---|---|
| S0 | Direct | Single-file/simple answer/no material risk | Main session only, no subagents |
| S1 | Focused specialist | One domain, limited uncertainty, moderate risk | 1 specialist + optional verifier |
| S2 | Fan-out | Multiple independent files/domains/questions | 2-5 specialists in parallel + integrator |
| S3 | Delivery swarm | Cross-layer implementation, tests, docs, review | cartographer → plan → implementer(s) → test runner → adversarial reviewer → final gate |
| S4 | Deep workflow | Repo-scale audit/migration/research, dozens of work units | optional saved workflow or agent team; otherwise batched subagent waves |

Routing rules:

- Use S0 when the answer can be completed safely in one direct pass.
- Use S1 when a specialist can isolate a narrow task without full swarm overhead.
- Use S2 when independent investigation paths exist.
- Use S3 when the task requires modifying code or producing a complex deliverable with verification.
- Use S4 only when the task would exceed the main context window or involves broad coverage as the success metric.

---

## 9. Core user experience

### 9.1 Main invocation

```text
/ultracode-high <task>
```

Expected behavior:

1. Parse the request.
2. Create an outcome contract.
3. Classify scope S0-S4.
4. Identify required specialists.
5. Ask clarifying questions only if a missing decision blocks safe progress.
6. Execute the planned mode.
7. Keep the user updated at phase boundaries.
8. Produce final deliverable with verification and improvement report.

### 9.2 Context-rich second opinion

```text
/fork Run the can-and-DOES-do-better protocol on the current work. Improve materially, report what changed, verify what can be verified, and return the final result.
```

Use when the final deliverable depends heavily on prior conversation context.

### 9.3 Specialist direct invocation

Examples:

```text
Use the data-bi-reviewer-high agent to audit this SQL and dashboard definition.
Use the adversarial-reviewer-high agent to find failure modes in this plan.
Use the test-and-build-runner-high agent to run the verification suite and summarize failures only.
```

### 9.4 Team/project install

Project-local install:

```text
.claude/skills/ultracode-high/SKILL.md
.claude/agents/*.md
```

Global install:

```text
~/.claude/skills/ultracode-high/SKILL.md
~/.claude/agents/*.md
```

---

## 10. Required subagents

All subagents must use:

```yaml
model: claude-opus-4-8
effort: high
```

### 10.1 MVP subagents

| Agent | Purpose | Tools | Writes? | When used |
|---|---|---:|---:|---|
| `ultracode-high-orchestrator` | Main coordinator for scope classification, fan-out, synthesis, and final handoff | Agent, Read, Grep, Glob, Bash | Optional | Main mode or top-level coordinator |
| `repo-cartographer-high` | Read-only repository mapping: architecture, dependencies, files, risk zones | Read, Grep, Glob, Bash | No | Before multi-file code work |
| `implementation-worker-high` | Implements scoped changes using repo conventions and minimal patches | Read, Edit, Write, Grep, Glob, Bash | Yes | S2-S3 code tasks |
| `test-and-build-runner-high` | Runs tests, lint, typecheck, build, data checks; summarizes failures only | Read, Grep, Glob, Bash | No by default | Any implementation or analytics verification |
| `adversarial-reviewer-high` | Looks for flaws, regressions, edge cases, unsupported claims, hidden risks | Read, Grep, Glob, Bash | No | Required for S2+ tasks |
| `final-integrator-high` | Merges findings, resolves conflicts, produces final result and verification ledger | Read, Grep, Glob, Bash | Optional | End of S2+ tasks |

### 10.2 Domain specialist subagents

| Agent | Purpose | Tools | Writes? | When used |
|---|---|---:|---:|---|
| `security-reviewer-high` | Auth, injection, secrets, permissions, data exposure, dependency risk | Read, Grep, Glob, Bash | No | Security-sensitive code changes |
| `performance-reviewer-high` | Algorithmic, query, rendering, network, concurrency, caching performance | Read, Grep, Glob, Bash | No | Performance-sensitive tasks |
| `data-bi-reviewer-high` | SQL/dbt/dashboard/metric correctness, grain, joins, nulls, reconciliation | Read, Grep, Glob, Bash | Optional | Analytics and BI work |
| `strategy-critic-high` | Business logic, options, tradeoffs, execution path, stakeholder risks | Read, Grep, Glob, Bash | No | Strategy, PRD, roadmap work |
| `writing-editor-high` | Structure, clarity, tone, evidence, executive polish | Read, Grep, Glob, Bash | Optional | Writing and docs deliverables |
| `ux-dashboard-reviewer-high` | Enterprise UI, dashboard UX, accessibility, information hierarchy | Read, Grep, Glob, Bash | No | Frontend/dashboard work |
| `context-compressor-high` | Produces compact state summaries, decision logs, and handoff context | Read, Grep, Glob, Bash | Optional | Long sessions or before compaction |
| `regression-guardian-high` | Checks backward compatibility, public APIs, fixtures, snapshots, migrations | Read, Grep, Glob, Bash | No | Refactors and migrations |

### 10.3 Optional Phase 3 subagents

| Agent | Purpose | Notes |
|---|---|---|
| `migration-operator-high` | Handles large, repetitive migration batches | Prefer `isolation: worktree` if editing many files |
| `debug-hypothesis-tester-high` | Tests one debugging hypothesis independently | Use multiple in parallel for hard failures |
| `dependency-impact-analyst-high` | Maps blast radius across dependencies and downstream consumers | Useful for monorepos |
| `release-note-writer-high` | Creates changelog, PR summary, migration note, docs update | Uses writing skill |
| `benchmark-runner-high` | Runs benchmarks and compares before/after | Read/Bash only unless configured otherwise |

---

## 11. Recommended subagent frontmatter patterns

### 11.1 Read-only specialist template

```yaml
---
name: repo-cartographer-high
description: Read-only Opus 4.8 High repository cartographer. Use for mapping architecture, dependencies, relevant files, conventions, and risk zones before multi-file implementation or review.
model: claude-opus-4-8
effort: high
tools: Read, Grep, Glob, Bash
permissionMode: plan
maxTurns: 20
color: blue
skills:
  - evidence-ledger
  - context-ledger
---
```

Body requirements:

- Never edit files.
- Return only a compact map.
- Include file paths and line references when possible.
- Identify unknowns and confidence levels.
- Do not include raw command logs unless required.

### 11.2 Implementation specialist template

```yaml
---
name: implementation-worker-high
description: Opus 4.8 High implementation worker for scoped code changes. Use after planning when the change is bounded, testable, and has acceptance criteria.
model: claude-opus-4-8
effort: high
tools: Read, Edit, Write, Grep, Glob, Bash
permissionMode: acceptEdits
maxTurns: 40
color: green
skills:
  - implementation-contract
  - verification-matrix
  - context-ledger
---
```

Body requirements:

- Read existing conventions before editing.
- Prefer minimal changes.
- Maintain behavior unless explicitly asked to change it.
- Add or update tests where appropriate.
- Report exact files changed and verification performed.
- Stop and ask the orchestrator if requirements conflict.

### 11.3 Adversarial reviewer template

```yaml
---
name: adversarial-reviewer-high
description: Opus 4.8 High adversarial reviewer. Use after plans, code changes, analytics outputs, PRDs, or final drafts to find errors, omissions, weak evidence, regressions, and unsupported claims.
model: claude-opus-4-8
effort: high
tools: Read, Grep, Glob, Bash
permissionMode: plan
maxTurns: 25
color: red
skills:
  - can-and-must-do-better
  - evidence-ledger
  - verification-matrix
---
```

Body requirements:

- Assume the current answer may be wrong.
- Find concrete failure modes.
- Separate critical blockers from polish.
- Provide evidence and reproducible checks.
- Do not rewrite the entire deliverable unless asked; return actionable findings.

### 11.4 Context compressor template

```yaml
---
name: context-compressor-high
description: Opus 4.8 High context compressor. Use during long tasks to preserve decisions, evidence, commands, files touched, open risks, and next actions while dropping noisy details.
model: claude-opus-4-8
effort: high
tools: Read, Grep, Glob, Bash
permissionMode: plan
maxTurns: 10
color: cyan
skills:
  - context-ledger
---
```

Body requirements:

- Produce a handoff block that can restart the task.
- Include only stable facts, decisions, evidence, open issues, and next actions.
- Do not include full logs.

---

## 12. Required skills

### 12.1 MVP skills

| Skill | Purpose | Invocation style | Context |
|---|---|---|---|
| `ultracode-high` | Top-level orchestration protocol | User + model | Inline |
| `task-intake-contract` | Converts messy request into goal, constraints, acceptance criteria, and missing decisions | Preloaded by orchestrator | Inline |
| `decomposition-router` | Classifies S0-S4 and chooses agents | Preloaded by orchestrator | Inline |
| `implementation-contract` | Coding standards: minimal diff, tests, repo conventions, rollback | Preloaded by implementer | Inline |
| `verification-matrix` | Standard verification gates for code, analytics, BI, writing | Preloaded by reviewers | Inline |
| `evidence-ledger` | Evidence/facts/assumptions format | Preloaded broadly | Inline |
| `context-ledger` | Compact task state and handoff format | Preloaded broadly | Inline |
| `final-report` | Final answer format: result, changes, verification, risks, follow-ups | Preloaded by integrator | Inline |
| `can-and-must-do-better` | Second-pass self-review and improvement demand | Existing dependency | Inline or fork |

### 12.2 Domain skills

| Skill | Purpose | Used by |
|---|---|---|
| `analytics-bi-rigor` | Metric grain, joins, nulls, filters, freshness, lineage, reconciliation | `data-bi-reviewer-high`, orchestrator |
| `strategy-rigor` | Options, decision criteria, economics, execution, risk, measurement | `strategy-critic-high` |
| `writing-rigor` | Structure, clarity, audience, voice, evidence, concision | `writing-editor-high` |
| `security-rigor` | Auth, injection, secrets, dependency, supply-chain, privacy checks | `security-reviewer-high` |
| `performance-rigor` | Complexity, DB efficiency, frontend performance, caching, concurrency | `performance-reviewer-high` |
| `ux-dashboard-rigor` | Dashboard design, visual hierarchy, accessibility, enterprise UI standards | `ux-dashboard-reviewer-high` |

### 12.3 Optional workflow skills

| Skill | Purpose | Context |
|---|---|---|
| `high-code-research` | Standalone repo exploration in isolated context | `context: fork`, custom read-only agent |
| `high-code-review` | Review current diff | `context: fork`, adversarial reviewer |
| `high-code-verify` | Run test/lint/build/check suite and return compact result | `context: fork`, test runner |
| `high-code-final-gate` | Forked final review with full result contract | `context: fork`, final integrator |

Important distinction:

- Use inline skills for standing guidance that the main session needs to remember.
- Use `context: fork` skills only for explicit, self-contained tasks where the skill content includes all necessary instructions.
- Use `/fork` directly when the reviewer must inherit the full parent conversation.

---

## 13. Top-level `ultracode-high` skill requirements

The `ultracode-high` skill should have frontmatter similar to:

```yaml
---
name: ultracode-high
description: Opus 4.8 High-only orchestration mode for complex coding, analytics, BI, strategy, and writing tasks. Use when a task spans multiple files or domains, has material risk, needs verification, or benefits from parallel review.
when_to_use: Invoke for large refactors, debugging, feature builds, analytics audits, dashboard/SQL checks, PRDs, strategy memos, and high-stakes writing where a single-pass answer may miss issues.
model: claude-opus-4-8
effort: high
allowed-tools: Agent Read Grep Glob Bash Edit Write
---
```

The body should define this protocol:

1. **Intake.** Restate the outcome, constraints, acceptance criteria, and blocking unknowns.
2. **Classify.** Assign S0-S4 scope.
3. **Choose mode.** Direct, single specialist, fan-out, delivery swarm, or deep workflow.
4. **Decompose.** Create work packages with owners and expected outputs.
5. **Delegate.** Spawn only the agents needed.
6. **Constrain returns.** Require finding cards, not raw logs.
7. **Synthesize.** Merge findings into one coherent result.
8. **Verify.** Run applicable checks.
9. **Improve.** Apply `can-and-must-do-better` before final response.
10. **Report.** Return final result, how it improved, verification ledger, and remaining risks.

---

## 14. Orchestration algorithm

### 14.1 Pseudocode

```text
on /ultracode-high(task):
  contract = build_task_intake_contract(task)
  scope = classify_scope(contract)

  if scope == S0:
      do_direct_work()
      self_review_light()
      return final_report()

  if scope == S1:
      specialist = select_best_specialist(contract)
      result = run_subagent(specialist, contract)
      verification = run_optional_verifier(contract, result)
      integrated = synthesize(result, verification)
      improve(integrated)
      return final_report()

  if scope == S2:
      packages = decompose_into_independent_workstreams(contract)
      results = run_parallel_subagents(packages)
      review = run_adversarial_review(results)
      integrated = synthesize(results, review)
      verify(integrated)
      improve(integrated)
      return final_report()

  if scope == S3:
      map = run(repo-cartographer-high)
      plan = create_implementation_plan(map, contract)
      implement = run(implementation-worker-high, plan)
      tests = run(test-and-build-runner-high, implement)
      reviews = run_parallel([
          adversarial-reviewer-high,
          security-reviewer-high if relevant,
          data-bi-reviewer-high if relevant,
          performance-reviewer-high if relevant
      ])
      fix_blockers()
      final = run(final-integrator-high)
      improve(final)
      return final_report()

  if scope == S4:
      ask for user confirmation on broad run and budget
      choose batched subagent waves or saved high-only workflow
      run coverage batches
      cross-check findings
      synthesize into prioritized output
      verify sampled results and critical paths
      improve and final_report()
```

### 14.2 Fan-out limits

Default limits for High-only mode:

| Scope | Default concurrent agents | Max agents per wave | Notes |
|---|---:|---:|---|
| S1 | 1 | 2 | optional verifier |
| S2 | 2-4 | 5 | independent paths only |
| S3 | 3-6 | 8 | separate plan/implement/review/test roles |
| S4 | 4-8 per wave | 12 | ask before broad runs; consider saved workflow |

The clone should avoid huge agent counts by default because High-only orchestration relies on structure, not brute-force token spending.

---

## 15. Output contracts

### 15.1 Work package card

Every delegated task should include:

```yaml
id: short stable identifier
owner: agent name
goal: one-sentence outcome
scope: files, modules, datasets, docs, or sections
inputs: relevant constraints and context
allowed_actions: read-only | edit | run-tests | write-docs
expected_output: finding-card | patch-summary | verification-card | memo
success_criteria: observable checks
stop_conditions: when to ask orchestrator instead of continuing
```

### 15.2 Finding card

Every reviewer finding should use:

```yaml
finding_id:
severity: critical | high | medium | low | suggestion
confidence: high | medium | low
category: correctness | security | performance | data-quality | UX | writing | strategy | maintainability
evidence: file/line, command, data check, quote, or reasoning basis
impact: why it matters
recommendation: specific fix or decision
verification: how to confirm the fix
```

### 15.3 Verification card

Every verification pass should use:

```yaml
check:
command_or_method:
status: passed | failed | skipped | not-applicable
summary:
evidence:
failure_details:
next_action:
```

### 15.4 Context ledger

At phase boundaries, maintain:

```yaml
objective:
constraints:
files_touched:
files_read:
commands_run:
decisions_made:
assumptions:
verified:
failed_or_skipped_checks:
open_risks:
next_actions:
```

### 15.5 Final report

Every final response should include:

1. Final result or deliverable.
2. What changed or what was produced.
3. How the work was improved by the final self-review.
4. Verification performed.
5. Remaining risks or assumptions.
6. Clear next step if human action is required.

---

## 16. Analytics and BI requirements

Analytics tasks must use `analytics-bi-rigor` and normally route to `data-bi-reviewer-high`.

### 16.1 Required checks

1. Metric definition: numerator, denominator, filters, time window, dimensionality.
2. Grain: source grain, join grain, output grain, dashboard grain.
3. Join safety: cardinality, fanout, duplicates, missing keys.
4. Filter logic: inclusive/exclusive dates, timezone, status filters, deleted/test rows.
5. Null and zero behavior: denominator zero, null categories, missing facts.
6. Reconciliation: compare to known totals or source-of-truth tables.
7. Freshness: data update cadence, lag, late-arriving records.
8. Lineage: upstream and downstream dependencies.
9. BI semantics: dashboard filters, drill paths, totals, row-level security.
10. Decision relevance: what business decision the analysis supports.

### 16.2 Analytics final output

Analytics outputs must include:

- metric contract;
- SQL or model changes;
- data checks run;
- reconciliation results;
- caveats;
- recommended business interpretation;
- what not to conclude.

---

## 17. Code requirements

### 17.1 Implementation standards

For code tasks, `implementation-worker-high` must:

1. inspect existing patterns before editing;
2. minimize diff size;
3. avoid broad rewrites unless justified;
4. preserve public behavior unless requirements say otherwise;
5. add or update tests when feasible;
6. avoid deleting code without understanding references;
7. document migrations and breaking changes;
8. run the appropriate checks;
9. stop if tests require secrets, services, or environment not available.

### 17.2 Review standards

For S2+ code tasks, the system must run at least one independent adversarial review. For security-sensitive changes, also run `security-reviewer-high`. For performance-sensitive or data-heavy changes, run the relevant domain reviewer.

### 17.3 Verification standards

Default verification matrix:

| Stack signal | Check examples |
|---|---|
| JavaScript/TypeScript | package manager detection, lint, typecheck, tests, build |
| Python | pytest, ruff, mypy/pyright when configured, package tests |
| SQL/dbt | dbt compile, dbt test, targeted query checks |
| Frontend | build, component tests, accessibility review, snapshot update check |
| APIs | unit tests, contract tests, route coverage, auth checks |
| Docs/writing | links, factual support, structure, consistency |

The system should not invent a verification result. If a check cannot run, mark it `skipped` or `not available` and explain why.

---

## 18. Writing and strategy requirements

Writing and strategy tasks should still use the same `ultracode-high` flow, but with different specialists.

### 18.1 PRD/strategy workstream

Use:

- `strategy-critic-high` for business logic and decision quality;
- `writing-editor-high` for clarity and polish;
- `adversarial-reviewer-high` for gaps and unsupported claims;
- `final-integrator-high` for the final artifact.

### 18.2 Required strategy checks

1. Who is the customer or stakeholder?
2. What problem is being solved?
3. What decision must be made?
4. What are the options?
5. What are the tradeoffs?
6. What assumptions drive the recommendation?
7. What evidence supports the recommendation?
8. What are the risks and mitigations?
9. What are the measurable success criteria?
10. What is the execution path?

### 18.3 Required writing checks

1. Audience fit.
2. Clear thesis.
3. Logical structure.
4. No unsupported claims.
5. Concise language.
6. Consistent terminology.
7. Actionable next steps.
8. Executive summary when long.
9. TLDR table when useful.

---

## 19. Context window management

The product must aggressively manage context.

### 19.1 Rules

1. Main session receives summaries, not raw logs.
2. Subagents return structured cards.
3. Long-running tasks maintain a context ledger.
4. Before compaction or after major phases, run `context-compressor-high`.
5. Use named subagents for fresh-context specialized tasks.
6. Use `/fork` when the reviewer needs full parent context.
7. Use worktree isolation for high-risk parallel edits.
8. Do not spawn agents that all read the same huge files unless each has a distinct purpose.

### 19.2 Subagent return budget

Each subagent should target:

- 10-20 bullets for broad map outputs;
- 3-7 finding cards for reviews;
- 1 verification table for test runners;
- no raw log longer than 50 lines unless specifically requested.

### 19.3 Handoff summary

A compact handoff should be sufficient to restart the task in a new Claude Code session.

---

## 20. Safety, permissions, and governance

### 20.1 Permission defaults

| Agent type | Default permission mode | Reason |
|---|---|---|
| cartographers/reviewers | `plan` or read-only tools | Prevent accidental edits |
| implementation workers | `acceptEdits` only when scoped | Allows code changes after plan |
| test runners | read-only + Bash | Runs checks without modifying files |
| migration operators | `acceptEdits` + `isolation: worktree` | Avoids main checkout conflicts |
| final integrator | read-only unless writing final docs | Reduces late-stage accidental edits |

### 20.2 Guardrails

1. Block destructive shell commands unless explicitly approved.
2. Never expose secrets in final summaries.
3. Do not run deployment, production data mutation, irreversible migrations, or destructive file operations without explicit user confirmation.
4. Use worktrees for competing implementations.
5. Require plan approval before schema changes, auth changes, destructive migrations, or broad rewrites.
6. Document any skipped verification.

### 20.3 Optional hooks

Add hooks later for deterministic enforcement:

- `PreToolUse` hook to block dangerous Bash commands.
- `PostToolUse` hook to summarize huge outputs or flag failed commands.
- `SubagentStop` hook to reject subagent output that lacks required sections.
- `TeammateIdle` hook, if agent teams are enabled, to require quality gates before teammates go idle.

---

## 21. Observability and auditability

The product should make orchestration visible enough to trust without overwhelming the user.

### 21.1 User-visible progress

For S2+ tasks, send updates at phase boundaries:

1. Intake and scope classification.
2. Agent plan.
3. Implementation/checkpoint.
4. Verification result.
5. Final synthesis.

### 21.2 Internal trace

Maintain a compact task ledger with:

- agents used;
- files read;
- files edited;
- commands run;
- checks passed/failed/skipped;
- unresolved risks;
- final review improvements.

### 21.3 Evaluation logs

For internal product improvement, track:

- scope level chosen;
- number of subagents spawned;
- wall-clock time;
- commands executed;
- test status;
- number of critical reviewer findings;
- whether final answer changed after `can-and-must-do-better`;
- user follow-up corrections.

---

## 22. Functional requirements

### FR1: High-only enforcement

Every provided subagent and skill must pin `model: claude-opus-4-8` and `effort: high`. The orchestrator must not instruct users to switch to `xhigh`, `max`, or `/effort ultracode` in strict mode.

### FR2: Task intake contract

The orchestrator must produce an internal contract with goal, constraints, acceptance criteria, risk level, and missing decisions.

### FR3: Scope classification

The orchestrator must classify S0-S4 and explain the classification briefly for S2+ tasks.

### FR4: Agent selection

The orchestrator must select the minimal sufficient agent set.

### FR5: Parallel fan-out

For S2+ tasks with independent workstreams, the orchestrator must run multiple agents in parallel or in batched waves.

### FR6: Context isolation

Noisy search, logs, tests, and broad reviews must run outside the main context when possible.

### FR7: Structured returns

Subagents must return work package results, finding cards, verification cards, or decision memos.

### FR8: Verification matrix

The system must run or explicitly skip the relevant checks.

### FR9: Adversarial review

S2+ tasks must include an adversarial review before final delivery.

### FR10: Improvement loop

The final answer must be processed through `can-and-must-do-better` or the equivalent final-gate protocol.

### FR11: Final report

Final output must include result, changes, verification, risks, and what improved in the final pass.

### FR12: Analytics/BI specialization

Analytics tasks must use data-quality and metric-grain checks.

### FR13: Writing/strategy specialization

Writing and strategy tasks must use structure, evidence, audience, and decision-quality checks.

### FR14: Safety prompts

The system must ask for explicit user confirmation before destructive operations, production-affecting operations, broad schema changes, or sensitive data actions.

### FR15: Installability

The project must be installable as a folder tree under `.claude/skills/` and `.claude/agents/`, and optionally packaged as a plugin later.

---

## 23. Non-functional requirements

| Requirement | Target |
|---|---|
| Reliability | Final answer must not claim tests passed unless they ran and passed |
| Latency | S0 stays direct; S2+ accepts slower execution for quality |
| Cost control | Agent fan-out bounded by scope defaults |
| Security | Read-only by default for reviewers and cartographers |
| Maintainability | Agents are focused, reusable, and version-controlled |
| Portability | Works in project-local and user-global Claude Code installs |
| Auditability | Verification ledger included in final output |
| Context efficiency | Main context receives summaries only |
| Human control | User can approve or cancel broad runs |

---

## 24. MVP package

### 24.1 Files to create first

```text
.claude/
  skills/
    ultracode-high/SKILL.md
    task-intake-contract/SKILL.md
    decomposition-router/SKILL.md
    implementation-contract/SKILL.md
    verification-matrix/SKILL.md
    evidence-ledger/SKILL.md
    context-ledger/SKILL.md
    final-report/SKILL.md
    can-and-must-do-better/SKILL.md
  agents/
    ultracode-high-orchestrator.md
    repo-cartographer-high.md
    implementation-worker-high.md
    test-and-build-runner-high.md
    adversarial-reviewer-high.md
    final-integrator-high.md
```

### 24.2 MVP workflows

1. Code change with tests.
2. Code review of current diff.
3. Analytics/SQL audit.
4. PRD/writing improvement.
5. Debugging with one or more hypotheses.

### 24.3 MVP acceptance criteria

The MVP is acceptable when:

1. `/ultracode-high` reliably classifies tasks S0-S4.
2. It avoids subagents for simple tasks.
3. It spawns appropriate subagents for complex tasks.
4. Every spawned subagent returns a structured summary.
5. S2+ tasks receive adversarial review.
6. Final output includes verification status and remaining risks.
7. No file in the package uses non-Opus models or non-high effort.
8. A long task can be compacted into a context ledger and resumed.

---

## 25. Phase 2 package

Add domain agents and skills:

```text
.claude/
  skills/
    analytics-bi-rigor/SKILL.md
    strategy-rigor/SKILL.md
    writing-rigor/SKILL.md
    security-rigor/SKILL.md
    performance-rigor/SKILL.md
    ux-dashboard-rigor/SKILL.md
  agents/
    data-bi-reviewer-high.md
    strategy-critic-high.md
    writing-editor-high.md
    security-reviewer-high.md
    performance-reviewer-high.md
    ux-dashboard-reviewer-high.md
    context-compressor-high.md
    regression-guardian-high.md
```

Phase 2 success criteria:

1. Analytics tasks produce metric contracts and data validation plans.
2. PRD/strategy tasks include options, assumptions, and success metrics.
3. Security-sensitive code changes trigger security review.
4. Long sessions produce compact handoff summaries.
5. Reviewer findings are deduplicated and prioritized.

---

## 26. Phase 3 package

Add advanced orchestration:

```text
.claude/
  agents/
    migration-operator-high.md
    debug-hypothesis-tester-high.md
    dependency-impact-analyst-high.md
    release-note-writer-high.md
    benchmark-runner-high.md
  hooks/
    block-dangerous-bash.sh
    require-subagent-output-contract.sh
    summarize-large-tool-output.sh
  workflows/
    high-code-audit.js
    high-code-migration.js
    high-code-deep-research.js
```

Phase 3 success criteria:

1. Large audits can run in batches with coverage tracking.
2. Migration runs can use isolated worktrees.
3. Hooks enforce dangerous-command blocking and output contracts.
4. Optional saved workflows can be rerun for repeated audits.
5. Agent teams can be enabled for tasks where specialists need to message each other directly.

---

## 27. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| High-only mode under-reasons vs native Ultracode | Missed edge cases | Use explicit decomposition, adversarial review, and verification gates |
| Too many agents increase cost/latency | Poor UX | S0-S4 router and fan-out caps |
| Subagents return verbose logs | Main context pollution | Strict output contracts and optional SubagentStop hook |
| Agents conflict on file edits | Broken working tree | Use one implementer by default; use worktrees for parallel edits |
| Reviewer finds issues but integrator ignores them | False confidence | Final report must list critical findings and disposition |
| Tests unavailable locally | Incomplete verification | Mark skipped checks clearly and provide manual verification steps |
| Skills become too long | Context bloat after invocation | Keep `SKILL.md` concise; put detailed references in supporting files |
| Agent teams instability | Lost coordination | Treat teams as optional Phase 3 only |
| Security-sensitive commands run accidentally | Data loss or exposure | Read-only defaults, hooks, explicit confirmations |
| Over-orchestration for small tasks | Slower than normal Claude Code | S0 direct path and scope thresholds |

---

## 28. Success metrics

### 28.1 Quality metrics

- Percentage of S2+ tasks with documented verification.
- Percentage of code tasks where tests/lint/build status is reported accurately.
- Number of critical issues found by adversarial reviewer before final delivery.
- Reduction in user-reported missed requirements.
- Reduction in follow-up corrections after final answer.
- PR acceptance rate or reduced reviewer comments.

### 28.2 Context metrics

- Main-session token growth per complex task.
- Subagent output compression ratio.
- Number of long tasks successfully resumed from context ledger.
- Frequency of compaction-related loss of important decisions.

### 28.3 Productivity metrics

- Time to first plan.
- Time to final verified output.
- Number of user interventions needed.
- Number of repeated manual prompts eliminated.
- Percentage of workflows that can be reused.

### 28.4 Analytics/BI metrics

- Percentage of metric changes with explicit grain definition.
- Percentage of dashboard audits with reconciliation checks.
- Number of join/cardinality issues caught before delivery.
- Number of freshness or filter caveats documented.

---

## 29. Test plan

### 29.1 Fixture tasks

Create a small benchmark suite of representative tasks:

1. Single-file bug fix — should route S0 or S1.
2. Multi-file feature implementation — should route S3.
3. SQL metric bug — should route to data/BI review.
4. Dashboard spec review — should use UX/dashboard and analytics checks.
5. PRD rewrite — should use strategy and writing critics.
6. Hard debugging task — should spawn competing hypothesis testers.
7. Repo-wide audit — should route S4 and ask for confirmation.

### 29.2 Evaluation rubric

Each test task should be scored on:

- correct scope classification;
- appropriate agent selection;
- relevant evidence gathered;
- correctness of output;
- verification accuracy;
- context efficiency;
- clarity of final report;
- whether the final self-review materially improved the result.

---

## 30. Open questions

1. Should strict mode forbid built-in Claude Code agents that may use non-Opus models?
2. Should the orchestrator ask before S3 fan-out, or only before S4?
3. Should implementation workers default to `isolation: worktree` for all edits, or only risky edits?
4. How much progress reporting does the user want during long runs?
5. Should hooks be bundled by default or offered as an opt-in hardened mode?
6. Should the feature be packaged as a plugin after the skills and agents stabilize?
7. Should the final report always include a TLDR table, or only for long deliverables?
8. How should the system detect analytics repositories, dbt projects, notebooks, semantic layers, and BI config files automatically?

---

## 31. Recommended build order

1. Create `ultracode-high` skill.
2. Create the six MVP agents.
3. Add `can-and-must-do-better` as a required final gate.
4. Create output-contract skills: evidence, verification, context, final report.
5. Test on five fixture tasks.
6. Add domain specialists for analytics, strategy, writing, security, and performance.
7. Add hooks for destructive command blocking and subagent output contracts.
8. Add optional saved workflows for repeated large audits.
9. Package as a Claude Code plugin if used across teams.

---

## 32. Summary

The best high-only Ultracode clone is not a single giant prompt. It is a small operating system of Claude Code skills and subagents. The top-level `ultracode-high` skill decides when orchestration is warranted. Specialized Opus 4.8 High subagents perform isolated research, implementation, testing, review, analytics validation, strategy critique, and writing polish. The final result goes through a mandatory “can and must do better” gate and returns with a verification ledger.

The clone should deliberately avoid pretending to be native Ultracode. Its value comes from making Opus 4.8 High act more like a disciplined delivery team: plan, fan out, verify, criticize, integrate, and report.

---

## 33. TLDR table

| Area | Recommendation |
|---|---|
| Product name | `ultracode-high` |
| Core constraint | Claude Opus 4.8 only, `effort: high` only |
| MVP agents | orchestrator, repo cartographer, implementer, test runner, adversarial reviewer, final integrator |
| MVP skills | ultracode-high, intake contract, decomposition router, implementation contract, verification matrix, evidence ledger, context ledger, final report, can-and-must-do-better |
| Main behavior | classify S0-S4, fan out when useful, verify, adversarially review, synthesize |
| Context strategy | named subagents for isolated work, `/fork` for full-context reviews, context ledger for handoffs |
| Analytics support | dedicated BI reviewer and metric-grain validation skill |
| Writing support | strategy critic, writing editor, evidence checks |
| Code support | cartography, scoped implementation, test/build runner, security/performance/regression review |
| Safety | read-only reviewers, explicit confirmations, optional hooks for destructive commands |
| MVP success | complex tasks produce better verified outputs without using `xhigh` or native Ultracode |

---

## Source notes

This PRD is based on the official Claude Code documentation for dynamic workflows, custom subagents, skills, forks, agent teams, hooks, and Anthropic guidance for Claude Opus 4.8 effort levels and prompting behavior.
