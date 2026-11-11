# Six-task production batch

Batch: SIX-TASK-2026-11-11  
Base pipeline commit: 452db4a29bb8f738a6547ebc1339fc88bbd1b035  
Working branch: six-task-run-2026-11-11

**Direction update (2026-11-11):** the initial AI Infra / Data / IAM / Release / Database / SRE list is superseded. The active six-task design is in [SIX_TASK_REDESIGN.md](SIX_TASK_REDESIGN.md). Do not continue the superseded topics unless a later explicit decision restores them.

| ID | New direction | Core decision |
|---|---|---|
| N01 | Payment ledger recovery after partial Redis failover | actual charges, balance state, refunds, suspensions and safe recovery |
| N02 | Tenant region-routing outage caused by failed edge-cache dependency | affected tenants, residency-safe fallback and re-entry |
| N03 | Silent ML decision degradation from feature semantic/unit change | affected predictions, point-in-time replay and rollback boundary |
| N04 | AI agent destructive-action incident | reconstruct actual tool/API/database effects and prove recoverability |
| N05 | Mass tenant deletion and multi-product disaster recovery at scale | affected-site scope, restore capacity, product-specific RPO and reopening decisions |
| N06 | SaaS usage metering and entitlement drift across billing-cycle boundary | contract entitlement, billable usage and invoice disposition |

## Global constraints

- Avoid the six explicitly excluded directions in the redesign document.
- Do not disguise a synthetic scenario as the author's real employer work.
- Each task must have a unique evidence topology, business decision and output contract.
- Each task requires 8–15 evidence-grounded hidden difficulties, 20×5 rubric, independent reference, valid alternative, targeted negatives, fail-closed schema preflight and content-level grader.
- Critical errors must incur severe, dependency-mapped penalties; no arbitrary blanket zero for cosmetic errors.
- Official gate: valid score <=50 and (actual task time >2400 seconds OR platform-verified steps >=50).
- Keep all model runs, including invalid and failed runs. No fabricated times or steps.
- C20 requires real qualified reviewers. AI cannot impersonate them.
- One author master ZIP is delivered, with PUBLIC and PRIVATE compartments separated. Only PUBLIC is used for Doubao blind runs.
- No PLATFORM_ACCEPTED status without an actual platform receipt.

See [SIX_TASK_REDESIGN.md](SIX_TASK_REDESIGN.md) for detailed incident bases, evidence requirements, difficulty design, rubric calibration and packaging contract.
