# Data Source Strategy

This skill is designed to work standalone by default, while still supporting the user's existing stock-analysis data workflow when explicitly requested.

## Preferred data-source order

1. Understand user-provided materials and reconcile important facts against original disclosures
2. Annual reports, official company disclosures and regulatory documents for accounting facts
3. Bundled embedded provider or connected market-data tools for quotes and structured inputs
4. Broker reports and public industry materials
5. Current web search for missing or updated items
6. An explicitly provided external project root, if the caller wants to override the embedded provider

## Market liquidity and expectations

For market liquidity and expectations, use the source matrix and comparability rules in `market-liquidity-expectations.md`: official monetary/exchange data, fund disclosures, and clearly attributed consensus estimates. The bundled stock-input scripts do not imply coverage of these series. Record observation periods, release/retrieval dates, methodology changes and availability at the research cutoff. Distinguish observed flows from vendor estimates and price-implied assumptions.

For announcements, broker reports, trading structure and chip data, use the source mapping in `evidence-packages.md`. These are collection options, not guaranteed embedded-provider coverage. For material commodity/overseas exposures, use `macro-policy-transmission.md`: reconcile market prices with realized prices, production, costs, ownership and FX. Official announcements outrank news summaries; external research opinions and target prices are not accounting facts.

## Portable embedded provider

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

Use the embedded provider or an available connector for structured collection. Verified disclosures can supply the same fields without redundant script calls. Only inspect an external project when:

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

The skill includes collection wrappers and calculation helpers:

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
  - input: profit series, actual years, optionally diluted shares or official per-share series
  - output: historical interval changes, meaningful CAGR, per-share and dilution diagnostics
  - historical description only; no six-method blend or automatic forecast
- `scripts/calc_valuation_zone.py`
  - v2 input: JSON with explicit scenarios, share_count, optional current_price and dates
  - output: scenario intrinsic values, safety-margin thresholds and price comparison
  - no G/deviation averaging or action matrix; see final-conclusion-logic.md
- `scripts/calc_commodity_sensitivity.py`
  - input: attributable production, USD price change, CNY/USD FX, profit pass-through, optional shares and multiples
  - output: conditional revenue-exposure, profit, EPS and valuation changes; not a complete company valuation
  - reconcile units, periods, ownership and hedges before using; see macro-policy-transmission.md
- `scripts/check_valuation_anchor.py`
  - input: anchor id/sub-industry and research cutoff date; optional custom anchor directory
  - output: date status for an existing method record, not validation of its sources or valuation assumptions

Preserve quote timestamps, report periods and publication dates independently. Empty or stale API results must not be labeled current. Never expose tokens in logs or reports. Prefer already installed dependencies; report unavailable providers and use official sources rather than fabricating missing fields.

These scripts are intentionally shallow. If they stop matching the embedded provider, update them directly instead of introducing more abstraction layers.
