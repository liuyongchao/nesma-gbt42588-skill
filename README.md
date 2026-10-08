# NESMA 功能规模测量技能

按 **GB/T 42588—2023《系统与软件工程 功能规模测量 NESMA 方法》**，把需求材料转成有边界、有依据、可复算的功能点清单。一个 `nesma-gbt42588` 技能入口，内部按任务读取 **14 张能力卡**，附确定性计算器、计数模板和来源问题清单。

这是依据用户提供的标准扫描件提炼的**限定范围辅助技能（试用草稿）**。仓库未包含原标准 PDF、扫描图或 OCR 全文。知识提炼使用 [cangjie-skill](https://github.com/kangarooking/cangjie-skill)；运行本技能不依赖 cangjie。

## 通过 GitHub 链接安装

将下面这段话发给支持 `skill-installer` 的 Codex：

```text
请使用 skill-installer 安装这个 NESMA 技能：
https://github.com/liuyongchao/nesma-gbt42588-skill/tree/main/skills/nesma-gbt42588
```

这里的链接指向完整技能目录，安装路径为 `skills/nesma-gbt42588`。仓库主页是 [https://github.com/liuyongchao/nesma-gbt42588-skill](https://github.com/liuyongchao/nesma-gbt42588-skill)。安装器应获取该目录内的 `SKILL.md`、`references/`、`resources/` 和编译清单；只复制 `SKILL.md` 会缺少能力卡与计算资源。安装完成后，下一轮对话即可使用该技能。

也可以下载 [技能 ZIP 包](dist/nesma-gbt42588-2023-single.zip)，解压后将完整的 `nesma-gbt42588` 文件夹放到 Codex 的用户技能目录。默认位置为 `~/.codex/skills/`；设置了 `CODEX_HOME` 时使用其 `skills/` 子目录。

## 开始使用

安装后可在对话中明确调用技能，并附上实际需求、功能清单或测算表：

```text
用 $nesma-gbt42588 对附件需求做估算功能点分析。
先明确应用边界，再列 ILF/ELF/EI/EO/EQ、分值、来源依据和待确认项。
```

```text
用 $nesma-gbt42588 复核这份测算表，检查重复、缺失维护、EO/EQ 分类、
DET/RET/FTR 与默认复杂度，并列出逐项修订理由。
```

```text
用 $nesma-gbt42588 根据变更前后需求和基线，分别计算增强项目规模与
增强后的应用存量，一次性转换功能单列。
```

没有安装时，也可让代理读取 [技能入口](skills/nesma-gbt42588/SKILL.md) 及其完整配套目录，再按同样的方式提交任务。

## 包含的 14 项能力

| 能力 | 交付内容 |
|---|---|
| 范围与方法 | 用户、边界、计数对象、时点和分析方式 |
| 模型预估 | 概念模型 35/15 与规范化模型 25/10 公式 |
| 逻辑数据归组 | 实体独立性、逻辑文件、主子表与 RET |
| FPA 表归组 | 代码常量表、维护方与标准事务 |
| 共享数据 | 永久数据、传输、摘录及本地副本的归属 |
| 数据功能 | ILF/ELF 识别、排除项与维护检查 |
| 事务功能 | 基本过程、EI/EO/EQ 分类与去重 |
| 元素与复杂度 | DET/RET/FTR、复杂度矩阵、权重与默认 |
| FP 汇总 | 已确认功能的合计、待计项与可复算明细 |
| 开发与增强 | 新建、增强、重建项目及应用存量 |
| 不完整规格 | 套装软件、手册、菜单、屏幕和原型 |
| 特殊功能 | 帮助、菜单、消息、列表、工具及归档 |
| 计数复核 | 差异解释、遗漏、重复、默认和来源证据 |
| 增长归因 | 自主增长、范围变更及预测所需证据 |

## 确定性计算器

需要 **Python 3.8 或以上**，无第三方 Python 依赖。计算器只计算已经确认的输入，不从表名、按钮数或代码行数自动识别功能。

把下列内容保存为 `input.json`：

```json
{"operation":"indicative","model":"conceptual","ilf":2,"elf":1}
```

在仓库根目录运行：

```bash
python skills/nesma-gbt42588/resources/nesma_calc.py input.json --output result.json
```

此例输出 **85 FP**。还支持 `complexity`、`aggregate`、`development`、`enhancement`。接口见 [计算器说明](skills/nesma-gbt42588/resources/calculator-guide.md) 与 [JSON 示例](skills/nesma-gbt42588/resources/calculator-examples.json)。未知参数使用 `null` 或省略，不用 `0` 代替；详细分析采用默认复杂度时必须显式允许。

## 文档与测试

- [标准精华提炼](DIGEST.md)：按标准结构解释判断规则和操作方法。
- [术语词典](GLOSSARY.md)：统一计数用语。
- [测试报告](TEST_RESULTS.md)：28 个代表任务、4 个修订后集成案例、56 个触发用例和 216 个计算器测试的结果与局限。
- [计数记录模板](skills/nesma-gbt42588/resources/measurement-template.json)：测量范围、功能、默认依据、来源和待核查项。
- [六组来源待核查问题](skills/nesma-gbt42588/resources/source-issues.md)：遇到原文歧义时保留证据和执行边界。
- [触发评测用例](test-prompts.json) 与 [公开测试摘要](audit/test-summary.json)：后续验证的参考。

所有技能运行文件及 ZIP 内容与已测试的交付版本一致；公开整理只调整了仓库说明和测试摘要。[编译清单](skills/nesma-gbt42588/BUILD_MANIFEST.json) 保存各运行文件哈希。原始候选表、扫描核查工作稿和批处理日志未在本仓库发布；来源问题资源中的候选编号及工作稿文件名是编制时的审计标识，执行边界已写在同一资源中。

本技能保留 NR01–NR06，不把原文争议自动解释为确定规则。有待计项时只报已确认小计；仅涉及完整性条文解释时，可给明确范围的合计并保留复核事项。它不提供统一工时率、单价、通用增长系数或正式符合性认证。
