---
name: a-share-report-analyzer
description: "Use when the user asks for an A-share company analysis report, stock valuation memo, annual-report plus broker-report synthesis, or a structured Chinese equity write-up covering data preparation, body analysis, and valuation conclusion. Supports a three-phase workflow: prepare data, write the main analysis, then produce the valuation conclusion. Default scope is A-share companies, with mandatory industry-specific overlays for every sub-industry and dedicated special rules for brokers, banks, and insurers."
---

# A-Share Report Analyzer

Use this skill to produce a Chinese stock analysis report with a stable core framework plus industry-specific overlays.

## What this skill does

- Runs a fixed three-phase workflow:
  1. `准备数据`
  2. `正文分析`
  3. `估值结论`
- Applies the same base framework to all A-share companies.
- Forces one extra layer of research for the target company's sub-industry before final judgment.
- Adds dedicated accounting and valuation rules for `券商`, `银行`, and `保险`.
- Keeps the main `SKILL.md` small and loads detailed references only when needed.

## Required operating rules

1. Always determine the company's market, sector, and sub-industry before writing conclusions.
2. Always run the general framework first, then add industry overlays. Do not replace the general framework with industry commentary.
3. If subagent tooling is available, always spawn a dedicated research subagent for `子行业分析原则与估值逻辑` before finishing phase 1.
4. If the company is a broker, bank, or insurer, also load the matching sector reference and rewrite the financial-quality section with sector-specific logic.
5. Use current sources for regulation, valuation norms, and industry logic when there is any meaningful chance they changed.
6. Never pretend that missing data is present. Mark missing items explicitly and explain the impact.
7. Separate facts from inference. When a judgment depends on interpretation, say so.
8. The deliverable is a report, not investment advice.

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
- all three phases were executed in order
- report headings follow `references/report-template.md`
- 5-year and 10-year valuation positions are shown, or missing-data impact is explained
- 5-6 year financial table is shown
- six-method growth table plus filtering, trimming, and `weighted_compound_growth` are shown
- all six phase-2 sections are present with scores and short justification
- peer table is present with at least one peer and normally 2-3 peers
- main valuation method and cross-check method are both present, unless one is genuinely unusable and the reason is stated
- `E`, `F`, `avg_dev`, `LOW`, `UP` are shown
- implied market-cap interval and price interval are shown
- facts and inference are clearly separated
- key missing data, if any, is marked with impact
- key risks are stated

If any mandatory item above is missing, the report must be labeled incomplete.

## Load these references

Read only what you need:

- `references/workflow-overview.md` for the mandatory end-to-end process.
- `references/phase-1-data-prep.md` for the data checklist and preparation rules.
- `references/phase-2-body-analysis.md` for the six-block body-analysis framework.
- `references/phase-3-valuation-conclusion.md` for valuation steps and conclusion logic.
- `references/industry-overlay-principle.md` for the mandatory general-plus-industry layering rule.
- `references/industry-research-checklist.md` for the subagent research task.
- `references/data-source-strategy.md` for how to use the user's existing data project and how to fall back.
- `references/growth-methodology.md` for the mandatory six-method profit-growth calculation.
- `references/peer-comparison.md` for the mandatory peer-comparison table rules.
- `references/final-conclusion-logic.md` for the mandatory valuation-zone and price-interval logic.
- `references/report-template.md` for the final report shape.
- `references/caller-hard-requirements.md` when the user wants a reusable strict-invocation prompt block.
- `references/scoring-rubric.md` for scoring guidance.
- `references/metric-definitions.md` for common metric definitions and reminders.

Use bundled scripts when they fit the task:

- `scripts/fetch_analysis_inputs.py` for phase-1 structured inputs from the external data project.
- `scripts/fetch_stock_universe.py` for refreshing A-share, HK, or US stock universes through Tushare Pro.
- `scripts/calc_profit_growth.py` for the mandatory six-method profit-growth calculation.
- `scripts/fetch_peer_snapshot.py` for the mandatory peer comparison baseline table.
- `scripts/calc_valuation_zone.py` for the mandatory final price-zone and action mapping.

Load one or more sector references when applicable:

- `references/sector-general-a-share.md`
- `references/sector-broker.md`
- `references/sector-bank.md`
- `references/sector-insurance.md`

## Mandatory workflow

1. Identify the target company, ticker, market, reporting periods, sector, and sub-industry.
2. Load `references/workflow-overview.md`.
3. Run phase 1 with `references/phase-1-data-prep.md`.
4. During phase 1, run the industry-overlay workflow:
   - Load `references/industry-overlay-principle.md`.
   - Load `references/industry-research-checklist.md`.
   - If subagent tooling exists, spawn an `explorer` subagent dedicated to researching:
     - the sub-industry business model
     - core operating metrics
     - common valuation anchors
     - cycle and policy sensitivity
     - differences versus the generic financial-analysis framework
   - If subagent tooling does not exist, perform the same research locally.
5. If the company is `券商`, `银行`, or `保险`, load the matching sector reference and integrate its rules into phase 2 and phase 3.
6. Run phase 2 with `references/phase-2-body-analysis.md`.
7. Before finalizing phase 2, build a peer-comparison table:
   - Load `references/peer-comparison.md`.
   - Run `scripts/fetch_peer_snapshot.py` when structured data can be fetched.
   - If sector-specific metrics are missing from the structured pipeline, supplement them with current disclosure or web research and merge them into the comparison table.
8. Run phase 3 with `references/phase-3-valuation-conclusion.md`.
9. During phase 3:
   - Load `references/growth-methodology.md`.
   - Run `scripts/calc_profit_growth.py` on the profit series.
   - Load `references/final-conclusion-logic.md`.
   - Run `scripts/calc_valuation_zone.py` once `M`, `B`, `C`, `G`, and valuation deviations are available.
10. Output the report using `references/report-template.md`.
11. Before finalizing:
   - run a template-compliance self-check against `references/report-template.md`, `references/phase-2-body-analysis.md`, and `references/phase-3-valuation-conclusion.md`
   - list satisfied items and missing items
   - if the user asked for files, save each report to the requested directory and return the path
   - if any mandatory item is still missing, mark the report incomplete and explain the impact

## Output expectations

- Write in Chinese.
- Keep standard finance terms in English when that improves precision: `PE`, `PB`, `ROE`, `DCF`, `ARR`, `LTV`, `NIM`.
- Show formulas and intermediate assumptions for important calculations.
- For profit growth, show the six-method table, filtering rule, trimming step, and final weighted compound growth.
- For competition, show at least one peer and aim for two to three peers with a comparison table.
- For the final conclusion, show the valuation-zone table and a model-implied price interval.
- Make it obvious which parts are source-based facts and which parts are analytical judgment.
- When industry overlays materially change the conclusion, state that explicitly.
- When using subagents, pass the hard requirements explicitly instead of assuming they will infer them from the skill name alone.

## Special reminders

- For industrial and technology companies, do not assume one universal valuation method. The sub-industry overlay may change the preferred anchor from `PE` to `PB`, `PS`, `EV/EBITDA`, `DCF`, or a mixed approach.
- For financial companies, the asset side, liability side, regulatory ratios, and capital constraints are part of the business model. Do not treat them as footnotes.
- If the user already provides screenshots, tables, or draft analysis, treat them as working inputs and reconcile them with current data rather than discarding them.
