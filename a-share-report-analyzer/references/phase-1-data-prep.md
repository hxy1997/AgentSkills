# Phase 1: Data Preparation

This phase builds the analysis inputs. The goal is not to write conclusions yet.

## Deliverables of phase 1

Produce a clean working set with:

- company identity: company name, ticker, listing board, sector, sub-industry
- latest valuation snapshot: market cap, PE, PB, dividend yield when relevant
- historical valuation anchors: at least 5-year and 10-year percentile or median comparisons when available
- multi-year financials: usually 5 to 6 reporting years
- basic business summary
- industry overlay research notes
- a list of missing items and data-confidence notes

## Core data checklist

### A. Valuation baseline

- latest market cap
- current `PE`
- current `PB`
- industry median or comparable-company range
- 5-year valuation position
- 10-year valuation position

### B. Multi-year financials

Use at least 5 years when possible:

- revenue
- attributable net profit
- ROE
- operating cash flow
- free cash flow when meaningful
- debt and cash structure
- dividend or buyback history when relevant

### C. Business and industry context

- core products or services
- revenue structure
- profit drivers
- customer type
- geographic exposure
- regulatory exposure
- main competitors

### D. Industry overlay package

The overlay package is mandatory. It must answer:

- what actually drives value in this sub-industry
- which reported metrics are the most decision-useful
- which accounting line items need caution
- which valuation method is usually more informative
- what the main cycle or policy risks are

## Subagent requirement

If subagent tooling exists, create a dedicated research subagent during this phase.

Recommended prompt shape:

- research only the target company's sub-industry
- summarize business model, key operating KPIs, accounting quirks, common valuation anchors, and major risks
- distinguish stable principles from current-cycle facts
- provide concise notes that can be merged into the main report

If subagents are unavailable, do the same work locally.

## Source strategy

Use the following priority:

1. User-provided data, screenshots, and prior calculations
2. Structured market and financial data
3. Annual reports and official company disclosures
4. Broker reports and industry public materials
5. Web search for missing or current items

For implementation notes and the user's external data project, load `data-source-strategy.md`.

## Data-quality rules

- Never mix periods inside one formula.
- Mark estimated values clearly.
- Note when trailing data, annual data, or interim data are mixed across sections.
- If a metric is unavailable for a sector, say it is not decision-useful rather than forcing it.
