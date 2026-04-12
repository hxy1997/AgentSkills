# Growth Methodology

Use this reference together with `scripts/calc_profit_growth.py`.

## Mandatory method set

Always calculate profit-growth estimates with these six methods:

1. 线性回归增长率法
2. 中位数增长率法
3. 指数平滑法 (`alpha = 0.5`)
4. 加权移动平均法
5. Theil-Sen 稳健回归法
6. 分位数回归法 (`q = 0.4`)

## Fixed formulas

### Profit CAGR

Use:

- `profit_cagr = (last_profit / first_profit)^(1/(n-1)) - 1`

### Linear regression growth

- Fit a least-squares line on the profit series.
- Convert the slope into a growth rate by dividing it by average profit.

### Median growth

- Compute period-over-period profit growth rates.
- Use the median of these growth rates.

### Exponential smoothing

- Use simple exponential smoothing with `alpha = 0.5`.
- Convert the final smoothed profit level into an average growth rate by comparing it with the first-period profit across the observed intervals.

### Weighted moving average

- Use period-over-period profit growth rates.
- Use fixed weights: `[0.1, 0.15, 0.2, 0.25, 0.3]`.
- If the sample is shorter than five intervals, align to the tail and renormalize the used weights.

### Theil-Sen

- Compute all pairwise slopes on the profit series.
- Use the median slope.
- Convert slope into a growth rate by dividing it by average profit.

### Quantile regression

- Fit a quantile regression to the period-over-period profit growth rates.
- Use `q = 0.4`.
- Use the fitted slope as the method result.

## Fixed filtering rule

1. Drop any method result with `abs(result) > 50%`.
2. If valid results count is at least 4, remove the maximum and minimum values once each.
3. Average the remaining values to get `estimated_avg_profit_growth`.
4. Combine `estimated_avg_profit_growth` with `profit_cagr` using equal weights:
   - `weighted_compound_growth = (profit_cagr + estimated_avg_profit_growth) / 2`

## Output requirements

Always show:

- the 6-method table
- the filtered results
- the trimmed results
- `estimated_avg_profit_growth`
- `profit_cagr`
- `weighted_compound_growth`

If the script fails because the series contains zero or negative profit values, say so and explain which methods become unreliable.
