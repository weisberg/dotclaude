---
name: analytics-spec-builder
description: Use this skill proactively when the user asks Claude Code to create, tighten, review, or improve a specification for a scoped analytics task/project—not a whole software product—including dashboards, reports, SQL/dbt models, metric definitions, semantic-layer changes, experiment/cohort analyses, data quality checks, reconciliations, KPI automation, notebooks, or analytics refactors. Ask targeted user questions, inspect relevant repo context, convert ambiguity into explicit assumptions/decisions, and produce an implementation-ready spec with scope, data sources, metric logic, grain, filters, validation plan, acceptance criteria, risks, and open questions before coding.
---

# Analytics Spec Builder

## Mission

Create or improve specifications for spec-driven analytics work. The output should make a scoped analytics task or project ready for implementation by clarifying what to build, why it matters, what data and definitions to use, how correctness will be judged, and what is explicitly out of scope.

This skill is for analytics-domain projects such as dashboards, reports, SQL/dbt models, semantic-layer changes, metric definitions, KPI automations, notebooks, experiment analyses, cohort analyses, data quality checks, reconciliations, and analytics refactors. It is not for broad product requirements, full application design, or company-wide strategy documents unless the user explicitly narrows the request to a concrete analytics deliverable.

## Core operating rules

1. **Ask questions before finalizing.** Ask targeted clarifying questions whenever important details are missing. Prefer 3-5 high-value questions in the first pass, not a long interrogation.
2. **Make questions easy to answer.** Use numbered questions. Include a recommended default or likely option when possible, and briefly explain why the question matters. Treat recommended defaults as proposals, not facts.
3. **Do not ask what the repo can answer.** First inspect available context when it is likely to contain the answer, then ask only for unresolved stakeholder/business decisions.
4. **Inspect available context.** In Claude Code, use read-only repo inspection to find existing specs, models, dashboards, tests, metric definitions, and naming conventions before inventing structure.
5. **Separate facts from assumptions.** Clearly label confirmed facts, assumptions, decisions, risks, and open questions. Do not invent owners, column names, tables, or approval paths.
6. **Treat analytics details as contract details.** Metric formulas, grain, filters, exclusions, time logic, joins, refresh cadence, privacy/access constraints, and validation are central requirements, not implementation trivia.
7. **Protect sensitive data.** Avoid copying raw PII or secrets into specs. Use masked examples or aggregate descriptions unless exact values are necessary and appropriate.
8. **Avoid premature implementation.** Do not edit production code, build models, or change dashboards while in spec-building mode unless the user explicitly asks you to proceed after the spec is drafted or approved.
9. **Keep the scope task-sized.** If the request expands into a whole product or program, narrow it into one or more analytics deliverable specs.

## First response pattern

When the skill triggers, choose the lightest pattern that fits the request:

- **Need context first:** briefly say you will inspect the repo/files, then use read-only discovery before asking questions or drafting.
- **Blocked by missing essentials:** ask 3-5 clarifying questions first. Do not draft a fake-complete spec.
- **Enough to draft:** create a provisional spec and include an `Open Questions` section for unresolved details.
- **User asks not to ask questions:** produce a provisional spec with explicit assumptions and a prominent list of items that still need confirmation.

A good first-pass question has this shape:

> 1. Which timestamp should define the reporting period: event time, created time, or completed time? Recommended default: event time, because it usually matches business activity unless this is an operations SLA report.

## Read-only context gathering in Claude Code

Use only the commands needed for the current task. Prefer targeted inspection over broad scans.

Suggested discovery commands:

```bash
pwd
ls
rg --files | rg -i '(^|/)(docs|specs|models|notebooks|dashboards|reports|semantic|lookml|tests|analysis|dbt|\.claude)/|spec|requirement|metric|dashboard|report'
find . -maxdepth 3 \( -iname '*spec*' -o -iname '*requirement*' -o -iname '*metric*' \) 2>/dev/null | head -100
rg -n "dashboard|metric|KPI|cohort|experiment|quality|reconciliation|acceptance|grain|dbt|LookML|semantic" .
```

Look for relevant context in:

- `README`, `docs/`, `specs/`, `tickets/`, `.claude/`, or project planning folders
- `dbt_project.yml`, `models/**/*.sql`, `models/**/*.yml`, `metrics.yml`, semantic model files, exposures, tests, snapshots, and seeds
- LookML, Tableau/Power BI/Mode/Hex/Looker Studio config, dashboard definitions, and dashboard screenshots if present
- notebooks, saved queries, scripts, orchestration files, data quality tests, and reconciliation queries
- existing metric dictionaries, data contracts, naming conventions, owner metadata, and review checklists

