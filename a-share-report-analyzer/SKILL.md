---
name: a-share-report-analyzer
description: "分析 A 股公司的经营质量、股东回报与情景估值，综合年报、公告、同行、市场预期和宏观传导生成中文研究报告；也支持持仓复核与组合初筛。针对金融、商品及其他子行业调整口径。"
---

# A-Share Report Analyzer

用可追溯的事实判断：能否理解企业、企业是否持续为普通股股东创造价值、价格是否留有容错空间。用户指定范围和格式优先。本 skill 也支持框架评审，此时无需虚构目标公司或执行公司研究流程。

## 选择模式

默认 `company_report`，无需用户持有该股票。用户要求持仓复核时用 `holding_report`，组合初筛时用 `portfolio_triage`，读取 `references/holding-portfolio-modes.md`；仅对重要问题深入完整公司研究。成本价不改变内在价值，默认隐去账户标识与绝对资产；本 skill 不执行交易或生成可执行订单。

纯港股、美股不套用 A 股特有数据要求；明确范围差异，只有其他研究能力实际可用时才建议转交。A/H 公司仍核对股份类别、汇率和实际总市值。

## 工作流

1. **准备数据**：确认代码、交易所、股份类别、币种、研究截止日与策略类型。读取 `references/phase-1-data-prep.md` 和 `references/data-source-strategy.md`。按 `references/evidence-packages.md` 核查公告、研报、宏观、交易结构与资金证据的重要性；按 `references/valuation-anchor-framework.md` 核查行业方法库。先形成业务理解与会计口径，再解读已采集的价格数据。
2. **判断企业质量**：读取 `references/phase-2-body-analysis.md`、`references/owner-economics.md`、`references/shareholder-friendliness.md`。用历史资本回报与每股增长、未来竞争结构、资本配置、财务生存能力形成判断。
3. **估值与持续验证**：读取 `references/phase-3-valuation-conclusion.md`、`references/market-liquidity-expectations.md`、`references/final-conclusion-logic.md`。核查市场环境、价格隐含预期与公司传导，再分开呈现估值情景、安全边际和历史估值位置，写明反证与跟踪条件。

每家公司均应用 `references/industry-overlay-principle.md`；按 `references/industry-research-checklist.md` 研究子行业。可用子代理时，将行业研究委派给专门子代理，再由主分析者核验和整合。多公司示例可分别委派行业证据收集，避免重复取数。对本 skill 的实质改版，可让独立子代理按新版完成一次样例前向验证。

银行、券商、保险分别读取 `references/sector-bank.md`、`sector-broker.md`、`sector-insurance.md`；其他公司读取 `sector-general-a-share.md`。金融业以普通股回报、资产负债、监管资本和可分配能力代替不适用的工业企业 ROCE/FCF，禁止强套。

商品价格、海外需求、外币收支或利率敏感性重大时，另读 `references/macro-policy-transmission.md`。商品企业建立现货/实现价/正常化价格及情景敏感性；与市场环境模块共用假设调整记录，避免重复分析和计价。

## 判断约束

- 三阶段是研究组织方式，不能要求明显不通过的企业仍强行估值。先做底线判断：通过 / 不通过 / 证据不足。严重治理或偿付问题不能由其他高分抵消；“未发现”不等于证明不存在。
- 质量复利、周期、资产折价、困境反转分开识别。未通过质量复利筛选不自动否定其他策略；不得无授权把报告改成另一种策略。
- 历史增长不默认等于未来预测。取消六方法强制平均、`weighted_compound_growth` 默认外推及增长率趋势斜率混算。读取 `references/growth-methodology.md`，按需运行增长脚本。
- 取消 `G`、`avg_dev`、`LOW/UP` 与自动“强烈买入/清仓”的强制映射。价格结论来自公开假设下的估值，质量、信心和价格分别判断。
- 流动性、交易活跃度和盈利预期分开判断；市场环境不能直接生成择时信号。同一利好对盈利、倍数和折现率的影响须核查重复计价，缺少独立依据不叠加调整。
- 事实、计算、假设、判断必须可区分。记录财务期间、公告日期、行情时间、来源、单位与合并/母公司/普通股口径；禁止把检索时间当行情时间。
- 关键证据缺失则降级对应结论：可完成经营研究，但估值暂缓或标为条件性。缺少非核心的历史分位不使整份报告自动失败。解释缺失如何影响结论，禁止用猜测补表。

## 报告与工具

默认按 `references/report-template.md` 输出中文完整报告；用户只要摘要时可缩减但保留影响结论的条件。研究产物默认保存在当前工作区 `reports/`，除非用户指定其他位置。同行用 `references/peer-comparison.md`，评分如有需要用 `references/scoring-rubric.md`。

- `scripts/fetch_analysis_inputs.py`：嵌入式数据源的基础输入；连接器/官方公告可补充或替代不可用源。
- `scripts/fetch_peer_snapshot.py`：同行基础输入，行业字段仍须补齐。
- `scripts/fetch_stock_universe.py`：按需更新股票列表。
- `scripts/calc_profit_growth.py`：历史逐年、CAGR、每股与稀释分析；无预测合成率。
- `scripts/calc_valuation_zone.py`：名称保留，v2 改为读取情景 JSON，计算内在价值与安全边际价格，不输出交易指令。使用方式见结论参考文件；旧 CLI/输出字段已停用。
- `scripts/calc_commodity_sensitivity.py`：商品价格对归属经济敞口、利润、EPS和估值的条件敏感性；统一单位、期间、持股权益和传导假设。
- `scripts/check_valuation_anchor.py`：行业方法库日期核查；日期通过不代表来源有效、方法适用或估值正确。

工具保持跨平台，不硬编码个人目录；`portable_data_provider/` 和可选 `--project-root` 继续保留。指标定义见 `references/metric-definitions.md`；严格调用块见 `references/caller-hard-requirements.md`。

## 完成检查

- 身份、股份口径、信息日期、业务理解与策略适用性明确。
- 证据包按重要性标注充分/部分/缺失/不适用；行业方法记录的版本、适用性和缺口说明清楚。交易数据缺失或方法库过期不自动否定已完成的经营研究。
- 五年以上历史数据或足以改变结论的缺口解释；资本/每股回报有分析或行业替代。
- 行业证据、竞争、股东友好度、底线判断、至少一名可比公司（通常二至三名）齐全。
- 估值主方法与经济逻辑不同的交叉检查；估值如可执行，列假设、情景、每股价值、安全边际与敏感性。缺关键数据不得声称可执行。
- 市场环境与预期差有简要核查：相关指标、可追溯来源与日期、公司传导、价格隐含假设及模型调整依据；证据不足时明确缺口，不强求全指标宏观报告。
- 有反证、跟踪触发条件、来源索引；计算实际运行且口径匹配。
- 分别标注研究状态与估值状态，不把“企业不通过”当成研究未完成。
