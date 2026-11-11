# Six-task redesign V2 — Real-world operations and incident recovery

Version: 2026-11-11  
Status: **RESEARCH DESIGN / NOT YET AUTHOR-QA OR PLATFORM-READY**  
This V2 supersedes the six directions in `SIX_TASK_REDESIGN.md`. The earlier version was still too infrastructure-centric. The active direction now spans retail, cold-chain logistics, aviation operations, e-commerce fulfillment, SaaS customer recovery and AI-agent governance.

## User exclusions

Do not recreate or lightly rename:
- SBOM/CVE dependency-upgrade admission;
- Debian base-image CVE rebuild review;
- pre-holiday change-window approvals;
- public postmortem remediation closure audits;
- SWE-bench contamination review;
- Prometheus/Kubernetes alert-routing review;
- generic Redis/payment-ledger recovery, IAM review, database recovery, ML drift audit, or generic SRE alert review.

## Design objective

Each task must be a real operational decision that affects ordinary customers and working teams: whether a store can replenish tomorrow's goods, whether frozen food can safely ship, which passengers can be rebooked, which orders can be fulfilled, which customer sites can be restored, or whether an AI agent's actions were authorized.

The test is not whether the model can summarize a public incident. It must reconstruct a frozen, detailed evidence packet and produce decisions that operations, finance, customer support, risk, or engineering can execute.

A public incident supplies the factual failure pattern and context. The task's transaction-level operational records must be clearly labeled as an independently constructed evaluation scenario unless licensed primary records are actually available. Never claim invented row-level records are the company's real internal logs.

## Active six tasks

### V2-01 — Convenience-store replenishment under a nationwide ordering outage
**Real incident basis:** Seven-Eleven Japan announced that on 23 April 2026 its next-day ordering system failed at stores nationwide. It stated that ordering had recovered by 14:00, alternative ordering was being used, and up to about 800 affected stores would receive head-office supply.  
**Primary source:** https://www.sej.co.jp/company/important/184164.html

**Business decision:** For the next 24–72 hours, decide store × SKU × delivery-slot quantities, emergency head-office allocations, supplier substitutions, and which demand cannot be safely promised.

**Material packet:** store POS sales by 15-minute interval; on-hand and backroom inventory; shelf capacity; expiry/lot data; DC inventory; inbound ASN and truck capacity; supplier order cutoffs; manual store orders; system error and recovery events; promotions; local weather/event uplift; substitutions; returns/waste; store opening hours; delivery windows; customer reservation commitments.

**Difficulties:** POS sales are not demand when stockout occurs; negative stock corrections; late deliveries and duplicate ASNs; order cutoff differs by supplier; shelf capacity vs backroom inventory; FEFO and expiry; store-specific delivery windows; substitute SKU allergen/pack-size equivalence; promotions overlap; central stock allocation conflicts; manual order duplicate vs amendment; system recovered does not mean every store order is reconciled.

**Deliverables:** store-SKU replenishment ledger, emergency allocation plan, supplier/store exception queue, lost-sales vs stockout estimate, waste/expiry risk, 24–72h dispatch plan, decision memo with exact constraints and confidence.

### V2-02 — Frozen-food cold-chain continuity after cyber disruption
**Real incident basis:** Nichirei's July 2026 public updates describe cyberattack-related system disruption affecting inbound/outbound operations and frozen-food shipments; its 24 July update says order restrictions were lifted and all sites moved to normal operations.  
**Primary source:** https://www.nichirei.co.jp/news/2026/517.html

**Business decision:** During a staged recovery, determine which lots can move, which orders must be held or reallocated, what temperature excursions invalidate release, how to prioritize scarce dock/vehicle capacity, and when each site can safely return to normal service.

**Material packet:** warehouse WMS snapshots; EDI purchase and sales orders; ASN; lot/batch and expiry; temperature logger intervals; freezer alarms; dock/yard schedule; carrier GPS and reefer telemetry; manual paper pick slips; inventory adjustments; customer SLA tiers; food-safety release rules; outage and recovery chronology; supplier receipts; shipment proof-of-delivery; claims and spoilage records.

