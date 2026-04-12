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

### 4. Apply sector specialization when needed

- `券商`: load `sector-broker.md`
- `银行`: load `sector-bank.md`
- `保险`: load `sector-insurance.md`
- Otherwise: load `sector-general-a-share.md`

### 5. Write the body analysis

- Use the six-block framework from `phase-2-body-analysis.md`.
- Integrate industry overlay results into each relevant section instead of appending a disconnected appendix.

### 6. Produce valuation and conclusion

- Use `phase-3-valuation-conclusion.md`.
- Choose valuation anchors that match the sub-industry logic.
- If the generic method and industry method disagree, show both and explain why.

## Hard stops

- If core data is missing and the missing item changes the conclusion, say the analysis is incomplete.
- If sector classification is uncertain, show the uncertainty before applying an overlay.
- If regulation has likely changed, verify with current sources before finalizing.
