# 能力索引（完整版）

| capability_id | 标题 | 重要度 | 意图 | 关键词 | 能力卡 |
|---|---|---|---|---|---|
| cap.gbt42588-2023.scope-and-method | 确定范围、边界、测量时点与分析方式 | critical | 确定应用或项目测量范围；选择功能点分析方式；澄清子系统边界与测量时点 | 范围、边界、用户、初期、中期、末期、scope、application boundary、indicative、estimated、detailed、lifecycle | capabilities/nesma-scope-and-method.md |
| cap.gbt42588-2023.indicative-sizing | 按模型层次计算预估功能点 | high | 用早期模型预估功能规模；区分两种预估公式；复核预估数量对象与FPA归组 | 预估、概念模型、第三范式、35、15、25、10、indicative、conceptual、normalized model、IFP | capabilities/nesma-indicative-sizing.md |
| cap.gbt42588-2023.logical-data-groups | 把规范化实体归组为逻辑文件 | high | 从规范化模型识别逻辑文件；处理主子表与键键实体；判断实体独立性和RET | 实体归组、第三范式、键键实体、逻辑文件、强制、可选、RET、normalized ER model、junction entity、mandatory、optional | capabilities/nesma-logical-data-groups.md |
| cap.gbt42588-2023.fpa-table-groups | 识别和归组FPA表及其标准事务 | high | 识别FPA代码常量表；按维护主体归组FPA表；计数FPA标准事务并标记复杂度疑点 | FPA表、码表、常量、字典、标准事务、FPA table、code table、maintenance owner、NR04 | capabilities/nesma-fpa-table-groups.md |
| cap.gbt42588-2023.shared-data | 判定跨应用共享、摘录和一次性传输 | high | 分类跨应用共享数据；区别一次性传输与永久外部数据；判断摘录和本地副本的ILF/ELF/EI/EO | 共享数据、同步、摘录、副本、一次性文件、shared data、persistent extract、one-time transfer、ILF、ELF | capabilities/nesma-shared-data.md |
| cap.gbt42588-2023.data-functions | 识别ILF/ELF与不计数的数据对象 | critical | 识别ILF和ELF；排除技术性数据对象；排查缺失维护功能及数据去重 | 内部逻辑文件、外部逻辑文件、维护、永久性、历史文件、ILF、ELF、data function、maintenance、technical file | capabilities/nesma-data-functions.md |
| cap.gbt42588-2023.transaction-functions | 识别基本过程并区分EI、EO、EQ | critical | 划分基本过程；区分EI/EO/EQ；去重多屏多介质事务；拆分逻辑布局与组合输出 | 基本过程、事务、输入、输出、查询、独特性、EI、EO、EQ、elementary process、logical layout、unique transaction | capabilities/nesma-transaction-functions.md |
| cap.gbt42588-2023.elements-and-complexity | 计数DET/RET/FTR、查复杂度并赋值 | critical | 计数DET、RET和FTR；判断功能复杂度并赋权；处理复杂度缺项与默认值 | DET、RET、FTR、复杂度、complexity matrix、weights、missing counts、默认复杂度 | capabilities/nesma-elements-and-complexity.md |
| cap.gbt42588-2023.fp-aggregation | 汇总估算与详细功能点并形成明细 | critical | 汇总已识别功能清单；比较估算与详细结果；交付可复算的计数明细及部分结果 | 总功能点、汇总、aggregate function points、estimated、detailed、partial count、计数明细 | capabilities/nesma-fp-aggregation.md |
| cap.gbt42588-2023.development-and-enhancement | 识别变更并计算开发、增强、重建规模 | critical | 识别功能修改与连带影响；计算增强项目及上线后应用规模；计算新建或整体重建项目规模 | 增强、增删改、DET修改、enhancement、development、conversion、redevelopment、CHGA、CHGB、AFPA | capabilities/nesma-development-and-enhancement.md |
| cap.gbt42588-2023.incomplete-specifications | 从套装、界面和原型材料恢复可计数需求 | high | 从手册截图菜单恢复功能清单；区分套装软件的有效规模与完整规模；判断原型可支持的测量程度 | 套装软件、屏幕、原型、不完整规格、package software、screens、menus、prototype、missing specifications | capabilities/nesma-incomplete-specifications.md |
| cap.gbt42588-2023.special-functions | 处理帮助、菜单、消息、列表、工具等特殊功能 | high | 判断帮助菜单登录等特殊对象是否计数；区分消息DET与独立报告；处理工具复用列表图形及清除归档 | 帮助、菜单、消息、列表、登录、报表工具、归档、help、menu、message、report generator、selection list、purge | capabilities/nesma-special-functions.md |
| cap.gbt42588-2023.count-review | 审查重复、遗漏、默认值与证据链 | critical | 审核功能点清单与计数依据；解释两份测算的差异；检查缺失维护输出和默认值 | 复核、审计、重复、遗漏、证据链、audit、reconcile counts、missing maintenance、default review | capabilities/nesma-count-review.md |
| cap.gbt42588-2023.growth-classification | 区分需求细化与范围变更并记录增长依据 | medium | 区分自主增长与范围变更；解释生命周期规模变化；记录组织增长预测所需证据 | 自主增长、需求细化、范围变更、增长率、autonomous growth、scope change、lifecycle size、growth factor | capabilities/nesma-growth-classification.md |