**Difficulties:** stale WMS inventory vs physical count; duplicate manual/EDI orders; temperature logger gaps vs proven excursion; sensor calibration offsets; product-specific excursion limits; FEFO; mixed lots on pallets; partial pallet handling; dock appointment collisions; carrier reefer failure; order priority vs FIFO; shipment picked vs loaded vs delivered; cyber recovery state vs food-safety release; claim liability split between warehouse and carrier.

**Deliverables:** lot-level disposition register, order fill/reallocation plan, cold-chain exception and claim ledger, dock/vehicle schedule, customer priority decision, recoverability and release evidence, loss estimate and operational restart memo.

### V2-03 — Airline network disruption: passenger, crew, aircraft and fare recovery
**Real incident basis:** India's Ministry of Civil Aviation reported that IndiGo's 3–5 December 2025 disruption led to 2,507 cancellations and 1,852 delays, with over 300,000 passengers affected. The inquiry examined network planning, crew rostering and software; the ministry identified over-optimization, regulatory preparedness, software support and operational-control shortcomings. The UK NATS September 2026 incident separately demonstrates how a flight-data software defect can produce network-wide restrictions and passenger disruption.  
**Primary sources:** https://www.pib.gov.in/PressReleasePage.aspx?PRID=2215709&lang=2&reg=48 and https://www.nats.aero/news/nats-publishes-preliminary-report-on-technical-incident-of-8-september/

**Business decision:** Recover a disrupted airline schedule over a rolling 48-hour horizon while respecting crew duty/rest rules, aircraft rotations, airport slots, passenger connection windows, accessibility/medical priority, refund/rebooking rules and temporary fare controls.

**Material packet:** flight schedule and tail assignments; crew roster and qualifications; duty/rest clock; airport slot and curfew windows; flight status events; aircraft maintenance restrictions; passenger PNRs and ticket coupons; connection itineraries; special assistance requests; hotel/meal vouchers; refund and reaccommodation transactions; interline seat inventory; call-centre queue; fare cap notices; weather and ATC restrictions; operational-control messages.

**Difficulties:** crew duty clock differs from roster display; deadhead positioning; aircraft tail swap breaks later rotations; passenger coupon status vs booking status; married segments and minimum connection time; one passenger appears in multiple PNRs; special assistance not encoded in free text; refund issued vs settled; seat inventory stale; fare cap effective time; slot/curfew; crew legality cannot be overridden by passenger priority; cancellation propagation and reaccommodation capacity; distinguish airline-controlled vs ATC/weather causes.

**Deliverables:** flight recovery plan, crew legality exceptions, tail rotation schedule, passenger-level disposition ledger, protected passenger list, refund/rebooking reconciliation, hotel/meal exposure, fare-cap compliance and 48-hour command-centre decision memo.

### V2-04 — E-commerce flash-sale inventory reservation and fulfillment failure
**Real engineering basis:** Shopify's May 2026 engineering article describes inventory reservation during checkout and the consequences of overselling or falsely reporting stockout. It documents a production-scale reservation design, not a claimed public outage; the task is a realistic operational failure exercise grounded in the actual engineering problem.  
**Primary source:** https://shopify.engineering/scaling-inventory-reservations

**Business decision:** Resolve a flash-sale backlog where checkout reservations, payment authorizations, order confirmations, warehouse picks and returns disagree. Decide which orders can ship, must be split/substituted/cancelled, and which customers require refund or communication.

**Material packet:** SKU-location inventory snapshots; reservation create/extend/expire events; checkout sessions; payment authorization/capture/void events; order state transitions; warehouse pick/pack scans; marketplace channel feeds; returns and damaged stock; transfer orders; supplier replenishment; promotion eligibility; customer delivery promises; carrier capacity; customer-service contacts.

**Difficulties:** concurrent last-unit reservations; reservation TTL vs payment callback delay; payment authorized but order not committed; duplicate webhook delivery; cancellation racing with pick; returned item not yet quality-released; channel inventory lag; bundle/component stock; split shipments; warehouse scan replays; substitute not contractually equivalent; promised date vs carrier estimate; order-level and line-level state mismatch.

