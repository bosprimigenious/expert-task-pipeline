# Staged run 02 — real result

Status: **COMPLETED / INVALID_SCHEMA / UNSCORABLE**

## Timings

| Stage | Time |
|---|---:|
| S1 intake | 3:57 |
| S2 R0 | 9:26 |
| S3 R1 | 4:17 |
| S4 R2 + RB | 3:55 |
| S5 final package | 2:26 |
| **Business stages total** | **24:01** |
| Export follow-ups S6/S7 | +6:36 |
| Total including export attempts | **30:37** |

- Start: 2026-11-08 01:25:01 +08:00
- S5 end: 2026-11-08 01:49:02 +08:00
- Conversation: https://www.doubao.com/chat/38452247448681986
- Input: 48 unpacked public files, 专家/对话
- 5 stage prompts + 2 export follow-ups = 7 model turns
- Official steps: **NOT_VERIFIABLE**

## Delivery

The model eventually delivered `results.zip` (28,284 bytes, 16 files) after two
follow-ups. It was downloaded successfully.

However, the package is **not schema-valid**:

- `final_decisions.csv` has no `snapshot` column;
- `indicator_results.csv` has no `snapshot` column;
- R0/R1/RB artifacts are absent;
- the standard grader crashes with `KeyError: 'snapshot'`.

Therefore no strict 76-check score can be produced.
**Score = null / INVALID_SCHEMA.**

## Business result reported by the model

| Unit | Model R2 | Reference R2 | Difference |
|---|---|---|---|
| U1 | 62.88 / C / 5 | 67.87 / D / 7 | wrong score/grade/rank |
| U2 | 88.6 / B / 2 | 88.74 / C / 4 | wrong grade/rank |
| U3 | 97 / A / 1 | 98 / A / 2 | wrong score/rank |
| U7 | 100 / A / 1 | 100 / A / 1 | match |
| U8 | 97 / A / 1 | 98 / A / 2 | wrong score/rank |
| U4 | 72 / C / 4 | 72 / D / 6 | wrong grade/rank |
| U6 | 88 / D / 6 | 88 / D / 5 | wrong rank |
| U5 | 90 / HOLD | 90 / HOLD | match |

Other reported mismatches:

- minimum-cost plan: **1** (only C08) vs reference **7**;
- legacy audit: **4/8 rejected** vs reference **8/8**;
- `self_check` claims PASS, but workbook formulas are `NOT_RUN`; this is an
  overclaim.

## Conclusion

Staging increased time from 13:39 to 24:01, but:

- still below 2400 s;
- final business result is substantively wrong;
- file delivery failed;
- no valid 76-check score.

This is a **better difficulty probe** than run 01, but still not a valid pass.
The next version must require the final files as an exportable artifact from
the start, and must add irreducible reconciliation/authority work.
