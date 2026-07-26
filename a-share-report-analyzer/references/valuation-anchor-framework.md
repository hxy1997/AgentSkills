# Valuation Anchor Framework

Use this reference whenever phase 1 or phase 3 needs to choose valuation methods.

## Core rule

Do not hard-code valuation anchors by sector. Use a versioned sub-industry anchor table that captures the current market pricing language.

The anchor table does not replace analysis. It decides which valuation methods deserve the most weight today, and which methods should be treated only as cross-checks or asset-floor references.

## Required phase-1 check

After identifying sector and sub-industry:

1. Find the closest `valuation_anchors/*.json` record.
2. Run `scripts/check_valuation_anchor.py`.
3. If status is `ok`, use the table.
4. If status is `expired`, update the table with current sources before phase 3.
5. If status is `missing`, create a new table or mark the valuation incomplete.

Never skip this check for technology, healthcare innovation, financial, energy transition, or other fast-changing sectors.

## Default freshness windows

Use the record's `refresh_interval_days` when present. Otherwise use:

| Sector type | Freshness window |
| --- | ---:|
| Semiconductors, AI, innovative drugs, military electronics | 100 days |
| Consumer, industrial manufacturing, cyclicals | 190 days |
| Banks, utilities, telecom operators | 190 days |
| Major policy, price-cycle, or market-valuation regime change | Immediately stale |

For commodity, export, overseas, or dollar-linked businesses, treat the anchor as immediately stale when a material change in real yields, FX, global liquidity, commodity-price regime, sanctions, taxes, or country risk invalidates the prior price deck or discount rate.

## Anchor table fields

Each valuation-anchor JSON should include:

- `anchor_id`
- `display_name`
- `sector`
- `sub_industry`
- `aliases`
- `last_updated`
- `next_review_due`
- `refresh_interval_days`
- `current_cycle_state`
- `primary_anchor`
- `secondary_anchors`
- `weak_or_floor_anchors`
- `disabled_anchors`
- `anchor_switch_rationale`
- `valid_when`
- `invalid_when`
- `peer_set`
- `market_pricing_language`
- `key_cycle_indicators`
- `confidence`
- `sources`
- `analyst_notes`

## Updating a stale anchor

When an anchor is stale, research:

- current peer multiples and dispersion
- current industry cycle drivers
- whether the market is paying for revenue, orders, capacity, AI exposure, localization, normalized earnings, cash flow, or asset backing
- whether the old primary anchor is still the dominant market language
- what would invalidate the current anchor
- whether policy, real-yield, FX, liquidity, or commodity-price changes require a new price deck or discount rate

Then update:

- `last_updated`
- `next_review_due`
- `current_cycle_state`
- `primary_anchor`
- `secondary_anchors`
- `disabled_anchors`
- `anchor_switch_rationale`
- `peer_set`
- `market_pricing_language`
- `sources`

If current data cannot be verified, do not force an update. Mark the report incomplete and explain the missing evidence.

## Phase-3 usage

The valuation section must show:

- anchor table id and version date
- freshness status
- primary anchor and why it fits the current cycle
- secondary or cross-check anchor
- weak/floor anchors and why they are downgraded
- disabled anchors and why they are not decision-useful
- conditions that would make the valuation anchor stale before the next scheduled review
- material external-variable assumptions and double-counting controls when the anchor depends on commodity prices, FX, or rates

## Technology-company guidance

For technology companies, classify the business before selecting anchors:

| Type | Examples | Common current anchors |
| --- | --- | --- |
| Cyclical technology | memory, panels, some components | `PS`, `EV/Sales`, normalized `PE`, sometimes `PB` floor |
| Equipment or hard-tech manufacturing | semicap equipment, industrial automation | orders, revenue, `PE`, `PEG`, `EV/EBITDA` |
| Platform R&D | AI chips, EDA, foundational software | `PS`, SOTP, milestone value, long-term normalized earnings |
| Software or SaaS-like | industrial software, cloud | ARR/revenue multiple, Rule of 40, FCF |
| Biotech innovation | innovative drugs | rNPV, pipeline SOTP, cash runway |
| Mature technology leader | stable hardware/software leaders | `PE`, FCF, ROIC, shareholder return |

If profit history contains multiple loss years or crosses break-even, do not let `weighted_compound_growth` mechanically drive valuation. Use revenue, gross profit, normalized margin, SOTP, or current-cycle anchors, and state why profit CAGR is not decision-useful.
