# Data Source Strategy

This skill is designed to work with the user's existing stock-analysis data workflow when available.

## Preferred data-source order

1. User-provided screenshots, calculations, tables, and draft notes
2. The user's structured data project at `H:\Project\PyProject\daily_stock_analysis`
3. Annual reports and official company disclosures
4. Broker reports and public industry materials
5. Current web search for missing or updated items

## How to use the external project

The referenced project already has a useful separation:

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

So, treat `研报` as a search-and-synthesis task rather than assuming a complete structured report API exists.

## Practical usage rule

When the analysis depends heavily on structured data collection, consider spawning a separate subagent to inspect the external project and summarize the most relevant scripts or modules for the target company.

Good targets include:

- valuation snapshot gathering
- multi-year fundamentals
- board and industry classification
- market snapshot or peer comparison

## Current implementation note

Do not copy the entire external project into this skill by default. Reuse it as a reference source and only extract thin wrappers later if repeated usage proves necessary.

## Bundled thin scripts

This skill now includes two thin wrappers for repeated high-frequency actions:

- `scripts/fetch_analysis_inputs.py`
  - input: stock code, optional project root, optional fundamental budget
  - output: JSON containing quote, fundamental context, and board membership
  - use when phase 1 needs a compact structured payload quickly
- `scripts/fetch_stock_universe.py`
  - input: market, token, output path
  - output: `.csv` or `.json` stock-universe file
  - use when you need to refresh a stock list without re-reading the larger project
- `scripts/fetch_peer_snapshot.py`
  - input: target code, peer codes, sector, optional supplemental metrics
  - output: normalized peer-comparison table
  - use when the competition section needs baseline comparable-company data
- `scripts/calc_profit_growth.py`
  - input: multi-year profit series
  - output: 6-method growth table plus filtered, trimmed, and weighted results
  - use when the valuation step needs a fixed growth calculation instead of free-form reasoning
- `scripts/calc_valuation_zone.py`
  - input: current market cap, intrinsic value, safety value, quality score, valuation deviations
  - output: valuation-zone classification plus market-cap and price interval
  - use in the final conclusion step

These scripts are intentionally shallow. If they stop matching the external project, update them directly instead of introducing more abstraction layers.
