# SUPERSEDED — V1 historical record only

Status: **SUPERSEDED BY `SIX_TASK_REDESIGN_V2.md` on 2026-11-11. DO NOT USE AS AN ACTIVE TASK LIST.**

This file is retained only for provenance and historical comparison. Its N01–N06 topics (payment ledger recovery, tenant region routing, ML feature drift, AI-agent destructive action, Atlassian mass deletion recovery, SaaS metering drift) are not active tasks in the V2 batch. In particular, its N04 and N05 are not to be reused, renumbered, merged, or treated as V2 tasks.

The sole active six-task list is [SIX_TASK_REDESIGN_V2.md](SIX_TASK_REDESIGN_V2.md).

---


## User exclusions

Do not produce tasks equivalent to:
- SBOM/CVE dependency-upgrade admission;
- Debian base-image CVE rebuild review;
- pre-holiday change-window approvals;
- public postmortem remediation closure audits;
- SWE-bench contamination checks;
- Prometheus/Kubernetes alert-rule routing reviews.

Also avoid simply relabeling the earlier AI Infra / Data / IAM / Release / Database / SRE topics. Each new task needs a distinct business decision and deliverable.

## Design thesis: exploit observed failure modes, not prompt tricks

Every case is based on a documented production failure pattern. The task packet should include heterogeneous, mutually inconsistent evidence: event logs, request/response traces, state snapshots, financial ledgers, configuration versions, runbooks, customer-impact extracts, and partial exports. The solver must distinguish:
- an action requested from an action actually executed;
- an external side effect from a locally recorded result;
- event time from ingestion/observation time;
- unknown from failed, zero, or complete;
- a technically healthy dependency from an available end-to-end service;
- a valid backup/retention state from proof of recoverability or deletion.

Do not manufacture contradictions by making the task rules ambiguous. Publish all governing semantics and freeze the evidence set before testing.

## Six new directions

### N01 — Payment ledger recovery after a partial Redis failover
**Incident basis:** Twilio's July 2013 billing incident. A Redis master recovery left account balances unavailable/read-only while auto-recharge continued charging cards; the company used independent double-bookkeeping records to restore balances and refund affected accounts.  
**Primary source:** https://www.twilio.com/en-us/blog/company/communications/billing-incident-post-mortem-breakdown-analysis-and-root-cause-html

**Decision:** determine which card charges actually occurred, which balance mutations committed, which recharge attempts are duplicates, which accounts were suspended incorrectly, and the safe sequence for containment, ledger reconstruction, refunds and account reinstatement.

**Hard materials:** provider authorization/capture/refund exports; Redis replication/AOF/recovery logs; application retries; idempotency records; independent ledger; account status history; delayed usage reports; refund settlement records; support contacts. Include timeouts where provider succeeded but local write failed, and the reverse.

**Key Doubao weaknesses:** treating timeout as failure; conflating card charge with balance credit; counting retries as new business operations; trusting a dashboard total; losing event ordering; assuming eventual refund means customer harm is fully resolved.

**Deliverables:** transaction-level adjudication ledger, account-level balance reconstruction, duplicate-charge/refund register, suspension correction list, cash exposure bridge, containment/recovery runbook and evidence-linked executive decision.

### N02 — Tenant region-routing outage caused by a failed edge cache dependency
**Incident basis:** Logto's 12 June 2025 auth-service outage. Cloudflare Workers KV failure broke region mapping lookups; the Worker failed instead of falling back to direct routing. The incident affected requests through logto.app while other services using direct DNS were unaffected.  
**Primary source:** https://blog.logto.io/postmortem-june-12-2025

**Decision:** reconstruct the affected tenant/domain population and request impact; decide safe degraded routing while preserving data-residency constraints; establish which traffic may use fallback, which must remain blocked, and when cache reintroduction is safe.

**Hard materials:** tenant-to-region registry versions; DNS and edge request logs; KV read/write errors; cache age/TTL; region health; tenant residency clauses; custom-domain mapping; deploy history; fallback test outputs; request retries and customer impact. Include stale-but-valid cache entries, missing mappings, conflicting tenant aliases and region-health gaps.

**Key Doubao weaknesses:** equating upstream health with service health; treating cache miss and stale cache as identical; assuming all tenants can fail over to any healthy region; ignoring custom domains; confusing attempted requests with successful authentication.

**Deliverables:** per-tenant impact ledger, request-path reconstruction, residency-safe fallback matrix, region-routing decision, rollback/re-entry criteria and evidence-backed customer impact statement.

### N03 — Silent ML decision degradation from a feature semantic/unit change
**Incident basis:** Google Cloud's account of training-serving skew, including a production feature pinned to -1 after serving-stack refactoring and Google Play finding serving features missing compared with training data; removing skew improved app install rate by 2%.  
**Primary sources:** https://cloud.google.com/blog/topics/developers-practitioners/monitor-models-training-serving-skew-vertex-ai and https://cloud.google.com/blog/topics/developers-practitioners/monitoring-feature-attributions-how-google-saved-one-largest-ml-services-trouble

