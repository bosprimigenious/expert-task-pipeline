> **Post-download run:** 1 real Doubao run completed on 2026-11-08:
> 13:39, 42/76 machine checks, interval 49–54, C20 not run.
> **TIME_FAIL** (819s < 2400s); steps unverified. See
> `04_evidence/DOUBAO-RUN-01-REPORT.md`.

# POWER-PERF-T2 作者研发包

**状态：INTERNAL_RESEARCH_PACKAGE / HUMAN_REVIEW_PENDING / DOUBAO_NOT_RUN / PLATFORM_BLOCKED。**

任务：某地市供电公司2025年度业绩核定、红线责任与申诉追溯复核。保持任务2的电力绩效与责任认定方向，不是MERCURY物资履约工程。最终交付是工作簿、业务底表、裁决和备忘录，代码只是工具。

## 必须先知道
所有新业务数据与制度均为AI合成研究资料；用户提供的本期规则明确禁止AI出题和虚构工作场景。本包可做内部研发、自测和质量核对，**不能据此宣称合规Q4提交、质检通过或可结算**。人工改名或去掉标签不能改变来源。真实材料替换也不自动解决AI参与禁令，需按项目允许边界处理。

## 目录
- 01_platform_upload：7个公开输入zip和UPLOAD-CHECK.json，仅这些zip可用于内部豆包盲测。
- 02_platform_fields：完整/精简字段、单轮题面、真实材料清单、提交检查及规则冲突。
- 03_private_review：20条rubric、12个难点、参考解、标答附件、评分器、76+4映射、人工表及3次空白自测记录。
- 04_evidence：来源说明、研究依据、独立核对、工作簿核验、评分器反例、包装与扫描记录。

## 内部盲测
新建豆包会话，上传01目录7个zip，粘贴02/task_prompt.md。不要上传整个作者包、标答、rubric、困难机制或旧成绩。不追加“注意某个陷阱”。三次同版本同配置，保留所有结果。具体记录方式见run_templates/three_run_protocol.md。

## 已实际执行
独立SQL/Fraction等162项核对；正确参考提交76项机器检查；14个已知错误/空提交反例；工作簿32行决策与128行指标核对、2项输入敏感性。精确状态以04目录JSON为准。不是3次豆包，不代表行业专家完成审核。

## 未执行
目标模型实测、人工C20及共因仲裁、真实行业专家验收、原生Microsoft Excel全量回算、平台质检和结算。
评分器参考机器部分95/95，正式总分null；不可把区间上限100当已确认总分。不要把162/76测试数当有效轮数，也不要把本地程序秒数当模型时长。

## 冻结
MANIFEST.sha256列本作者目录中全部常规文件（不含自身）；输入zip另有逐包hash。保留历史失败反例报告，不改写过去结果。完整作者zip含私有答案，不能整体发给受测模型。
