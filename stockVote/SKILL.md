---
name: stock-vote
description: Reuse daily_stock_analysis data and single-stock analysis to produce role-based stock verdicts. Use when the user wants a stock analyzed through predefined personas such as balanced analyst, momentum trader, or 史诗级韭菜.
---

# Stock Vote

This skill turns `/Users/hexingyuan/CodeProjects/daily_stock_analysis` into a reusable, role-based stock analysis workflow.

Use this skill when the user wants:
- A single stock analyzed with a predefined role or persona
- The original `daily_stock_analysis` result rewritten into a voting-style verdict
- A compact decision memo with supporting evidence, objections, risks, and action conditions

## Inputs

Expected inputs:
- `stock_code`: stock ticker or code such as `600519`, `AAPL`, `00700`
- `role`: one of `balanced-analyst`, `momentum-trader`, `epic-bagholder`, or `史诗级韭菜`
- `full_report`: optional, defaults to `false`
- `output_format`: optional, `markdown` by default, `json` supported

## Default Workflow

1. Reuse `/Users/hexingyuan/CodeProjects/daily_stock_analysis/analyzer_service.py` and call `analyze_stock()`.
2. Extract structured evidence from the returned `AnalysisResult`.
3. Apply the requested role lens.
4. Emit a voting-style report using the format in `references/output-format.md`.

Do not reimplement the upstream data-fetch layer unless the user explicitly asks to decouple it later.

## Roles

Read `references/roles.md` before writing the final report.

Role selection guidance:
- `balanced-analyst`: default neutral synthesis
- `momentum-trader`: trend, price action, catalyst and timing first
- `epic-bagholder` or `史诗级韭菜`: skeptical, safety-margin-first, aggressively seeks disconfirming evidence

## Script Entry Point

Use the bundled script:

```bash
python /Users/hexingyuan/CodeProjects/skills/stockVote/scripts/run_stock_vote.py 600519 --role balanced-analyst
```

JSON output:

```bash
python /Users/hexingyuan/CodeProjects/skills/stockVote/scripts/run_stock_vote.py AAPL --role "史诗级韭菜" --json
```

The script automatically adds `/Users/hexingyuan/CodeProjects/daily_stock_analysis` to `sys.path`. Override with:
- `--repo /custom/path/to/daily_stock_analysis`
- or env var `DAILY_STOCK_ANALYSIS_PATH`

## Environment Prerequisites

- The Python interpreter used for `run_stock_vote.py` must be able to import the upstream project's dependencies.
- In the current workspace, a missing dependency such as `litellm` will prevent runtime execution until the upstream environment is installed.
- Prefer running this skill inside the same virtualenv or interpreter used by `daily_stock_analysis`.

## Output Rules

- Always separate supporting evidence from opposing evidence.
- Always include risks and invalidation conditions.
- Always show the upstream recommendation for comparison.
- For `史诗级韭菜`, list reasons not to buy before reasons to consider buying.

## Cross-Platform Notes

- `SKILL.md`, `scripts/`, `references/`, and `templates/` are platform-neutral.
- `agents/openai.yaml` is for Codex/OpenAI-style skill discovery.
- `claude/CLAUDE.md` gives Claude Code-specific invocation guidance.
- Qoder can use this skill directly from `SKILL.md` without extra metadata files.
