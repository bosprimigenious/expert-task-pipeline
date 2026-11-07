# Case study: POWER-PERF (canonical failure case)

This is the case that forced the pipeline to add a strict schema gate.

## Task

A synthetic city power utility’s 2025 annual performance review:

- 8 assessed units;
- 24 feeders × 12 months = 288 feeder-months;
- 1,504 source records;
- 12 incidents, 6 appeals;
- R0 / R1 / R2 / RB snapshots;
- workbook + 11 CSVs + 4 JSON/MD files in `results.zip`.

The package is labeled synthetic. It is not a real utility’s records.

## Reference

```text
schema_preflight(reference)  PASS
grader(reference)            76 / 76
```

The reference answer passes. That only proves the author-side package is
internally consistent; it does not prove a model can do it.

## Run 01 — single round, 专家/对话

- Start: 2026-11-08 00:46:07 +08:00
- End: 2026-11-08 00:59:46 +08:00
- Wall: **819 s = 13:39**
- Input: 48 unpacked files (`UNPACKED_48_FILES`); Doubao web input rejected zip
- Output: `results.zip` (16 files) + workbook

Old grader:

```text
42 / 76 machine checks
interval 49–54
C20 manual 5/5
legacy soft total 54
```

Strict preflight:

```text
INVALID_SCHEMA
indicator_results.status = OK
```

So 54 is **not a valid score**. The old grader tolerated the enum; the strict
gate does not. Time also fails (819 s < 2400 s).

The model’s R2 table was mostly correct, but C03–C06, C11–C13, C17 and one C19
check failed. Correct main numbers did not rescue the intermediate/schema
discipline.

## Run 02 — five staged prompts, 专家/对话

Stages: intake → R0 → R1 → R2/RB → final package.

| Stage | Time |
|---|---:|
| S1 intake | 3:57 |
| S2 R0 | 9:26 |
| S3 R1 | 4:17 |
| S4 R2/RB | 3:55 |
| S5 final package | 2:26 |
| **business total** | **24:01** |
| export follow-ups | +6:36 |
| total | 30:37 |

The model delivered a 28,284-byte `results.zip` after two follow-ups. It was
not schema-valid:

- no `snapshot` in `final_decisions.csv` / `indicator_results.csv`;
- 45 preflight blockers;
- R0/R1/RB absent;
- grader would crash with `KeyError: 'snapshot'`;
- no valid score.

Reported business table also differed from the reference:

| Unit | Model | Reference |
|---|---|---|
| U1 | 62.88 / C / 5 | 67.87 / D / 7 |
| U2 | 88.6 / B / 2 | 88.74 / C / 4 |
| U3 | 97 / A / 1 | 98 / A / 2 |
| U8 | 97 / A / 1 | 98 / A / 2 |
| U4 | 72 / C / 4 | 72 / D / 6 |
| U6 | 88 / D / 6 | 88 / D / 5 |
| U5 | 90 / HOLD | 90 / HOLD |
| U7 | 100 / A / 1 | 100 / A / 1 |

Other mismatches: plan cost 1 vs 7; legacy audit 4/8 rejected vs 8/8.

## What this case proves

1. The author-side package is internally consistent.
2. The model can produce a plausible R2 table quickly.
3. The task is **not long/hard enough**: 13:39 and 24:01.
4. Staging alone does not create difficulty.
5. Schema and artifact contracts must be hard gates.
6. A correct-looking business table is not a valid submission.

## What it does not prove

- That Doubao cannot do the task in general.
- That the task is platform-ready.
- That the synthetic company/data can be submitted as real work.
- That the 54 legacy score is valid.

## Next version

- Require `snapshot` and R0/R1/R2/RB in every stage;
- require a file card at every stage;
- add irreducible reconciliation/authority work;
- run 3 new sessions;
- preflight each output before grading;
- only then re-run the 12-point checklist.
