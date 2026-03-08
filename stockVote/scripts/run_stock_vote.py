#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


DEFAULT_REPO = Path("/Users/hexingyuan/CodeProjects/daily_stock_analysis")
DEFAULT_ROLE = "balanced-analyst"
ROLE_ALIASES = {
    "balanced-analyst": "balanced-analyst",
    "balanced": "balanced-analyst",
    "momentum-trader": "momentum-trader",
    "momentum": "momentum-trader",
    "epic-bagholder": "epic-bagholder",
    "史诗级韭菜": "epic-bagholder",
}
ROLE_DISPLAY = {
    "balanced-analyst": "balanced-analyst",
    "momentum-trader": "momentum-trader",
    "epic-bagholder": "史诗级韭菜",
}


@dataclass
class VoteResult:
    stock: dict[str, Any]
    role: str
    verdict: str
    vote_summary: str
    supporting_votes: list[dict[str, str]]
    opposing_votes: list[dict[str, str]]
    evidence: list[str]
    risks: list[str]
    action_conditions: list[str]
    upstream: dict[str, Any]
    data_sources: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run stockVote against daily_stock_analysis.")
    parser.add_argument("stock_code", help="Ticker or stock code")
    parser.add_argument("--role", default=DEFAULT_ROLE, help="Role name or alias")
    parser.add_argument("--repo", help="Path to daily_stock_analysis repo")
    parser.add_argument("--full-report", action="store_true", help="Request upstream full report")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    return parser.parse_args()


def resolve_repo(cli_repo: str | None) -> Path:
    repo = Path(cli_repo or os.environ.get("DAILY_STOCK_ANALYSIS_PATH") or DEFAULT_REPO)
    if not repo.exists():
        raise FileNotFoundError(f"daily_stock_analysis repo not found: {repo}")
    return repo


def normalize_role(role: str) -> str:
    normalized = ROLE_ALIASES.get(role, role)
    if normalized not in ROLE_DISPLAY:
        valid = ", ".join(sorted(ROLE_DISPLAY))
        raise ValueError(f"Unsupported role '{role}'. Valid roles: {valid}, 史诗级韭菜")
    return normalized


def load_upstream(repo: Path):
    repo_str = str(repo)
    if repo_str not in sys.path:
        sys.path.insert(0, repo_str)

    try:
        from analyzer_service import analyze_stock  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Failed to import daily_stock_analysis dependencies. "
            f"Missing module: {exc.name}. "
            "Install the upstream project's Python dependencies first."
        ) from exc

    return analyze_stock


def collect_lines(*values: Any) -> list[str]:
    lines: list[str] = []
    for value in values:
        if not value:
            continue
        if isinstance(value, str):
            for part in value.splitlines():
                text = part.strip().lstrip("-").strip()
                if text:
                    lines.append(text)
        elif isinstance(value, list):
            for item in value:
                lines.extend(collect_lines(item))
        elif isinstance(value, dict):
            for item in value.values():
                lines.extend(collect_lines(item))
    return dedupe(lines)


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def extract_sources(result: Any) -> list[str]:
    sources = collect_lines(
        getattr(result, "data_sources", ""),
        getattr(result, "model_used", ""),
        getattr(result, "search_performed", False) and "联网搜索已执行",
    )
    if not sources:
        sources.append("daily_stock_analysis/analyzer_service.analyze_stock")
    return sources


