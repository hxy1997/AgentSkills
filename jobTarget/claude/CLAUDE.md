# jobTarget for Claude Code

Use this folder as a reusable job-opportunity evaluation skill.

Recommended invocation pattern:

- Read `../SKILL.md`
- If the user provides a JD, resume, company context, and candidate priorities, build a scorecard first
- Then render a concise Chinese decision report
- When evidence is missing, convert it into reverse-questions instead of guessing

Priority checks for this skill:

- actual work intensity
- HC type and org stability
- work-content mix
- AI or Agent relevance
- performance, compensation, and commute

Expected outputs:

- one scorecard artifact
- one final report artifact

If web evidence is used:

- separate `fact`, `community signal`, and `inference`
- prefer official sources before community posts
- record observation dates for time-sensitive claims
