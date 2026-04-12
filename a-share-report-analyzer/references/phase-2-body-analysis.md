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
- business clarity score

### 2. 经营稳定性

Cover:

- company stage in the industry cycle
- revenue and profit volatility
- internal operating risks
- external environment sensitivity
- stability score

### 3. 定价权

Cover:

- source of pricing power
- customer positioning and stickiness
- evidence of premium pricing or weak pricing
- pricing-power score

### 4. 成长分析

Cover:

- what drove past growth
- whether those drivers are repeatable
- capacity or capability expansion
- order backlog or project reserve where relevant
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
- overall financial-quality score

## Integration rule

Do not write the industry overlay as a detached appendix. Instead:

- inject industry KPIs into the relevant section
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
