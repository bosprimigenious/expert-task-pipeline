# 平台字段组织稿（内部原型；禁止冒充合规Q4提交物）
本包为AI生成的模拟研究案例。已读平台规则禁止AI出题/虚构工作场景；只有获准的使用方式与真实业务来源才能解除相应阻塞。这里提供完整字段方便内部研发与专家对照，不表示可以直接提交。

## 分类字段
- 任务名称：某地市供电公司2025年度业绩核定、红线责任与申诉追溯复核。
- 任务类型：数据、财务与业务运营。
- 任务形式：单轮，7包一次给齐；R0/R1/R2/RB为历史视图，不是隐式多轮。
- L1行业：能源、公用事业与环保（依据已读分类）。
- L2行业：公用事业（依据已读分类）；“电力供应”可作业务描述，不擅作平台枚举。
- L1职业：绩效考核归口对应的人力资源类候选，完整职业树未取得，待按实际下拉确认。
- L2职业：绩效考核专责/绩效管理类候选，待实际树确认。

## 题目-文字
# 某地市供电公司年度业绩核定、红线责任与申诉追溯复核

**内部研发演练题；所有企业、业务记录和制度均为合成材料，不是真实供电企业文件。**

## 业务背景与角色
澄川市供电公司（模拟）人力资源部承担绩效考核归口职责。公司下辖8家被考核单位；经营数据来自计量、财务、营销与调度等台账。2025年度初评后，陆续收到计量撤回与恢复、银行对账、配网职责交接更正、责任决定及申诉材料。已有工作表和部门意见不能直接作为终评依据。

你是本次考核复核专责。请为考核委员会形成可直接审阅的核定底表、责任与等级裁决、三次审阅时点的变化说明，以及尚不能定级单位的补证安排。结果仅供审核决策，不能声称已经发文、付款、执行处分或取得尚缺的证据。

考核年度为2025年1—12月；不是2026全年预测。本题采用已经结束的业务年度，避免在2026年11月使用尚未发生的12月实绩。所有时刻为北京时间（+08:00）。

## 一、单轮资料合同
A00—A06七个zip在开始时一次提供。解压后保留同名目录。全部文件均可见，无隐藏阶段释放、外部账号、生产系统或额外口头补充。网络查询不能替代题内模拟制度。允许Python、SQL、电子表格和批处理；不要求交付软件系统。

依据review_contract.json分别重建R0（2026-01-12 17:00）、R1（2026-01-26 17:00）、R2（2026-02-09 17:00）的当时可知结果。另生成RB，对R0进行独立历史回放。RB的业务结果应与R0一致，不能使用R1/R2后来获知的信息改写原判断。四个视图都需实际交付，不是四个独立题目。

## 二、业务任务
1. 核验七包及输入清单，选择各截点有效记录，保留排除、撤回和规范化记录；按公开的历史职责安排将月度计量和事故归到正确单位。
2. 重建K1综合线损、K2供电可靠、K3电费回收、K4客户投诉四类指标。依据原始分子分母计算，分别报告计算值、扣分、适用性与可判定状态。完整覆盖8家单位及全部适用月份。
3. 对12起事故分别审查正式文书、权限、送达、生效、责任类型和事件时点归口。输出设备责任、运行责任、扣分、降级和等级上限。尚未有效裁决的事项只能保留相应未决，不能补造责任。
4. 处理6项申诉，说明已成立、不成立、待处理或当时尚未提出。申诉请求、整改完成和正式责任撤销不能混同。
5. 为每一视图计算8家单位的指标扣分、事故扣分、已知项暂计分、正式分数、原始等级、降级、等级上限、最终等级和排名。若仍有影响结果的未决项目，按P-04处理，不能以0分、满分替代未知。
6. 审核A06中的旧工作簿和8条旧意见，给出定位、问题、修复和复核证据。比较R0→R1、R1→R2的全部规定字段，明确变化与保持不变的对象。
7. 按review_plan_contract.json提出满足覆盖、前置、互斥和预算约束的最低成本补证复核计划。计划不等于补证已完成，不得据此改变R2未决事实。

## 三、交付
提交一个results.zip，内部至少含：
- Power_Performance_Review.xlsx：首表Review Summary，另外保留Monthly Inputs、Indicator Model、Case Decisions、Appeal Decisions、Change Log、Legacy Audit、Review Plan、Sources。可以增加工作表，不使用宏、外部工作簿链接、隐藏计算区。原始选择与业务裁决可作为输入，但月度到指标、指标到总分、分数到等级必须保留可追踪公式，不只贴最终数值。
- selected_records.csv、exception_log.csv、organization_mapping.csv、monthly_kpis.csv、indicator_results.csv、event_assessment.csv、appeal_decisions.csv、final_decisions.csv、change_impact.csv、legacy_audit.csv、evidence_index.csv。
- review_plan.json、review_memo.md、self_check.json、manifest.json。

