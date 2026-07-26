# Final Conclusion Logic

Use this reference together with `scripts/calc_valuation_zone.py`.

## Required variables

- `M`: current market cap
- `B`: intrinsic market cap
- `C`: safety-margin market cap
- `G`: company-quality coefficient, defined as `clamp(weighted_score_10 / 10, 0.4, 1.0)`
- `dev_5y`: 5-year valuation deviation
- `dev_10y`: 10-year valuation deviation

## Fixed formulas

- `E = (M - B) / B`
- `F = (M - C) / C`
- `avg_dev = mean([dev_5y, dev_10y, E, F])`
- `LOW = -0.18 / G`
- `UP = 0.18 * G`

## Company quality buckets

- `G >= 0.8`: `好公司`
- `0.6 < G < 0.8`: `中公司`
- `G <= 0.6`: `差公司`

## Price buckets

- `avg_dev < LOW`: `低价`
- `LOW <= avg_dev <= UP`: `中价`
- `avg_dev > UP`: `高价`

## Research-stance mapping

| 公司质量 | 低价 | 中价 | 高价 |
| --- | --- | --- | --- |
| 好公司 | 估值偏低，组合增配复核 | 估值合理，维持复核 | 估值偏高，等待复核 |
| 中公司 | 估值偏低，谨慎复核 | 估值合理，中性复核 | 估值偏高，降配复核 |
| 差公司 | 高风险观察 | 质量风险复核 | 高风险降配复核 |

This is a research stance, not an executable trade instruction. Portfolio actions require the separate portfolio strategy engine, current weights, risk constraints, and user review.

## Price interval

After calculating `avg_dev`, `LOW`, and `UP`, convert the zone into a market-cap and price interval:

- `lower_factor = (1 + LOW) / (1 + avg_dev)`
- `upper_factor = (1 + UP) / (1 + avg_dev)`
- `lower_market_cap = M * lower_factor`
- `upper_market_cap = M * upper_factor`
- `lower_price = current_price * lower_factor`
- `upper_price = current_price * upper_factor`

## Output requirement

The final conclusion must show:

- expected return logic
- `E`, `F`, `avg_dev`, `LOW`, `UP`
- company-quality bucket
- price bucket
- research stance
- model-implied market-cap interval
- model-implied price interval
