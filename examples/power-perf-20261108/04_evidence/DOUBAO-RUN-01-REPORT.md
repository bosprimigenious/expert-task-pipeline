# Doubao run 01 — real result

Status: **COMPLETED / NOT A PASS**

## Run

| Item | Value |
|---|---|
| Task | 某地市供电公司2025年度业绩核定、红线责任与申诉追溯复核 |
| Conversation | https://www.doubao.com/chat/38452148980505346 |
| Model / mode | 豆包 2.1 Pro / 专家 |
| Input | 48 unpacked public files (A00–A06); `.zip` is not accepted by the web file input |
| Start | 2026-11-08 00:46:07 +08:00 |
| End | 2026-11-08 00:59:46 +08:00 |
| Wall time | **819 s = 13 min 39 s** |
| Verified steps | **NOT_VERIFIABLE** |
| Output | `results.zip`, `Power_Performance_Review.xlsx` |

## Grader

| Item | Value |
|---|---|
| Machine checks | **42 / 76** |
| Score interval | **49–54** |
| Final score | **null** (C20 human review not run) |
| C20 | NOT_RUN |
| Result | **TIME FAIL** (819 s < 2400 s); steps unverified |

Artifacts:

- `04_evidence/doubao-run-01/results.zip` — SHA-256 `557b0de0…`
- `04_evidence/doubao-run-01/Power_Performance_Review.xlsx` — SHA-256 `44c37d99…`
- `04_evidence/doubao-run-01/doubao_grade.json`
- `04_evidence/doubao-run-01/run01-output-text.txt`

## What the model did

- Produced a 16-file `results.zip` and a multi-sheet workbook.
- Its R2 table visually matches the reference:
  U7 100/A/1, U3 98/A/2, U8 98/A/2, U2 88.74/C/4, U6 88/D/5,
  U4 72/D/6, U1 67.87/D/7, U5 HOLD.
- It found the minimum-cost plan 7 and two equivalent optima.
- It audited old claims L01–L08.

## Why 42/76, not higher

The main R2 table is close, but the submission fails schema/consistency checks:

- `indicator_results.status` uses `OK`; the reference and task semantics use
  `DETERMINED` / `UNDETERMINED`. This trips C03–C06 across snapshots.
- `final_decisions` has empty/HOLD/format fields that make C12/C13 raise
  `Decimal.ConversionSyntax` / `int('A')`; these are submission-format failures.
- 42/76 = 34 failed machine checks; C20 is still pending, so `final_score=null`.

## Difficulty conclusion

**Not an effective difficulty pass.** The model finished in 13:39, far below the
40-minute threshold, and produced the correct R2 business table. Even if a
format-normalized grader were used, the run still fails the time criterion.
The task needs more irreducible work (required reconciliation/enumeration/
judgment) or a different target model, not just more files.

## Caveat

The web file input does not accept `.zip`; this run used 48 unpacked files.
It is a real model run, but not byte-identical to the “7 zip” protocol. Label it
`UNPACKED_48_FILES`, not the official protocol.
