# NESMA 确定性计算器

`nesma_calc.py` 只按已给定事实执行 GB/T 42588-2023 的矩阵、权重和公式。它不会从功能名称推断类别，不会判断数据组、基本过程、DET/RET/FTR 的语义正确性，也不会证明资料完整或计数符合标准。条目 ID 唯一仅防止相同 ID 重复，不能代替语义去重。

## 运行

需要 Python 3.8 或更高版本，无第三方依赖。先把一个请求对象保存为 UTF-8 JSON，再运行：

```text
python nesma_calc.py input.json
python nesma_calc.py input.json --output result.json
```

标准输出始终为 JSON。`--output` 只在成功处理请求时写入；不得指向输入文件或程序本身（也检查同一文件的硬链接）。父目录须已存在。路径由运行者明确提供；程序不联网、不调用外部命令。已有结果文件可被明确的 `--output` 替换，因此为每轮结果选择独立文件名。

字段名称、类别和枚举值区分大小写。额外字段、重复 JSON 键、布尔值冒充整数、负数、小数、数字字符串及 NaN/Infinity 均拒绝。数量/FP 均为非负整数，DET/RET 必须为正整数，FTR 可以为 0；不舍入、不把缺失自动当零。

## 状态与边界

以下状态是本计算器的交互约定，不是国标新增术语。

| status | 含义 | 退出码 |
|---|---|---:|
| calculated | 所请求算术有完整的给定输入，或明确采用估算方法/帮助专门规则 | 0 |
| calculated_with_defaults | 详细输入缺元素，调用者显式允许附录 B 默认值 | 0 |
| partial | 部分计算已确定，其他所需事实缺失或待核查 | 0 |
| needs_input | 合法请求缺计数事实；不产生未知部分的分值 | 0 |
| needs_review | 该部分存在来源解释问题或调用者标为待核查 | 0 |
| error | 请求结构、数值、路径或 JSON 错误 | 2 |

退出码 0 不表示已完成测量，自动流程必须同时检查 `status`、缺项、`unresolved_ids`，不能只检查进程成功。`error` 包含 `error.code`、`message`，字段错误还包含 `path`。程序从不以 0 FP 替代未知项。

## 1. 预估 indicative

概念模型使用逻辑文件数量：

```json
{"operation":"indicative","model":"conceptual","ilf":2,"elf":1}
```

输出 `total_fp:85`，公式为 35×ILF+15×ELF。原文式(1)的外部文件变量写 CEIF，此处用类别名称 ELF。

规范化模型使用维护/引用的实体类型数量，不能代入先归组后的普通逻辑文件数：

```json
{"operation":"indicative","model":"normalized","netm":3,"nete":2}
```

输出 `total_fp:95`，公式为 25×NETM+10×NETE。两个模型的字段不可混用。计数可以省略或为 `null`，此时返回 `needs_input`；模型必须已选定。输入前完成 5.2.1 的 FPA 表归组与维护方判断。

## 2. 复杂度 complexity

`method` 必须为 `detailed` 或 `estimated`，`type` 必须为 ILF、ELF、EI、EO、EQ 之一。

```json
{"operation":"complexity","method":"detailed","type":"EO","det":20,"ftr":1}
```

输出中复杂度和 `unit_fp:5`。ILF/ELF 使用 `ret`；EI/EO/EQ 使用 `ftr`。不得同时传入错误的另一轴，即使其值为 `null`。元素可省略或为 `null`，但已给定元素仍严格校验。

详细分析缺任一所需元素时，默认返回 `needs_input`。只有 `allow_defaults:true` 才依附录 B 取数据功能低、事务功能中，并输出 `calculated_with_defaults`、`defaulted:true` 和缺失字段。这不意味着详细元素已全部核验。

估算分析固定采用数据低、事务中，不需要元素；若额外给定元素，仍校验其类型和范围，但它们不改变估算权重，输出 `basis` 明示估算方式。估算方法本身不是“详细参数未知默认”。

`special` 默认 `normal`；特殊情况如下：

- `help`：只允许 EQ，同一种帮助已先按 6.13 去重。详细低（3 FP），估算中（4 FP），使用帮助专门规则，不套普通矩阵。
- `fpa_standard_transaction`：只允许 EI/EO/EQ。详细分析返回 `needs_review`、`review_ids:["NR04"]`；即使给定普通 FTR 或允许默认，也不替换 6.20 中未核清的特殊轴。估算分析则明确采用该方法的事务中复杂度。该标志必须由语义识别阶段传入，计算器无法自行识别被错误标为普通事务的 FPA 标准事务。

