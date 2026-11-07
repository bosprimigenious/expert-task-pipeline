# 20条研究Rubric（候选，未获平台认可）

**总分100：20×5。采用5/2/0候选分档，不能冒称平台已确认。**

每条有4个核验单元：全部满足5分；至少2项但未全部满足2分；0—1项满足0分。C20由独立人工审阅。测试数量不是分数或有效步数。
对正确的等价实现、行序差异、合法最优解不能误罚；数值按公开schema容差。C11—C15部分采用跟随计算，避免上游同一错误机械重复扣分。若上游错误与下游失分同时出现，grader将相应条目标为ROOT_CAUSE_REVIEW_REQUIRED并输出分数区间，人工判断是否是独立义务错误；未完成仲裁不得报正式总分。
规则冻结后不针对模型输出调权重。字段缺失按局部义务判定，不把一个格式问题自动扩大为全卷0分。

## C01｜版本选择与撤回（5分）
业务义务：各族先过滤known_at与重复，再选最终版本；撤回不回退。依据：P-01 §1-2。
检查产物：selected_records.csv;exception_log.csv。
- C01-a：ENERGY selected identities and statuses。
- C01-b：BILL selected identities and statuses。
- C01-c：COMPLAINT selected identities and statuses。
- C01-d：OUTAGE selected identities and statuses。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C02｜历史归口（5分）
业务义务：按月初及当时可知职责重建馈线归口。依据：P-01 §3。
检查产物：organization_mapping.csv。
- C02-a：R0 assignment mapping。
- C02-b：R1 assignment mapping。
- C02-c：R2 assignment mapping。
- C02-d：RB assignment mapping。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C03｜K1双制度期核算（5分）
业务义务：分子分母及区间加权扣分；缺失不补零。依据：P-02-K1。
检查产物：indicator_results.csv;monthly_kpis.csv。
- C03-a：R0 K1 values。
- C03-b：R1 K1 values。
- C03-c：R2 K1 values。
- C03-d：RB K1 values。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C04｜K2曝光与扣分（5分）
业务义务：使用独立客户分钟分母与正确档位。依据：P-02-K2。
检查产物：indicator_results.csv;monthly_kpis.csv。
- C04-a：R0 K2 values。
- C04-b：R1 K2 values。
- C04-c：R2 K2 values。
- C04-d：RB K2 values。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C05｜K3账量和豁免（5分）
业务义务：余额替代、授权范围及分母调整。依据：P-02-K3。
检查产物：indicator_results.csv;monthly_kpis.csv。
- C05-a：R0 K3 values。
- C05-b：R1 K3 values。
- C05-c：R2 K3 values。
- C05-d：RB K3 values。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C06｜K4全渠道去重（5分）
业务义务：同客户同事件，保留独立客户投诉。依据：P-02-K4。
检查产物：indicator_results.csv;monthly_kpis.csv。
- C06-a：R0 K4 values。
- C06-b：R1 K4 values。
- C06-c：R2 K4 values。
- C06-d：RB K4 values。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C07｜事故身份覆盖（5分）
业务义务：12个物理事故，不按工单重复。依据：P-03 physical event register。
检查产物：event_assessment.csv。
- C07-a：R0 physical case identity。
- C07-b：R1 physical case identity。
- C07-c：R2 physical case identity。
- C07-d：RB physical case identity。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C08｜事故日双角色归口（5分）
业务义务：设备与运行责任分开、追溯更正正确。依据：P-01 §3; P-03。
检查产物：event_assessment.csv。
- C08-a：R0 case-day roles。
- C08-b：R1 case-day roles。
- C08-c：R2 case-day roles。
- C08-d：RB case-day roles。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C09｜权限送达与效力（5分）
业务义务：只用有权且已知/生效/送达的正式文书。依据：P-03 authority and effect。
检查产物：event_assessment.csv。
- C09-a：R0 legal effectiveness within stipulated policy。
- C09-b：R1 legal effectiveness within stipulated policy。
- C09-c：R2 legal effectiveness within stipulated policy。
- C09-d：RB legal effectiveness within stipulated policy。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C10｜申诉裁决（5分）
业务义务：六项按各截点分别判断，不把申请当撤销。依据：P-05。
检查产物：appeal_decisions.csv。
- C10-a：R0 appeal outcomes。
- C10-b：R1 appeal outcomes。
- C10-c：R2 appeal outcomes。
- C10-d：RB appeal outcomes。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C11｜角色处罚执行（5分）
业务义务：按已裁定类型正确执行4/5等责任与限制。依据：P-03 penalty table。
检查产物：event_assessment.csv。
- C11-a：R0 follows submitted valid-classification arithmetic。
- C11-b：R1 follows submitted valid-classification arithmetic。
- C11-c：R2 follows submitted valid-classification arithmetic。
- C11-d：RB follows submitted valid-classification arithmetic。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C12｜汇总分数勾稽（5分）
业务义务：自身明细到总表正确汇总、暂计分不伪装正式分。依据：P-04 §1-2。
检查产物：final_decisions.csv。
- C12-a：R0 downstream self-consistency rather than duplicate truth penalty。
- C12-b：R1 downstream self-consistency rather than duplicate truth penalty。
- C12-c：R2 downstream self-consistency rather than duplicate truth penalty。
- C12-d：RB downstream self-consistency rather than duplicate truth penalty。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C13｜等级未决与排名（5分）
业务义务：先降级后封顶，HOLD排除，名次按等级/分数。依据：P-04 §3-4。
检查产物：final_decisions.csv。
- C13-a：R0 grade/hold/rank applied to own evidence。
- C13-b：R1 grade/hold/rank applied to own evidence。
- C13-c：R2 grade/hold/rank applied to own evidence。
- C13-d：RB grade/hold/rank applied to own evidence。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C14｜历史回放不污染（5分）
业务义务：RB与R0的选择、指标、事件和裁决一致。依据：P-01 §1。
检查产物：R0/RB in selected_records,indicators,events,decisions。
- C14-a：RB replays R0: selected_records.csv。
- C14-b：RB replays R0: indicator_results.csv。
- C14-c：RB replays R0: event_assessment.csv。
- C14-d：RB replays R0: final_decisions.csv。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C15｜更新和不变集合（5分）
业务义务：两相邻视图11字段全部比较，保持项不遗漏。依据：P-05 change contract。
检查产物：change_impact.csv。
- C15-a：Complete 176 change/invariance keys。
- C15-b：before matches submitted decision snapshot。
- C15-c：after matches submitted decision snapshot。
- C15-d：Changed flags reflect semantic difference。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C16｜旧稿审核（5分）
业务义务：8项旧意见的结论、规则依据与定位。依据：A06 legacy claims; P-01..P-05。
检查产物：legacy_audit.csv。
- C16-a：Old-draft objections L01,L02。
- C16-b：Old-draft objections L03,L04。
- C16-c：Old-draft objections L05,L06。
- C16-d：Old-draft objections L07,L08。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C17｜补证计划（5分）
业务义务：覆盖、前置、互斥、预算和最优性。依据：A06 review_plan_contract。
检查产物：review_plan.json。
- C17-a：All four required gaps covered。
- C17-b：Prerequisites, exclusions, no duplicate actions。
- C17-c：True cost and budget。
- C17-d：Minimum cost and plan-only boundary。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C18｜工作簿模型（5分）
业务义务：可读、无危险特性、关键计算保留引用公式。依据：task.md delivery; P-04 §5。
检查产物：Power_Performance_Review.xlsx。
- C18-a：Readable workbook, required sheets。
- C18-b：No macros/external workbook links/hidden sheets。
- C18-c：Schema-located summary and indicator linkage formulas (layout independent)。
- C18-d：Cached values present and free of Excel errors。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C19｜交付一致性（5分）
业务义务：表结构、总表值、引用覆盖、哈希清单一致。依据：output_schema.json。
检查产物：all structured files + manifest.json。
- C19-a：Required CSV schemas and unique keys。
- C19-b：Workbook summary equals submitted CSV。
- C19-c：All unit/case decisions have traceable evidence entries。
- C19-d：Output manifest binds actual bytes without self-hash。
5分：四项均通过；2分：两项或三项通过；0分：零项或一项通过。存在共因混杂时暂停正式判分并仲裁。

## C20｜业务备忘录与证据审查（5分）
业务义务：人工检查事实支持、变化解释、未决边界及完成声明。依据：task.md memo and evidence obligations。
检查产物：review_memo.md;evidence_index.csv;self_check.json。
- C20-a：R2结论、HOLD与业务用途准确，不能只报程序通过。
- C20-b：关键结论的证据真实支持对应对象/期间/效力；能追溯原始记录。
- C20-c：两次变化、保持项和未决解释完整；不把未来信息写成过去已知。
- C20-d：补证/发布/处分未执行时如实声明；复核根因传播，接受合法替代证据。
5分：四项均满足；2分：至少两项满足；0分：仅零或一项满足。C20需人工，不由关键词命中替代事实审查。
