# 按模型层次计算预估功能点

## R — 原文与定位

> 应谨慎使用这种预估功能点分析，因为可能出现高达50%的偏差。

GB/T 42588—2023，5.2.1.1，印刷第10页 / PDF第14页。两条公式及输入要求见5.2.1.1–5.2.1.3；原文算例见D.5，印刷第57页 / PDF第61页。

## I — 方法自述

预估是用数据模型推测整体功能规模的方法，不能从任意数据库表数直接计算。
概念模型中的计数对象是逻辑文件；第三范式模型中的计数对象是维护或引用的实体类型。
这两种对象处于不同抽象层级，必须使用各自公式，不能交换数量或系数。
先识别FPA表，把本应用维护和外部维护的两类分别归组，每类最多贡献一个计数对象。
预估系数隐含典型事务构成，得到的数值不是对实际事务逐项核实的证明。
模型维护关系不明时先补资料；小数、负数及只称“几张表”的数量不能静默接收。
交付要同时显示模型层次、数量来源、公式、预估性质和限制，留待更完整资料复测。

## A1 — 原文算例

类型：资料性附录算例，D.5，印刷第57页 / PDF第61页，案例c56。

原文已给定1个客户ILF、1个员工ELF。以该逻辑文件层次代入概念模型公式：`1×35 + 1×15 = 50 FP`，复现其预估数值。这里仅复现原文给定计数下的算术；附录D的事务分类、详细DET/FTR及增强范围另有缺口，不能以50 FP验证这些事项。原文没有提供实际项目结算或测量误差结果。

## A2 — 触发与邻近区分

- 只有早期数据模型：“先粗估功能点／indicative functional size from data model”。
- 对比两种公式：“35和15、25和10各用在哪／conceptual vs normalized model”。
- 检查表数误用：“有五张数据库表能算多少／table count to indicative FP”。

本卡用于已确定范围下的预估计算。选方法用 `nesma-scope-and-method`；FPA表判断用 `nesma-fpa-table-groups`；已识别五类功能并采用低/中权重时属于 `nesma-fp-aggregation` 的估算，不用本卡的35/15或25/10。

## E — 执行

**输入契约。** 必需：应用/项目边界及版本、`model_level`（`conceptual` 或 `normalized_3nf`）、模型条目及维护主体、FPA表判定与归组记录。数量单位均为“个”，要求非负整数；0表示经清单核实不存在，未知不能填0。概念模式提供CILF、CEIF；规范化模式提供NETM、NETE，不允许两套数量混用。数值若无条目清单，只能给“在所给数量成立时”的条件计算。

1. **确认模型层次。** 看模型实际内容，不只看文件名。概念逻辑数据组走概念公式；第三范式或相当详细程度的实体类型走规范化公式。只有物理表清单、无法确认层次时暂停公式选择。完成标准：模型层次与计数对象一一对应。
2. **先归并FPA表。** 按 `nesma-fpa-table-groups` 检查常量/文本/解码等实体，本应用维护的全部合为一个维护组，其他应用维护且被引用的全部合为一个引用组。不存在的组不计。因此所有FPA表在两种公式中均最多贡献两个对象；不要既逐表计数又增加组。完成标准：每个原始实体有归组或非FPA理由。
3. **登记公式专属数量。**

   | 模型 | 变量及含义 | 公式 |
   |---|---|---|
   | 概念 | CILF：内部逻辑文件数；CEIF：外部逻辑文件数（保留公式原变量名，类别通常写ELF） | `IFP = 35×CILF + 15×CEIF` |
   | 第三范式/相当层次 | NETM：本应用维护的实体类型数；NETE：引用、由其他应用维护的实体类型数 | `IFP = 25×NETM + 10×NETE` |

   规范化分支的普通实体数量不能先压缩为概念逻辑文件数量后继续套25/10；概念分支也不能把物理表数直接填入CILF/CEIF。完成标准：每个计入对象有名称、维护方、证据和对应变量。
4. **计算并复算。** 分别列两个乘积再相加，单位FP；输入是整数且系数整数，不做四舍五入。资源 `nesma_calc.py` 可执行已确认数量的确定性计算，配套说明为 `calculator-guide.md`。实现接口是 `python nesma_calc.py input.json [--output result.json]`；概念模型输入如 `{"operation":"indicative","model":"conceptual","ilf":2,"elf":1}`，规范化模型输入如 `{"operation":"indicative","model":"normalized","netm":3,"nete":2}`，读取输出 `total_fp`。这些JSON及字段名是本技能实现约定；脚本拒绝负数、布尔值、浮点或字符串冒充数量，不替代模型判断或FPA归组。完成标准：公式、两项小计与总计可独立复算且无重复对象。
5. **标明结果适用性。** 输出“预估功能规模”及标准版本，列缺失事务/属性细节。说明原文提示可能出现高达50%的偏差，不把它变成经统计验证的置信区间、保证误差上限或自动给出的预算上下限。明确何时获得事务资料后转估算/详细复测。完成标准：读者不会把预估与逐项详细计数混同。

**输出契约。** `scope / specification_version / model_level / object_register / fpa_grouping / variable_counts / formula / subtotals / indicative_fp / status / limitations / next_evidence`。`status`可表述为已确定输入的预估、条件计算或缺资料；这是交付约定。只提供已确定部分时注明不是完整总量。案例源可查资源 `source-cases.json`。

## B — 边界与判停

- 只有表数，或维护方/模型层次未知：不得选系数凑结果，先索取模型和责任说明。
- 两个公式是替代路径，不相加、不平均，也不取较高者作为“更稳妥”结论。
- 系数隐含的典型EI/EO/EQ不是实际功能清单；不能另把假定事务重复加到预估结果上。
- 复杂度矩阵和增强前后存量公式不在本卡内。项目若含增删改，先明确对象，不能将数据模型预估机械当作增强项目净变化。
- 附录D相关NR01/NR02保留在 `source-issues.md`；这里只使用其给定逻辑文件数复算，不借该案例自动裁决相似项目的范围或类别。

## 相关能力

- 依赖 `nesma-scope-and-method`：固定范围与选型。
- 组合 `nesma-fpa-table-groups`：正确处理两类FPA表。
- 对比 `nesma-fp-aggregation`：已有五类功能时采用估算/详细汇总。

## 配套资源

路径相对于本文件；脚本需先检查运行条件，不因附带而自动执行。

- [resources/calculator-examples.json](../../resources/calculator-examples.json)
- [resources/calculator-guide.md](../../resources/calculator-guide.md)
- [resources/nesma_calc.py](../../resources/nesma_calc.py)
- [resources/source-cases.json](../../resources/source-cases.json)
- [resources/source-issues.md](../../resources/source-issues.md)
