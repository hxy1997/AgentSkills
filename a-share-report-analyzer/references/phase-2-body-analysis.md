# Phase 2: Body Analysis

This phase produces the main narrative analysis. Use the fixed six-block structure below unless the user asks for a different order.

## Six required sections

1. `业务及产品清晰度`
2. `经营稳定性`
3. `产品定价权及定价权种类`
4. `成长分析`
5. `行业竞争度`
6. `财务质量分析`

## Section rules

### 1. 业务及产品清晰度

Cover:

- main products or services
- industry development logic and cycle attribute
- business model and main profit sources
- capital or working-capital pattern
- material announcements that clarify or change the business structure
- broker-report consensus and disagreement about the business model
- business clarity score

### 2. 经营稳定性

Cover:

- company stage in the industry cycle
- revenue and profit volatility
- internal operating risks
- external environment sensitivity
- macro-news and policy sensitivity, including rates, FX, commodity prices, demand cycle, regulation, and geopolitical shocks when material
- when decision-useful, distinguish policy expectations, real yields, FX, liquidity, and demand effects instead of using a one-line rate rule
- K-line volatility, drawdown, liquidity, and abnormal-trading evidence
- capital-flow and chip-pressure evidence, especially lockup expiry, margin pressure, and block trades
- stability score

### 3. 定价权

Cover:

- source of pricing power
- customer positioning and stickiness
- evidence of premium pricing or weak pricing
- macro or policy variables that change price power, such as commodity price cycle, tariffs, subsidies, price controls, procurement policy, or capacity restrictions
- for price-taking commodity companies, separate external benchmark pricing from cost-curve, grade, recovery, and product-mix advantages
- announcement or report evidence that supports or contradicts pricing power
- pricing-power score

### 4. 成长分析

Cover:

- what drove past growth
- whether those drivers are repeatable
- capacity or capability expansion
- order backlog or project reserve where relevant
- macro or policy catalysts that change demand runway, financing conditions, project execution, or valuation duration
- for commodity-driven growth, separate volume growth from commodity-price inflation and show whether the price assumption is spot, realized, or cycle-normalized
- broker-report EPS forecast direction and estimate dispersion
- company announcements about orders, capacity, projects, M&A, incentives, or guidance
- growth sustainability coefficient when useful
- growth score

For the quantitative growth block:

- load `references/growth-methodology.md`
- run `scripts/calc_profit_growth.py`
- show the six-method result table
- show the filtering, trimming, and averaging process
- use `weighted_compound_growth` as the default growth output unless the sector clearly requires another anchor

### 5. 行业竞争度

Cover:

- industry rivalry
- concentration and market position
- substitutes and barriers to entry
- main competitors
- industry-report evidence about supply-demand, price cycle, and valuation anchors
- macro-policy evidence that changes industry supply-demand balance, entry barriers, or cross-border competition
- monetary-policy and FX evidence when they change global demand, financing, inventories, or the cost of capital
- competition score

Hard requirements:

- load `references/peer-comparison.md`
- provide at least one peer, defaulting to two to three peers
- output a comparison table
- use `scripts/fetch_peer_snapshot.py` for baseline structured fields when possible
- supplement sector-specific metrics when the baseline script does not provide them

The competition score must be justified using the comparison table, not only narrative language.

### 6. 财务质量分析

Start from the generic financial-quality framework, then apply the industry overlay.

At minimum assess:

- asset quality
- profit quality
- cash-flow quality
- financial-statement consistency or red flags
- announcement-driven red flags: pledges, guarantees, lawsuits, inquiry letters, penalties, related-party transactions, refinancing, or audit changes
- capital-flow/chip signals that may affect short-term financial risk, such as margin balance jumps, lockup expiry, and concentrated block trades
- overall financial-quality score

## Integration rule

Do not write the industry overlay as a detached appendix. Instead:

- inject industry KPIs into the relevant section
- inject K-line, macro-news/policy, research-report, capital-flow/chip, and announcement evidence into the section where it changes the judgment
- inject the external-variable dependency map and shock ledger when monetary policy, FX, liquidity, or commodity prices materially affect the company
- change metric weights when the sector demands it
- explain why the generic method is insufficient

Examples:

- Manufacturing may need inventory turns, capex intensity, and utilization.
- SaaS or cloud may need recurring revenue, retention, and operating leverage.
- Semicap may need orders, localization, and cycle timing.
- Financial firms need sector-specific asset-liability and regulatory analysis.

## Writing standard

- Every score should have short justification.
- Use data first, judgment second.
- State both upside logic and fragility points.
