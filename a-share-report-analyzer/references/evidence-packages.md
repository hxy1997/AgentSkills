# Evidence Packages: K-line, Macro, Research, Capital, Announcements

Use these packages during phase 1 and integrate them into phase 2. They are evidence inputs, not standalone investment signals.

## Package checklist

### A. K-line and trading structure

Collect when available:

- latest close, interval return, volume, amount, turnover, amplitude, volatility
- daily K-line for at least 120 trading days; add weekly or monthly view when the business is cyclical
- MA5, MA10, MA20, MA60, MA120, and MA250 position when available
- drawdown from recent high, rebound from recent low, gap, limit-up or limit-down history
- volume-price relationship: breakout with volume, shrinkage, distribution, or failed rebound
- abnormal trading days and whether they match announcements, sector moves, or market-wide shocks

Analysis rules:

- Use K-line analysis to judge market pricing state, sentiment, liquidity, and risk timing.
- Do not use chart patterns as the primary fundamental conclusion.
- Separate source-based trading facts from inferred technical interpretation.
- If K-line data conflicts with fundamentals, state the conflict instead of forcing agreement.

### B. Macro news and policy environment

Collect when available:

- latest macro events that can affect the target's sector: interest rates, liquidity, exchange rates, inflation, fiscal or industrial policy, trade policy, tariffs, export controls, sanctions, and geopolitical shocks
- monetary-policy path and expectations: policy rate, 2-year yield, 10-year nominal and real yields, inflation expectations, yield curve, credit spreads, and central-bank liquidity when material
- sector-specific external variables: commodity prices, product price indices, freight, energy cost, inventory cycle, capacity cycle, demand indicators, policy subsidies, procurement signals, or regulation
- market-regime context: broad index trend, sector index trend, risk appetite, style rotation, credit conditions, and cross-border capital flow when relevant
- event recency and source hierarchy: official policy or central-bank release, regulator or exchange document, credible commodity/industry data, company disclosure, then news articles
- explicit transmission path from event to company variables: demand, price, cost, margin, capex, financing cost, discount rate, project execution, regulatory constraint, or valuation multiple

Analysis rules:

- Macro news is not a conclusion by itself. Use it only when it changes a financial assumption, valuation assumption, timing risk, or confidence level.
- Load `macro-policy-transmission.md` when monetary policy, real yields, FX, liquidity, commodity prices, overseas funding, or global demand are material.
- Do not reduce central-bank analysis to “rate hike bearish / rate cut bullish.” Separate expectations from surprises, nominal from real rates, and demand-driven tightening from supply-shock inflation or financial stress.
- Separate durable macro drivers from short-lived market noise.
- For commodity and cyclical companies, separate spot, realized, and normalized prices; translate macro news into a bear/base/bull price deck, cost curve, inventory, and cycle-position assumptions.
- When production exposure is available, calculate commodity-price sensitivity and state the pass-through assumptions for cost, tax, royalties, minority interests, JV ownership, hedging, and FX.
- For export, overseas, or dollar-linked companies, include FX, trade policy, sanctions, and geopolitical risk when material.
- Map revenue, cost, debt, interest, and capex currencies before calling currency appreciation or depreciation positive or negative.
- For financial companies, translate macro news into NIM, credit cost, capital markets activity, solvency, or investment-yield assumptions.
- If macro news conflicts with company fundamentals, state whether the conflict is a timing issue, a valuation-multiple issue, or a real change in earnings power.
- Maintain a shock ledger. Do not count the same policy shock once through commodity/product prices and again through an unexplained earnings haircut or multiple penalty.

### C. Broker reports and industry research

Collect when available:

- latest individual-company reports: title, institution, analyst, publish date, rating, target price, EPS forecast, valuation method
- latest industry reports for the confirmed sub-industry: demand, supply, price cycle, policy, competitive structure, valuation anchors
- consensus expectation changes and major estimate-revision direction
- key assumptions behind bullish, neutral, and bearish reports
- original PDFs or official report pages when possible

Analysis rules:

- Treat broker reports as sourced opinions, not facts.
- Compare report assumptions against the company's disclosed financials and announcements.
- Highlight estimate dispersion, stale reports, and sell-side incentive bias.
- Use industry reports to strengthen the sub-industry overlay and valuation-anchor update.

### D. Capital-flow and chip structure

Collect when available:

- intraday or minute-level fund flow: main-force, super-large, large, medium, and small order net inflow
- 60 to 120 trading days of daily fund flow
- northbound flow when applicable and source quality is acceptable
- margin financing and securities lending: balance, purchase, repayment, and trend
- dragon-tiger list records, top buy/sell seats, institution seats, and reasons
- block trades: date, price, volume, premium or discount, buyer and seller departments
- lockup expiry: historical and next 90 days
- shareholder count, quarter-over-quarter change, and average holding per account
- dividend and buyback records when relevant to capital return

Analysis rules:

- Use capital-flow data to assess crowding, short-term pressure, liquidity, and chip concentration.
- Do not equate short-term inflow with intrinsic value.
- For small caps, refinancing, lockup expiry, pledges, and block trades may materially change risk scoring.
- If data comes from sources with known throttling or missing periods, say so.

### E. Company announcements

Collect when available:

- latest 6 to 12 months of official announcements, plus older announcements that are material to current valuation
- periodic reports, performance previews, earnings express reports, and audit-opinion changes
- major contracts, orders, capacity expansion, M&A, asset sales, equity incentives, buybacks, dividends
- pledges, guarantees, lawsuits, investigations, penalties, regulatory inquiry letters, related-party transactions
- share issuance, convertible bonds, refinancing, employee stock ownership plans, and lockup changes

Analysis rules:

- Treat official announcements as primary-source facts.
- Reconcile announcement claims with later execution data and financial statements.
- Mark whether each announcement is already reflected in price, still pending, or failed to materialize.
- Put material unresolved announcements into key risks or catalysts.

## Source strategy inspired by `simonlin1212/a-stock-data`

Use the external project as a reference or explicit override, not as an implicit hard dependency.

Preferred source mapping:

- K-line and trading: `mootdx`, Tencent quote, Baidu K-line
- macro news and policy: official central-bank/regulator/ministerial releases, government-bond and real-yield market data, exchange notices, industry association data, commodity exchanges, customs and statistics releases, company IR, then reputable news sources
- broker reports: Eastmoney `reportapi`, industry reports with `qType=1`, PDF download, Tonghuashun EPS consensus, iwencai natural-language report search
- capital-flow and chips: Eastmoney `datacenter`, `push2`, `push2his`, dragon-tiger, lockup expiry, margin trading, block trade, shareholder count
- announcements: cninfo official announcements with dynamic `orgId`; exchange or company IR pages as fallback

Operational notes:

- Prefer stable low-throttling sources for high-frequency quote and K-line data.
- Use Eastmoney mainly for data it uniquely provides, and apply throttling/retry discipline.
- If a field is unavailable from the embedded provider, either use current web research or an explicit external-project checkout.
- Do not silently substitute news for official announcements or broker-report summaries for PDF content.
- Do not silently substitute general macro headlines for a company-specific transmission path.

## Missing-data handling

For each package, report one of:

- `complete`: enough data for normal analysis
- `partial`: enough for directional analysis, with missing fields listed
- `missing`: unavailable; explain whether the report conclusion is still usable
- `not decision-useful`: structurally irrelevant to the sector or current question

When a package is `partial` or `missing`, explain impact on confidence, scoring, and valuation.