系统消息、附录 D 明细、边界和其他来源疑点须在调用前识别。不要先擅自选定 DET 再让矩阵的正确算术掩盖来源争议；汇总时将受影响条目标为 `needs_review`。

## 3. 汇总 aggregate

```json
{"operation":"aggregate","method":"estimated","items":[
  {"id":"customer-files","type":"ILF","count":2},
  {"id":"employee","type":"ELF","count":1},
  {"id":"inputs","type":"EI","count":4},
  {"id":"outputs","type":"EO","count":2},
  {"id":"queries","type":"EQ","count":3}
]}
```

输出 `total_fp:57`，每项有 `unit_fp` 和 `fp`。推荐一个逻辑功能一个 ID、`count:1`；确认同类同复杂度且已去重时可合并数量。ID 必须唯一，`count` 必填且可为 0；空清单算术结果为 0，但不代表程序验证了确实没有功能。

详细条目允许两种互斥输入：① `det` 与 `ret`/`ftr`；②已经有外部依据的 `complexity:"low"|"medium"|"high"`。后者只执行赋值，`basis` 会说明证据未被程序核验。显式复杂度不能同时传任何元素字段；估算方法不能传显式复杂度。帮助由特殊规则决定，不能同时传显式复杂度。详细 FPA 标准事务即使传显式复杂度仍待核查。

`allow_defaults` 在请求顶层统一控制普通条目的缺项默认，缺省为 false。条目 `state` 默认 `ready`，也可为 `needs_input` 或 `needs_review`；后两者必须给非空 `reason`。类别尚未确定可使用 `type:null`，但仅允许处于后两种状态，且不能夹带复杂度、元素或特殊规则字段。

有未解决条目时，仅输出 `known_subtotal_fp` 和 `unresolved_ids`，**不输出 `total_fp`**；已确定和待核查条目同时保留。部分小计包含已明确许可的默认值时，每一行仍保留 `defaulted` 和 `missing`，复核时逐项检查。零数量且状态未解决的行仍保留未解决状态，程序不代替调用者删除问题。

## 4. 增强 enhancement

```json
{"operation":"enhancement","baseline":200,"add":30,"deleted":10,
 "changed_before":20,"changed_after":25,"conversion":8}
```

结果为 `project_core_fp:65`、`project_fp:73`、`application_fp:225`、`net_application_change_fp:25`。

- 项目核心规模 = ADD+DEL+CHGA；项目总规模再加必要的一次性转换功能。
- 应用存量 = 基线+ADD−DEL+CHGA−CHGB；不含一次性转换。
- 输入均已是 FP；未改而被事务引用的既有文件不能自动塞入 ADD/CHGA。
- 每个数值可省略或为 `null`。缺 CHGB 或基线仍可给已确定项目结果，但没有 `application_fp`。缺转换量仍可给核心项目结果，但没有完整 `project_fp`。确认无转换必须显式写 0。
- 结果为负应用规模时返回错误，提示核对基线与变更分区。程序不检查删除/修改项是否重叠或跨边界，须由人工/能力卡审查。

## 5. 开发 development

```json
{"operation":"development","new_application":120,"conversion":8,"other_application_changes":15}
```

输出 `application_fp:120`、`project_fp:143`。三个输入分别是新应用规模、必要的一次性转换功能、项目内对其他应用的变更功能规模；均已是 FP。无某一项目范围应明确写 0，缺失不默认为 0。其他受影响应用的新存量需分别按其边界计算，不被此操作求出。完整重建仅在 5.6.5 的前提成立时使用开发路径。

## 来源与已知限制

来源是用户提供的 GB/T 42588-2023 扫描 PDF（SHA256 `52916F13A5383FA6D3C1171BF4D341FCEE1ED889980AD95347954325F801630B`），印刷页码 = PDF 页码 − 4。公式(1)(2)见印刷10页/PDF14，应用增强式(3)见13页/PDF17，项目增强式(4)见16页/PDF20；开发见15页/PDF19；矩阵/权重见规范性附录 B，51–54页/PDF55–58。帮助见 6.13。计算器实现时直接核对了这些图像及既有来源审计。

EO 与 EQ 均采用此版 NESMA 的 DET 1–5/6–19/≥20、FTR 0–1/2–3/≥4 矩阵，不套用其他方法的阈值记忆。全部输出保留 `scope`；数值测试仅证明给定测试输入的计算、边界处理与接口行为，不证明功能识别、元素计数或整个技能在真实项目中正确。
