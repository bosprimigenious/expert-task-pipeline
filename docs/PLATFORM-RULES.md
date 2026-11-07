# Project rules used by this pipeline

These are the author-side rules this repository is designed around. They are
not a substitute for the current project FAQ or platform UI.

## Source

- Task must come from real work the author can cover.
- Synthetic examples are drafts, not submittable real work.
- Public data + a declared scenario may be allowed only if the project rules
  explicitly permit it.

## Test

- Specified product and mode must match the official evaluation.
- New session; only prompt + public attachments.
- Keep every run; no cherry-picking.
- Do not tell the model the score, step target or time target.
- No model self-score as the final score.

## Difficulty

- Score ≤ 50/100;
- AND verified steps ≥ 50 OR actual task time > 2400 s.
- Steps must use the project definition; tool calls and prose length are not
  substitutes.
- If no step log, use reliable timing.

## Submission

- 12 checks in `SUBMISSION-READINESS.md` must pass.
- Standard answer text + attachment are both required.
- Do not click “completed” until the pack is ready; the platform window is
  time-limited.
- A local PASS is not a platform PASS.
