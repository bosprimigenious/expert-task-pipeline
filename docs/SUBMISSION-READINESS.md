> Paths in this checklist are relative to `examples/power-perf-20261108/07_submission/`.

# Submission readiness — POWER-PERF-20261108

Status: **NOT READY TO SUBMIT**

The technical package is assembled; the content is not platform-submittable yet.

## Technical package

- 7 upload zips: `01_platform_upload/`
- platform fields: `02_platform_fields/`
- rubric/answer/solution/answer attachment: `03_private_review/`
- reference preflight: **PASS** (`04_preflight/reference.json`)
- run 01 preflight: **INVALID_SCHEMA**
- run 02 preflight: **INVALID_SCHEMA**

## 12 checks

| # | Check | Status |
|---|---|---|
| 1 | Real L1/L2 work and real source | **BLOCKED** — synthetic fictional utility; no real work authorization |
| 2 | Concrete task name | PASS |
| 3 | Clear prompt and deliverable | PASS |
| 4 | Attachments self-contained | PASS — 7 zips, ≤2GB |
| 5 | One complex goal, not unrelated tasks | PASS |
| 6 | 8–15 hidden difficulties | PASS — 12 mechanisms |
| 7 | Each difficulty has scoring | PASS — 20 criteria / 76 checks |
| 8 | Objective TRUE/FALSE, units/tolerance | **CONDITIONAL** — C20 manual; 5/2/0 candidate not platform-confirmed |
| 9 | Standard answer + attachment | PASS |
| 10 | Solution approach | PASS |
| 11 | Specified model self-test | **FAIL** — no valid score; strict preflight invalid for both runs |
| 12 | Score ≤50 and (steps ≥50 or time >2400s) | **FAIL** — run 01 invalid/819s; run 02 invalid/1441s |

## Blockers

1. **Source**: the task uses fictional `澄川市供电公司` data. Platform rules require a real work task; public data + scenario is allowed, but this package is synthetic and labeled as such.
2. **No valid self-test**: both runs fail strict schema preflight. Run 01 `status=OK`; run 02 missing `snapshot`/R0/R1/RB.
3. **Difficulty**: best business run 13:39; staged 24:01; both below 40 minutes.
4. **Rubric**: 20×5 5/2/0 candidate not confirmed; C20 manual not independent.
5. **AI participation / real-material boundary**: unresolved; do not remove the synthetic label.

## What is needed before clicking submit

1. Replace the synthetic company/data with a real task + real/public authorized materials, or get project owner approval for a public-data scenario.
2. Rebuild/freeze reference answer and rubric on the real materials.
3. Fix prompt/schema so model output includes `snapshot` and R0/R1/R2/RB.
4. Run 3 new sessions; pass strict preflight; score ≤50 and time >2400s (or verified steps ≥50).
5. Re-run the 12 checks.

**Do not submit this package as real work.**
