# Task 01 — Draft task design (not frozen)

## Working title
Multi-tenant GPU Cluster Capacity Review: Training-vs-LLM-Inference Evidence Reconciliation and Scheduling Decision

## Classification proposal
- Task type: Engineering, Product & Professional Research (confirm platform taxonomy).
- L1 industry: Technology, Software & Digital Infrastructure.
- L2 industry: AI & Data Technology or Hardware, Semiconductor, Cloud & Communications; choose one only after checking current platform taxonomy and task emphasis.
- L1 occupation: Platform / Infrastructure Engineering.
- L2 occupation: Infrastructure Engineer / SRE; verify exact current platform enum.

## Scenario boundary
An infrastructure analyst supports a cloud/AI capacity review using two independent public traces: Microsoft Philly multi-tenant DNN training and Alibaba MaaS LLM inference. This is an explicitly declared public-data research scenario, not a claim of employment by either operator.

## Required outputs
1. Executive decision memo with separate Philly and Alibaba sections and bounded comparison.
2. Dataset manifest with per-file hashes and license notices.
3. Philly job-attempt reconstruction; queue/wait/runtime and placement analysis; incomplete attempts retained.
4. Philly GPU utilization and machine-capacity reconciliation; offline NA preserved.
5. Alibaba daily instance-segment analysis; fractional GPU allocation and additive GPU-hours.
6. Alibaba five-minute time-series analysis with half-open window semantics.
7. Alibaba app-metrics analysis; normalized QPS and latency metrics distinguished.
8. Capacity and scheduling option matrix, assumptions, uncertainty and sensitivity.
9. Validation report with commands, tool versions and test results.
10. Evidence index mapping every decision claim to source file, row/key, time window and calculation.

No production configuration change or live infrastructure action is authorized.

## Hidden-difficulty candidates (confirm against acquired data)
1. Jobs with no scheduling attempts remain in the population and are separately classified.
2. Missing attempt timestamps are not imputed as zero duration.
3. Null end time on final attempt may indicate still-running job, not failure.
4. GPU reservations reconstructed across attempts without retry double-counting.
5. Offline NA telemetry is not zero utilization.
6. Machine inventory and per-GPU memory constrain capacity.
7. Philly timezone and daylight-saving transitions normalized without event-order shifts.
8. Alibaba daily multi-segment instance-days aggregate additive GPU-hours.
9. Fractional gpu_count preserved; integer rounding changes denominators.
10. Weekly samples are five-minute averages over [time_s,time_s+300), not point samples.
11. series_id is not an instance identifier.
12. qps_norm is normalized and cannot be reported as absolute QPS.
13. Daily/weekly/app windows differ; no unsupported full-period correlation.
14. Training and inference populations are not pooled; comparisons require harmonization and limitations.

Retain only 8–15 data-proven items after inspecting acquired data. Each must affect a required decision and map to a rubric check.

## Reference and grader design
- Recompute reference independently from acquired files; do not copy paper figures or README summaries.
- Publish exact output columns, units, precision, timezone and null semantics.
- Grader inspects actual deliverables, not self-reported assessment JSON.
- Require one substantively different valid alternative and targeted negative baselines.
- Missing required files/columns or invalid enums return INVALID_SCHEMA before grading.
- Rubric: 20 criteria x 5 points; C01-C19 machine-evaluable (max 95), C20 independent human review (5; pending two reviewers and arbitrator).
- Difficulty gate uses only valid blind runs: score <=50 and (actual task time >2400 seconds or platform-verified steps >=50).

## Freeze blockers
Raw data not acquired; source hashes absent; Alibaba redistribution terms conditional; no independent reference, grader, alternative, negative baselines, blind run, C20 or platform acceptance. Do not submit this draft as a completed task.