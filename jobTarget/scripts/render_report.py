#!/usr/bin/env python3
"""Render a Markdown report from a scorecard JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def get(data: dict, path: str, default: str = "待补充") -> str:
    current = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    if current in ("", None, []):
        return default
    if isinstance(current, list):
        return "；".join(str(item) for item in current)
    return str(current)


def render(data: dict) -> str:
    return f"""# 岗位分析报告

## 一、结论摘要
- 最终建议：{get(data, 'recommendation.label')}
- 一句话判断：{get(data, 'recommendation.summary')}
- 当前结论置信度：{get(data, 'recommendation.confidence')}

## 二、为什么值得考虑
- 业务潜力：{get(data, 'business_potential.summary')}
- 公司/产品竞争力：{get(data, 'competitiveness.summary')}
- 成长性与可迁移性：{get(data, 'growth.summary')}

## 三、主要风险
- 组织与团队风险：{get(data, 'org_risk.summary')}
- 岗位真实性风险：{get(data, 'role_realism.summary')}
- 口碑与工作方式风险：{get(data, 'community.summary')}
- 候选人匹配风险：{get(data, 'candidate_fit.summary')}

## 四、候选人匹配度
- 已有优势：{get(data, 'candidate_fit.strengths')}
- 关键短板：{get(data, 'candidate_fit.gaps')}
- 是否值得补齐后继续推进：{get(data, 'candidate_fit.next_step')}

## 五、面试准备建议
- 必补内容：{get(data, 'interview_prep.must_prepare')}
- 高概率追问：{get(data, 'interview_prep.likely_questions')}
- 推荐强调的经历：{get(data, 'interview_prep.stories')}

## 六、反问问题
- 问题 1：{get(data, 'reverse_questions.q1')}
- 问题 2：{get(data, 'reverse_questions.q2')}
- 问题 3：{get(data, 'reverse_questions.q3')}

## 七、下一步行动
- 继续推进前必须验证：{get(data, 'next_actions.verify')}
- 建议的面试策略：{get(data, 'next_actions.strategy')}
- 是否值得和其他机会继续比较：{get(data, 'next_actions.compare')}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a markdown report from scorecard JSON.")
    parser.add_argument("scorecard", help="Path to scorecard JSON.")
    parser.add_argument("-o", "--output", help="Output markdown path.")
    args = parser.parse_args()

    data = json.loads(Path(args.scorecard).read_text(encoding="utf-8"))
    content = render(data)
    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
