---
name: selftest-kit
description: >-
  Known-answer self-test harness for ultracode-high. Use to verify that the
  orchestration mechanism fires: plan critique blocks bad manifests, verification
  catches planted failures, constraints survive long runs, unknowns are flagged,
  and enumerable tasks close completely.
model: claude-opus-4-8
effort: high
---

# Selftest Kit

Run known-answer tests before treating the orchestration scaffold as releaseable.
These tests prove that the procedure fires; they do not replace qualitative
fixture review.

## Status

KA-1 through KA-5 are defined in `references/known-answer-tests.md`; the seeded
fixture files and CI wiring that would let `gate_check.py` grade them
automatically are deferred (PRD §13). Until then, `gate-kit`'s
`references/example-gates.json` is the runnable smoke test that the gate runner
itself works, and KA grading is performed by hand against the criteria below.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your tests
prove that the system catches the five procedural failure modes it claims to
address.

## Required KA tests

See `references/known-answer-tests.md` for the current KA-1 through KA-5 suite.

Each test must state:

- seeded input;
- expected failure mode;
- gate used to grade it;
- pass/fail criterion;
- result and evidence.

Release only when all required known-answer tests pass.
