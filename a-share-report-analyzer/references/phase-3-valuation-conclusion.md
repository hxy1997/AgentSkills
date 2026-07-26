# Phase 3: Valuation and Conclusion

This phase turns the analysis into a valuation view and a final judgment.

## Required outputs

- valuation position summary
- script-based growth-rate estimation
- at least one primary valuation method
- one cross-check or alternative method when useful
- safety-margin discussion
- valuation impact from macro-news and policy variables when they change demand, pricing, cost, financing, discount rate, regulation, or risk appetite
- valuation impact from broker-report assumptions and material company announcements
- timing or risk adjustment from K-line, capital-flow, and chip evidence when material
- final conclusion table
- model-implied price interval

## Default sequence

### 1. Valuation position

Compute or summarize:

- current market cap
- current `PE` and `PB`
- 5-year valuation position
- 10-year valuation position

### 2. Profit-growth estimation

This step is mandatory and script-based:

- load `references/growth-methodology.md`
- run `scripts/calc_profit_growth.py`
- show the 6-method table
- show the filter rule, trimmed set, and average result
- use `weighted_compound_growth` as the default growth output in later valuation steps

Do not replace this with a free-form narrative summary.

### 3. Main valuation method

Pick the method from the fresh valuation-anchor table:

- `PE` or `PEG` for stable profit businesses
- `PB` and `ROE` logic for balance-sheet-heavy sectors
- `PS` or `EV/Sales` for early or margin-transition businesses
- `DCF` when cash-flow visibility is credible
- mixed method when no single anchor is sufficient

Show the anchor table id, `last_updated`, freshness status, primary anchor, and anchor-switch rationale. If the table is expired or missing, do not finalize valuation until it is updated or the report is labeled incomplete.

Before finalizing the main method:

- translate material macro-news and policy evidence into explicit growth, margin, multiple, discount-rate, commodity-price, or risk-premium assumptions
- load `references/macro-policy-transmission.md` when rates, real yields, FX, liquidity, commodity prices, overseas funding, or global demand materially affect valuation
- reconcile profit and growth assumptions with material official announcements
- compare the selected growth or multiple with broker-report consensus and estimate dispersion
- state whether any announcement creates a pending catalyst, execution risk, dilution risk, or regulatory risk
- do not let K-line or capital-flow data determine intrinsic value, but use it to discuss timing risk, crowding, and confidence in near-term price behavior
- do not let general macro-news heat determine intrinsic value unless the transmission path to company earnings or valuation is explicit

### 3a. Commodity and monetary-policy overlay

For commodity-driven companies, the main valuation is incomplete unless it shows or explicitly marks missing:

- current spot price
- company realized price when disclosed
- cycle-normalized bear/base/bull price deck
- attributable production and unit cost or `AISC/C1`
- taxes, royalties, minority interests, JV ownership, hedging, and FX treatment
- price sensitivity using `scripts/calc_commodity_sensitivity.py` when inputs are available

Do not use a generic discount to consensus earnings as the only normalization method.

For material monetary-policy exposure:

- show policy expectations, real yields, FX, liquidity, and the reason for the policy stance
- translate the regime through commodity/product prices, demand, financing, FX, discount rate, or risk premium
- show DCF/NAV discount-rate sensitivity when terminal value or long-life assets are material
- create a shock ledger and verify the same policy effect is not counted twice

If policy has already changed the commodity price deck, do not apply a second unexplained policy haircut to earnings. A separately disclosed discount-rate change is allowed because it changes present value.

### 4. Alternative method

Use one cross-check where possible:

- `DCF`
- peer multiple comparison
- downside case or safety-margin price
- historical median valuation method

The alternative method should normally come from `secondary_anchors`. Use `weak_or_floor_anchors` only as downside or balance-sheet support, and explain why `disabled_anchors` are not decision-useful.

### 5. Final conclusion

This step is mandatory and script-based:

- load `references/final-conclusion-logic.md`
- run `scripts/calc_valuation_zone.py`
- show `E`, `F`, `avg_dev`, `LOW`, `UP`
- classify company quality and price bucket
- output the implied market-cap interval and price interval

Summarize:

- expected return logic
- valuation gap or premium/discount
- safety margin
- whether evidence packages strengthen, weaken, or leave unchanged the valuation confidence
- whether the stock looks low, fair, or expensive under the chosen framework
- what research stance the logic matrix maps to; do not turn it into an executable order

## Financial-sector rule

For brokers, banks, and insurers:

- do not force a standard industrial-company DCF if it is not decision-useful
- prefer capital-return and balance-sheet-aware valuation discussion
- explain why the chosen anchor fits the sector

## Conflict rule

If the generic valuation anchor and the industry-preferred anchor point in different directions:

- show both
- explain the disagreement
- state which one carries more weight and why

If the fresh valuation-anchor table and the generic sector rule disagree, the fresh anchor table carries more weight unless the evidence is weak. State the confidence level and invalidation conditions.