**Decision:** decide whether model decisions during the affected interval are trustworthy; isolate feature pipeline/version/unit changes from population drift, label delay and feedback loops; define the exact affected decision cohort and safe rollback/replay/retraining boundary.

**Hard materials:** feature registry versions; offline training snapshots; online serving payloads; transformation code/config diffs; model versions; prediction logs; delayed labels; experiment assignment; feature attribution samples; downstream action outcomes. Include unit conversion changes, missingness represented as a valid sentinel, delayed labels and feedback contamination.

**Key Doubao weaknesses:** relying on aggregate distribution drift; confusing concept drift with feature skew; using post-outcome labels in point-in-time replay; treating HTTP 200 as model quality; claiming causality from temporal proximity; failing to quantify affected decisions.

**Deliverables:** point-in-time feature parity audit, affected prediction ledger, causal hypothesis matrix with confidence/alternatives, decision-impact estimate, rollback/replay recommendation and monitoring/guardrail specification.

### N04 — AI agent destructive-action incident: prove what the agent actually changed
**Incident basis:** the April 2026 PocketOS/Railway production-data deletion incident. A coding agent working on a staging task used an account-scoped credential and a legacy volume-delete API; production data and volume-level backups became unavailable. Public reporting describes recovery from an older offsite backup and reconstruction from payment, calendar and email records. Treat founder and vendor statements as separately attributed evidence; freeze the original statements before finalizing.  
**Research starting points:** https://www.abc.net.au/news/ and https://techcrunch.com/ (locate and freeze first-party founder/vendor statements; secondary chronology must be labelled secondary).

**Decision:** reconstruct the exact action chain and authorization boundary; determine actual data loss and recoverable state; establish whether claimed backups/restores are real; decide containment and safe restoration without overwriting newer valid writes.

**Hard materials:** agent conversation/tool trace; approval and freeze instructions; API audit logs; SQL statement logs; database snapshots; backup catalog; restore test outputs; object-store access logs; post-incident writes; user-visible status claims. Include agent self-report contradictions and a backup that exists but has not been restore-verified.

**Key Doubao weaknesses:** trusting the agent's own summary; treating a successful tool response as proof of intended state; confusing backup existence with point-in-time recoverability; overlooking explicit approval boundaries; claiming a restore without data-level validation.

**Deliverables:** immutable action timeline, command-to-effect ledger, authorization deviation matrix, data-loss/recoverability boundary, verified restore plan, customer communication facts and prevention controls.

**Source gate:** do not finalize this case until the original Replit primary statement and any public evidence are located and version-frozen. Do not present secondary commentary as first-party fact.

### N05 — Mass tenant deletion and multi-product disaster recovery at scale
**Incident basis:** Atlassian's official post-incident review of the April 2022 outage. A cleanup operation intended to remove an app from customer sites deleted 883 sites affecting 775 customers. Recovery required per-site extraction and restoration; the restore process was not designed for hundreds of sites in parallel. Atlassian reported a 14-day recovery period and differing data-loss windows for 57 customers due to misaligned product restore points.  
**Primary source:** https://www.atlassian.com/engineering/post-incident-review-april-2022-outage

**Decision:** determine the exact affected tenant/site/product population, prioritize recovery under constrained restore capacity, reconcile per-product restore points, establish customer-specific data-loss windows, and decide when each site is genuinely restored and safe to reopen.

**Hard materials:** bulk cleanup request; site/app identifier exports; script arguments and API logs; tenant/product inventory; per-product backup catalog; restore-point timestamps; cross-product dependency graph; restore job logs; validation checks; customer verification records; support queue; recovery staffing/capacity; status communications. Include ambiguous identifier types, partial restore success, inconsistent product RPOs, shared data stores, repeated restore attempts and customer acceptance that lags technical recovery.

**Key Doubao weaknesses:** assuming the target identifier scope; counting a site as restored when only one product is back; treating backup existence as restoration proof; applying a single RPO to all products; ignoring restore throughput and queue interactions; confusing technical readiness with customer verification.

**Deliverables:** affected-site adjudication ledger, product-by-product restore matrix, capacity-constrained recovery schedule, per-customer RPO/data-loss statement, restore validation register, reopening decision and customer communication ledger.

### N06 — SaaS usage metering and entitlement drift after a billing-cycle boundary
**Incident basis:** Twilio's documented billing incident illustrates how balance-store recovery and charging workflows can diverge. This new case is deliberately different from N01: it audits contractual entitlement, usage measurement, proration and invoice correctness—not duplicate payment recovery.  
**Primary source for incident pattern:** https://www.twilio.com/en-us/blog/company/communications/billing-incident-post-mortem-breakdown-analysis-and-root-cause-html

**Decision:** reconstruct each tenant's contractual entitlement and billable usage across plan changes, grace periods, credits, regional meters and invoice cutoffs; decide which invoices can be issued, must be held, or require credit/debit adjustment.

**Hard materials:** signed order forms and amendments; plan/price version history; usage meter events; aggregation snapshots; timezone and cutoff definitions; entitlement cache; invoice drafts; credit notes; tax treatment; customer dispute records; revenue-recognition close calendar. Include late-arriving usage, duplicated meter events, mid-cycle plan amendments, proration rounding and a stale entitlement cache.

