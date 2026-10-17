# 情景估值与结论

旧 `E/F/avg_dev/LOW/UP` 综合评分与动作矩阵已停用。安全边际不再作为一项独立估值重复平均。

## 脚本接口

`python scripts/calc_valuation_zone.py --input valuation-input.json`

输入示例（演示数字，不是投资标准）：

```json
{"current_price": 10, "share_count": 100, "scenarios": [
  {"name": "保守", "method": "pe", "eps": 1, "multiple": 10, "margin_of_safety": 0.2},
  {"name": "基准", "method": "pe", "eps": 1.1, "multiple": 12, "margin_of_safety": 0.2},
  {"name": "乐观", "method": "pe", "eps": 1.2, "multiple": 14, "margin_of_safety": 0.2}
]}
```

share_count为实际股数，所有金额及每股价格币种相同。current_price可缺，不能杜撰。可选 quote_date、currency、assumptions 元数据。金融使用bank_pb：bvps、roe、cost_of_equity、growth；隐含分红率=1−growth/roe，须验证资本/增长与分配相容。脚本仅提供稳态估值，不能替代过渡期预测。

另支持dividend（next_dividend、cost_of_equity、growth），ev_ebit（operating_profit、multiple、net_claims），equity_value（已由外部模型求出的equity_value）。net_claims=债务+其他优先索取权+少数股东权益−合格冗余现金−单独估值的非经营资产；须避免重复计入现金和利润。

## 公式和解释

- PE每股价值=可持续普通股EPS×合理倍数。
- 稳态银行PB=(ROE−g)/(Ke−g)，每股价值=普通股BVPS×PB；Ke>g、ROE>g，不支持不相容增长。增长所需留存= g/ROE。
- 股利每股价值=D1/(Ke−g)；D1是下一期可持续股利，不是最近单次已付金额。
- EV每股价值=(经营利润×倍数−net_claims)/普通股数。
- 安全边际价格=每股价值×(1−安全边际率)。安全边际为分析假设，不是回报保证。
- 当前折价=1−当前价格/内在价值；负值代表溢价。

所有情景分别列出。不得自动把概率赋给三个情景或声称区间有统计覆盖率。交叉方法分表，解释差异。

A/H公司模型普通股权益价值可按相同经济权利推每股人民币价值，但实际市值须A股价格×A股数+H股价格×H股数×汇率；不能把总股数×A股价命名为实际总市值。估值日股数与历史加权平均股数分开。

## 结论格式

分别回答企业质量、证据强度、该日价格、哪些假设会推翻结果。写“在这些假设下低于/高于安全边际门槛”，不自动生成强烈买入/清仓。个人仓位与交易计划不属于默认公司研究范围。

## 计算器与经济模型的边界

上述 EPS 和倍数示例仅演示接口，不能替代 business-to-value.md 的经营证据链。此脚本没有自动预测或多期 DCF 功能；多期模型需在可复算表格或等价脚本中计算，再通过 equity_value 输入已核验的普通股权益现值。保留原始模型、公式、时点和来源；不把未来退出价格当今日价值。脚本只接受正内在价值；若压力情景权益价值为零、负净资产或存在破产风险，应另表报告清偿顺序及股东损失，不为通过接口强行改成正值。
