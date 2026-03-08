# Workflow

## 1. Data extraction

- Identify accounting standard: `HKFRS/IFRS`, `US-GAAP`, or `CN-GAAP`.
- Extract all required line items from the user-provided reports first.
- Standardize them into a multi-period comparison table.
- If a line item is missing, write `⚠️ 数据缺失：[科目名]`.
- Confirm fiscal year range; if using interim data, label any annualized cash-flow metric.

## 2. Latest external data (mandatory)

Must fetch:

- Latest stock price and date
- Latest market cap
- Latest shares outstanding
- Latest dividend yield (TTM)
- Latest PB (MRQ)
- Actual controller / top shareholder and ownership ratio
- SOE layer if applicable
- Latest market cap of listed subsidiaries / associates if relevant
- Buyback records in the last 12 months if relevant to `C1b`
- Full annual statements and dividend history if the user reports are incomplete
- Management insider buy/sell records in the last 12 months
- Main business segments and revenue mix

Priority:

1. `MCP`
2. Web search only when MCP cannot provide a reliable answer

## 3. Business model scan

Assess:

- Core business and cash-generation logic
- Revenue composition and value-chain position
- Customer structure and concentration
- Cyclicality and current cycle stage
- Pricing power
- Moat: brand, network effects, switching cost, scale, license, cost advantage

## 4. Management and governance

Assess:

- Ultimate controller and control chain
- Management stability
- Holdings and insider trading records in the last 12 months
- Incentives and capital-allocation behavior
- Integrity record, disclosure quality, related-party risk, dividend intent

Governance score:

- Interest alignment: `0-3`
- Governance structure: `0-3`
- Integrity record: `0-2`
- Communication transparency: `0-2`

## 5. Three-pillar evaluation

### Pillar 1: asset backing

Compute `T0_NAV`, `T1_NAV`, `T2_NAV` with the latest available report period.

Formulas:

- `T0_NAV = (现金等价物 + 短期理财 + 定期存款 - 总负债) / 总股本`
- `T1_NAV = (现金等价物 + 短期理财 + 定期存款 - 有息负债) / 总股本`
- `有息负债 = 短期借款 + 长期借款 + 应纳入的租赁负债 + 视同负债的质押资产`
- `T2_NAV = ((现金等价物 + 短期理财 + 定期存款)×1.0 + 应收账款×0.85 + 存货×折扣 + 其他流动资产×0.5 - 总负债) / 总股本`

Inventory discount guide:

- White liquor / low-obsolescence consumer goods: `0.8`
- General manufacturing: `0.7`
- Electronics / fashion: `0.5`
- Near-completion real-estate projects: `0.7`

Special handling:

- Contract liabilities in prepaid-heavy industries: add to T0/T1 cash pool, but keep conservative treatment in T2.
- Restricted cash: remove from T0/T1 cash pool if `5%-20%`; veto if `>20%` of total cash.
- Negative equity: PB not meaningful; use `市值/总资产` and flag.

### Pillar 2: low maintenance burn

Compute:

- `FCF = 经营性现金流 - 资本开支`
- `资产烧损率 = FCF / 资产垫(对应T级NAV × 总股本)`
- `FCF转换率 = FCF / 净利润`
- `SG&A占比 = 销售管理费用 / 营收`

Three-pass rule: pass if at least `2/3` below are true:

1. Latest full-year `FCF > 0`
2. Burn rate passes the relevant T-grade threshold
3. Operating cash flow positive for 3 consecutive years

Thresholds:

- `T0`: pass `>=0%`, warning `-5%~0%`, veto `<-5%`
- `T1`: pass `>=5%`, warning `0%~5%`, veto `<0%`
- `T2`: pass `>=10%`, warning `5%~10%`, veto `<5%`

### Pillar 3: realization path

Determine subtype strictly.

#### A: high-dividend broken-net

All core conditions must pass:

1. Dividend yield meets market threshold: `HK >=6%`, `A-share >=4%`, `US >=5%`
2. `PB <= 0.5`
3. Continuous dividends `>= 5 years`

