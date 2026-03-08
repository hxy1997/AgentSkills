# Job Target Design

## Goal

Create a skill that helps a candidate evaluate whether a target role is worth pursuing during a job switch. The skill should combine business potential, company and product competitiveness, org and team health, workplace community sentiment, candidate fit, interview preparation, and a final recommendation.

## Recommended shape

- One top-level skill named `job-target`
- Progressive disclosure through `references/`, `assets/`, and `scripts/`
- Default mode `balanced`, with `offline` and `research` variants
- Two-stage output:
  - structured scorecard
  - final decision-oriented report

## Core design choices

- Keep the orchestration logic in `SKILL.md`
- Keep evaluative heuristics in `references/`
- Keep report structures in `assets/`
- Keep deterministic parsing and rendering in `scripts/`
- Avoid forcing a single search provider; allow Tavily or other web-search backends

## Evaluation frame

The scorecard should cover:

- input completeness
- business potential
- company and product competitiveness
- org and team signals
- workplace community sentiment
- role realism
- candidate fit
- growth and transferability
- reward-to-risk ratio
- opportunity cost
- interview prep priorities
- risks
- reverse questions
- final recommendation

## Search policy

- Prefer official and high-confidence sources first
- Use community sources as directional evidence
- Convert unresolved uncertainty into reverse questions

## Iteration plan

- Run the skill on real JD and resume pairs
- Observe where evidence collection or fit analysis feels weak
- Split reusable sub-capabilities into separate skills only after repeated use proves the boundary
