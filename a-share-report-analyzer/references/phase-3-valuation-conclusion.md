# Phase 3: Valuation and Conclusion

This phase turns the analysis into a valuation view and a final judgment.

## Required outputs

- valuation position summary
- script-based growth-rate estimation
- at least one primary valuation method
- one cross-check or alternative method when useful
- safety-margin discussion
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

Pick the method that matches the sub-industry:

- `PE` or `PEG` for stable profit businesses
- `PB` and `ROE` logic for balance-sheet-heavy sectors
- `PS` or `EV/Sales` for early or margin-transition businesses
- `DCF` when cash-flow visibility is credible
- mixed method when no single anchor is sufficient

### 4. Alternative method

Use one cross-check where possible:

- `DCF`
- peer multiple comparison
- downside case or safety-margin price
- historical median valuation method

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
- whether the stock looks low, fair, or expensive under the chosen framework
- what action the logic matrix maps to

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
