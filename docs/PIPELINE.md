# Pipeline

This is the author-side pipeline. It produces a task pack, runs a specified
product in a new session, and freezes the evidence. It does not replace platform
review.

## 0. Scope

Inputs:

- L1/L2 industry and occupation the author can actually cover;
- a real work context (or an explicitly approved public-data + scenario);
- authorized materials and their provenance;
- the decision the deliverable will support;
- the specified product, mode and tools.

If the source is synthetic, the task is a **draft**, not a submittable case.

## 1. Material acceptance

For each material:

- source URL/path, capture time, version, SHA-256;
- authorization/redaction status;
- license and redistribution boundary;
- whether the material is enough to decide the business question;
- missing evidence list.

Reject or mark `CONDITIONAL` when the material cannot support a decision without
a private system, account or oral supplement.

## 2. Task design

Write:

- one concrete work name (object + action, not an abstract ability);
- role, inputs, business rules, version/cutoff times, prohibited actions;
- one final deliverable set;
- 8–15 hidden difficulties (material conflict, unit/period mismatch, state
  misjudgment, shortcut failure, false anomaly);
- a 20-criterion rubric at 5 points each = 100;
- machine checks and a C20 manual review.

Every hidden difficulty must be on the required path and must have a check that
can be graded TRUE/FALSE.

## 3. Reference and grader

- independently recompute the answer;
- open/run the actual workbook and CSVs;
- test the grader on:
  - the reference answer (must pass);
  - a local wrong answer (must lose the right points);
  - an empty submission (must not pass);
- freeze the answer, rubric, check map and hashes.

## 4. Public pack

- model-visible prompt;
- 7 public input packs (or the project’s approved count);
- no answer, rubric, hidden-difficulty list or author notes;
- zip list checked after packaging, not just in the source tree.

## 5. Product self-test

- specified product, mode, tools, account and network;
- new session;
- only prompt + public inputs;
- no score, step or time hints to the model;
- record start/end with timezone, attachments/hashes, outputs, tool log, errors,
  and the platform conversation URL;
- set a hard test limit; distinguish “completed late” from “stopped at limit”.

Use 3 runs for a qualification decision. Keep every run.

## 6. Strict preflight

Run **before** the grader:

```bash
python3 tools/schema_preflight.py \
  --submission <submission> --public <public_unpacked> \
  --output preflight.json
```

Hard fail when:

- required files/columns are missing;
- `snapshot` is absent;
- R0/R1/R2/RB is absent for a snapshot-scoped file;
- `indicator_results.status` is not `DETERMINED` / `UNDETERMINED` /
  `NOT_APPLICABLE`;
- a numeric column contains `HOLD` or an enum;
- keys are duplicated;
- workbook sheets are missing.

`INVALID_SCHEMA` means no score. Do not normalize after seeing the result.

## 7. Grading

- 76 machine checks for C01–C19;
- C20 manual review (5 points);
- report criterion-level pass counts, not just a total;
- keep the interval when C20 is pending;
- no model self-score.

## 8. Difficulty gate

Target:

```text
score ≤ 50 / 100
AND (verified steps ≥ 50 OR actual task time > 2400 s)
```

If the run is too short:

- add required per-record judgment, reconciliation, enumeration, scheduling,
  testing or recalculation;
- do **not** add irrelevant files, forced waiting, broken links or artificial
  step counts.

If the run scores high:

- remove hints from the prompt;
- put the difficulty back into the details;
- add version/authority/state conflicts;
- make checks concrete numbers or “no credit if X”.

## 9. Submission readiness

Use the 12-point checklist in
[`SUBMISSION-READINESS.md`](SUBMISSION-READINESS.md). A technical package is not a
submission until the source, self-test, difficulty and platform fields are all
ready.

## 10. Evidence retention

Per run keep:

- prompt version and hashes;
- public pack hashes;
- output files and preflight/grade reports;
- screenshots and conversation URL;
- start/end timestamps and timezone;
- human interventions and failures;
- final status (`COMPLETED`, `INVALID_SCHEMA`, `TEST_BLOCKED`, etc.).

Do not rewrite a failed run as a pass.