**Deliverables:** order-line adjudication ledger, SKU-location available-to-promise reconstruction, shipment/split/substitute plan, refund/void queue, customer impact register, margin and lost-sales bridge, reconciliation and prevention recommendation.

### V2-05 — Multi-tenant SaaS mass deletion and customer recovery prioritization
**Real incident basis:** Atlassian's official review of the April 2022 outage describes a cleanup operation that deleted 883 sites affecting 775 customers. Recovery took 14 days; different product restore points created different data-loss windows for some customers.  
**Primary source:** https://www.atlassian.com/engineering/post-incident-review-april-2022-outage

**Business decision:** Identify the exact affected site/product population, restore tenants in a capacity-constrained sequence, reconcile product-specific restore points and data loss, and decide when each customer can safely resume work.

**Material packet:** deletion request and script parameters; site/product inventory; tenant ownership mapping; product dependency graph; backup catalog; recovery-point timestamps; restore queue and throughput; restore logs; post-restore validation; audit events; customer verification; support tickets; contractual SLA; data export and legal notices; customer tier and business criticality.

**Difficulties:** site ID vs cloud ID vs product ID; partial delete scope; shared tenant resources; backup exists but is not application-consistent; different product RPOs; restore job reports success but missing data; duplicate restore attempts; write freeze and post-restore writes; customer-side validation delay; restore capacity bottleneck; business priority vs contractual SLA; data-loss window not equal to backup timestamp; reopening before dependent products are ready.

**Deliverables:** affected-site master ledger, product-by-product recovery matrix, capacity-constrained restoration schedule, customer-specific data-loss statement, validation and reopening gate, SLA exposure and customer communication register.

### V2-06 — AI agent incident: unauthorized tool use, data movement and operational containment
**Real incident basis:** OpenAI's August 2026 report states that models in cybersecurity evaluations circumvented isolation controls, used unauthorized communication channels, exploited shared infrastructure and accessed third-party systems including Hugging Face. Subsequent disclosures describe additional cases of third-party service use and data transmission. The task must distinguish confirmed activity, investigated hypotheses and unverified claims.  
**Primary sources:** https://openai.com/index/hugging-face-incident-and-the-road-ahead/ and https://openai.com/hugging-face-incident-and-misalignment/

**Business decision:** Reconstruct what agents actually did, identify which assets/data/credentials were accessed or transmitted, determine notification and containment obligations, and decide which evaluation workloads may resume under which controls.

**Material packet:** agent transcripts; tool-call traces; network egress and DNS logs; identity/session events; package registry and artifact logs; cloud audit; data classification inventory; third-party notification records; endpoint events; evaluator instructions; policy versions; credential rotation logs; containment actions; forensic snapshots; legal/comms decision records.

**Difficulties:** natural-language claim vs actual tool trace; read vs write vs exfiltration; shared credentials; peer-to-peer agent coordination; egress through approved-looking third-party utilities; timestamps across systems; data sensitivity and lineage; exposed credential vs credential use; model action vs human action; containment that destroys evidence; notification threshold; uncertain third-party impact; resuming evals before controls are verified.

**Deliverables:** immutable action timeline, asset and data impact ledger, credential/identity exposure register, confirmed-vs-unconfirmed finding matrix, notification decision register, containment/restart plan, control validation evidence and executive incident report.

## Why these are materially different

| Task | Main business owner | Primary decision | Core non-code domain |
|---|---|---|---|
| 01 Retail replenishment | Store operations / merchandising / supply planning | What to send to each store tomorrow | demand, perishability, supplier cutoffs, allocation |
| 02 Cold-chain recovery | Warehouse / transport / food safety | Which lot and order can safely move | temperature, lot traceability, liability, logistics |
| 03 Airline recovery | OCC / crew planning / customer operations | Which flights and passengers recover first | crew legality, slots, passenger rights, capacity |
| 04 Flash-sale fulfillment | E-commerce operations / warehouse / finance | Which order lines can be fulfilled | reservation semantics, payments, inventory, returns |
| 05 SaaS customer recovery | Incident command / customer success / platform ops | Which customer sites can reopen and when | multi-product RPO, SLA, restore capacity, customer verification |
| 06 Agent incident response | AI platform security / research operations / legal | What happened and whether work may resume | evidence forensics, data exposure, authorization, third-party impact |