各文件列名、主键、枚举和容差见A06/output_schema.json；CSV用UTF-8（BOM可选）。额外诊断列允许，但不得删除规定列。结构化数值至少保留6位小数；业务分数在报告展示时保留2位，计算与定级前不先舍入。空值、0、NOT_APPLICABLE、UNDETERMINED、HOLD必须区分。

备忘录不超过2500个中文字符，写明时间口径、R2逐单位裁决、两次复核变化、未决与补证、旧工作簿问题、真实完成与未执行事项。引用必须能定位到source_id或文件及业务主键。格式与脚本不是最终业务目的。

## 四、完成标准
重新读取实际产物，检查主键与行数、数据勾稽、源文件引用、RB回放、多文件一致性和公式。self_check仅记录实际执行结果，无法检查的项目写NOT_RUN。实际缺证按规则保留，不临时猜测。无平台回执时不得自报正式模型分数、运行轮数或已通过验收。


## 题目-附件
- `A00_contract.zip`
- `A01_organization.zip`
- `A02_metering.zip`
- `A03_commercial.zip`
- `A04_incidents.zip`
- `A05_reviews.zip`
- `A06_delivery.zip`

## 考点/rubric
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


## 作答思路
# 专家合理作答路径（参考，不发给受测模型）
1. 先冻结7包哈希、年度、R0/R1/R2/RB。先检查record counts和字段单位，不直接信旧工作簿。
2. 使用P-01对各台账分族选择版本，记录剔除理由；选择后CANCELLED保持缺失。组织记录以assignment_id选版本再以业务日查询，F18的迟到追溯更正不能污染R0。
3. 构建月度单位指标事实。计量kWh规范化；K1缺值沿字段级传播；K2曝光独立；K3用余额替代、授权豁免减分母；K4跨三渠道按客户+事件去重。
4. 从月度聚合到年度。K1两个政策期分别计率/扣分，再按供电量权重合并；K2/K3/K4按公开档位向上取整。中间保留精度。
5. 阅读12份事故报告与新旧文书；过滤权限、known_at、送达、生效及文种。正式撤销不回退原决定；PENDING只影响该类责任的单位。依据事故日历史归口算角色，不套当前名称。
6. 逐项办理申诉，不将申诉申请、整改回执或补证计划当撤销。各截点独立重建，R0/RB相同。
7. 汇总已知扣分与暂计分。未决保留final_score空与HOLD；其余先按分数定原始等级、再降级、再封顶，并按最终等级/分数排名。
8. 审核旧稿和工作簿公式；列两次更新全部字段的变化与不变。枚举8动作的可行子集或采用任意正确求解器找最低成本，接受两个等价最优方案。
9. 构建公式工作簿，重读CSV，检查主键、字段、引用、RB、数值勾稽、敏感性与manifest。备忘录讲清业务结论及未执行事项，不暴露私有思维链。


## 标准答案-文字
# 标准答案文字｜仅供内部评审
状态：合成实例的程序参考解，未获真实行业专家审核；不是原v3的修复成绩。

## 关键裁决
| 单位 | 暂计分 | 正式分 | 最终等级 | 排名 | 未决 |
|---|---:|---:|---|---:|---|
|U1|67.87|67.87|D|7|无|
|U2|88.74|88.74|C|4|无|
|U3|98.00|98.00|A|2|无|
|U4|72.00|72.00|D|6|无|
|U5|90.00|未定|HOLD|不参排|C08|
|U6|88.00|88.00|D|5|无|
|U7|100.00|100.00|A|1|无|
|U8|98.00|98.00|A|2|无|

最终U5仍因C08待决而HOLD，暂计90不是正式90分。R2事故扣分应分别为：U1=20、U2=5、U3=0、U4=28、U5=10、U6=12、U7=0、U8=0。C03设备方4、运行方5；R1/R2运行方为U2，R0/RB按当时可知文书为U1。
R0、R1、R2、RB各输出8单位、32项指标、12起事故和6条申诉；RB语义与R0完全一致。最终指标采用原始精度，显示结果不用于反推扣分。
补证最低资源成本为7；A1+A2+A3与A1+A8均是等价最优解，必须接受，禁止用参考动作列表逐字限制合法解。

## 完整答案附件
reference_answer/含全部要求CSV/JSON、备忘录和Power_Performance_Review.xlsx。各数值依据逐表/逐行保存，不用“测试全过”替代业务标答。
旧稿8条意见均不成立，原因与工作簿位置在legacy_audit.csv。每项来源可从evidence_index回溯。

## 未决与限制
未获得目标豆包接口/产品会话；三次自测NOT_RUN。生成器与主求解器独立文件不自动等于独立专家审查；独立检查覆盖范围见04_evidence，不夸大审计。


## 标准答案-附件
`03_private_review/standard_answer_attachments.zip`，仅供评审，不发给作答模型。