def classify_votes(result: Any, role: str) -> tuple[list[dict[str, str]], list[dict[str, str]], list[str], list[str], list[str], str]:
    support: list[dict[str, str]] = []
    oppose: list[dict[str, str]] = []

    score = getattr(result, "sentiment_score", None)
    advice = getattr(result, "operation_advice", "")
    trend = getattr(result, "trend_prediction", "")
    confidence = getattr(result, "confidence_level", "")

    if isinstance(score, int):
        if score >= 65:
            support.append({"dimension": "综合评分", "vote": "看多", "reason": f"情绪得分 {score}，处于偏强区间"})
        elif score <= 40:
            oppose.append({"dimension": "综合评分", "vote": "看空", "reason": f"情绪得分 {score}，处于偏弱区间"})
        else:
            oppose.append({"dimension": "综合评分", "vote": "中性", "reason": f"情绪得分 {score}，多空优势不明显"})

    if trend:
        if "看多" in trend:
            support.append({"dimension": "趋势判断", "vote": "看多", "reason": trend})
        elif "看空" in trend:
            oppose.append({"dimension": "趋势判断", "vote": "看空", "reason": trend})
        else:
            oppose.append({"dimension": "趋势判断", "vote": "中性", "reason": trend})

    if advice:
        if advice in {"买入", "加仓", "持有"}:
            support.append({"dimension": "上游建议", "vote": "偏多", "reason": advice})
        else:
            oppose.append({"dimension": "上游建议", "vote": "偏空", "reason": advice})

    dashboard = getattr(result, "dashboard", {}) or {}
    data_perspective = dashboard.get("data_perspective", {})
    intelligence = dashboard.get("intelligence", {})
    battle_plan = dashboard.get("battle_plan", {})

    support.extend(
        {
            "dimension": "技术/数据",
            "vote": "看多",
            "reason": line,
        }
        for line in collect_lines(data_perspective)[:2]
    )
    oppose.extend(
        {
            "dimension": "风险/情报",
            "vote": "看空",
            "reason": line,
        }
        for line in collect_lines(intelligence.get("risk_alerts"), getattr(result, "risk_warning", ""))[:3]
    )

    evidence = collect_lines(
        getattr(result, "analysis_summary", ""),
        getattr(result, "key_points", ""),
        getattr(result, "buy_reason", ""),
        data_perspective,
        intelligence.get("positive_catalysts"),
        battle_plan,
    )[:8]
    risks = collect_lines(
        getattr(result, "risk_warning", ""),
        intelligence.get("risk_alerts"),
        getattr(result, "company_highlights", ""),
    )[:6]

    action_conditions = collect_lines(
        battle_plan,
        getattr(result, "short_term_outlook", ""),
        getattr(result, "medium_term_outlook", ""),
    )[:5]

    if role == "momentum-trader":
        action_conditions = prepend_unique(
            action_conditions,
            [
                "需要确认趋势延续，不能只靠静态叙事入场",
                "若量价不能共振，优先视为观察而非追价",
            ],
        )
    elif role == "epic-bagholder":
        risks = prepend_unique(
            risks,
            [
                "先验证最强反对理由，而不是先替持仓找借口",
                "缺失数据视为风险项，不能默认按利好处理",
            ],
        )
        action_conditions = prepend_unique(
            action_conditions,
            [
                "只有在最关键证伪点被解除后，才允许进入观察名单",
                "若没有明确安全边际和退出纪律，默认不交易",
            ],
        )

    if role == "epic-bagholder":
        verdict = epic_bagholder_verdict(score, advice, risks)
    else:
        verdict = generic_verdict(score, advice, confidence)

    vote_summary = f"{count_positive(support)} 票偏多 / {count_negative(oppose)} 票偏空"
    return support, oppose, evidence, risks, action_conditions, verdict


def prepend_unique(items: list[str], prefix: list[str]) -> list[str]:
    return dedupe(prefix + items)


def count_positive(votes: list[dict[str, str]]) -> int:
    return sum(1 for vote in votes if vote["vote"] in {"看多", "偏多"})


def count_negative(votes: list[dict[str, str]]) -> int:
    return sum(1 for vote in votes if vote["vote"] in {"看空", "偏空"})


def generic_verdict(score: int | None, advice: str, confidence: str) -> str:
    if isinstance(score, int) and score >= 70:
        return f"偏多，可重点跟踪（置信度 {confidence or '中'}）"
    if isinstance(score, int) and score <= 40:
        return f"偏空，优先回避（置信度 {confidence or '中'}）"
    if advice:
        return f"{advice}，但需要结合证伪条件执行"
    return "结论中性，继续观察"