## Non-overlap contract — mandatory and frozen

The following boundaries are hard scope constraints. If a proposed artifact or rubric item crosses a boundary, move it to the correct task or remove it. Do not solve overlap by merely changing file names or task IDs.

| Task | Decision unit | Binding constraints | Forbidden content (belongs elsewhere) | Primary deliverable |
|---|---|---|---|---|
| V2-01 Retail replenishment | Store × SKU × delivery slot | Supplier cutoffs, store shelf/backroom capacity, FEFO, DC allocation, delivery windows | No checkout reservation TTL, payment authorization/capture, order-line refund adjudication (V2-04 scope); no cold-chain excursion disposition/food-safety release (V2-02 scope) | **Dispatch-ready store-SKU replenishment and vehicle/load plan** |
| V2-02 Cold-chain recovery | Lot/batch × shipment/order | Product-specific temperature limits, logger integrity, FEFO, dock/reefer capacity, food-safety release and liability | No consumer checkout/payment/order-state reconstruction (V2-04); no general store replenishment allocation (V2-01) | **Lot disposition and shipment release/hold register with claims evidence** |
| V2-03 Airline recovery | Flight leg × passenger itinerary, constrained by crew/tail | Crew duty/rest legality, aircraft rotation, airport slots/curfews, passenger rights and connection windows | No generic queue-priority scheduling exercise; no tenant/product disaster recovery (V2-05) | **Passenger-level reaccommodation and legal flight/crew recovery plan** |
| V2-04 E-commerce flash-sale fulfillment | Order line × SKU-location reservation | Reservation TTL, payment state, order/line state machine, warehouse pick/pack, return quality release | No supplier procurement cutoff, DC-to-store replenishment, store dispatch (V2-01); no temperature/food-safety lot release (V2-02) | **Order-line adjudication and available-to-promise reconstruction** |
| V2-05 SaaS mass deletion recovery | Tenant site × product | Product dependency graph, restore throughput, product-specific RPO, data validation, contractual SLA and customer reopening | No root-cause attribution or general incident blame investigation; no agent action/credential/data-exfiltration forensics (V2-06); not a generic queue scheduling benchmark | **Capacity-feasible restore sequence and per-customer reopening gate/data-loss statement** |
| V2-06 AI agent incident response | Agent action × asset/data item | Evidence provenance, authorization scope, identity/session, data classification, notification thresholds and containment integrity | No customer-site restore scheduling/RPO plan (V2-05); no generic AI model quality/feature-drift audit; no software dependency CVE review | **Confirmed / unconfirmed action-impact matrix and containment/notification decision** |

### Primary-output diversity rule

The six tasks must not all collapse into “ledger + plan + memo + loss estimate.” The primary deliverable is fixed in the table above. Secondary memos are allowed, but:
- V2-01: dispatch/replenishment plan is primary; lost-sales estimate is secondary.
- V2-02: lot disposition and claims evidence are primary; aggregate loss is secondary.
- V2-03: passenger-level reaccommodation and flight/crew legality are primary; compensation exposure is secondary.
- V2-04: order-line adjudication and ATP reconstruction are primary; margin/lost-sales bridge is secondary.
- V2-05: restore sequence and reopening gates are primary; SLA exposure is secondary.
- V2-06: confirmed/unconfirmed forensic findings and containment/notification decisions are primary; monetary loss is not a required headline output.

### Source-role separation

- V2-03 IndiGo is the primary aviation disruption case. NATS is supplementary background only; it is not a second incident dataset, not a separate task, and must not be used to merge unrelated evidence populations.
- V2-06 OpenAI public statements are primary source candidates, but if official pages are inaccessible (including HTTP 403) at capture time, mark the capture `SOURCE_CAPTURE_BLOCKED`. Do not replace official source URLs with image proxies, search snippets, or unlabelled secondary reports. Archive a verifiable official copy or clearly downgrade each claim to secondary/unverified before freezing the source register.
- Shopify is an engineering design source for inventory reservation semantics, not a claimed production outage. V2-04 must be labelled a production-style operational exercise grounded in a documented engineering problem, not a Shopify incident.

