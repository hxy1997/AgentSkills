# Report Template

Use this as the default output structure. Adjust only if the user explicitly wants a different format.

## 标题

`[公司名]分析及评估报告`

## 免责声明

简要说明数据来源用于归纳整理，不构成投资建议，并注明关键数据截止日期。

## 一、准备工作一：估值分位计算

- 基础估值数据表
- 5年和10年估值分位表
- 子行业估值锚表版本检查
  - anchor id
  - version date
  - freshness status
  - primary anchor
  - secondary anchor
  - stale/missing handling if any

## 二、准备工作二：利润成长性分析

- 近 5 至 6 年财务表
- CAGR 计算
- 6 种数学方法评估平均利润增长率表
- 过滤、去极值、求平均过程
- 利润加权复合增长率

## 三、准备工作三：交易、宏观、研报、资金面与公告证据包

- K线及交易结构
  - 数据状态：complete / partial / missing / not decision-useful
  - 关键事实：区间涨跌幅、成交额/换手、均线位置、波动、回撤、异常交易日
  - 分析判断：市场定价状态、拥挤度、风险时点
- 宏观新闻及政策环境
  - 数据状态
  - 关键事实：利率、汇率、流动性、商品价格、产业政策、地缘风险、行业供需事件
  - 货币政策状态：政策预期、实际利率、收益率曲线、美元或相关汇率、信用与流动性
  - 传导路径：新闻/政策 -> 核心外部变量 -> 财务指标/估值假设
  - 外部变量依赖图：收入、成本、债务、capex、税费与折现率分别受哪些变量影响
  - 若为商品公司：spot、realized、cycle-normalized price，熊/基准/牛价格情景及敏感度
  - 双重计价检查：同一政策冲击是否已通过商品价格、FX、利润、折现率或估值倍数计入
  - 分析判断：强化、削弱或不改变当前估值结论；若只影响交易情绪，应标为短期风险而非基本面变化
- 券商研报及行业研报
  - 数据状态
  - 关键事实：报告日期、机构、评级、目标价、EPS预测、主估值方法
  - 分析判断：核心假设、分歧、是否支持子行业估值锚
- 资金面及筹码面
  - 数据状态
  - 关键事实：资金流、北向、两融、龙虎榜、大宗交易、解禁、股东户数、分红/回购
  - 分析判断：短期压力、流动性、筹码集中度和事件风险
- 公司公告
  - 数据状态
  - 关键事实：重要公告清单、日期、类型、事项、执行状态
  - 分析判断：对业务、财务质量、估值和风险的影响
- 缺失数据及影响

## 四、业务及产品清晰度

按六大正文部分之一输出，并给分。

## 五、经营稳定性

按六大正文部分之一输出，并给分。

## 六、产品定价权及定价权种类

按六大正文部分之一输出，并给分。

## 七、成长分析

按六大正文部分之一输出，并给分。

## 八、行业竞争度

- 至少 1 个、默认 2 至 3 个核心竞争对手
- 同行关键指标对比表
- 基于对比表的竞争结论与评分

## 九、财务质量分析

- 资产质量
- 利润质量
- 现金流质量
- 财务勾稽或一致性检查
- 财务质量综合得分

## 十、总评分

- 分项评分表
- 平均分或加权分

## 十一、企业估值

- 未来成长率保守估算
- 子行业估值锚表引用与当前市场定价语言
- 若货币政策或外部变量重要：政策情景、实际利率、FX、融资成本和折现率处理
- 若为商品公司：spot/realized/normalized price、熊/基准/牛 price deck、产量与成本假设、价格敏感度
- 主估值方法
- 交叉验证方法
- 安全边际估值
- shock ledger 与 double-counting 自检

## 十二、最终结论

- 估值结论表
- `E`、`F`、平均偏离、`LOW`、`UP`
- 公司质量分类
- 价格高低分类
- 研究立场映射（不得表述为可执行订单）
- 模型推导的市值区间
- 模型推导的价格区间
- 核心依据
- 关键风险

## Template notes

- If the industry overlay changes the valuation method, explain that inside `企业估值`.
- If the valuation-anchor table changes or overrides the generic method, explain the anchor version and rationale inside `准备工作一` and `企业估值`.
- If K-line, macro-news/policy, research-report, capital-flow/chip, or announcement packages are unavailable, mark status and explain impact inside `准备工作三`.
- If some preparation tables are unavailable, say what is missing and continue with the highest-confidence subset.
- If commodity prices materially drive profit, a price deck and sensitivity table are required; a generic earnings haircut alone is insufficient.
- If monetary policy is material, state whether it acts through prices, demand, FX, financing, discount rate, or risk premium, and show the double-counting check.
- The final conclusion should not stop at “偏高/偏低/合理”; it must also provide the model-implied price interval.
