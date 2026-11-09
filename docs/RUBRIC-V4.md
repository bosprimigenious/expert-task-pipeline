# Rubric v4：19 criteria + 200 分制硬门 + 工作场景扣分

## 1. v3 基础（平台机器分，满分 95）
- 19 criteria，每个 5 分，内含 4 个 binary subcheck（共 76 项）。
- 计分：某 criterion 的 4 个 subcheck 全部通过才得 5 分；否则该 criterion 为 0（无部分分）。

## 2. 200 分制（内部难度尺）
- 40 criteria × 5 = 200；每 criterion 4/4 才得分。
- 硬门（任一不过，总分 0）：
  1. manifest 存在且 ≥15 文件（含 sha256）
  2. CHECKPOINT_S1..S5 全在
  3. PDF 引用（handoff/memo 含页码或 §）
  4. 19 个 v3 criterion 全过
- 平台映射：machine = score_200 / 2（≤95）+ C20 5。

## 3. v4 工作场景扣分（每项 −5）
在 v3 机器分上扣，用于把“看起来做完”降到真实水平：
- 缺 `validation_results.json`，或 validation 无 command/method/未按契约项校验
- 缺逐记录/逐窗口/逐事件文件（如 daily segment、instance continuity、session rows≠契约）
- memo/handoff 无 PDF 页码或 §
- fencing 缺关键写入证据；memo 缺精确窗口/不变量
- manifest <15 或 release_decision 过短/缺 regression evidence
- assessment 未写 trust/OIDC 修复

## 4. 参考解要求
- 参考解在 v3 76/76=95、v4=95；否则 rubric 无效。
- 参考解必须含逐记录账本、完整 memo、可复核 validation，不得用“见附件”占位。
