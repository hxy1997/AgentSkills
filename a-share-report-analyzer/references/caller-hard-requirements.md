# Caller Hard Requirements

Use this block when you want strict compliance instead of a loosely structured research memo.

## Reusable strict prompt block

```text
Hard requirements:
1. Execute the full three-phase workflow in order. Do not skip any phase.
2. Follow the heading order defined by report-template.md. Do not collapse the output into a free-form summary.
3. The report must include:
   - company identification plus sector and sub-industry confirmation
   - 5-year and 10-year valuation-position table; if missing, state the missing item and its impact
   - 5-6 year financial table
   - six-method profit-growth table, filter rule, trimming process, and weighted_compound_growth
   - all six body-analysis sections, each with a score and short justification
   - 2-3 peer comparisons by default
   - one main valuation method plus one cross-check method
   - E, F, avg_dev, LOW, and UP
   - implied market-cap interval and implied price interval
   - core evidence and key risks
4. Separate facts from judgment.
5. If any key data is missing, do not skip it. Explicitly state what is missing and how it affects the conclusion.
6. Output a complete Markdown report, not an executive summary.
7. Save each report to the requested directory and return the file path.
8. Before finalizing, run a template-compliance self-check. List satisfied and missing items. If anything mandatory is still missing, continue or mark the report incomplete.
```

## Usage note

When dispatching subagents, paste the block directly into the subagent task instead of only mentioning the skill name. This materially reduces format drift.
