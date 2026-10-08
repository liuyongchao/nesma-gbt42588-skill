# 汇总估算与详细功能点并形成明细

## R — 原文

> “功能点计数是那些位于被统计对象（例如应用程序或项目）的边界之内的所有功能被分配的功能点数的总和。”

出处：GB/T 42588—2023，4.10，印刷9页／PDF13页；方式与权重依据5.2.2–5.2.3、表1及附录B.6（印刷11、54／PDF15、58）。

## I — 自述

先拿到已经识别并去重的功能清单，再汇总分值。
估算分析使用数据功能低、事务功能中，不需要假造逐功能复杂度证据。
详细分析按每项证据确定复杂度，不能只凭五类数量冒称详细结果。
同一数量乘不同权重代表不同方法和条件，必须保留方式标签。
分项与总计都用FP，功能项数不能直接当FP。
不确定项需要留在清单里，并与已确定小计分开。
算术正确只证明加总正确，不证明需求分类、边界及完整性已经正确。

## A1 — 原文算例

资料性算例：附录D.7，印刷57／PDF61，原文给定1ILF、1ELF、4EI、1EO、1EQ。估算使用7、5、4、5、4权重，`7+5+4×4+5+4=37FP`。这是复现给定分类下的算术；附录查询分类及明细缺口属于NR01/NR02，不把37FP作为相似项目的自动答案。

## A2 — 何时使用

- “功能清单齐了，帮我算总FP／aggregate function points”。
- “估算和详细怎么算、为什么不一样／estimated versus detailed size”。
- “有几个待定功能，怎样出可复算报告／partial count with unresolved items”。

与相邻能力的区分：只有概念或规范化数据模型时用 `nesma-indicative-sizing`；单功能元素和等级用 `nesma-elements-and-complexity`；增删改的项目/存量公式用 `nesma-development-and-enhancement`，不能拿本清单加总替代增强公式。

## E — 执行

**输入契约。** 需要目的、应用边界、分析方式、去重后的功能ID及类型、证据来源。数量为非负整数，合并行需说明所有功能具有同类同等级与相同适用规则；详细条目需给复杂度的证据，或DET/RET/FTR及专门标识。仅给总FP无法唯一反推明细，先索取底稿。

1. **冻结范围和方式。** 标明estimated或detailed；不得把预估35/15或25/10公式混入此表。检查ID唯一及功能跨入口去重；边界不清先处理范围。完成标准：每项都能追到一个应用和一份需求事实。
2. **逐项赋值。** estimated权重为ILF7、ELF5、EI4、EO5、EQ4。detailed使用 `nesma-elements-and-complexity` 的完整规则，五类低/中/高权重分别为ILF7/10/15、ELF5/7/10、EI3/4/6、EO4/5/7、EQ3/4/6；帮助详细EQ固定低。原文允许的缺参数默认要标为默认，不能写成已核实详细参数。功能本身缺条件、已知来源冲突不可借默认静默解决。
3. **分类汇总。** 每行 `FP=数量×该类该等级权重`；逐类小计，再总和。整数精确运算，不舍入。任何待补充或待复核项保留占位，不设零分，不从清单消失；输出“已确定小计+待计项”，不能用小计冒充完整总量。基于已披露默认的行另列默认依据，结果名称反映存在默认。
4. **交叉复算。** 可用 `resources/nesma_calc.py`：`python nesma_calc.py input.json --output result.json`。请求 `operation: aggregate`，method、allow_defaults及items；每item含唯一id、type、count，详细用complexity或det/ret/ftr二选一，特殊项传special。未决行传state为needs_input或needs_review并写reason；部分结果只有known_subtotal_fp，没有total_fp。详见 `resources/calculator-guide.md`。脚本不替代语义复核。
5. **生成可审阅报告。** 使用 `resources/measurement-template.json` 的字段组织方式，列“需求ID—功能ID—类别—数量—复杂度—证据/默认—权重—FP—状态—问题”。报告方式、时点、边界、资料版本、按类小计、总量或部分小计、待计项及影响。逐行加总、逐类加总和脚本输出须一致。

**输出契约。** 交付计数明细、汇总表、公式和未决项。采用本技能状态约定：可确定、按标准默认值估算、待补充输入、原文歧义待复核。明确是完整已识别范围还是部分范围；无法验证完整性时写明缺口，不宣称标准验收通过。

## B — 边界

- 不把复用率、工时、生产率、调整因子、费用或示例增长率乘到本功能规模里；费用换算需另有用户提供的依据。
- 估算数据低/事务中是明确方法口径，不能由表1灰色说明中的“预估”字样把两种方式合并。
- 不为凑齐总数补造功能或复杂度。NR01–NR06受影响行见 `resources/source-issues.md`，冲突不能被汇总掩盖。

相关能力：依赖 `nesma-elements-and-complexity`；与 `nesma-count-review` 组合检查完整性；与 `nesma-indicative-sizing` 对比选择方式。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/calculator-examples.json](../../resources/calculator-examples.json)
- [resources/calculator-guide.md](../../resources/calculator-guide.md)
- [resources/measurement-template.json](../../resources/measurement-template.json)
- [resources/nesma_calc.py](../../resources/nesma_calc.py)
- [resources/source-cases.json](../../resources/source-cases.json)
- [resources/source-issues.md](../../resources/source-issues.md)
