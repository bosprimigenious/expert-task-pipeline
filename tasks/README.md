# Six-task production batch

Batch: SIX-TASK-2026-11-11  
Working branch: six-task-run-2026-11-11

<aside>
**Single source of truth:** V2 is the only active task list. V1 and all earlier lists are historical/superseded and must not be used to create, number, claim, or submit tasks.
</aside>

Active design: [SIX_TASK_REDESIGN_V2.md](SIX_TASK_REDESIGN_V2.md).

| ID | Active V2 direction | Decision unit | Primary decision |
|---|---|---|---|
| V2-01 | Convenience-store replenishment outage | Store × SKU × delivery slot | Emergency replenishment quantities and dispatch plan |
| V2-02 | Cold-chain cyber disruption | Lot × order | Food-safety disposition, release and claims |
| V2-03 | Airline network disruption | Flight × passenger | Flight/crew legality and passenger recovery |
| V2-04 | Flash-sale inventory reservation failure | Order line | Fulfil, split, substitute, cancel or refund |
| V2-05 | SaaS mass tenant deletion | Tenant site × product | Recovery schedule, product RPO and reopening |
| V2-06 | AI agent unauthorized activity | Agent action × asset/data item | Confirmed impact, containment, notification and safe resumption |

## Non-overlap and delivery contracts

See the mandatory `Non-overlap contract` section in V2. No task may absorb another task's excluded workflow merely to increase complexity. Each task has a distinct primary deliverable and distinct business owner.

## Global production gates

- Each task needs 8–15 evidence-grounded hidden difficulties, 20×5 rubric, independent reference, valid alternative, at least 10 targeted negatives, fail-closed schema preflight and content-level grader.
- Critical errors receive dependency-mapped penalties only; no arbitrary global zero.
- Difficulty gate: valid score <=50 AND (actual task time >2400 seconds OR platform-verified steps >=50).
- Keep all model runs, including invalid and failed runs. Never invent elapsed time or steps.
- C20 requires qualified human reviewers. AI cannot impersonate them.
- One author master ZIP is delivered with PUBLIC and PRIVATE compartments separated. Only PUBLIC goes to Doubao.
- No PLATFORM_ACCEPTED status without an actual platform receipt.
- Public incident evidence does not authorize redistribution of private operational records. Synthetic records must be labelled synthetic and platform permission must be confirmed.

## Historical documents

- [SIX_TASK_REDESIGN.md](SIX_TASK_REDESIGN.md): V1, **SUPERSEDED — HISTORY ONLY**.
- Initial engineering-only task directions: superseded; see Git history and archive.

Do not open a second task list or mix V1 identifiers into V2.
