# stockVote for Claude Code

Use this folder as a portable stock-analysis skill.

Recommended invocation pattern:
- Read `../SKILL.md`
- If the user requests role-based stock analysis, run `../scripts/run_stock_vote.py`
- Use `--json` when the result needs further machine processing

Examples:

```bash
python /Users/hexingyuan/CodeProjects/skills/stockVote/scripts/run_stock_vote.py 600519 --role balanced-analyst
python /Users/hexingyuan/CodeProjects/skills/stockVote/scripts/run_stock_vote.py 00700 --role "史诗级韭菜" --full-report
```

Environment expectations:
- Python environment must be able to import the upstream project dependencies
- Upstream repo path defaults to `/Users/hexingyuan/CodeProjects/daily_stock_analysis`
- Override via `DAILY_STOCK_ANALYSIS_PATH` or `--repo`
- If import fails on modules like `litellm`, install the upstream project's dependencies in the active interpreter first
