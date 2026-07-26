---
name: a-share-report-analyzer
description: "显式调用：生成A股公司、A股持仓或A股组合初筛报告；覆盖估值、财务、子行业、K线、宏观政策、研报、资金筹码、回购与公告。用于研究与人工组合复核，禁止下单；美股和港股转交 equity-research-analyzer。"
---

# A-Share Report Analyzer

Use this skill to produce a Chinese stock analysis report with a stable core framework plus industry-specific overlays.

## Select the mode

- `company_report`: analyze an A-share company without requiring it to be held.
- `holding_report`: add redacted current weight, cost-relative risk, concentration, currency, and thesis-fit context.
- `portfolio_triage`: rank A-share holdings by weight, concentration, factor coverage, research staleness, and thesis risk; run the full report only for material exceptions.

For US or Hong Kong securities, preserve the canonical ticker and hand off to `equity-research-analyzer`. Do not force A-share-only evidence such as northbound flow or dragon-tiger data onto a foreign listing.

## What this skill does

- Runs a fixed three-phase workflow:
  1. `准备数据`
  2. `正文分析`
  3. `估值结论`
- Applies the same base framework to all A-share companies.
- Forces one extra layer of research for the target company's sub-industry before final judgment.
- Requires a versioned valuation-anchor table for the target sub-industry, with quarterly freshness checks for fast-changing technology sectors.
- Requires five evidence packages when available: `K线交易结构`, `宏观新闻/政策环境`, `券商研报及行业研报`, `资金面/筹码面`, and `公司公告`.
- Requires explicit external-variable and monetary-policy transmission when rates, real yields, FX, liquidity, or commodity prices materially affect earnings or valuation.
- Adds dedicated accounting and valuation rules for `券商`, `银行`, and `保险`.
- Keeps the main `SKILL.md` small and loads detailed references only when needed.

## Required operating rules

1. Always determine the company's market, sector, and sub-industry before writing conclusions.
2. Always run the general framework first, then add industry overlays. Do not replace the general framework with industry commentary.
3. If subagent tooling is available, always spawn a dedicated research subagent for `子行业分析原则与估值逻辑` before finishing phase 1.
4. Before choosing valuation methods, check the versioned valuation-anchor table for the target sub-industry. If the anchor is missing or stale, update it with current sources before final valuation.
5. During phase 1, build K-line, macro-news/policy, research-report, capital-flow/chip, and announcement evidence packages. If any package is missing or not decision-useful, state that explicitly and explain impact.
6. If the company is a broker, bank, or insurer, also load the matching sector reference and rewrite the financial-quality section with sector-specific logic.
7. Use current sources for regulation, valuation norms, industry logic, official announcements, and sell-side expectations when there is any meaningful chance they changed.
8. For commodity, cyclical, export, overseas, or dollar-linked companies, load `references/macro-policy-transmission.md` and convert monetary policy into explicit price, demand, cost, FX, financing, discount-rate, or risk-premium assumptions.
9. Do not use a generic earnings haircut as the only substitute for an explicit commodity price deck when commodity prices materially drive profit.
10. Never pretend that missing data is present. Mark missing items explicitly and explain the impact.
11. Separate facts from inference. When a judgment depends on interpretation, say so.
12. The deliverable is a report, not investment advice.
13. Cost basis must not alter intrinsic value. Use it only for tax, behavior, and portfolio-transition context.
14. Default to portfolio percentages; redact account identifiers, quantities, absolute balances, and raw broker payloads.
15. Read-only means read-only: never submit, replace, or cancel an order and never generate an executable broker order payload.

## Non-negotiable output contract

Treat the following as hard requirements, not suggestions:

1. Execute all three phases in order. Do not skip a phase even if the user asks for a quick result.
2. Output the final report in the title order defined by `references/report-template.md`. Do not collapse the report into a free-form memo or summary unless the user explicitly asks for a different format.
3. The final report must include all of the following, or explicitly mark the missing item and explain the impact:
   - company identification plus sector and sub-industry confirmation
   - 5-year and 10-year valuation-position table
   - 5-6 year financial table
   - six-method profit-growth table
   - filter rule, trimming step, and `weighted_compound_growth`
   - valuation-anchor table status, version date, current primary anchor, secondary anchor, and stale/missing handling
   - K-line/trading-structure evidence package status and key observations
   - macro-news and policy-environment evidence package status, key external variables, and transmission path
   - explicit monetary-policy regime, real-yield, FX, and liquidity assessment when decision-useful
   - commodity price deck and price-sensitivity table when commodity prices materially drive earnings
   - broker-report and industry-research evidence package status and key assumption differences
   - capital-flow/chip evidence package status, including fund flow, margin, dragon-tiger, block trade, lockup, and shareholder-count items when available
   - company-announcement evidence package status and material announcements or missing-disclosure impact
   - all six body-analysis sections, each with a score and short justification
   - peer-comparison table with 2-3 peers by default
   - one main valuation method plus one cross-check method
   - `E`, `F`, `avg_dev`, `LOW`, `UP`
   - implied market-cap interval and implied price interval
   - core evidence and key risks
