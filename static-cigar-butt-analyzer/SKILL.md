---
name: static-cigar-butt-analyzer
description: Use this skill when the user asks for a static-value cigar-butt stock analysis, deep value asset-backing analysis, T0/T1/T2 NAV evaluation, high-dividend broken-net stock review, holding-company discount/SOTP analysis, event-driven value release analysis, or a full Markdown report based on at least two financial-report periods. Supports HKFRS/IFRS, US-GAAP, and CN-GAAP. Requires latest market data from MCP first and web fallback only when MCP is unavailable or insufficient.
---

# Static Cigar-Butt Analyzer

Use this skill to turn raw filings plus latest market data into a strict, full-length Markdown report for the user's "静态价值型烟蒂股" framework.

## What this skill does

- Analyzes a company under three pillars: asset backing, low maintenance burn, and value realization path.
- Classifies the stock into subtype `A`, `B`, `C1a`, `C1b`, `C1c`, `C2`, or valid mixed labels.
- Produces a complete Chinese-first Markdown report with English finance terms retained.
- Enforces hard-gate rules, no-guessing rules, and explicit formula display.

## Required inputs

- Company name and/or ticker.
- At least two reporting periods from user-provided reports or reliable external structured data.
- Enough balance sheet / cash flow / dividend history data to run the framework.

If the user gives only one report period and no reliable external multi-period financials are available, stop and say the analysis is blocked by missing periods.

## Load these references

Read only what you need:

- `references/workflow.md` for the mandatory 9-step process and hard rules.
- `references/accounting-mapping.md` for line-item mapping across HKFRS/IFRS, US-GAAP, and CN-GAAP.
- `references/report-template.md` for the exact report structure.

## Non-negotiable rules

1. Use `MCP` first for price, market cap, shares outstanding, PB, dividends, financial statements, cash flow, and buybacks when covered.
2. Use web search only when MCP is unavailable, missing the item, or clearly wrong.
3. Never skip MCP in favor of web search when MCP can provide the data.
4. Never guess a missing line item. Mark it as `⚠️ 数据缺失：[科目名]`.
5. Use the latest available report period for primary calculations. If interim is newer than annual, use interim for the main calculation and annual as comparison.
6. Do not mix periods within one formula.
7. Show every key calculation as `公式 + 代入数字 + 结果`.
8. Core subtype conditions are hard gates. Any failed core condition means the subtype does not exist.
9. Fact Check must list all 22 items and every warning must be tagged `WARNING-Data` or `WARNING-Risk`.
10. Record all external sources in the final `数据来源` section.

## Working procedure

Follow the steps in `references/workflow.md` in order:

1. Extract and normalize multi-period financial data.
2. Fetch latest external data with MCP-first discipline.
3. Scan business model, cyclicality, pricing power, and moat.
4. Analyze controller, management, incentives, and governance.
5. Evaluate the three pillars and determine T-grade.
6. Run subtype-specific analysis only for subtypes whose core conditions fully pass.
7. Complete all 22 Fact Check items and compute the final rating.
8. Generate entry/exit/positioning/return scenarios.
9. Output the exact report template.

## Output style

- Use Chinese for structure and explanation.
- Keep finance terms in English when standard: `NAV`, `FCF`, `SOTP`, `PB`, `EBITDA`, `SG&A`.
- Be explicit and audit-friendly.
- If a field is missing, state the impact on the conclusion.

## Special handling reminders

- Negative equity: PB is not meaningful; use `市值/总资产` as the valuation anchor and flag it clearly.
- Dual-class shares: use total issued shares across all classes.
- Cross-listed subsidiaries: use same-day FX and the conservative listed price.
- Interim cash flow metrics that need annualization must be labeled `年化数据（基于中报×2）` and note seasonality limits.
- Dividend cut >30% requires the high-base test before a sell-rule conclusion.
- `#20` listed holdings and `#21` SOE status are bonus items, not substitutes for failed core gates.
- If there is no valid realization path among `A/B/C`, cap the rating at `C` and mark value-trap risk.

## Deliverable

Return one complete Markdown report using `references/report-template.md`. Do not omit sections. Do not replace failed sections with a short summary.
