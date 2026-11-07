# 评分和验证说明

## 不混淆四种结果
1. 独立参考核对162项：SQL窗口选择、Fraction核算、另写的状态期待与组合枚举。覆盖范围明确，不等于双专家审查。
2. 评分器76项：正确参考提交应通过；19个考点各4项。另有C20四项人工。
3. 负向测试14项：13种已知错误及空提交，确认评分器能识别；不是目标模型运行。
4. 豆包自测：三次均NOT_RUN，不存在新的模型分数、时间或步骤。

## 使用
先跑 schema preflight；不通过就停，不要送进 grader。
在作者目录根部运行（Python3.10+；xlsx 校验需要 openpyxl）：
```sh
python 03_private_review/tools/unpack_public.py --uploads 01_platform_upload --output public_unpacked
python 03_private_review/tools/schema_preflight.py --submission <submission> --public public_unpacked --output preflight.json
python 03_private_review/tools/reference_engine.py --input public_unpacked --output recalculated_csv
python 03_private_review/tools/verify_reference.py --public public_unpacked --reference 03_private_review/reference_answer --output verify.json
python 03_private_review/tools/score_with_preflight.py --submission <豆包产物解压目录> --reference 03_private_review/reference_answer --public public_unpacked --output run_grade.json
# 或先 preflight；INVALID_SCHEMA 时 grader 不运行
python 03_private_review/tools/test_grader_mutations.py --public public_unpacked --reference 03_private_review/reference_answer --output mutation.json
```
reference_engine重建数值CSV和review_plan，不宣称它会重建全部叙述/工作簿；已交付工作簿本身含可复算公式。工作簿生成使用artifact_tool，当前只实际验证该引擎；原生Excel重新计算NOT_RUN。

## 分数
结果包含machine_checks_passed、score_interval与每项状态，final_score默认null。参考提交机器核验76/76，对应已计算95分；C20未人工裁决，不能把区间上界100当已确认100分。存在同根因传播的条目需要仲裁，区间可能更宽。

## 修复记录
负向测试初次发现空提交的空集合比较使RB回放四项误通过。现已增加非空和键集覆盖要求，空提交不再通过任何机器项。保留initial报告与修后报告，不覆盖问题历史。这是评分器修复，不是为了压低豆包分数。

## 人工检查不可省略
原始证据语义、任意合法替代推理、工作簿全面敏感性和所有输入边界并非完全自动证明。不得用脚本PASS冒充上述审核。不得执行受测模型上传的任意脚本以判分；本比较器只读数据/工作簿结构与缓存。

## 版式公平性修复
最终打包前发现评分器依赖参考总表固定行列，已改为按公开字段表头定位，不限制标题行位置或列序，也不要求私有的100条公式阈值。按公开业务义务检查各行公式与交叉引用；已用表头移动/列序反转的解析级单元测试验证，不能把这两项称为原生Excel回算。
