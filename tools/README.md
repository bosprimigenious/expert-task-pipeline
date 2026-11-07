# Tools

- `schema_preflight.py` — example-specific hard gate for the POWER-PERF schema.
- `score_with_preflight.py` — runs preflight, and only then the grader.
- `grader.py` — the 76-check example grader.

Usage from the repository root:

```bash
python3 tools/schema_preflight.py \
  --submission examples/power-perf-20261108/03_private_review/reference_answer \
  --public /path/to/public_unpacked \
  --output /tmp/preflight.json
```

`INVALID_SCHEMA` means no score. Do not “fix” a submission by adding snapshot
labels after the fact; rerun the model or mark the run invalid.
