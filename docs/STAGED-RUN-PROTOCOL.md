# 分阶段盲测协议（S1–S5）

## 会话
- 每题只开一个豆包工作模式会话（2.1 Pro 高），S1–S5 复用。
- 仅上传 PUBLIC；不给 rubric/reference/grader。
- 每段 ≤4 个核心文件 + `CHECKPOINT_Sn.json`；禁止一次性丢整题。

## 每段输入
- 题面 + 当前段目标 + 逐字列契约（列名、行数、枚举值）。
- 明确“无法证明写 NOT_PROVEN/NOT_RUN；不得声称已执行生产变更”。

## 每段回收
- 优先真实文件卡/zip；下载不稳定时要求代码块（文件名+内容）并本地落盘。
- 回收后立即跑 v3/v4 评分并记录 failed subchecks。

## 环境故障（实测）
- 工作模式 `+` 菜单可能打不开：先点击 composer 左侧 plus（约 523,942），再找“上传文件或图片”。
- 标签页可能被重定向到别的会话：每次操作前校验 `location.href` 与目标 session。
- textarea 可写但不提交：焦点到 textarea，insertText 后用真实 Enter/发送按钮，确认为新消息再继续。

## 难度门槛
- `score ≤ 50` 且（`net_time > 2400s` 或 `verified_steps ≥ 50`）。
- 小数据题需追加 S6–S15 或全量大文件重跑；记录墙钟与步数，不能只报分数。