Do not run destructive commands. Do not run expensive queries or modify files unless the user asks and the project context makes it appropriate. Avoid dumping large files into context; inspect only the relevant sections.

## Classify the analytics request

Classify the task before drafting because each type needs different questions and acceptance criteria.

| Request type | Typical examples | Spec emphasis |
| --- | --- | --- |
| Dashboard/report | Add a filter, create a KPI dashboard, revise a report | Audience, decisions supported, layout, filters, defaults, refresh, access, QA |
| SQL/dbt/modeling | Build or change a model, add a field, refactor logic | Grain, primary key, sources, joins, incremental/backfill behavior, tests, downstream dependencies |
| Metric definition | Define churn, activation, conversion, ARR, retention | Business meaning, formula, numerator/denominator, time basis, exclusions, source of truth |
| Data discrepancy/bug | Numbers do not match, dashboard looks wrong | Observed vs expected, examples, source of truth, impact, root-cause hypotheses, validation |
| Experiment/cohort/ad hoc analysis | Evaluate a test, retention cohort, segmentation analysis | Unit of analysis, windows, assignment/exposure logic, metric hierarchy, cuts, methodology |
| Data quality/monitoring | Freshness, uniqueness, nulls, anomaly detection | Rule, threshold, severity, owner, alerting/reporting path, remediation expectation |
| Migration/refactor | Move dashboard/model/logic without behavior change | Parity definition, downstream dependencies, cutover plan, rollback, historical backfill |
| KPI automation | Scheduled report, recurring extract, executive metric pack | Schedule, recipients/consumers, format, freshness SLA, failure handling, sign-off |

## Clarifying question protocol

Ask only questions that would materially change the spec or implementation. Prioritize in this order:

1. **Outcome:** What decision, action, or workflow should this support?
2. **Consumer:** Who will use it and in what format?
3. **Scope:** What is in scope, out of scope, and non-negotiable?
4. **Data contract:** Which sources, grain, time basis, filters, and definitions are authoritative?
5. **Correctness:** What validation target, tolerance, and acceptance criteria define done?
6. **Operational constraints:** Refresh, latency, access, privacy, owners, dependencies, and rollout.

Use these question banks selectively.

### Universal questions

- What decision or action should this work enable?
- Who is the primary audience, and where will they consume the output?
- What is the smallest useful deliverable for this iteration?
- What is explicitly out of scope?
- What existing asset should be treated as the source of truth?
- What would make the stakeholder say this is done?
- What validation target should the final output reconcile to?
- Are there privacy, access, or sensitive-data constraints?

### Dashboard/report questions

- Which dashboard/report should be created or changed, and where does it live?
- Should the change apply globally or only to specific tiles/pages/views?
- What are the default filter values, date range, timezone, and comparison periods?
- Which metrics must be shown, hidden, renamed, or drillable?
- What export, subscription, alert, or sharing behavior is required?
- What freshness SLA is acceptable, and how should stale data be communicated?

### SQL/dbt/modeling questions

- What is the target model/table name and intended grain?
- What columns are required, and which are dimensions, measures, keys, or metadata?
- Which upstream sources are authoritative, and what join keys/cardinalities are expected?
- Should the model be full-refresh, incremental, snapshot-based, or ephemeral?
- Is historical backfill required? If yes, for what date range?
- What tests are required: uniqueness, not-null, accepted values, relationships, freshness, custom assertions?

### Metric definition questions

- What is the business definition in plain language?
- What are the numerator, denominator, eligibility criteria, and exclusions?
- What is the entity grain: user, account, order, session, subscription, event, or something else?
- Which timestamp controls the metric period?
- How should nulls, duplicates, late-arriving records, refunds/cancellations, test/internal records, and inactive entities be handled?
- Which existing report or query should this match, and what tolerance is acceptable?

### Experiment/cohort/ad hoc analysis questions

- What is the unit of analysis and population eligibility?
- How are cohorts, treatments, exposures, or segments assigned?
- What are the primary, secondary, and guardrail metrics?
- What analysis window, observation window, and timezone should be used?
- What cuts or segments are required?
- What methodology is expected: descriptive readout, confidence intervals, hypothesis test, causal estimate, or exploratory analysis?

### Data discrepancy/bug questions

- What exact number looks wrong, where was it observed, and when?
- What was the expected number, and what source produced it?
- Provide one or more example entities, dates, dashboard tiles, or query results that reproduce the issue.
- What business impact or stakeholder impact is known?
- Should the spec focus on root-cause investigation, remediation, or both?

