# Task 01 — AI Infrastructure

Status: MATERIALS_BLOCKED / RESEARCH_IN_PROGRESS
Research date: 2026-11-11
Base pipeline commit: 452db4a29bb8f738a6547ebc1339fc88bbd1b035

## Intended decision
Prepare a defensible capacity and scheduling recommendation from two independent public GPU-cluster trace populations. Explain utilization/fragmentation and workload characteristics, quantify uncertainty, and propose operational actions with evidence.

## Population separation (hard rule)
1. Microsoft Philly: multi-tenant DNN training workload trace, 2017-08-07 through 2017-12-22.
2. Alibaba MaaS: anonymized LLM inference trace, six months; online and offline workloads.

These populations must never be pooled, row-joined, or treated as one continuous cluster. Cross-source comparison is limited to semantically comparable normalized metrics with separate denominators, windows, caveats and provenance. Training vs inference is a workload distinction, not an interchangeable cohort.

## Acquisition blockers
- Philly: repository metadata confirms CC-BY-4.0. Actual trace archive is external; not downloaded in this execution environment.
- Alibaba MaaS: public README and manifest/schema were inspected. Repository metadata exposes no dataset license identifier; public availability is insufficient to assert redistribution permission. Data terms and platform permission remain CONDITIONAL.
- Current execution container cannot resolve external hosts (Git clone failed with DNS resolution error). No raw trace bytes were acquired or hashed. No dataset lock or recomputed reference is claimed.

## Acceptance state
| Gate | Result |
|---|---|
| Public source discovery | PASS |
| Philly license metadata | PASS (CC-BY-4.0; attribution required) |
| Alibaba dataset schema discovery | PASS |
| Alibaba data license / redistribution terms | CONDITIONAL |
| Raw dataset acquisition | BLOCKED |
| SHA-256 / archive CRC / Parquet validation | NOT RUN |
| Independent reference | NOT RUN |
| Grader / mutation tests | NOT RUN |
| Model blind run | NOT RUN |
| Difficulty gate | NOT RUN |
| C20 | PENDING |

## Next action
Acquire official Philly and Alibaba MaaS archives in a network-enabled environment. Verify bytes, archive CRC, Parquet schemas/row counts, null and key profiles, then freeze hashes. Only after acceptance can the prompt, independent reference, grader and negative baselines be finalized.