# Workflow Overview

Use this workflow in order. Do not jump to valuation before the data and industry overlay are stable.

## Phase map

1. `准备数据`
2. `正文分析`
3. `估值结论`

## Workflow detail

### 1. Prepare scope

- Confirm company name and ticker.
- Confirm market is mainly `A股`. If not, note the mismatch and continue only if the user still wants the framework applied.
- Identify reporting periods to use.
- Identify sector and sub-industry.

### 2. Prepare baseline data

- Gather valuation snapshot, multi-year financials, cash flow, and shareholder-return context.
- Gather K-line/trading structure, macro-news/policy evidence, broker-report and industry-research evidence, capital-flow/chip evidence, and official announcements.
- Gather business description from annual reports, broker reports, and public industry material.
- Gather comparable-company context when available.

### 3. Mandatory industry overlay research

- This step is required for every company, not only financials.
- If subagent tooling exists, spawn one dedicated subagent for industry research.
- Keep the subagent scoped to the industry overlay task. Do not mix it with the main writing task.
- The subagent should return:
  - sub-industry business model
  - key operating indicators
  - common accounting distortions or special line items
  - common valuation anchors
  - cycle, policy, or supply-demand drivers
  - which parts of the generic framework need to be reweighted

### 3b. Mandatory evidence-package preparation

- Load `evidence-packages.md`.
- Build five package status blocks:
  - K-line and trading structure
  - macro news and policy environment
  - broker reports and industry research
  - capital-flow and chip structure
  - company announcements
- Use each package in the relevant body-analysis sections.
- If a package is missing, partial, or not decision-useful, explain the impact on confidence, scoring, and valuation.

### 3c. Conditional macro-policy transmission

- Load `macro-policy-transmission.md` when rates, real yields, FX, liquidity, commodity prices, overseas financing, or global demand materially affect the company.
- Build the chain `policy expectation -> market variable -> company exposure -> financial statement -> valuation`.
- For commodity companies, separate spot, realized, and cycle-normalized prices.
- Prepare a bear/base/bull price deck and deterministic sensitivity when exposure data is available.
- Add a double-counting check before valuation.

### 4. Mandatory valuation-anchor check

- Load `valuation-anchor-framework.md`.
- Use `scripts/check_valuation_anchor.py` to check whether the target sub-industry has a fresh versioned anchor table.
- If the anchor is missing or stale, update or create it using current sources before choosing valuation methods.
- If current sources cannot support an update, label the valuation incomplete instead of applying stale fixed logic.

### 5. Apply sector specialization when needed

- `券商`: load `sector-broker.md`
- `银行`: load `sector-bank.md`
- `保险`: load `sector-insurance.md`
- Otherwise: load `sector-general-a-share.md`

### 6. Write the body analysis

- Use the six-block framework from `phase-2-body-analysis.md`.
- Integrate industry overlay results into each relevant section instead of appending a disconnected appendix.

### 7. Produce valuation and conclusion

- Use `phase-3-valuation-conclusion.md`.
- Choose valuation anchors from the fresh sub-industry anchor table, not from a static sector rule.
- If the generic method and industry method disagree, show both and explain why.

## Hard stops

- If core data is missing and the missing item changes the conclusion, say the analysis is incomplete.
- If sector classification is uncertain, show the uncertainty before applying an overlay.
- If the valuation-anchor table is missing or stale and cannot be updated with current evidence, mark the valuation incomplete.
- If regulation has likely changed, verify with current sources before finalizing.
- If official announcements are unavailable or materially conflict with secondary sources, privilege official disclosures and mark the secondary-source conclusion uncertain.
- If K-line or capital-flow signals conflict with fundamentals, state the divergence and treat the signal as timing or risk evidence, not intrinsic-value proof.
- If macro-news or policy signals conflict with fundamentals, state whether the signal changes earnings power, valuation multiple, timing risk, or only market sentiment.
- If a commodity-driven valuation lacks a price deck or material exposure sensitivity, label the valuation incomplete or explicitly lower confidence; do not hide the gap inside a generic earnings haircut.
- If monetary policy is counted through commodity prices, FX, or demand, do not apply the same shock again as an unexplained earnings or multiple penalty.
