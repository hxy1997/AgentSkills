#!/usr/bin/env python3
"""Compare JD requirements and resume text to highlight likely fit and gaps."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STOPWORDS = {
    "and",
    "the",
    "with",
    "for",
    "in",
    "of",
    "to",
    "负责",
    "熟悉",
    "相关",
    "能力",
    "经验",
    "岗位",
    "工作",
    "1",
    "2",
    "3",
    "1.",
    "2.",
    "3.",
    "职位名称",
    "岗位职责",
    "任职要求",
    "加分项",
}


def tokenize(text: str) -> list[str]:
    cleaned = re.sub(r"[\r\n\t]+", " ", text.lower())
    parts = re.findall(r"[A-Za-z][A-Za-z0-9+#.-]{1,}", cleaned)
    return [part for part in parts if part not in STOPWORDS and len(part) > 1]


def extract_phrases(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        cleaned = re.sub(r"^[\-\u2022\*0-9]+[.)、 ]*", "", raw.strip())
        if not cleaned or cleaned in STOPWORDS:
            continue
        pieces = re.split(r"[，,；;。:：/]", cleaned)
        for piece in pieces:
            phrase = piece.strip()
            if not phrase or phrase in STOPWORDS or len(phrase) < 2:
                continue
            if phrase.lower() in STOPWORDS:
                continue
            lines.append(phrase)
    deduped = []
    seen = set()
    for item in lines:
        key = item.lower()
        if key not in seen:
            deduped.append(item)
            seen.add(key)
    return deduped[:20]


def extract_concepts(phrases: list[str]) -> list[str]:
    concepts = []
    boilerplate = [
        "负责",
        "具备",
        "熟悉",
        "能够",
        "独立",
        "推动",
        "持续",
        "优化",
        "优先",
        "以上",
        "经验",
        "产品者",
    ]
    for phrase in phrases:
        normalized = phrase
        for token in boilerplate:
            normalized = normalized.replace(token, " ")
        parts = re.split(r"[、和与及 ]+", normalized)
        for part in parts:
            candidate = part.strip(" ，,；;。:：")
            if len(candidate) < 2:
                continue
            if candidate.lower() in STOPWORDS:
                continue
            concepts.append(candidate)
    deduped = []
    seen = set()
    for item in concepts:
        key = item.lower()
        if key not in seen:
            deduped.append(item)
            seen.add(key)
    return deduped[:25]


def extract_jd_terms(text: str) -> list[str]:
    phrases = extract_phrases(text)
    concepts = extract_concepts(phrases)
    keywords = tokenize(text)
    combined = concepts + phrases + keywords
    deduped = []
    seen = set()
    for item in combined:
        normalized = item.lower()
        if normalized in seen or normalized in STOPWORDS:
            continue
        if normalized in {"岗位职责", "任职要求", "职位名称", "加分项"}:
            continue
        deduped.append(item)
        seen.add(normalized)
    return deduped[:25]


def analyze(jd_text: str, resume_text: str) -> dict:
    jd_keywords = extract_jd_terms(jd_text)
    resume_text_lower = resume_text.lower()
    resume_keywords = set(tokenize(resume_text))
    matched = []
    missing = []
    for keyword in jd_keywords:
        normalized = keyword.lower()
        if normalized in resume_text_lower or normalized in resume_keywords:
            matched.append(keyword)
        else:
            missing.append(keyword)
    matched = matched[:15]
    missing = missing[:15]
    fit = "high"
    if len(missing) > len(matched):
        fit = "medium"
    if len(missing) >= 10 and len(matched) <= 3:
        fit = "low"
    prep = missing[:5]
    return {
        "fit": fit,
        "jd_keywords": jd_keywords,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "prep_priorities": prep,
    }


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze resume to JD fit.")
    parser.add_argument("--jd", required=True, help="Path to JD text or markdown file.")
    parser.add_argument("--resume", required=True, help="Path to resume text or markdown file.")
    args = parser.parse_args()

    result = analyze(read_text(args.jd), read_text(args.resume))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
