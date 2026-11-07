# Failure catalog

Failures observed in the POWER-PERF case, and the pipeline fix.

## F1. Web input rejects zip

Doubao’s web file input silently ignored `.zip`; `.md` uploaded correctly.
A 48-file unpacked upload worked.

**Fix:** record `input_mode=UNPACKED_48_FILES`; do not pretend the 7-zip
protocol was used.

## F2. `status=OK` is not a valid enum

The model wrote `indicator_results.status=OK`; the schema uses
`DETERMINED` / `UNDETERMINED` / `NOT_APPLICABLE`.

**Fix:** strict preflight; any other enum = `INVALID_SCHEMA`.

## F3. No snapshot / R0/R1/RB

Run 02 delivered an R2-only set: no `snapshot` column, no R0/R1/RB.

**Fix:** preflight checks snapshot coverage; the grader is not allowed to run.

## F4. Grader crash on a missing column

The old grader raised `KeyError: 'snapshot'`. A crash is not a score.

**Fix:** `score_with_preflight.py`; invalid schema returns `INVALID_SCHEMA`
with findings.

## F5. Binary export is not guaranteed

The model first said it could not send a binary zip; later it produced an
`attachment_file_item`, which downloaded correctly. The first “delivery” was
only a workspace path.

**Fix:** require a file card/attachment, not “saved in workspace”; verify by
downloading and hashing.

## F6. Staging is not difficulty

Five stages took 24:01, still below 40 minutes. Staging adds turns but not
necessarily irreducible work.

**Fix:** add required per-record judgment/reconciliation/enumeration; measure
actual task time, not wall-clock waiting.

## F7. Business score vs evaluation score

A unit’s business score of 97 is not the model’s evaluation score. The model
can get a plausible business table while failing schema and intermediate
snapshots.

**Fix:** report business data and rubric score separately.

## F8. Old grader tolerated a bad enum

The soft 54 was produced before strict preflight. It is not a valid score.

**Fix:** freeze preflight before scoring; mark legacy soft scores as invalid.

## F9. Self-check overclaim

A submission may claim `PASS` while a formula check is `NOT_RUN`.

**Fix:** C20 review checks actual claims; self-check cannot replace execution.

## F10. Export follow-up can take longer than the task

Two export follow-ups added 6:36. Delivery is part of the work, not an
afterthought.

**Fix:** require artifacts at every stage; test the file card early.
