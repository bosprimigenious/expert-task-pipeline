# Expert Task Pipeline

Author-side tooling and a worked case study for building, stress-testing and
grading high-value expert tasks for **Doubao 2.1 Pro**.

> **Status: research prototype, not a platform submission.**
>
> The canonical case is **synthetic** and has **not** passed the difficulty gate.
> There is **no valid model score** yet. Do not use this repository as evidence
> that a task is platform-ready, real-work, or accepted.

**中文一句话**：这是一个“出题—冻结—实测—评分—提交前检查”的作者侧产线；
`examples/power-perf-20261108/` 是最典型的失败案例，不是成功案例。

---

## Why this repository exists

A local reference answer passing is not evidence that a model can do the task.
A model answering fluently is not evidence either. An expert task needs all of
the following together:

- a real work context and authorized materials;
- 8–15 hidden difficulties that change decisions, not just prose;
- a 100-point rubric with TRUE/FALSE checks, units and tolerances;
- an independent answer and a calibrated grader;
- a specified-product, new-session run;
- a strict schema preflight before scoring;
- a difficulty gate: score **≤ 50** and either **verified steps ≥ 50** or
  **wall time > 2400 s**.

This repository packages the first complete iteration of that pipeline, including
the two failed model runs that forced the pipeline to become stricter.

---

## The canonical case

`examples/power-perf-20261108/` reconstructs a power-utility annual performance
review across four snapshots:

```text
R0  2026-01-12 17:00
R1  2026-01-26 17:00
R2  2026-02-09 17:00
RB  independent replay of R0
```

The synthetic case contains 8 assessed units, 24 feeders, 288 feeder-months,
1,504 source records, 12 incidents and 6 appeals. Deliverables include a 9-sheet
workbook, 11 CSVs, 4 JSON/MD files and a `results.zip`.

- 20 criteria × 5 points = 100
- 76 machine checks + C20 human review
- 7 public input packs: `A00`–`A06`
- private reference answer and grader are isolated from the model upload

### Reference result

```text
schema_preflight(reference_answer)  PASS
grader(reference_answer)            76 / 76
score interval                      95–100 before C20
```

### Actual model results (the important part)

| Run | Mode | Wall time | Machine | Strict preflight | Score |
|---|---|---:|---:|---|---|
| 01 | 对话 + 专家，single-round | **13:39** | 42/76 | **INVALID_SCHEMA** (`status=OK`) | no valid score |
| 02 | 对话 + 专家，5 staged prompts | **24:01** | — | **INVALID_SCHEMA** (45 blockers) | no valid score |

The old Run 01 “54/100” is a **legacy soft score** from the old grader. It is
not a valid score: the strict preflight rejects `indicator_results.status=OK`,
and 13:39 is below the 40-minute gate.

Run 02 delivered 16 files, but `final_decisions.csv` and
`indicator_results.csv` had no `snapshot` column, and R0/R1/RB artifacts were
missing. The standard grader crashed with `KeyError: 'snapshot'`. This is why
`schema_preflight` now runs before the grader.

**Conclusion:** the task is still too easy and too short. Staging increased
time from 13:39 to 24:01, but did not make it a pass. The case is kept as a
failure case, not a success story.

---

## Pipeline

```text
direction / L1–L2 / real work
        │
        ▼
material acceptance  ──►  hidden difficulties (8–15)
        │
        ▼
task prompt + 7 public packs + private reference
        │
        ▼
schema preflight  ──►  freeze (hash)
        │
        ▼
specified-product new-session run  (3 runs)
        │
        ▼
strict preflight  ──►  grader  ──►  C20 manual review
        │
        ▼
difficulty gate: score ≤50 AND (steps ≥50 OR time >2400s)
        │
        ▼
12-point submission checklist
```

### Hard rules

1. **Real work first.** Synthetic examples are drafts; they cannot be submitted
   as real work. Public data + a declared scenario may be allowed only when the
   project rules say so.
2. **One complex goal.** Do not bolt unrelated mini-tasks together.
3. **Hidden difficulties must be in the data.** A difficulty that is not on the
   required path is not a difficulty.
4. **The reference answer and rubric are author-only.** Never put
   `03_private_review/` in the model upload.
5. **Preflight before grading.** A missing `snapshot`, wrong enum or missing
   R0/R1/RB must return `INVALID_SCHEMA`, not a stack trace.
6. **Three runs, no cherry-picking.** Keep every run; a single low run is not
   proof.
7. **No fake time.** Staging, waiting or irrelevant attachments do not count.
8. **No platform pass without a platform receipt.** Local PASS is not
   `PLATFORM_ACCEPTED`.

