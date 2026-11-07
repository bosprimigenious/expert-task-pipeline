# Strict grading addendum v1 (frozen before staged run)

Applies to `POWER-PERF-STAGED-v2`; use with `rubric_20.md`.

## Stricter rules

1. **All four snapshots required**: R0, R1, R2, RB. Missing/incorrect
   intermediate snapshot is not excused by a correct R2.
2. **Schema enum**: `indicator_results.status` must be `DETERMINED` /
   `UNDETERMINED` (or the schema-defined enum). `OK` is a failure.
3. **No grader exceptions**: any `Decimal.ConversionSyntax`, `int('A')`, or
   empty/HOLD in a numeric column is a failure, not a warning.
4. **Stage gates**: Stage 1 intake, R0, R1, R2+RB, final package. A missing
   stage artifact caps the related criteria at 0.
5. **No future information** in R0/RB; a single leaked later record fails the
   affected criterion.
6. **No draft-as-final**, no double-counted event, no ranking a HOLD unit.
7. **Evidence**: each key conclusion needs a source_id/file + business key.
8. **C20**: human review; no credit for “completed” without files.
9. **Time/steps**: record wall time and verified decision rounds; platform
   target `S<=50 AND (T>2400 OR V>=50)`; internal strict
   `S<50 AND T>2400 AND V>=50`. Do not infer steps from tool calls.
10. **Freeze**: this addendum and the 20-item rubric are frozen before the run;
    do not adjust after seeing the output.

## Known observed failure modes to score explicitly

- `indicator_results.status=OK` instead of `DETERMINED`;
- numeric columns containing `HOLD`/empty;
- R0/R1 wrong while R2 looks right;
- missing RB;
- final package missing one of the required files;
- self_check claims more than actually run.
