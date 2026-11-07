# Blind-test kit (only these files go to the model)

Give the model:

- `task_prompt.md`
- the 7 zips in `01_public_inputs/`

Do **not** give the author package, rubric, answer, difficulty cards, grader,
reference workbook, or prior scores.

## Before each run

- New conversation; same model/mode/network; record model label and thinking mode.
- Record start/end in +08:00; do not include upload preparation.
- Record official wall-clock, full model decision steps, and tool calls separately.
- Keep all 3 runs; do not keep only the lowest score.

## After each run

- Freeze the full output and files with SHA-256.
- Grade only after the run is closed; do not change the run after seeing the score.
- Fill `run_0N.json`; mark unverifiable fields `NOT_VERIFIABLE`.
- Score with `03_private_review/tools/grader.py`; C20 is human review.
- Report `Score`, `Time`, `Verified Steps`, validity, and pending adjudication.

## Boundaries

- Platform rule cited by the package: `S<=50 AND (T>2400 OR V>=50)`.
- Internal strict target: `S<50 AND T>2400 AND V>=50`.
- 3/3 are observations, not a guarantee; the package is synthetic and cannot be
  submitted as real Q4 work while the AI/synthetic rule is unresolved.
