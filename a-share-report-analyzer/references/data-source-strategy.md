# Data Source Strategy

This skill is designed to work standalone by default, while still supporting the user's existing stock-analysis data workflow when explicitly requested.

## Preferred data-source order

1. User-provided screenshots, calculations, tables, and draft notes
2. Bundled scripts plus the embedded provider shipped inside this skill
3. Annual reports and official company disclosures
4. Broker reports and public industry materials
5. Current web search for missing or updated items
6. An explicitly provided external project root, if the caller wants to override the embedded provider

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

So, treat `研报` as a search-and-synthesis task rather than assuming a complete structured report API exists.

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

These scripts are intentionally shallow. If they stop matching the embedded provider, update them directly instead of introducing more abstraction layers.
