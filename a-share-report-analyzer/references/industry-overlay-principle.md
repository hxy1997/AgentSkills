# Industry Overlay Principle

This is a hard rule for the whole skill.

## Core principle

Use `通用框架 + 行业叠加`, not `通用框架` alone and not `只有行业故事`.

That means:

1. Start with the standard company-analysis base.
2. Identify what is special about the target sub-industry.
3. Reweight the framework with industry-specific metrics, risks, and valuation anchors.

## Why this is mandatory

The same reported numbers mean different things in different sectors.

Examples:

- `半导体设备` often needs order visibility, localization progress, customer capex cycle, and R&D strength.
- `云服务` often needs recurring revenue quality, retention, customer economics, and operating-leverage path.
- `消费品` may require brand power, channel health, and repeat-purchase quality.
- `银行`, `券商`, and `保险` require regulatory-capital and balance-sheet logic.

## Required overlay questions

For every sub-industry, answer these before final judgment:

- What truly drives revenue and profit in this industry?
- Which metrics are most predictive?
- Which accounting lines can mislead a generic reader?
- What valuation anchors are commonly used and why?
- What cycle, policy, or supply-demand factors dominate the narrative?
- Which parts of the generic framework should carry more or less weight?

## Subagent policy

If a subagent tool exists, use it for this overlay research by default.

Why:

- the task is parallelizable
- it keeps the main analyst focused on synthesis
- it reduces context crowding in the main thread

Recommended pattern:

- main agent: prepare baseline financial and company data
- subagent: research the target sub-industry's analysis and valuation principles
- main agent: integrate the subagent output into the report

If the environment has no subagent support, perform the same workflow locally.
