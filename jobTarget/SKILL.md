---
name: job-target
description: Analyze whether a social-hiring role is worth pursuing by combining JD analysis, resume-to-JD fit, company and business research, org and team signal assessment, workplace community sentiment, interview reverse-question design, and a final go/no-go recommendation. Use when evaluating a target job, team, or offer with materials such as a JD, resume, company context, candidate priorities, and optionally public web sources.
---

# Job Target

## Overview

Use this skill to produce a structured hiring-opportunity assessment for job switches. Default to a two-stage output:

1. Build a structured scorecard from user inputs and external evidence.
2. Render a final decision-oriented report from that scorecard.

Prefer the default `balanced` mode:

- Start from user-provided JD, resume, company or team context, and candidate priorities.
- Search the web only when core evidence is missing or needs verification.
- Distinguish facts, community anecdotes, and inference.

Support three research modes when useful:

- `offline`: do not browse; rely only on user materials.
- `balanced`: browse only for missing or high-value evidence. This is the default.
- `research`: perform broader external research and expand the evidence log.

## Required Inputs

Collect these inputs before making strong recommendations:

- JD or a faithful JD summary
- Candidate resume
- Company name and, if known, team or business line
- Candidate priorities such as compensation, growth, stability, title, tech stack, or work-life balance

If any input is missing, stop the analysis flow long enough to request or reconstruct the gap. Use [assets/missing-info-checklist.md](./assets/missing-info-checklist.md) to keep those requests short and actionable.

## Workflow

### 1. Check input completeness

- Verify which required inputs are present.
- Record missing items in the scorecard.
- If a missing item blocks reliable judgment, ask for it before continuing.

### 2. Parse the JD

- Extract business domain, seniority clues, required skills, core responsibilities, org signals, and ambiguity signals.
- Run [scripts/extract_jd_signals.py](./scripts/extract_jd_signals.py) when the JD is long or inconsistent.
- Use [references/evaluation-dimensions.md](./references/evaluation-dimensions.md) and [references/business-potential-framework.md](./references/business-potential-framework.md) to classify business potential and role realism.

### 3. Compare the resume against the JD

- Identify direct matches, transferable strengths, likely gaps, and prep priorities.
- Run [scripts/analyze_resume_gap.py](./scripts/analyze_resume_gap.py) for a first-pass keyword and signal comparison.
- Refine the result with [references/resume-jd-analysis-rules.md](./references/resume-jd-analysis-rules.md). Do not rely on keyword overlap alone.

### 4. Research company, product, and org context

- In `balanced` or `research` mode, search for company strategy, business momentum, product competitiveness, org changes, and public hiring signals.
- Prioritize official sources, earnings materials, interviews, product launches, recruiting pages, and major news coverage before community posts.
- If community sources are needed, apply [references/community-source-reliability.md](./references/community-source-reliability.md).

### 4.1 Always verify decision-changing dimensions

- Unless the user explicitly narrows scope, always evaluate these dimensions because they frequently change the recommendation:
  - actual work intensity: average end time, late meetings, oncall, weekend support, peak-season rhythm
  - HC and org stability: new headcount vs backfill, predecessor exit reason, recent reorgs, reporting line
  - work-content mix: platform building vs business requests vs firefighting vs customer delivery/support
  - AI or Agent relevance: whether it is roadmap-critical work or only an optional plus
  - performance, compensation, and commute: KPI logic, ranking pressure, compensation structure, location and commute cost
- If the evidence is unavailable, do not hide the gap. Record it explicitly and convert it into reverse-questions.
- When the candidate has strong stated priorities such as work-life balance or AI relevance, raise the weight of the matching dimensions in the final recommendation.

### 5. Separate evidence from inference

- Label each claim as `fact`, `community signal`, or `inference`.
- Downgrade confidence when evidence is sparse, stale, or single-sourced.
- If evidence is insufficient, convert the gap into interview reverse-questions instead of forcing a conclusion.

### 6. Build the scorecard

- Fill [assets/scorecard-template.md](./assets/scorecard-template.md).
- Cover all core dimensions:
  - input completeness
  - business potential
  - company and product competitiveness
  - org and team signals
  - decision-changing dimensions
  - community sentiment
  - role realism
  - candidate fit
  - growth and transferability
  - reward-to-risk ratio
  - opportunity cost
  - interview prep priorities
  - risk list
  - reverse questions
  - final recommendation

### 7. Render the final report

- Use [assets/final-report-template.md](./assets/final-report-template.md).
- Run [scripts/render_report.py](./scripts/render_report.py) if the scorecard already exists as JSON.
- End with one explicit recommendation:
  - `建议冲`
  - `可继续推进但需重点验证`
  - `谨慎推进`
  - `不建议`

## Evidence Policy

- Treat official company materials, financial filings, product launches, executive interviews, and verified hiring pages as higher confidence.
- Treat anonymous community posts as directional signals, not proof.
- Note the observation date when using time-sensitive information.
- When browsing is unavailable or blocked, say so explicitly and degrade to interview validation questions.

## Output Contract

Produce two artifacts unless the user requests otherwise:

1. A structured scorecard in Markdown or JSON using [assets/scorecard-template.md](./assets/scorecard-template.md)
2. A concise final report in Chinese using [assets/final-report-template.md](./assets/final-report-template.md)

The report should be concise, sectioned, and decision-oriented. Include concrete evidence, confidence notes, and interview prep advice. Prefer actionable judgment over generic summaries.
Always include a short section on what additional information should be collected next and how that information could change the conclusion.

## Resource Guide

- Read [references/evaluation-dimensions.md](./references/evaluation-dimensions.md) for the full evaluation frame and score meanings.
- Read [references/business-potential-framework.md](./references/business-potential-framework.md) when judging business importance, product strength, org stability, or role realism.
- Read [references/community-source-reliability.md](./references/community-source-reliability.md) when using Maimai, Nowcoder, Kanzhun, Boss, Zhihu, or forum content.
- Read [references/resume-jd-analysis-rules.md](./references/resume-jd-analysis-rules.md) when translating resume evidence into interview prep.
- Read [references/interview-question-patterns.md](./references/interview-question-patterns.md) when evidence gaps must be validated in interviews.
- Read [references/decision-rubric.md](./references/decision-rubric.md) before assigning the final recommendation.

## Scripts

- [scripts/extract_jd_signals.py](./scripts/extract_jd_signals.py): extract responsibilities, requirements, seniority, business clues, and ambiguity flags from a JD.
- [scripts/analyze_resume_gap.py](./scripts/analyze_resume_gap.py): compare a resume against JD requirements and rank likely prep priorities.
- [scripts/render_report.py](./scripts/render_report.py): render a Markdown report from a scorecard JSON file.

## Cross-Platform Notes

- `SKILL.md`, `assets/`, `references/`, and `scripts/` are platform-neutral.
- `agents/openai.yaml` is for Codex/OpenAI-style skill discovery.
- `claude/CLAUDE.md` gives Claude Code-specific invocation guidance.
- Qoder can use this skill directly from `SKILL.md` without extra metadata files.
