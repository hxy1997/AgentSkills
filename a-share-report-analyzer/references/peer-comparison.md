# Peer Comparison

Use this reference together with `scripts/fetch_peer_snapshot.py`.

## Minimum rule

- Always provide at least 1 peer.
- Default target is 2 to 3 peers.
- Always output a comparison table, not just narrative.

## Selection rule

Prefer peers that are:

- direct business-model competitors
- likely industry leaders or high-quality comparables
- listed and observable in the same market context where possible

## Field sets

### General companies

- `market_cap`
- `pe`
- `pb`
- `roe`
- `revenue_yoy`
- `net_profit_yoy`

### Banks

- `market_cap`
- `pb`
- `roe`
- `nim`
- `npl_ratio`
- `provision_coverage`
- `cet1_ratio`

### Brokers

- `market_cap`
- `pb`
- `roe`
- `ib_rank`
- `institutional_revenue_share`
- `risk_coverage_ratio`

### Insurers

- `market_cap`
- `pb`
- `roe`
- `combined_ratio`
- `solvency_ratio`
- `investment_yield`

## Data rule

- Use `scripts/fetch_peer_snapshot.py`, an available market-data connector, or official disclosures for baseline fields; do not repeat calls when equivalent verified data already exists.
- If sector-specific fields are not available, supplement them from current disclosures or reliable public sources.
- Mark supplemented fields clearly if they come from manual or web-collected inputs.
- Compare like periods and share classes. Mark annualized versus unannualized ROE, ordinary versus total equity, trailing versus forecast earnings, and differing regulatory measurement methods. Do not rank incomparable figures as if they were equivalent.

## Interpretation rule

After the table, explain:

- where the target is stronger
- where the target is weaker
- whether the market is already pricing those differences

Do not let the competition section end with only qualitative statements.
