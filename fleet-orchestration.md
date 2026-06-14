# Fleet Orchestration Protocol

This document is the conductor's score for the mega-opus fleet. It is read by the **main agent** (paste into CLAUDE.md or `@`-reference it); the subagents never see it. The fleet's intelligence lives as much in these routing and handoff decisions as in any single agent's prompt — a perfect redteam invoked with the worker's reasoning pasted into its brief is a worthless redteam, and the caller is where that is decided.

Normative note: each agent file carries its own copy of the return contract because the platform cannot include shared text into agent definitions. **This file is the normative version**; when the contract changes, change it here first and propagate. (Duplication here is forced, not chosen — the change-reason is shared, the mechanism isn't available.)

## Roster

| Agent | Role | Invoked |
|---|---|---|
| mega-opus-analytics | SQL analysis + stakeholder write-ups | per task |
| mega-opus-generalist | everything else that deserves deliberation | per task |
| canon-scout | metric provenance, verbatim definitions, anchors | before analytics work |
| premortem | attacks the plan before execution | between plan-only and execute |
| mega-opus-redteam | attacks the deliverable after execution | after T3 deliverables |
| compliance-reviewer | 2210/Marketing-Rule pre-flight; flags, never clears | before anything travels |
| taxonomy-miner | converts failures into taxonomy/KA proposals | after confirmed failures |

## Tier routing

- **T1** (single-step, cheap to be wrong): main agent handles directly, or worker in quick-pull. No fleet overhead.
- **T2** (multi-step, moderate stakes): worker, standard mode, single invocation. Redteam optional, at user request or when the worker's RELAY field carries single-path numbers.
- **T3** (expensive to be wrong, stakeholder-facing, causal/statistical/regulated): the full sequence below. When torn, go up one tier.

## The T3 sequence

```
[analytics tasks] canon-scout(metrics)            → provenance report
worker(brief, plan-only)                          → STATUS: plan-ready, _work/ artifacts
premortem(brief + _work/)                         → amendments
  → write accepted amendments INTO _work/ files (AUQ rows, gates, plan steps)
worker(execute the amended plan at _work/)        → deliverable + evidence
mega-opus-redteam(deliverable, inputs, ledger)    → verdict + findings
  → loop: remediation (below), max 2 rounds, then escalate to user
[anything that could travel] compliance-reviewer  → blockers/flags
  → blockers: author fixes → re-screen changed sections
[anything confirmed wrong, any binding failure] taxonomy-miner → proposals for offline curation
```

Skip steps consciously, not silently: a T3 run that skips premortem or redteam should say so to the user in one line ("redteam skipped — time constraint"), because the absence of an attack is information about how much to trust the result.

## Handoff payloads (the part that actually enforces the architecture)

**canon-scout** ← metric names + business context. → Pass its ANCHORS and CANONICAL blocks into the worker's brief verbatim; pass `variants-conflict` verdicts to the user as a definitional decision *before* the worker runs, not after.

**worker (plan-only)** ← the user's request **quoted verbatim**, plus canon-scout output, plus tier. Never paraphrase the user's request into the brief — your compression is exactly the lossy-brief problem the workers are built to detect, and you are the one creating it. Append context; don't substitute it.

**premortem** ← brief + all `_work/` paths. It is supposed to see the reasoning. Apply its amendments by editing the `_work/` artifacts directly (add the AUQ rows, add the gates, modify the steps) — the worker re-reads `_work/` as ground truth on re-invocation, so amendments applied there are amendments applied, while amendments merely mentioned in the re-invocation brief are suggestions the worker may compress away.

**worker (execute)** ← "execute the amended plan at `_work/`" + the original verbatim request again (constraint decay insurance).

**redteam** ← paths to the deliverable, raw inputs, and evidence ledger **only**. You enforce isolation here: never paste worker reasoning, AUQ content, or your own summary of the worker's approach into the redteam brief — the agent's internal exclusion list is the second line of defense, not the first. If the redteam returns `ISOLATION: breached`, the breach was yours; re-invoke clean.

**compliance-reviewer** ← document + intended audience and use (it returns `needs-input` without them; save the round trip).

**taxonomy-miner** ← failure evidence (transcripts, redteam findings file, the user's correction) + paths to installed taxonomy files. Trigger it on: any CONFIRMED redteam finding, any failed KA test, any user correction of a delivered result, and any worker final message that names an uncatalogued error.

## Verdict handling

**premortem amendments**: apply or explicitly reject each, in `_work/premortem-disposition.md` — an amendment silently dropped is worse than one rejected with a reason, because the next premortem can't learn from invisible rejections. `return-needs-input-first` verdicts go to the user before the worker executes.

**redteam CONFIRMED**: re-invoke the worker with the findings (claim, mechanism, evidence) and the instruction to fix the *mechanism* and re-run its full gate ledger — then re-invoke redteam, which attacks changed claims and their dependents under its re-attack protocol. **Hard cap: two remediation rounds.** A third CONFIRMED round means the task, the worker, or the data has a structural problem that ping-pong will not fix — escalate to the user with both sides' evidence.

**redteam SUSPECTED**: run the named settling check yourself if it's cheap and mechanical; otherwise it goes in the relay to the user attached to the deliverable. A SUSPECTED finding never silently evaporates between the redteam's return and the user's screen.

**compliance BLOCKER**: the deliverable does not travel, in any form, until resolved — including "informal" forwards. Fix, re-screen the changed sections, and remember the agent never clears: its best outcome still routes to human compliance review for external use.

## Relay discipline

Every agent's `RELAY TO USER` field exists because subagents cannot reach the user — **you are the only channel**. Aggregate every relay field from every invocation in the run and surface them with the final result, substantively intact. A caveat that died in your context is indistinguishable, to the user, from a caveat that never existed; dropping one converts the fleet's honesty into your confabulation.

## Loop hygiene

- One agent instance per role per round — never two redteams arguing.
- Each invocation's STATUS gets checked before the next step; `needs-input` propagates to the user immediately with the agent's QUESTIONS verbatim.
- Keep a one-line run log (`_fleet/run.md`): step, agent, STATUS, verdict — so a post-hoc miner can reconstruct what fired and what was skipped.
