---
name: task-intake-contract
description: >-
  Build a compact, explicit intake contract for messy requests before planning
  or delegation. Use inside ultracode-high and other high-rigor workflows to
  identify the goal, artifact, constraints, acceptance criteria, missing
  decisions, risk level, and verification target.
model: claude-opus-4-8
effort: high
---

# Task Intake Contract

Convert the request into a contract another agent could execute without guessing.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when running inside this repo
or the installed `ultracode-high` skill package. Your output becomes the
goal-contract that every downstream agent re-reads to prevent constraint decay.

## Fields

```yaml
goal:                    # objective, quoted verbatim where load-bearing
artifact:
audience:
decision_supported:
constraints:
acceptance_criteria:
scope_in:
non_goals:
known_inputs:
unknowns:                # each: { q, disposition: search | compute | ask | flag }
missing_decisions:
decisions:               # appended as the run proceeds: { decision, rationale }
risk_of_being_wrong: low | moderate | high
verification_target:
permission_boundaries:
```

## Persistence

Write the contract to `.claude/ultracode-high/<run-id>/CONTRACT.md` at intake so it
survives main-context compaction. Re-read it every iteration and inject it into
every subagent's work package; workers should receive the contract plus their one
item, never raw conversation history, so they cannot drift. Append decisions with
rationale as the run proceeds and never silently drop a constraint.

## Rules

- Infer reasonable defaults only when the decision would not materially change.
- Ask or return `needs-input` when a missing decision changes the deliverable.
- Quote user constraints verbatim when they are load-bearing.
- Separate facts, assumptions, and unknowns.
- Give every Unknown a disposition: `search` (find it), `compute` (derive it),
  `ask` (block on the user), or `flag` (surface it as a residual risk). A definite
  claim for an unresolved Unknown must fail verification rather than be invented.
- Include the smallest next artifact that would unlock progress when blocked.