### Data quality/monitoring questions

- What rule should be monitored, and at what grain?
- What threshold separates pass, warn, and fail?
- How often should the check run, and how fresh must the data be?
- Who owns remediation, and what should happen when the rule fails?
- Should the check block deployments, alert consumers, or only create a report?

### Migration/refactor questions

- What behavior must remain identical after the change?
- Which downstream assets depend on the current asset?
- What parity checks are required before cutover?
- Is a historical backfill needed?
- What is the rollback plan if numbers diverge?

## Spec template

Use this structure unless the repository already has a convention. Keep sections concise; omit sections that do not apply, but do not omit data definitions, validation, or acceptance criteria for analytics work.

```markdown
# [Task / Project Name] Spec

## Status
Draft | In Review | Approved | Implemented

## Owner and reviewers
- Owner:
- Reviewers:
- Stakeholders / consumers:

## Summary
One-paragraph description of the requested analytics deliverable or change.

## Background
What prompted the request, current pain point, and relevant existing assets.

## Objective
The decision, action, workflow, or stakeholder outcome this work supports.

## Deliverables
- [ ] Artifact 1: dashboard/report/model/query/notebook/test/spec update
- [ ] Artifact 2:

## Scope
### In scope
- 

### Out of scope
- 

## Current state
Existing dashboards, reports, models, queries, docs, or workflows that matter.

## Data contract
### Sources of truth
| Source | Role | Notes |
| --- | --- | --- |
|  |  |  |

### Grain and keys
- Target grain:
- Primary / unique key:
- Required dimensions:
- Required measures:

### Time logic
- Reporting timestamp:
- Timezone:
- Date range / historical coverage:
- Late-arriving data handling:

### Filters and exclusions
- Included records:
- Excluded records:
- Test/internal data handling:

### Metric definitions
| Metric | Plain-language definition | Formula / logic | Grain | Filters / exclusions | Rounding |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Requirements
### Functional requirements
- 

### Analytics logic requirements
- 

### Output / UX requirements
- Fields, labels, filters, defaults, sort order, drilldowns, exports, subscriptions, and layout requirements.

### Operational requirements
- Refresh cadence:
- Freshness SLA:
- Performance expectations:
- Access / privacy constraints:

## Validation plan
- Row count checks:
- Uniqueness / null checks:
- Metric reconciliation target:
- Known examples to spot-check:
- Historical backfill or parity checks:
- Acceptable tolerance:

## Acceptance criteria
- [ ] Requirement 1 is met and verified by [specific check].
- [ ] Metric(s) reconcile to [source] within [tolerance].
- [ ] Stakeholder/reviewer signs off on [artifact].
- [ ] Tests/docs/owners are updated as needed.

## Implementation notes
Suggested implementation sequence, affected files/assets, dependencies, rollout, and rollback considerations. Keep this practical, not overly prescriptive.

## Risks and assumptions
### Assumptions
- 

### Risks
- 

### Open questions
- 

## Decision log
| Date | Decision | Rationale | Owner |
| --- | --- | --- | --- |
|  |  |  |  |
```

## Improving an existing spec

When the user asks to improve a spec:

1. Read the existing spec and any nearby repo context.
2. Preserve valid decisions, terminology, stakeholder names, file paths, and constraints.
3. Identify gaps using the review rubric below.
4. Produce either a rewritten spec or a patch-style set of edits, depending on the user's request and repo norms.
5. Include a concise change summary and the remaining questions that still need stakeholder input.

### Review rubric

Score or comment on these areas:

| Area | What to check |
| --- | --- |
| Outcome clarity | Does the spec say what decision/action/workflow it supports? |
| Scope | Are in-scope and out-of-scope boundaries explicit? |
| Consumer/output | Is the audience, artifact, and consumption path clear? |
| Source of truth | Are authoritative tables/models/dashboards/files named? |
| Grain and keys | Is the target row/entity grain and unique key clear? |
| Metric logic | Are formulas, filters, exclusions, nulls, duplicates, and rounding defined? |
| Time logic | Is timestamp choice, timezone, windowing, and late data handling clear? |
| Dependencies | Are upstream/downstream assets and owners identified? |
| Validation | Are reconciliation checks, tests, sample cases, and tolerances specified? |
| Acceptance criteria | Can an implementer and reviewer objectively decide done/not done? |
| Operations | Are refresh, SLA, performance, access, privacy, rollout, and rollback addressed? |
| Open questions | Are unresolved issues visible and assigned where possible? |

