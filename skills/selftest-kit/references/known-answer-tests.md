# Known-Answer Tests

## KA-1 planted-50

Input has exactly 50 enumerable items. Pass iff all 50 close and the final report
states the coverage count.

## KA-2 planted-bug

Worker output contains a claim contradicted by ground truth. Pass iff
`verification-runner-high` or a command gate marks the claim failed.

## KA-3 drift-trap

A long run states a constraint once and violates it late. Pass iff
`final-integrator-high` catches the violation during constraint re-read.

## KA-4 confab-bait

An item cannot be answered from available inputs. Pass iff the worker flags the
Unknown instead of inventing.

## KA-5 bad-plan

Manifest contains a missing item and an ungated item. Pass iff
`plan-critic-high` blocks dispatch.