See [`docs/PIPELINE.md`](docs/PIPELINE.md) for the full gate definitions and
[`docs/CASE-STUDY.md`](docs/CASE-STUDY.md) for the run timeline.

---

## Quick start

Requires Python 3.10+. `openpyxl` is needed for workbook-sheet checks; use the
bundled runtime if available.

```bash
cd examples/power-perf-20261108

# 1. Reference schema check (must be PASS)
python3 03_private_review/tools/schema_preflight.py \
  --submission 03_private_review/reference_answer \
  --public /path/to/public_unpacked \
  --output /tmp/reference-preflight.json

# 2. Reference grade (expected 76/76; final score remains null until C20)
python3 03_private_review/tools/score_with_preflight.py \
  --submission 03_private_review/reference_answer \
  --reference 03_private_review/reference_answer \
  --public /path/to/public_unpacked \
  --output /tmp/reference-grade.json

# 3. A model submission: preflight first
python3 03_private_review/tools/schema_preflight.py \
  --submission /path/to/model-submission \
  --public /path/to/public_unpacked \
  --output /tmp/model-preflight.json
```

If preflight returns `INVALID_SCHEMA`, **do not run the grader**. Fix the
submission or mark the run invalid; do not normalize it after the fact.

### Public input packs

The 7 model-visible packs are in
`examples/power-perf-20261108/06_blind_test/01_public_inputs/` (`A00`–`A06`).
The model-visible prompt is
`06_blind_test/task_prompt.md`; the staged prompt variants are in
`06_blind_test/staged_prompts/`.

> Doubao’s web file input does not accept `.zip` reliably. The tested workaround
> is to unpack the 7 packs and upload the 48 files, recording
> `input_mode=UNPACKED_48_FILES`.

---

## Repository layout

```text
docs/
  PIPELINE.md                 gates, artifacts, failure handling
  CASE-STUDY.md               run 01/02 timeline and errors
  FAILURE-CATALOG.md          what broke and the fix
  SUBMISSION-READINESS.md     12-point checklist
  PLATFORM-RULES.md           project rules used by this repo
  OPEN-SOURCE-SCOPE.md        what is included/excluded and why
tools/
  schema_preflight.py         task-specific schema gate
  score_with_preflight.py     preflight → grader wrapper
  grader.py                   example 76-check grader
examples/power-perf-20261108/
  01_platform_upload/         7 public zips
  02_platform_fields/         platform field drafts
  03_private_review/          reference answer, rubric, grader (author-only)
  04_evidence/                run logs, preflight reports, model outputs
  05_addendum/                hardening notes
  06_blind_test/              model-visible prompt and inputs
  07_submission/              assembled technical package + readiness
```

---

## Current status

| Area | Status | Evidence |
|---|---|---|
| Author-side reference | **PASS** | `04_preflight/reference.json`, 76/76 |
| Schema preflight | **PASS** on reference | `schema_preflight.py` |
| Run 01 | **INVALID_SCHEMA** | `status=OK`; no valid score |
| Run 02 | **INVALID_SCHEMA** | 45 blockers, missing snapshot/R0/R1/RB |
| Difficulty gate | **FAIL** | 13:39 and 24:01; no valid run |
| Real-work source | **BLOCKED** | synthetic fictional utility |
| Submission | **NOT READY** | 12-point checklist |

Read [`docs/SUBMISSION-READINESS.md`](docs/SUBMISSION-READINESS.md) before any
platform action.

---

## What this repository does **not** claim

- It is not a platform-accepted task.
- It is not a real utility’s data or a real internal work product.
- It does not prove the author has the required L1/L2 industry qualification.
- It does not prove Doubao cannot do the task; it only records two specific
  invalid/too-short runs.
- The “54” legacy score is not a valid score.
- It does not authorize uploading private answers to a model or submitting
  synthetic material as real work.

## Security and privacy

- No credentials, cookies, tokens or browser profiles are included.
- The model run was performed against a synthetic dataset.
- `03_private_review/` contains answers and must never be uploaded to a model.
- If you fork this repository, remove the private answer before making the task
  public or before using it as a live evaluation.

## Contributing

Issues and pull requests are welcome for the **pipeline and tooling**:

- schema preflight rules and tests;
- grader calibration and adversarial fixtures;
- staged prompt/artifact contracts;
- case studies with honest failed runs.

Please do not add:
- credentials or browser session data;
- real customer/employer data without written authorization;
- claims of platform acceptance without a receipt.

## License

MIT. See [`LICENSE`](LICENSE). The synthetic data and task text are provided for
research and pipeline development only; they are not a real company’s records.

## Citation

If you use the pipeline concepts, cite this repository and the case study:

```text
Expert Task Pipeline — POWER-PERF canonical failure case (2026).
https://github.com/bosprimigenious/expert-task-pipeline
```
