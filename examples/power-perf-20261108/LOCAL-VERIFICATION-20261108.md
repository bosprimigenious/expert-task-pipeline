# POWER-PERF local verification (2026-11-08)

Source: `inbox/POWER-PERF-DELIVERABLE-20261107-ASCII.zip`
Expected SHA-256: `40d861a7fd6e35854437dd359ba1f6828e20cd484a5bcf33b9d08767a063d670`
Actual SHA-256:   `40d861a7fd6e35854437dd359ba1f6828e20cd484a5bcf33b9d08767a063d670`

## Author-side checks actually run here

| Check | Result |
|---|---|
| Outer zip test | no errors |
| Package `MANIFEST.sha256` | **71/71 OK** |
| 7 public zips: size + SHA-256 + CRC | **7/7 OK** |
| `unpack_public.py` safe extraction | 36 public files, no private-answer extraction |
| Independent `verify_reference.py` | **162/162 PASS** |
| Reference `grader.py` | **76/76 machine checks**, interval **95–100**, `final_score=null` |
| Mutation `test_grader_mutations.py` | **14/14 PASS** |
| `reference_engine.py` vs reference CSVs/JSON | **10/10 byte-identical** |
| Workbook verification JSON | 32 decision rows / 128 indicator rows match CSV; 2/2 sensitivity; native Excel **NOT_RUN** |
| Private names in public unpack | none found |
| Doubao self-test | **0/3, NOT_RUN** |

## Status

```text
AUTHOR_SIDE_VERIFIED
HUMAN_REVIEW = NOT_RUN
DOUBAO_SELF_TEST = 0 / 3
DIFFICULTY_VALIDATED = NO
PLATFORM_STATUS = BLOCKED_AI_SYNTHETIC
```

This is **not** a Q4 pass, not a platform acceptance, and not a model score.
The package is an explicitly synthetic internal research prototype. Do not
remove the synthetic label or present it as real work.

## What remains

1. Run 3 fresh single-round Doubao 2.1 Pro sessions with only
   `06_blind_test/task_prompt.md` + the 7 public zips.
2. Have C20 human review/adjudication.
3. Resolve real-material and AI-participation rules with the project owner.
4. If the package is kept as an internal power-domain gold example, keep it
   under this status until 1–3 are done.
