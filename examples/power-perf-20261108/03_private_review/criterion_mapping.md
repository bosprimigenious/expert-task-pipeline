# 20条考点—80个核验单元映射

19×4=76项机器检查，C20对应4项人工检查。没有把76条当76分。所有ID均可定位到grader.py或人工表。

| 考点 | 核验ID | 类型 | 描述 | 产物 |
|---|---|---|---|---|
|C01|C01-a|AUTOMATED|ENERGY selected identities and statuses|selected_records.csv;exception_log.csv|
|C01|C01-b|AUTOMATED|BILL selected identities and statuses|selected_records.csv;exception_log.csv|
|C01|C01-c|AUTOMATED|COMPLAINT selected identities and statuses|selected_records.csv;exception_log.csv|
|C01|C01-d|AUTOMATED|OUTAGE selected identities and statuses|selected_records.csv;exception_log.csv|
|C02|C02-a|AUTOMATED|R0 assignment mapping|organization_mapping.csv|
|C03|C03-a|AUTOMATED|R0 K1 values|indicator_results.csv;monthly_kpis.csv|
|C04|C04-a|AUTOMATED|R0 K2 values|indicator_results.csv;monthly_kpis.csv|
|C05|C05-a|AUTOMATED|R0 K3 values|indicator_results.csv;monthly_kpis.csv|
|C06|C06-a|AUTOMATED|R0 K4 values|indicator_results.csv;monthly_kpis.csv|
|C07|C07-a|AUTOMATED|R0 physical case identity|event_assessment.csv|
|C08|C08-a|AUTOMATED|R0 case-day roles|event_assessment.csv|
|C09|C09-a|AUTOMATED|R0 legal effectiveness within stipulated policy|event_assessment.csv|
|C10|C10-a|AUTOMATED|R0 appeal outcomes|appeal_decisions.csv|
|C11|C11-a|AUTOMATED|R0 follows submitted valid-classification arithmetic|event_assessment.csv|
|C12|C12-a|AUTOMATED|R0 downstream self-consistency rather than duplicate truth penalty|final_decisions.csv|
|C13|C13-a|AUTOMATED|R0 grade/hold/rank applied to own evidence|final_decisions.csv|
|C02|C02-b|AUTOMATED|R1 assignment mapping|organization_mapping.csv|
|C03|C03-b|AUTOMATED|R1 K1 values|indicator_results.csv;monthly_kpis.csv|
|C04|C04-b|AUTOMATED|R1 K2 values|indicator_results.csv;monthly_kpis.csv|
|C05|C05-b|AUTOMATED|R1 K3 values|indicator_results.csv;monthly_kpis.csv|
|C06|C06-b|AUTOMATED|R1 K4 values|indicator_results.csv;monthly_kpis.csv|
|C07|C07-b|AUTOMATED|R1 physical case identity|event_assessment.csv|
|C08|C08-b|AUTOMATED|R1 case-day roles|event_assessment.csv|
|C09|C09-b|AUTOMATED|R1 legal effectiveness within stipulated policy|event_assessment.csv|
|C10|C10-b|AUTOMATED|R1 appeal outcomes|appeal_decisions.csv|
|C11|C11-b|AUTOMATED|R1 follows submitted valid-classification arithmetic|event_assessment.csv|
|C12|C12-b|AUTOMATED|R1 downstream self-consistency rather than duplicate truth penalty|final_decisions.csv|
|C13|C13-b|AUTOMATED|R1 grade/hold/rank applied to own evidence|final_decisions.csv|
|C02|C02-c|AUTOMATED|R2 assignment mapping|organization_mapping.csv|
|C03|C03-c|AUTOMATED|R2 K1 values|indicator_results.csv;monthly_kpis.csv|
|C04|C04-c|AUTOMATED|R2 K2 values|indicator_results.csv;monthly_kpis.csv|
|C05|C05-c|AUTOMATED|R2 K3 values|indicator_results.csv;monthly_kpis.csv|
|C06|C06-c|AUTOMATED|R2 K4 values|indicator_results.csv;monthly_kpis.csv|
|C07|C07-c|AUTOMATED|R2 physical case identity|event_assessment.csv|
|C08|C08-c|AUTOMATED|R2 case-day roles|event_assessment.csv|
|C09|C09-c|AUTOMATED|R2 legal effectiveness within stipulated policy|event_assessment.csv|
|C10|C10-c|AUTOMATED|R2 appeal outcomes|appeal_decisions.csv|
|C11|C11-c|AUTOMATED|R2 follows submitted valid-classification arithmetic|event_assessment.csv|
|C12|C12-c|AUTOMATED|R2 downstream self-consistency rather than duplicate truth penalty|final_decisions.csv|
|C13|C13-c|AUTOMATED|R2 grade/hold/rank applied to own evidence|final_decisions.csv|
|C02|C02-d|AUTOMATED|RB assignment mapping|organization_mapping.csv|
|C03|C03-d|AUTOMATED|RB K1 values|indicator_results.csv;monthly_kpis.csv|
|C04|C04-d|AUTOMATED|RB K2 values|indicator_results.csv;monthly_kpis.csv|
|C05|C05-d|AUTOMATED|RB K3 values|indicator_results.csv;monthly_kpis.csv|
|C06|C06-d|AUTOMATED|RB K4 values|indicator_results.csv;monthly_kpis.csv|
|C07|C07-d|AUTOMATED|RB physical case identity|event_assessment.csv|
|C08|C08-d|AUTOMATED|RB case-day roles|event_assessment.csv|
|C09|C09-d|AUTOMATED|RB legal effectiveness within stipulated policy|event_assessment.csv|
|C10|C10-d|AUTOMATED|RB appeal outcomes|appeal_decisions.csv|
|C11|C11-d|AUTOMATED|RB follows submitted valid-classification arithmetic|event_assessment.csv|
|C12|C12-d|AUTOMATED|RB downstream self-consistency rather than duplicate truth penalty|final_decisions.csv|
|C13|C13-d|AUTOMATED|RB grade/hold/rank applied to own evidence|final_decisions.csv|
|C14|C14-a|AUTOMATED|RB replays R0: selected_records.csv|R0/RB in selected_records,indicators,events,decisions|
|C14|C14-b|AUTOMATED|RB replays R0: indicator_results.csv|R0/RB in selected_records,indicators,events,decisions|
|C14|C14-c|AUTOMATED|RB replays R0: event_assessment.csv|R0/RB in selected_records,indicators,events,decisions|
|C14|C14-d|AUTOMATED|RB replays R0: final_decisions.csv|R0/RB in selected_records,indicators,events,decisions|
|C15|C15-a|AUTOMATED|Complete 176 change/invariance keys|change_impact.csv|
|C15|C15-b|AUTOMATED|before matches submitted decision snapshot|change_impact.csv|
|C15|C15-c|AUTOMATED|after matches submitted decision snapshot|change_impact.csv|
|C15|C15-d|AUTOMATED|Changed flags reflect semantic difference|change_impact.csv|
|C16|C16-a|AUTOMATED|Old-draft objections L01,L02|legacy_audit.csv|
|C16|C16-b|AUTOMATED|Old-draft objections L03,L04|legacy_audit.csv|
|C16|C16-c|AUTOMATED|Old-draft objections L05,L06|legacy_audit.csv|
|C16|C16-d|AUTOMATED|Old-draft objections L07,L08|legacy_audit.csv|
|C17|C17-a|AUTOMATED|All four required gaps covered|review_plan.json|
|C17|C17-b|AUTOMATED|Prerequisites, exclusions, no duplicate actions|review_plan.json|
|C17|C17-c|AUTOMATED|True cost and budget|review_plan.json|
|C17|C17-d|AUTOMATED|Minimum cost and plan-only boundary|review_plan.json|
|C18|C18-a|AUTOMATED|Readable workbook, required sheets|Power_Performance_Review.xlsx|
|C18|C18-b|AUTOMATED|No macros/external workbook links/hidden sheets|Power_Performance_Review.xlsx|
|C18|C18-c|AUTOMATED|Schema-located summary and indicator linkage formulas (layout independent)|Power_Performance_Review.xlsx|
|C18|C18-d|AUTOMATED|Cached values present and free of Excel errors|Power_Performance_Review.xlsx|
|C19|C19-a|AUTOMATED|Required CSV schemas and unique keys|all structured files + manifest.json|
|C19|C19-b|AUTOMATED|Workbook summary equals submitted CSV|all structured files + manifest.json|
|C19|C19-c|AUTOMATED|All unit/case decisions have traceable evidence entries|all structured files + manifest.json|
|C19|C19-d|AUTOMATED|Output manifest binds actual bytes without self-hash|all structured files + manifest.json|
|C20|C20-a|HUMAN|R2结论、HOLD与业务用途准确，不能只报程序通过|review_memo.md;evidence_index.csv;self_check.json|
|C20|C20-b|HUMAN|关键结论的证据真实支持对应对象/期间/效力；能追溯原始记录|review_memo.md;evidence_index.csv;self_check.json|
|C20|C20-c|HUMAN|两次变化、保持项和未决解释完整；不把未来信息写成过去已知|review_memo.md;evidence_index.csv;self_check.json|
|C20|C20-d|HUMAN|补证/发布/处分未执行时如实声明；复核根因传播，接受合法替代证据|review_memo.md;evidence_index.csv;self_check.json|
