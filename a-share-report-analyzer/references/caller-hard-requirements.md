# Caller Hard Requirements

Use this block when you want strict compliance instead of a loosely structured research memo.

## Reusable strict prompt block

```text
Hard requirements:
1. Execute the full three-phase workflow in order. Do not skip any phase.
2. Follow the heading order defined by report-template.md. Do not collapse the output into a free-form summary.
3. The report must include:
   - company identification plus sector and sub-industry confirmation
   - 5-year and 10-year valuation-position table; if missing, state the missing item and its impact
   - sub-industry valuation-anchor table status, including anchor id, version date, freshness status, primary anchor, secondary anchor, and stale/missing handling
   - 5-6 year financial table
   - six-method profit-growth table, filter rule, trimming process, and weighted_compound_growth
   - K-line/trading-structure evidence package status and key observations
   - macro-news/policy evidence package status, key external variables, and transmission path to financial or valuation assumptions
   - monetary-policy regime, real-yield, FX, liquidity, and external-variable transmission when decision-useful
   - commodity price deck and deterministic price sensitivity when commodity prices materially drive earnings
   - broker-report and industry-research evidence package status, key assumptions, and estimate dispersion
   - capital-flow/chip evidence package status, including fund flow, margin, dragon-tiger, block trade, lockup, and shareholder-count items when available
   - company-announcement evidence package status, material announcements, and missing-disclosure impact
   - all six body-analysis sections, each with a score and short justification
   - 2-3 peer comparisons by default
   - one main valuation method plus one cross-check method chosen from a fresh valuation-anchor table; if the table is stale or missing, update/create it first or mark valuation incomplete
   - E, F, avg_dev, LOW, and UP
   - implied market-cap interval and implied price interval
   - core evidence and key risks
4. Separate facts from judgment. Treat official announcements as primary-source facts, broker reports as sourced opinions, macro-news/policy as external-variable evidence, and K-line/capital-flow data as timing or risk evidence rather than intrinsic-value proof.
5. If any key data or evidence package is missing, do not skip it. Explicitly state what is missing and how it affects confidence, scoring, valuation, or conclusion.
6. Do not replace an explicit commodity price deck with a generic earnings haircut, and do not double count the same monetary-policy shock through prices, earnings, discount rates, and multiples.
7. Output a complete Markdown report, not an executive summary.
8. Save each report to the requested directory and return the file path.
9. Before finalizing, run a template-compliance self-check. List satisfied and missing items. If anything mandatory is still missing, continue or mark the report incomplete.
```

## Usage note

When dispatching subagents, paste the block directly into the subagent task instead of only mentioning the skill name. This materially reduces format drift.
