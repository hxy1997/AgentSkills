# Data Source Strategy

This skill is designed to work standalone by default, while still supporting the user's existing stock-analysis data workflow when explicitly requested.

## Preferred data-source order

1. User-provided screenshots, calculations, tables, and draft notes
2. Bundled scripts plus the embedded provider shipped inside this skill
3. Annual reports and official company disclosures
4. Official announcements from cninfo, exchanges, and company IR
5. Official macro-policy releases, commodity/industry data, and market-regime sources
6. Broker reports and public industry materials
7. K-line, capital-flow, chip, and event data from structured providers
8. Current web search for missing or updated items
9. An explicitly provided external project root, if the caller wants to override the embedded provider

## Embedded provider first

The skill now bundles a portable local provider so the default scripts can run without:

- absolute paths
- mutating `sys.path` toward a hard-coded local checkout
- depending on one specific workstation layout

The embedded provider keeps the same broad role split:

- local manager and failover logic in `portable_data_provider/manager.py`
- fundamental normalization in `portable_data_provider/fundamental_adapter.py`
- unified real-time schema in `portable_data_provider/realtime_types.py`

## Optional external-project override

If the caller explicitly passes `--project-root`, the wrappers may still load an external `daily_stock_analysis` checkout for compatibility.

The referenced external project has a useful separation:

- routing and fallback logic in `data_provider/base.py`
- fundamental normalization in `data_provider/fundamental_adapter.py`
- unified real-time schema in `data_provider/realtime_types.py`
- agent-facing wrappers in `src/agent/tools/`

The project is strongest in:

- market data
- A-share fundamentals
- industry and board data

It is weaker in:

- standardized broker-report extraction
- full official-announcement extraction
- complete K-line and chip-data coverage inside this skill's portable provider

So, treat `研报` as a search-and-synthesis task rather than assuming a complete structured report API exists.
Treat `公告` as an official-disclosure retrieval and reconciliation task rather than a news-summary task.
Treat `宏观新闻` as an external-variable translation task rather than a headline-summary task.
Treat `货币政策` as a market-variable research task: official decisions and projections, policy expectations, nominal and real yields, FX, liquidity, credit, and the company's exposure map.

## External reference: `simonlin1212/a-stock-data`

When the user explicitly references this project, use it as a source-design reference or as an external checkout if available. Do not make it an implicit dependency of the bundled scripts.

Useful capability mapping from the project:

- K-line and trading: `mootdx` for K-line, quote, F10, order book, and transaction data; Tencent for quote, PE, PB, market cap, turnover, limit-up/down; Baidu K-line for daily K-line with MA5/MA10/MA20.
- Macro news and policy: official central-bank, regulator, ministry, exchange, statistics, customs, industry association, and commodity-exchange releases first; reputable news and data vendors only as supplements.
- Broker reports: Eastmoney `reportapi` for company reports, Eastmoney industry reports with `qType=1`, report PDF download, Tonghuashun EPS consensus, and iwencai natural-language report search.
- Capital-flow and chips: Eastmoney `push2` and `push2his` for minute and 120-day fund flow; Eastmoney `datacenter` for dragon-tiger, lockup expiry, margin trading, block trades, shareholder count, dividends, and related event tables.
- Announcements: cninfo official announcement search with dynamic `orgId`, plus mootdx F10 announcement summaries as a secondary source.

Source-priority lessons:

- Prefer `mootdx` and Tencent for high-frequency market data when available because they are lower-throttling.
- Use Eastmoney for its unique report, flow, chip, and event data, with throttling and retry discipline.
- Use cninfo or exchange/company pages for announcements before news articles or broker summaries.
- Use official macro-policy and commodity data before media interpretation, and always state the transmission path to company variables.
- Use official central-bank releases for decisions and rationale; use current market data for expected policy paths, nominal and real yields, FX, and credit conditions.
- For commodity companies, reconcile spot and forward-market data with company realized prices, production, costs, ownership, and hedging before calculating sensitivity.
- Mark source instability when Eastmoney `push2`, `search-api`, or similar endpoints return empty data due to throttling.

## Practical usage rule

When the analysis depends heavily on structured data collection, use the embedded provider first. Only inspect an external project when:

- the user explicitly points to one
- the embedded provider lacks a required field
- you need to compare behavior against the user's custom pipeline

Good targets include:

- valuation snapshot gathering
- multi-year fundamentals
- board and industry classification
- market snapshot or peer comparison
- K-line and trading-structure package
- macro-news and policy-environment package
- broker-report and industry-report discovery
- capital-flow, chip, and event package
- official-announcement retrieval or reconciliation

## Current implementation note

Do not reintroduce hard-coded workstation paths into this skill. Keep the bundled scripts portable and cross-platform.

## Bundled thin scripts

This skill now includes two thin wrappers for repeated high-frequency actions:

- `scripts/fetch_analysis_inputs.py`
  - input: stock code, optional project root, optional fundamental budget
  - output: JSON containing quote, fundamental context, and board membership
  - default behavior: use the embedded provider
  - optional override: use `--project-root` to point at an external project
  - use when phase 1 needs a compact structured payload quickly
- `scripts/fetch_stock_universe.py`
  - input: market, token, output path
  - output: `.csv` or `.json` stock-universe file
  - use when you need to refresh a stock list without re-reading the larger project
- `scripts/fetch_peer_snapshot.py`
  - input: target code, peer codes, sector, optional supplemental metrics
  - output: normalized peer-comparison table
  - default behavior: use the embedded provider
  - optional override: use `--project-root` to point at an external project
  - use when the competition section needs baseline comparable-company data
- `scripts/calc_profit_growth.py`
  - input: multi-year profit series
  - output: 6-method growth table plus filtered, trimmed, and weighted results
  - use when the valuation step needs a fixed growth calculation instead of free-form reasoning
- `scripts/calc_valuation_zone.py`
  - input: current market cap, intrinsic value, safety value, quality score, valuation deviations
  - output: valuation-zone classification plus market-cap and price interval
  - use in the final conclusion step
- `scripts/calc_commodity_sensitivity.py`
  - input: attributable production, commodity-price move, FX, pass-through range, and optional shares/multiples
  - output: revenue, net-profit, EPS, and implied price sensitivity
  - use for commodity-driven businesses after reconciling unit, ownership, cost, tax, hedging, and FX assumptions

These scripts are intentionally shallow. If they stop matching the embedded provider, update them directly instead of introducing more abstraction layers.
