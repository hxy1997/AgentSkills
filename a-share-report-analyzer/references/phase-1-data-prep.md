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
- valuation-anchor table status, version date, and freshness conclusion
- K-line/trading-structure package status and key observations
- macro-news/policy package status, external variables, and transmission-path notes
- monetary-policy regime, real-yield, FX, liquidity, and commodity/product-price dependency map when material
- broker-report and industry-research package status and key assumptions
- capital-flow/chip package status and key pressure or support points
- company-announcement package status and material events
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

### E. Valuation-anchor package

This package is mandatory before phase 3:

- closest anchor table id
- `last_updated` and `next_review_due`
- freshness status from `scripts/check_valuation_anchor.py`
- primary anchor
- secondary anchors
- weak or floor anchors
- disabled anchors
- current market pricing language
- stale/missing handling

If the anchor table is expired or missing, update or create it with current sources before valuation. If that cannot be done, mark the valuation portion incomplete.

### F. K-line and trading-structure package

Load `references/evidence-packages.md` and collect:

- latest quote and recent return
- 120 trading days of daily K-line when available
- MA5, MA10, MA20, MA60, MA120, MA250 position when available
- volume, amount, turnover, amplitude, drawdown, rebound, gap, and limit-up/down context
- abnormal trading days linked to announcements, sector moves, or market-wide shocks

### G. Macro-news and policy-environment package

Load `references/evidence-packages.md` and collect:

- macro events and policy changes that can affect the target's sector
- sector-specific price, demand, inventory, capacity, cost, exchange-rate, or funding variables
- broad market and sector risk-appetite context when it changes valuation timing
- source, date, affected variable, and expected duration for each material event
- transmission path: event -> company variable -> financial statement or valuation assumption

If monetary policy, FX, global liquidity, or commodity prices materially affect the company, also load `references/macro-policy-transmission.md` and collect:

- policy rate and expected path rather than one isolated meeting
- 2-year yield, 10-year nominal yield, and 10-year real yield when relevant
- inflation expectations, yield-curve shape, credit spreads, and central-bank liquidity when relevant
- `DXY` or the company's relevant revenue, cost, debt, and capex exchange rates
- spot price, company realized price, and cycle-normalized price for each material commodity
- attributable production, unit cost or `AISC/C1`, hedging, royalties, taxes, minority interests, and JV ownership
- a bear/base/bull external-variable table
- a shock ledger identifying earnings, financing, discount-rate, and multiple effects without double counting

For commodity-driven companies, a generic consensus-earnings haircut is not a substitute for an explicit price deck.

### H. Broker-report and industry-research package

Load `references/evidence-packages.md` and collect:

- recent company reports, rating changes, target prices, EPS forecasts, and valuation methods
- industry reports for the confirmed sub-industry
- consensus estimate direction and assumption dispersion
- report freshness, source institution, and whether original PDF or official page was checked

### I. Capital-flow and chip package

Load `references/evidence-packages.md` and collect:

- minute or daily fund flow when available
- 60 to 120 trading days of main-force or order-size flow
- northbound flow when applicable
- margin financing and securities lending
- dragon-tiger list, block trades, lockup expiry, shareholder count, dividends, and buybacks when available

### J. Company-announcement package

Load `references/evidence-packages.md` and collect:

- latest 6 to 12 months of official announcements
- periodic reports, performance previews, major contracts, M&A, incentives, buybacks, dividends, refinancing, pledges, guarantees, lawsuits, penalties, and inquiry letters
- material older announcements that still affect current valuation
- execution status: reflected in financials, pending, delayed, failed, or unclear

## Subagent requirement

If subagent tooling exists, create a dedicated research subagent during this phase.

Recommended prompt shape:

- research only the target company's sub-industry
- summarize business model, key operating KPIs, accounting quirks, common valuation anchors, and major risks
- distinguish stable principles from current-cycle facts
- provide concise notes that can be merged into the main report

If subagents are unavailable, do the same work locally.

## Valuation-anchor requirement

Load `references/valuation-anchor-framework.md` and run:

```bash
python3 scripts/check_valuation_anchor.py --sub-industry "<confirmed sub-industry>"
```

If the alias match is uncertain, use `--list` to inspect available anchor ids. If no suitable anchor exists, create a new `valuation_anchors/<anchor_id>.json` record from current evidence before phase 3.

## Source strategy

Use the following priority:

1. User-provided data, screenshots, and prior calculations
2. Structured market and financial data
3. Annual reports and official company disclosures
4. Company announcements and exchange or company IR disclosures
5. Macro-policy releases, commodity/industry data, and market-regime sources
6. Broker reports and industry public materials
7. K-line, capital-flow, chip, and event data from structured providers
8. Web search for missing or current items

For implementation notes and the user's external data project, load `data-source-strategy.md`.

## Data-quality rules

- Never mix periods inside one formula.
- Mark estimated values clearly.
- Note when trailing data, annual data, or interim data are mixed across sections.
- If a metric is unavailable for a sector, say it is not decision-useful rather than forcing it.