When gaps exist, do not only say they are missing. Add suggested wording, proposed defaults, or specific questions that would close the gap.

## Analytics-specific requirements to enforce

For analytics work, a spec is incomplete until it addresses the relevant items below or explicitly marks them as not applicable.

### Metrics

Define each metric with:

- plain-language meaning
- formula or pseudo-SQL logic
- numerator and denominator, if applicable
- entity grain and aggregation grain
- timestamp used for reporting
- eligibility rules, filters, and exclusions
- null, duplicate, late-arriving, test/internal, cancellation/refund, and inactive-record handling
- rounding and display format
- source-of-truth comparison and acceptable tolerance

### Data modeling

Specify:

- source tables/models/files and ownership when known
- join keys and expected cardinality
- deduplication rules
- primary key / uniqueness expectation
- materialization or persistence expectations when relevant
- backfill and incremental behavior
- required tests and documentation updates

### BI and reporting

Specify:

- dashboard/report location and consumers
- page/tile/visual affected
- filters, parameters, defaults, and cross-filter behavior
- field labels, sort order, drilldowns, exports, subscriptions, and alerts
- refresh cadence, stale-data messaging, and access restrictions
- QA steps including screenshots or reviewer sign-off if appropriate

### Analysis and experimentation

Specify:

- population, unit of analysis, cohorts, and eligibility
- treatment/exposure assignment and analysis windows
- primary, secondary, and guardrail metrics
- segmentation/cuts
- statistical or descriptive method expected
- caveats, limitations, and decision threshold

### Data quality and reconciliation

Specify:

- rule definition and grain
- pass/warn/fail thresholds
- run cadence and freshness SLA
- owner and escalation path when known
- expected remediation or consumer-facing behavior
- historical comparison, anomaly detection, or source parity checks

## File creation and editing behavior

When asked to create a spec file:

1. Use the repository's existing convention if one exists.
2. If no convention exists, propose `docs/specs/<descriptive-slug>.md` or `.claude/specs/<descriptive-slug>.md` and ask for confirmation if the user has not specified a path.
3. Do not overwrite an existing spec unless the user explicitly requested that path to be updated.
4. Keep the spec task-sized. Split large requests into multiple specs when one file would mix unrelated deliverables.

When asked to improve a spec file:

1. Read the file first.
2. Inspect nearby context if it affects requirements.
3. Make focused edits that improve clarity, implementability, validation, and acceptance criteria.
4. Include a change summary and remaining open questions.

## Output modes

Use the mode that best matches the user's request. For long specs or reviews, include a short summary and a compact TLDR table so the user can quickly see readiness, blockers, and next actions.


### TLDR table for long specs/reviews

```markdown
| Item | Status | Notes |
| --- | --- | --- |
| Objective | Clear / Needs input |  |
| Scope | Clear / Needs input |  |
| Data contract | Clear / Needs input |  |
| Metric logic | Clear / Needs input |  |
| Validation | Clear / Needs input |  |
| Acceptance criteria | Clear / Needs input |  |
| Implementation readiness | Ready / Not ready / Ready with assumptions |  |
```

### Questions needed

Use when essential details are missing.

```markdown
I need a few details before this can be implementation-ready:

1. [Question]? Recommended default: [default]. Why it matters: [reason].
2. ...

Once answered, I will turn this into a spec with scope, data definitions, validation, and acceptance criteria.
```

### Provisional spec

Use when enough information exists to draft, but some details need confirmation.

```markdown
Below is a provisional spec. I marked assumptions and open questions separately so implementation can start only after the risky items are confirmed.
```

### Spec review

Use when improving or auditing an existing spec.

```markdown
## Spec review
| Area | Finding | Severity | Suggested fix |
| --- | --- | --- | --- |
|  |  |  |  |

## Improved spec
[Rewritten or patched spec]

## Remaining questions
1. ...
```

### Implementation-readiness summary

Use at the end of a spec or review.

```markdown
## Implementation readiness
Ready / Not ready / Ready with assumptions

Blocking items:
- 

Non-blocking follow-ups:
- 
```

## Quality gate before finalizing

Before presenting a spec as ready, verify that it answers these questions:

- Who will use the deliverable?
- What decision, action, or workflow will it support?
- What exactly is in scope and out of scope?
- Which data sources and definitions are authoritative?
- What is the grain, time basis, filter logic, and metric logic?
- How will the result be validated?
- What acceptance criteria define done?
- What risks, assumptions, and open questions remain?
- Who needs to review or approve it?

If any answer is missing, either ask the user a targeted question or mark it clearly as an open question with a recommended default.
