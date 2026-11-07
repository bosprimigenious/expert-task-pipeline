# Mode and staging decision

## What was run

- UI: 对话
- Mode: 专家
- Input: all 48 unpacked public files at once
- Prompt: one single-round task prompt
- Result: 13:39, 42/76, interval 49–54, TIME_FAIL

This matches the POWER-PERF package: **single-round, R0/R1/R2/RB snapshots**,
seven packs at once. It is not the old MERCURY M0–M6 staged engineering task.

## M0–M6 is a different task

The old MERCURY task used S0 + M1–M6 stage packs, `submit_stage.py`, and a
staged upload server. The current power performance task has no M0–M6 stages;
it has business snapshots R0/R1/R2/RB. Sending it in M0–M6 stages would:

- change the task form and the seven-column contract;
- make the 20-item rubric and 76 checks incomparable;
- add artificial waiting, not real difficulty.

Do not mix the two.

## 工作 vs 专家

- 对话 + 专家: reasoning/chat surface; this is what run 01 used.
- 工作: agent workspace surface; may be better for file generation and long
  artifact workflows, but it is a different product surface, not a staged task.
- The project rule cited so far says “豆包 2.1 Pro, reasoning unrestricted”; it
  does not establish 工作 as the official mode. Use the mode the project owner
  confirms.
- If testing 工作, keep the same single-round prompt and same 7 packs; only
  change the surface. Do not also switch to M0–M6 staging, or the comparison is
  confounded.

## Why 13:39 is short

Not a mode bug. The task is scriptable and the model solved the main R2 table
quickly. Staging would only add turns/waiting; it would not make the business
judgment harder.

## Next experiment

1. A/B one **工作** run with the same single-round prompt and inputs.
2. If still <2400 s, revise the task: add irreducible reconciliation, authority
   conflicts, and required intermediate deliverables; do not fake time.
3. Only if the platform explicitly allows staged tasks, design a separate
   M0–M6 staged task and a separate rubric.
