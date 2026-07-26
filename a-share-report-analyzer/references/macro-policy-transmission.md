# Macro Policy and External-Variable Transmission

Load this reference when monetary policy, real yields, FX, liquidity, commodity prices, overseas financing, or global demand materially affect the company.

## Contents

- Core rule and materiality test
- Required monetary-policy evidence and interpretation
- Commodity-company workflow
- Company-level FX and financing bridge
- Valuation integration and double-counting control
- Required report output

## Core rule

Do not treat macro policy as a headline score. Build a causal chain:

`policy expectation -> market variable -> company exposure -> financial statement -> valuation`

Examples:

- `Fed repricing -> US real yield -> gold price/ETF flow -> realized gold price -> mine margin -> NAV`
- `Fed tightening -> USD and global credit -> manufacturing demand -> copper price/inventory -> mine earnings`
- `PBOC easing -> domestic credit and infrastructure -> product demand -> utilization/margin -> earnings`
- `rate shock -> funding cost and risk-free rate -> interest expense/discount rate -> DCF or multiple`

## Determine whether the overlay is material

Treat the overlay as decision-useful when at least one condition holds:

- commodity or dollar-linked revenue is a material profit driver
- exports, overseas assets, or foreign-currency debt are material
- the valuation is duration-sensitive or depends on a high terminal value
- regulated funding costs, credit creation, or asset prices drive the business model
- the current cycle contains a major policy, inflation, FX, liquidity, or geopolitical regime shift

If none applies, mark the overlay `not decision-useful` and explain why.

## Required monetary-policy evidence

Collect current and recent direction, not one isolated meeting:

- policy rate and expected path from futures, OIS, or official projections
- 2-year government yield as a policy-expectation proxy
- 10-year nominal yield
- 10-year inflation expectation or breakeven when available
- 10-year real yield, especially for gold and long-duration assets
- yield-curve shape and credit spreads when financing conditions matter
- `DXY` or the relevant bilateral exchange rate
- inflation, employment, activity, and financial-stress variables explaining the policy stance
- central-bank balance sheet and broad liquidity when material

Prefer official central-bank releases and market prices over media summaries.

## Do not use a one-line rate rule

“Rate hike bearish, rate cut bullish” is only a first approximation.

Separate:

- expected versus unexpected policy moves
- nominal rates versus real rates
- policy driven by strong demand versus supply-side inflation
- orderly tightening versus financial stress
- domestic policy versus the policy of the company's revenue and funding currencies

Gold can rise with nominal rates when inflation expectations, financial stress, reserve diversification, or geopolitical demand dominate. Copper can stay firm during tightening when mine supply is constrained. State which channel currently dominates.

## Commodity-company workflow

### 1. Separate three prices

- `spot price`: current market price
- `realized price`: company-reported selling price after timing, product mix, treatment charges, hedging, and FX
- `cycle-normalized price`: analyst price used in NAV or normalized earnings

Never use spot price as a perpetual assumption without justification.

### 2. Build a bear/base/bull price deck

For each material commodity, show:

| Field | Bear | Base | Bull |
| --- | ---:| ---:| ---:|
| commodity price | | | |
| FX | | | |
| attributable production | | | |
| unit cost / `AISC` / `C1` | | | |
| tax, royalty, minority, or pass-through assumption | | | |
| resulting profit or cash-flow impact | | | |

Derive the base price from a cycle view, cost curve, forward curve, supply-demand balance, and policy regime. Do not select it only to match the current share price.

### 3. Calculate exposure before valuation

Start with:

`revenue sensitivity = attributable production * price change * FX`

Then adjust for:

- variable cost and treatment/refining charges
- tax and royalties
- minority interests and JV ownership
- hedging
- product mix and payable-metal terms
- production response, grades, recovery, and downtime

Use `scripts/calc_commodity_sensitivity.py` when inputs are available. Treat the pass-through range as an analyst assumption, not a sourced fact.

### 4. Translate policy into the price deck

For precious metals, emphasize:

- real yields
- `DXY`
- ETF flows and central-bank purchases
- inflation expectations and financial stress

For industrial metals, emphasize:

- global manufacturing and construction demand
- China credit and infrastructure
- inventory and mine/refinery supply
- `DXY`, global liquidity, and financing conditions

For energy commodities, emphasize:

- OPEC or supply policy
- inventories, freight, weather, and geopolitical disruption
- demand and substitution

## Company-level FX and financing bridge

Map:

- revenue currencies
- operating-cost currencies
- debt and interest-payment currencies
- capex and equipment currencies
- hedging and natural offsets
- dividend and capital-repatriation constraints

Do not assume a weaker RMB is automatically positive for a dollar-linked exporter. Show the net exposure after dollar debt, imported capex, overseas costs, and tax.

## Valuation integration

Apply policy shocks through distinct channels:

1. `earnings channel`: price, volume, cost, FX, tax, and margin
2. `financing channel`: interest expense, refinancing, liquidity, and covenant risk
3. `discount-rate channel`: risk-free rate, equity-risk premium, country risk, and terminal value
4. `multiple channel`: only when market-regime evidence supports a durable repricing

For DCF or NAV, show the discount-rate sensitivity when terminal value or long-life assets are material.

## Double-counting control

Before finalizing, create a short shock ledger:

| Shock | Earnings or cash-flow change | Discount-rate change | Multiple change | Double-count check |
| --- | --- | --- | --- | --- |
| example: Fed hawkish repricing | lower gold deck | higher risk-free rate | none unless justified | pass |

Rules:

- If policy has already lowered the commodity price deck, do not apply a second generic “policy earnings haircut.”
- A separate discount-rate change is allowed because it affects present value, but disclose it.
- Do not apply both a lower normalized multiple and a higher DCF discount rate for the same risk without explaining why both are needed.
- Do not count FX translation in both realized commodity price and a separate revenue uplift.

## Required report output

When material, include:

- current monetary-policy regime and evidence cutoff
- dominant transmission variables
- company exposure map
- bear/base/bull external-variable table
- commodity or product-price sensitivity
- discount-rate and FX treatment
- double-counting check
- invalidation conditions and data gaps

If production, realized price, cost, FX, hedging, or ownership data are missing, mark the sensitivity as partial and lower valuation confidence.
