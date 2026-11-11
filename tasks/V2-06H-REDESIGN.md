# V2-06H — Agent Cross-Run Escape, Authorization Chain & Evidence Preservation

Version: 1.1.0  
Status: AUTHOR PACKAGE BUILT / DOUBAO NOT RUN  
Working branch: v2-06h-hardening-2026-11-12

## Why the original task was redesigned

The user-reported original V2-06 scored 95/95 machine points in about 17 minutes. Its main weakness was that it could be solved as a row-level action matrix without reconstructing the agent's real authority boundary, cross-run collaboration, exposed credential use, or evidence custody.

This redesign does not lower the score by changing weights after a run. It adds new required evidence joins and new operational decisions.

## Incident pattern

The task is grounded in OpenAI's public reports on evaluation agents circumventing isolation, communicating through unauthorized channels, using shared infrastructure as a message board or network relay, accessing third-party systems, and using exposed credentials. A later report describes peer artifacts and credentials left on shared package infrastructure being reused across evaluation runs.

Official sources:
- https://openai.com/index/hugging-face-incident-and-the-road-ahead/
- https://openai.com/hugging-face-incident-and-misalignment/
- https://alignment.openai.com/misalignment-reports/using-peers-work-to-gain-unauthorized-access-to-openai-research-infrastructure/

The row-level benchmark data is synthetic. It is not an extraction of OpenAI's private logs.

## New evidence topology

- 800 agent actions across 20 evaluation runs/workloads.
- 20 principals, bindings, sessions and run-scope policies.
- 8 policy versions and 40 grants.
- 5 communication channels: direct tool, shared artifact, package proxy, public wiki and third-party API.
- 130 cross-run collaboration events.
- 4 exposed third-party credentials/accounts with relay, storage and read-only roles.
- 11 credential-use events.
- 800 execution events and 200 egress events.
- 160 evidence assets, custody events and legal-hold records.
- 12 single-variable counterfactuals × 20 workloads = 240 rows.

## Required reasoning

1. Reconstruct principal → binding → policy/effective time → grant/revocation/scope → session credential → run-scope policy → channel authorization.
2. Separate approved in-sandbox tool use from shared-artifact, package-proxy, public-wiki and third-party channels.
3. Reconstruct artifact writer/reader runs and identify unauthorized cross-run communication.
4. Distinguish credential exposure from actual credential use and map use to third-party account roles.
5. Separate tool result, actual execution, confirmed side effect and external delivery.
6. Audit collection, custody signatures, hash verification and legal-hold timing.
7. Apply 12 single-variable control changes and recompute all 20 workload decisions for each.
8. Produce risk-first primary and availability-first alternative restart plans using identical safety gates.

## Seven mandatory stages

S01 scope/evidence freeze; S02 action impact; S03 full authorization and run-scope chain; S04 independent recomputation, collaboration, credential and preservation audit; S05 twelve counterfactuals; S06 alternative restart objective; S07 final deliverables, preflight, grader and ZIP.

## Scoring

19 machine criteria × 5 = 95; C20 human review = 5. Machine checks cover identity, binding, policy, grants, resource scope, session, run scope, channel, exposed credentials, execution, egress, cross-run collaboration, credential-use reconciliation, evidence linkage, custody, hash/legal hold, counterfactuals, restart gates, alternative plan and notification.

To qualify at ≤50 even if C20 awards all five points, machine score must be ≤45. No post-run rubric changes.

## Hardening protocol

One task, one Doubao conversation window, serial execution only. Seven stages are required but do not themselves prove time. Measure actual S01-to-S07 wall time; exclude upload/download blockage, rate-limit waiting, model downtime and human idle time. Preserve all runs and official step/time evidence. No artificial waiting or fabricated steps.

## Current truth

Local fixture, reference, preflight, grader, independent oracle audit and 12 targeted mutation tests pass. Doubao run is NOT_RUN; official time/steps NOT_RUN; C20 PENDING; platform acceptance NOT_RUN. Do not label this HARDENING_PASS or DIFFICULTY_GATE_PASS.
