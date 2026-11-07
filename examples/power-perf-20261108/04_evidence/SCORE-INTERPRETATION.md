# 业务分 ≠ 豆包评测分

Run 02 的表里：

- `62.88 / C / 5`、`97 / A / 1` 是**被考核单位的业务分**；
- 不是豆包的 20 条 rubric 得分；
- 当前豆包评测分是 `null`，因为提交 schema 无效，grader 不能运行。

## 严格口径下哪些会挂

| 项 | 问题 | 影响 |
|---|---|---|
| C01–C06 | `final_decisions.csv` / `indicator_results.csv` 没有 `snapshot`；R0/R1/RB 缺失 | 中间视图无法验证 |
| C11–C13 | 下游勾稽/等级/排名对不上；格式异常 | 失分 |
| C16 | 旧意见 4/8 驳回 vs 参考 8/8 | 失分 |
| C17 | 补证成本 1 vs 参考 7 | 失分 |
| C18 | 工作簿公式 `NOT_RUN` | 失分 |
| C19 | schema/交付清单不一致 | 失分 |
| C20 | `self_check` 声称 PASS，但公式未跑 | 过度声明 |

所以：

```text
业务分看起来 88–100
不等于豆包评测分高
```

严格评分不是 90+；当前是 `INVALID_SCHEMA / SCORE_NULL`。  
要得到合法分数，先过 schema preflight：
1. 所有 required CSV 必须有 `snapshot`；
2. R0/R1/R2/RB 四套产物必须存在；
3. 数字列/枚举/HOLD 必须符合 schema；
4. 工作簿公式和 self_check 必须一致；
5. 然后才跑 grader。

不能拿业务分直接当模型分。