def epic_bagholder_verdict(score: int | None, advice: str, risks: list[str]) -> str:
    if risks:
        return "先不买，除非关键风险被逐项证伪"
    if isinstance(score, int) and score >= 70 and advice in {"买入", "加仓"}:
        return "勉强可看，但必须先定义退出纪律"
    return "证据不足，默认不交易"


def build_vote_result(result: Any, role: str) -> VoteResult:
    normalized_role = normalize_role(role)
    support, oppose, evidence, risks, action_conditions, verdict = classify_votes(result, normalized_role)
    stock = {
        "code": getattr(result, "code", ""),
        "name": getattr(result, "name", ""),
        "current_price": getattr(result, "current_price", None),
        "change_pct": getattr(result, "change_pct", None),
    }
    upstream = {
        "sentiment_score": getattr(result, "sentiment_score", None),
        "trend_prediction": getattr(result, "trend_prediction", ""),
        "operation_advice": getattr(result, "operation_advice", ""),
        "confidence_level": getattr(result, "confidence_level", ""),
    }
    return VoteResult(
        stock=stock,
        role=ROLE_DISPLAY[normalized_role],
        verdict=verdict,
        vote_summary=f"{count_positive(support)} 票偏多 / {count_negative(oppose)} 票偏空",
        supporting_votes=support,
        opposing_votes=oppose,
        evidence=evidence,
        risks=risks,
        action_conditions=action_conditions,
        upstream=upstream,
        data_sources=extract_sources(result),
    )


def to_markdown(vote: VoteResult) -> str:
    lines = [
        "# 个股投票结论",
        "",
        f"- 标的：{vote.stock['name']} ({vote.stock['code']})",
        f"- 角色：{vote.role}",
        f"- 最终结论：{vote.verdict}",
        f"- 投票结果：{vote.vote_summary}",
        "",
        "## 结论摘要",
        f"- 上游建议：{vote.upstream.get('operation_advice') or '未知'}",
        f"- 趋势判断：{vote.upstream.get('trend_prediction') or '未知'}",
        f"- 情绪得分：{vote.upstream.get('sentiment_score')}",
        "",
        "## 支持票",
    ]
    lines.extend(f"- {item['dimension']}：{item['vote']} | {item['reason']}" for item in vote.supporting_votes[:5])
    lines.extend(["", "## 反对票"])
    lines.extend(f"- {item['dimension']}：{item['vote']} | {item['reason']}" for item in vote.opposing_votes[:5])
    lines.extend(["", "## 关键证据"])
    lines.extend(f"- {item}" for item in vote.evidence[:6])
    lines.extend(["", "## 风险与证伪条件"])
    lines.extend(f"- {item}" for item in vote.risks[:6])
    lines.extend(["", "## 行动条件"])
    lines.extend(f"- {item}" for item in vote.action_conditions[:5])
    lines.extend(["", "## 原始分析对照"])
    lines.append(f"- 原始建议：{vote.upstream.get('operation_advice') or '未知'}")
    lines.append(f"- 原始趋势：{vote.upstream.get('trend_prediction') or '未知'}")
    lines.append(f"- 原始置信度：{vote.upstream.get('confidence_level') or '未知'}")
    lines.extend(["", "## 数据来源"])
    lines.extend(f"- {item}" for item in vote.data_sources)
    return "\n".join(lines)


def main() -> int:
    try:
        args = parse_args()
        repo = resolve_repo(args.repo)
        analyze_stock = load_upstream(repo)
        result = analyze_stock(args.stock_code, full_report=args.full_report)
        if result is None:
            raise RuntimeError(f"Upstream analysis returned no result for {args.stock_code}")

        vote_result = build_vote_result(result, args.role)
        if args.json:
            print(json.dumps(asdict(vote_result), ensure_ascii=False, indent=2))
        else:
            print(to_markdown(vote_result))
        return 0
    except Exception as exc:
        print(f"stockVote failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