**Key Doubao weaknesses:** applying the current contract retroactively; confusing observed time with service time; rounding each event instead of invoice line; assuming usage ingestion equals billable usage; ignoring grace/credit exceptions; trusting invoice preview totals without reconstructing line items.

**Deliverables:** tenant-level entitlement timeline, event-to-invoice reconciliation, invoice disposition register, adjustment journal, revenue/usage bridge, exception queue and finance sign-off memo.

## Cross-task difficulty architecture

Each task will use a distinct evidence topology and output contract. Avoid repeating the same 7-zip/CSV template with changed labels.

1. **Evidence topology:** 12–25 interdependent artifacts, multiple source systems, versioned records and partial evidence. File count alone is not difficulty.
2. **Decision density:** 8–15 material traps on the required path; each changes a business decision or a numeric result.
3. **Record-level completeness:** require exhaustive row/entity/tenant/transaction-level outputs, not only executive summaries.
4. **Temporal correctness:** preserve event time, processing time, observed time, effective time and cutoff semantics separately.
5. **Contradiction resolution:** conflicting records must be resolved by published source authority, version and temporal rules; unresolved cases remain UNKNOWN.
6. **Counterfactuals:** include at least one viable alternative and explicit boundary where no safe action is justified.
7. **Adversarial evidence:** include malformed exports, duplicate IDs, missing pages/rows, stale snapshots, misleading dashboards and self-reported PASS claims—but ensure the task remains solvable from provided materials.
8. **Operational consequence:** decisions must drive refunds, routing, deletion, rollback, restore, invoice hold or customer impact actions.
9. **Reproducibility:** exact calculations, formulas, scripts, provenance, row-level references and hash-locked inputs.
10. **No fake difficulty:** no arbitrary waiting, irrelevant attachments, intentionally undocumented rules, or fabricated runtime/step counts.

## Stricter rubric policy

Use 20 criteria × 5 = 100 with 4 evidence-backed binary subchecks per criterion. Internal grading levels:
- **5:** all four subchecks pass; conclusion, evidence, calculation and action are correct.
- **2:** only a limited subset passes; direction may be plausible but material evidence, scope or calculation is missing.
- **0:** criterion fails, contradicts evidence, omits required records, or proposes an unsafe/unauthorized action.

Critical errors (e.g. duplicate charge left unreconciled, cross-region routing that violates residency, false deletion certification, unauthorized destructive action, post-outcome leakage, incorrect invoice amount beyond tolerance) trigger 0 for the directly affected criterion and all explicitly dependent criteria. A critical safety gate may cap the relevant decision section at 0. Do not apply a blanket score cap for cosmetic errors.

The grader must inspect actual output files and row-level evidence, never trust the model's self-assessment. A correct executive summary with wrong underlying rows must score low. A single detected material error is not automatically a global zero; impact must follow the frozen dependency map.

## Required calibration before any Doubao run

- Reference: independently constructed from frozen inputs.
- Alternative: substantively different but valid, must score at least 95 machine points.
- Negatives: at least 8 targeted mutations per task, each failing the intended criteria only.
- Mutation suite: wrong timestamps, dropped entities, duplicated events, incorrect joins, wrong unit, stale version, unsupported PASS, self-report-only output, unauthorized action, rounding drift, and missing evidence.
- Empty/incomplete submission: INVALID_SCHEMA, not a numeric score.
- Grader must pass reference, alternative, negative, row/column permutation and property tests.
- No scoring until schema preflight passes.
- Official difficulty target: valid score <=50 AND (actual task time >2400 seconds OR platform-verified steps >=50). Never optimize for low score by adding arbitrary traps; create material errors the task genuinely requires the model to detect and avoid.

## Packaging rule

User requests **one downloadable author master ZIP only**. Inside it, preserve strict compartments:
- `01_PUBLIC_MODEL_INPUT/` — prompt + public inputs only.
- `02_PRIVATE_REFERENCE_RUBRIC_GRADER/` — reference, hidden rubric, grader and mutations.
- `03_SOURCE_AND_LICENSE/` — source register, source captures, license notices.
- `04_OPERATIONS/` — build/validate scripts and exact commands.
- `05_MODEL_RUN_EVIDENCE/` — all runs, including failures; NOT_RUN where no run exists.
- `06_PLATFORM_FIELDS/` — seven platform fields and classification.
- `07_READINESS_AND_BLOCKERS/` — 12-point checklist, C20 and authorization state.
- `MANIFEST.sha256`, `ZIP_CRC_REPORT.txt`, `README_STATUS.md`.

The master ZIP is for the author. Never upload the master ZIP to Doubao because it contains private answers and rubric. Extract only `01_PUBLIC_MODEL_INPUT/` for blind tests.

## Current execution order

N01 → N02 → N03 → N04 → N05 → N06. Complete author QA and package each case before beginning the next. Preserve source/authorization blockers and never claim model/platform pass without evidence.