4. Separate source-based facts from analytical judgment inside each major section.
5. If any key data is missing, do not silently skip it. State the missing item, why it is missing, and how it changes confidence or the conclusion.
6. The output must be a complete Markdown report, not a short executive summary, unless the user explicitly asks for a summary.
7. If the user asks for file output, save each report to the requested directory and return the file path.
8. Before finalizing, run a template-compliance self-check. If any mandatory item is unsatisfied, continue the research or mark the report incomplete instead of pretending it is finished.

## Definition of done

A report is complete only when every item below is satisfied:

- exact company, ticker, market, sector, and sub-industry are confirmed
- report mode and evidence cutoff are stated; holding context is redacted when applicable
- all three phases were executed in order
- report headings follow `references/report-template.md`
- 5-year and 10-year valuation positions are shown, or missing-data impact is explained
- 5-6 year financial table is shown
- six-method growth table plus filtering, trimming, and `weighted_compound_growth` are shown
- valuation-anchor version is checked; if missing or stale, the report either uses an updated anchor table or is labeled incomplete
- K-line/trading, macro-news/policy, broker-report/research, capital-flow/chip, and announcement evidence packages are shown or marked missing/not decision-useful with impact
- all six phase-2 sections are present with scores and short justification
- peer table is present with at least one peer and normally 2-3 peers
- main valuation method and cross-check method are both present, unless one is genuinely unusable and the reason is stated
- `E`, `F`, `avg_dev`, `LOW`, `UP` are shown
- implied market-cap interval and price interval are shown
- facts and inference are clearly separated
- key missing data, if any, is marked with impact
- key risks are stated
- no broker order fields, order ids, quantities, or trading-write actions are present

If any mandatory item above is missing, the report must be labeled incomplete.

## Load these references

Read only what you need:

- `references/workflow-overview.md` for the mandatory end-to-end process.
- `references/phase-1-data-prep.md` for the data checklist and preparation rules.
- `references/phase-2-body-analysis.md` for the six-block body-analysis framework.
- `references/phase-3-valuation-conclusion.md` for valuation steps and conclusion logic.
- `references/industry-overlay-principle.md` for the mandatory general-plus-industry layering rule.
- `references/industry-research-checklist.md` for the subagent research task.
- `references/valuation-anchor-framework.md` for versioned valuation-anchor checks and update rules.
- `references/data-source-strategy.md` for how to use the user's existing data project and how to fall back.
- `references/evidence-packages.md` for mandatory K-line, macro-news/policy, research-report, capital-flow/chip, and announcement evidence packages.
- `references/macro-policy-transmission.md` for monetary-policy, real-yield, FX, liquidity, commodity-price, and discount-rate transmission rules.
- `references/growth-methodology.md` for the mandatory six-method profit-growth calculation.
- `references/peer-comparison.md` for the mandatory peer-comparison table rules.
- `references/final-conclusion-logic.md` for the mandatory valuation-zone and price-interval logic.
- `references/report-template.md` for the final report shape.
- `references/caller-hard-requirements.md` when the user wants a reusable strict-invocation prompt block.
- `references/scoring-rubric.md` for scoring guidance.
- `references/metric-definitions.md` for common metric definitions and reminders.

Use bundled scripts when they fit the task:

- `scripts/fetch_analysis_inputs.py` for phase-1 structured inputs from the embedded provider by default, with optional external-project override.
- `scripts/fetch_stock_universe.py` for refreshing A-share, HK, or US stock universes through Tushare Pro.
- `scripts/calc_profit_growth.py` for the mandatory six-method profit-growth calculation.
- `scripts/fetch_peer_snapshot.py` for the mandatory peer comparison baseline table, using the embedded provider by default.
- `scripts/calc_valuation_zone.py` for the mandatory final price-zone and research-stance mapping.
- `scripts/calc_commodity_sensitivity.py` for deterministic commodity-price revenue, profit, EPS, and price sensitivity.
- `scripts/check_valuation_anchor.py` for checking whether a sub-industry valuation-anchor table exists and is fresh enough.

Embedded provider notes:

- The skill now ships with a portable local provider under `portable_data_provider/`.
- By default, the bundled data scripts do not depend on any absolute path or any other local project.
- `--project-root` remains available only as an explicit compatibility override when the user wants to point at an external `daily_stock_analysis` checkout.
- Keep all script logic cross-platform. Do not introduce Windows-only shell assumptions into bundled Python tools.

Load one or more sector references when applicable:

- `references/sector-general-a-share.md`
- `references/sector-broker.md`
- `references/sector-bank.md`
- `references/sector-insurance.md`

## Mandatory workflow

1. Identify the target company, ticker, market, reporting periods, sector, and sub-industry.
2. Load `references/workflow-overview.md`.
3. Run phase 1 with `references/phase-1-data-prep.md`.
4. During phase 1, load `references/evidence-packages.md` and build the five evidence packages:
   - K-line and trading structure
   - macro news and policy environment
   - broker reports and industry research
   - capital-flow and chip structure
   - company announcements
   If rates, real yields, FX, liquidity, or commodity prices are material, also load `references/macro-policy-transmission.md` and build an external-variable dependency map.
