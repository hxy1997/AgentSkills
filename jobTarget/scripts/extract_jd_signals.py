#!/usr/bin/env python3
"""Extract structured signals from a JD text file."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADING_PATTERNS = {
    "responsibilities": [
        r"岗位职责",
        r"工作职责",
        r"职责描述",
        r"Responsibilities",
    ],
    "requirements": [
        r"任职要求",
        r"职位要求",
        r"岗位要求",
        r"Qualifications",
        r"Requirements",
    ],
    "highlights": [
        r"加分项",
        r"优先",
        r"Plus",
        r"Preferred",
    ],
}

BUSINESS_KEYWORDS = [
    "增长",
    "商业化",
    "广告",
    "支付",
    "电商",
    "AI",
    "大模型",
    "平台",
    "出海",
    "风控",
    "供应链",
]

SENIORITY_KEYWORDS = {
    "senior": ["资深", "高级", "专家", "senior", "staff", "principal"],
    "manager": ["负责人", "manager", "lead", "主管"],
}

AMBIGUITY_SIGNALS = [
    "其他相关工作",
    "跨部门协同",
    "推动落地",
    "快速响应",
    "灵活支持",
]


def load_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return input()


def is_heading(line: str, patterns: list[str]) -> bool:
    normalized = line.strip().strip(":：")
    return any(re.fullmatch(pattern, normalized, re.IGNORECASE) for pattern in patterns)


def find_section(text: str, patterns: list[str]) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    hits = []
    active = False
    for line in lines:
        if is_heading(line, patterns):
            active = True
            continue
        if active and any(
            is_heading(line, group)
            for group in HEADING_PATTERNS.values()
        ):
            break
        if active and not line:
            continue
        if active:
            cleaned = re.sub(r"^[\-\u2022\*0-9]+[.)、 ]*", "", line).strip()
            if cleaned:
                hits.append(cleaned)
    return hits[:12]


def extract(text: str) -> dict:
    normalized = text.replace("\r\n", "\n")
    result = {
        "business_keywords": [kw for kw in BUSINESS_KEYWORDS if kw.lower() in normalized.lower()],
        "responsibilities": find_section(normalized, HEADING_PATTERNS["responsibilities"]),
        "requirements": find_section(normalized, HEADING_PATTERNS["requirements"]),
        "highlights": find_section(normalized, HEADING_PATTERNS["highlights"]),
        "seniority_signals": [],
        "ambiguity_signals": [sig for sig in AMBIGUITY_SIGNALS if sig in normalized],
    }
    for label, keywords in SENIORITY_KEYWORDS.items():
        if any(keyword.lower() in normalized.lower() for keyword in keywords):
            result["seniority_signals"].append(label)
    result["role_realism_risk"] = "medium" if result["ambiguity_signals"] else "low"
    if len(result["responsibilities"]) < 3 or len(result["requirements"]) < 3:
        result["role_realism_risk"] = "medium"
    if len(result["responsibilities"]) == 0 and len(result["requirements"]) == 0:
        result["role_realism_risk"] = "high"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract signals from a JD text file.")
    parser.add_argument("path", nargs="?", help="Path to a JD text or markdown file.")
    args = parser.parse_args()

    text = load_text(args.path)
    print(json.dumps(extract(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
