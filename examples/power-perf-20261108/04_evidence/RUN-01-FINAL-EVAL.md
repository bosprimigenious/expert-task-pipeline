# Run 01 final evaluation (manual C20)

Status: **LEGACY SOFT SCORE / STRICT PREFLIGHT INVALID**

## Machine checks

- 42 / 76 machine checks passed
- machine interval: 49–54
- C20 manual review: **5 / 5**
- **Legacy soft total: 54 / 100**
- **Strict preflight: INVALID_SCHEMA** (`indicator_results.status=OK`)

C20 rationale: the memo gives time/visibility rules, per-unit R2 decisions, R0→R1→R2 changes, U5 HOLD, plan cost 7, legacy audit, and explicit “not executed” boundaries. It does not claim platform acceptance or a model score.

## Criterion pass counts

| Criterion | Passed |
|---|---|
| C01 | 4/4 |
| C02 | 4/4 |
| C03 | 0/4 |
| C04 | 0/4 |
| C05 | 0/4 |
| C06 | 0/4 |
| C07 | 4/4 |
| C08 | 4/4 |
| C09 | 4/4 |
| C10 | 4/4 |
| C11 | 0/4 |
| C12 | 0/4 |
| C13 | 0/4 |
| C14 | 3/4 |
| C15 | 4/4 |
| C16 | 4/4 |
| C17 | 0/4 |
| C18 | 4/4 |
| C19 | 3/4 |
| C20 | manual 5/5 |

## Why not higher

- C03–C06 all fail because `indicator_results.status` is `OK`, not the required `DETERMINED/UNDETERMINED`.
- C11–C13 fail with format/consistency exceptions.
- C17 fails; C19 has one manifest/consistency failure.
- The main R2 table is right, but intermediate/schema discipline is not.

## Threshold

Run 01: 819 s, 54/100.

- Platform target `S<=50 AND (T>2400 OR V>=50)` → **score and time fail**.
- Internal strict `S<50 AND T>2400 AND V>=50` → **fail**.
- Steps: NOT_VERIFIABLE.

## Caveat

C20 was reviewed by the author-side analysis, not an independent domain expert. The 54 is a legacy soft score; strict preflight rejects the submission. Do not use 54 as a valid submission score.