5. During phase 1, run the industry-overlay workflow:
   - Load `references/industry-overlay-principle.md`.
   - Load `references/industry-research-checklist.md`.
   - If subagent tooling exists, spawn an `explorer` subagent dedicated to researching:
     - the sub-industry business model
     - core operating metrics
     - common valuation anchors
     - cycle and policy sensitivity
     - differences versus the generic financial-analysis framework
   - If subagent tooling does not exist, perform the same research locally.
6. During phase 1, run the valuation-anchor workflow:
   - Load `references/valuation-anchor-framework.md`.
   - Run `scripts/check_valuation_anchor.py` with the closest `anchor_id` or `--sub-industry` alias.
   - If the status is `ok`, use that anchor table in phase 3.
   - If the status is `expired` or `missing`, update or create the anchor table from current sources before phase 3. Do not silently fall back to fixed valuation logic.
7. If the company is `券商`, `银行`, or `保险`, load the matching sector reference and integrate its rules into phase 2 and phase 3.
8. Run phase 2 with `references/phase-2-body-analysis.md`.
9. Before finalizing phase 2, build a peer-comparison table:
   - Load `references/peer-comparison.md`.
   - Run `scripts/fetch_peer_snapshot.py` when structured data can be fetched.
   - If sector-specific metrics are missing from the structured pipeline, supplement them with current disclosure or web research and merge them into the comparison table.
10. Run phase 3 with `references/phase-3-valuation-conclusion.md`.
11. During phase 3:
   - Load `references/growth-methodology.md`.
   - Run `scripts/calc_profit_growth.py` on the profit series.
   - Use the fresh valuation-anchor table to select the main valuation method and cross-check method.
   - For commodity-driven companies, show a bear/base/bull price deck, state spot versus normalized prices, and run `scripts/calc_commodity_sensitivity.py` when production exposure is available.
   - Reconcile monetary-policy effects through metal/product prices, FX, financing cost, and discount rate without double counting the same shock.
   - Load `references/final-conclusion-logic.md`.
   - Run `scripts/calc_valuation_zone.py` once `M`, `B`, `C`, `G`, and valuation deviations are available.
12. Output the report using `references/report-template.md`.
13. Before finalizing:
   - run a template-compliance self-check against `references/report-template.md`, `references/phase-2-body-analysis.md`, and `references/phase-3-valuation-conclusion.md`
   - list satisfied items and missing items
   - if the user asked for files, save each report to the requested directory and return the path
   - if any mandatory item is still missing, mark the report incomplete and explain the impact
   - never emit an executable order; use a research stance and defer portfolio weight changes to `portfolio-strategy-engine`

## Output expectations

- Write in Chinese.
- Keep standard finance terms in English when that improves precision: `PE`, `PB`, `ROE`, `DCF`, `ARR`, `LTV`, `NIM`.
- Show formulas and intermediate assumptions for important calculations.
- For profit growth, show the six-method table, filtering rule, trimming step, and final weighted compound growth.
- For competition, show at least one peer and aim for two to three peers with a comparison table.
- For valuation, show which valuation-anchor table version was used, why the primary anchor fits the current cycle, and which conditions would invalidate it.
- For the final conclusion, show the valuation-zone table and a model-implied price interval.
- Make it obvious which parts are source-based facts and which parts are analytical judgment.
- When industry overlays materially change the conclusion, state that explicitly.
- When using subagents, pass the hard requirements explicitly instead of assuming they will infer them from the skill name alone.
- K-line, capital-flow, and chip data support timing and risk judgments; they must not override company fundamentals or official disclosures without explanation.
- Macro news and policy events affect the report only through explicit transmission paths: demand, price, cost, financing, discount rate, regulation, supply chain, or risk appetite. Do not treat generic news heat as proof of intrinsic value.
- For Federal Reserve or other central-bank analysis, focus on policy expectations, real yields, the yield curve, FX, liquidity, and the reason for the policy move. Do not reduce the conclusion to “rate hike bearish / rate cut bullish.”
- Treat monetary policy as an upstream driver of commodity prices and discount rates, not as an unrelated third factor. State and prevent double counting.
- For commodity companies, separate spot price, realized price, and cycle-normalized price. Show the price deck, production exposure, unit-cost or `AISC/C1` context, FX, taxes, minority interests, hedging, and the resulting sensitivity range.
- Broker reports and industry reports are external opinions. Summarize their assumptions and dispersion instead of treating their ratings as facts.
- Company announcements are primary-source facts. Reconcile them with financial statements and later execution.

## Special reminders

- For industrial and technology companies, do not assume one universal valuation method. The sub-industry overlay may change the preferred anchor from `PE` to `PB`, `PS`, `EV/EBITDA`, `DCF`, or a mixed approach.
- For financial companies, the asset side, liability side, regulatory ratios, and capital constraints are part of the business model. Do not treat them as footnotes.
- If the user already provides screenshots, tables, or draft analysis, treat them as working inputs and reconcile them with current data rather than discarding them.
