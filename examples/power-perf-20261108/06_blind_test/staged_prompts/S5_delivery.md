第 5 阶段：把前四阶段成果整理为最终交付，不再改变任何业务事实。

生成 results.zip，至少包含：
- Power_Performance_Review.xlsx（Review Summary、Monthly Inputs、Indicator Model、Case Decisions、Appeal Decisions、Change Log、Legacy Audit、Review Plan、Sources；核心计算保留公式）；
- selected_records.csv、exception_log.csv、organization_mapping.csv、monthly_kpis.csv、indicator_results.csv、event_assessment.csv、appeal_decisions.csv、final_decisions.csv、change_impact.csv、legacy_audit.csv、evidence_index.csv；
- review_plan.json、review_memo.md、self_check.json、manifest.json。

要求：
- 严格按 A06/output_schema 的列名、主键、枚举和容差；
- indicator_results 的状态用 DETERMINED/UNDETERMINED，不要用 OK；
- final_decisions 的数字列留空/用规定枚举，不要把 HOLD 写进数字列；
- self_check 只记录实际执行过的检查，未执行写 NOT_RUN；
- 回复实际文件清单、行数、自检结果和未执行事项。


schema 硬要求：
- `final_decisions.csv`、`indicator_results.csv` 必须有 `snapshot` 列；
- 必须包含 R0/R1/R2/RB 四套行，不能只交 R2；
- `indicator_results.status` 仅用 `DETERMINED` / `UNDETERMINED` / `NOT_APPLICABLE`；
- 数字列不得写 `HOLD` 或枚举；
- 先运行 schema_preflight，FAIL 就修，不要声称交付完成；
- `results.zip` 必须作为文件卡片发到对话；如果二进制不行，至少把 xlsx 和每个 CSV 作为文件卡片发出，不能只说保存在工作区。