#### B: holding-company discount / SOTP

All core conditions must pass:

1. Holding-company discount `>= 30%`
2. At least one listed subsidiary stake `>= 10%`
3. Visible holding value coverage `>= 30%`
4. Parent net cash `> 0`

`SOTP = Σ(子公司市值 × 持股比例) + 母公司净现金`

#### C1: traditional event-driven

- `C1a`: asset sale / spin-off
- `C1b`: buyback-driven
- `C1c`: liquidation / delisting / privatization

#### C2: policy / institutional risk repair

All entry conditions must pass:

1. Official positive policy signal
2. At least one precedent, or explicit official timetable if first-of-kind
3. Healthy operations: positive operating cash flow, revenue not collapsing, no veto facts
4. Valuation already depressed: `PB <= 0.6` or adjusted `PE <= 6x`, and drawdown vs pre-shock peak `>= 60%`

Score dimensions:

- Policy certainty `0-3`
- Comparable precedent `0-3`
- Company execution progress `0-2`
- Valuation cushion `0-2`

Even with total score `>=6`, `valuation cushion = 0` means `C2` fails.

## 6. Subtype-specific analysis

Only run for valid subtypes.

- `A`: dividend sustainability score, high-base dividend-cut test, payback period
- `B`: SOTP table, discount decomposition, bull/base/bear sensitivity
- `C1`: event probability-return matrix and timeline
- `C2`: admission test plus 10-point scorecard
- Mixed labels only when every included subtype fully passes its core gates

## 7. Fact Check (22 items)

### Core checks 1-19

Asset quality:

1. Restricted cash
2. Pledged assets
3. Goodwill ratio
4. Goodwill impairment history
5. AR quality
6. Inventory turnover / DIO trend
7. Intangible-asset reasonableness

Liability risks:

8. Off-balance-sheet liabilities
9. Capital commitments
10. Guarantees / cross guarantees
11. Pension gap
12. Environmental / legal liabilities
13. Other payables anomaly

Operating quality:

14. Related-party transactions
15. Revenue concentration
16. Q4 revenue spike
17. Audit opinion
18. Management integrity
19. Government-subsidy dependency

### Bonus checks 20-21

20. Listed holdings coverage bonus
21. SOE layer / control bonus

### Asset-structure check 22

Non-current financial asset ratio:

- `<=15%`: pass
- `15%-30%`: `WARNING-Risk`
- `30%-50%`: severe `WARNING-Risk`; calculate core T-grade safety margin
- `>50%`: veto

Additional `WARNING-Risk` if:

- Level 3 detail disclosure is poor
- Investment income >50% of total profit
- Fair-value volatility over 2 years exceeds `±20%`

### Warning classification

- `WARNING-Data`: missing or undisclosed data prevents confirmation
- `WARNING-Risk`: a real risk signal exists

### Rating

- `A`: no `WARNING-Risk`
- `B`: `WARNING-Risk <= 3`
- `C`: `WARNING-Risk > 3` or near-veto issue
- `D`: any veto

Bonus adjustment:

- Base `B` + bonus `>=2` -> `B+`
- Base `C` + bonus `>=3` -> `B`
- Base `D` cannot be upgraded

If no valid realization path exists among `A/B/C`, cap the rating at `C`.

## 8. Trade plan and scenario returns

Entry thresholds:

- `T0`: `股价 < T0_NAV × 0.85`
- `T1`: `股价 < T1_NAV × 0.80`
- `T2`: `股价 < T2_NAV × 0.70`

Sizing guide:

- `T0`: up to `10%`
- `T1`: up to `8%`
- `T2`: up to `5%`
- `C1`: `5%-8%`
- `C2`: `2%-5%`, `C2+` can reach `5%-8%`

Hard stop:

- General: `-25%`
- `C1`: `-20%`

Return calculation must show:

- Conservative / base / optimistic `PB` target
- Capital gain formula
- Tax-adjusted dividend yield
- Holding-period total return and IRR

## 9. Final output

Use the exact Markdown structure from `report-template.md`.

Do not omit sections.