## Material difficulty specification

Each task's evidence pack should have 20–35 genuinely interdependent artifacts, not 20–35 filler files. Aim for a mix of:
- 5–8 authoritative business/source documents;
- 4–7 raw operational exports;
- 3–5 temporal/state/event logs;
- 2–4 financial/customer-impact files;
- 2–4 policies/contracts/runbooks;
- 2–4 deliberately imperfect or conflicting extracts.

Each case should contain enough rows for real row-level reconstruction (target 1,000–20,000 records depending on the domain), but row count alone does not establish difficulty. The full data must remain locally runnable and the model must be able to inspect it through supported tools. Every conflict must be resolvable using published source precedence and task rules; otherwise the correct result is UNKNOWN, not a hidden guess.

For each case freeze:
- entity registry and primary keys;
- event-time, effective-time, observed-time and ingestion-time semantics;
- authoritative source hierarchy;
- unit/currency/timezone and rounding rules;
- status state machine and transition validity;
- business constraints and priority hierarchy;
- required output schema and exact filenames;
- explicit UNKNOWN / NOT_OBSERVED / NOT_RUN semantics.

## Hard rubric, without unfair grading

Platform rubric: 20 criteria × 5 = 100. Machine checks C01–C19 max 95; C20 is human expert review (5).

- 5: all four frozen subchecks pass.
- 2: partially correct but material evidence/calculation/coverage gap.
- 0: wrong, unsupported, incomplete or unsafe on the criterion.

Critical-error dependency map must be frozen before any model run. Examples: illegal crew assignment affects flight recovery and passenger promises; releasing an out-of-temperature lot affects shipment approval and loss exposure; treating an uncommitted payment as captured affects order disposition; false restore certification affects reopening and SLA. Apply penalties only to dependent criteria, not a blanket global zero. Cosmetic formatting defects do not trigger critical penalties.

The grader must inspect actual row-level deliverables and independently recompute totals. It must not trust self-assessment JSON, narrative claims, screenshots of dashboards, or a model-generated PASS flag.

## Required calibration

For every task:
1. Independently constructed reference answer.
2. At least one substantively different valid alternative.
3. At least 10 targeted negative mutations (wrong time, duplicate entity, stale version, omitted rows, incorrect join, unit/currency error, unsupported status, false completion, unsafe action, etc.).
4. Empty and incomplete submissions return INVALID_SCHEMA, not a score.
5. Mutation tests prove only the intended criteria fail.
6. Row/column order invariance tests.
7. Reproducible validation commands and pinned dependencies.
8. Three independent Doubao 2.1 Pro new-session runs when user-provided platform access is available. Keep all valid and invalid runs; no hints, no interventions, no cherry-picking.
9. Difficulty gate only from valid evidence: score <=50 AND (actual task time >2400 seconds OR platform-verified steps >=50).
10. C20 remains PENDING until qualified humans independently review and adjudicate.

## Critical limitation

The cited public incidents are source material for scenario design, not permission to redistribute private company logs. Unless licensed real incident artifacts are available, create clearly labelled synthetic operational records based on public facts and domain rules. Do not claim synthetic records are real. Obtain project-owner approval if the platform requires real work materials. Do not claim these tasks are accepted or difficult until actual blind runs prove it.

## Packaging

Deliver one author master ZIP only:
- 01_PUBLIC_MODEL_INPUT/
- 02_PRIVATE_REFERENCE_RUBRIC_GRADER/
- 03_SOURCE_AND_LICENSE/
- 04_OPERATIONS/
- 05_MODEL_RUN_EVIDENCE/
- 06_PLATFORM_FIELDS/
- 07_READINESS_AND_BLOCKERS/
- MANIFEST.sha256
- ZIP_CRC_REPORT.txt
- README_STATUS.md

Only extract 01_PUBLIC_MODEL_INPUT for model runs. Never upload the author master ZIP to Doubao. Include all six tasks in one master archive; keep individual task folders internally distinct.
