#!/usr/bin/env python3
"""Check freshness of versioned valuation-anchor tables."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_REFRESH_INTERVAL_DAYS = 100


def parse_date(raw: str) -> date:
    return datetime.strptime(raw, "%Y-%m-%d").date()


def default_anchors_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "valuation_anchors"


def load_anchor(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    payload["_path"] = str(path)
    return payload


def iter_anchors(anchors_dir: Path) -> Iterable[Dict[str, Any]]:
    if not anchors_dir.exists():
        return []
    anchors: List[Dict[str, Any]] = []
    for path in sorted(anchors_dir.glob("*.json")):
        if path.name == "index.json":
            continue
        anchors.append(load_anchor(path))
    return anchors


def normalize_alias(raw: str) -> str:
    return raw.strip().lower().replace(" ", "").replace("-", "_")


def match_anchor(
    anchors: Iterable[Dict[str, Any]], *, anchor_id: Optional[str] = None, sub_industry: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    wanted_id = normalize_alias(anchor_id) if anchor_id else None
    wanted_alias = normalize_alias(sub_industry) if sub_industry else None

    for anchor in anchors:
        ids = [anchor.get("anchor_id", ""), anchor.get("display_name", ""), anchor.get("sub_industry", "")]
        ids.extend(anchor.get("aliases", []))
        normalized = {normalize_alias(str(item)) for item in ids if item}
        if wanted_id and wanted_id in normalized:
            return anchor
        if wanted_alias and wanted_alias in normalized:
            return anchor
    return None


def check_anchor_freshness(anchor: Dict[str, Any], as_of: date) -> Dict[str, Any]:
    last_updated = parse_date(anchor["last_updated"])
    refresh_days = int(anchor.get("refresh_interval_days") or DEFAULT_REFRESH_INTERVAL_DAYS)
    due_raw = anchor.get("next_review_due")
    next_review_due = parse_date(due_raw) if due_raw else last_updated + timedelta(days=refresh_days)
    age_days = (as_of - last_updated).days
    stale_by_age = age_days > refresh_days
    stale_by_due = as_of > next_review_due
    expired = stale_by_age or stale_by_due

    return {
        "status": "expired" if expired else "ok",
        "anchor_id": anchor.get("anchor_id"),
        "display_name": anchor.get("display_name"),
        "sub_industry": anchor.get("sub_industry"),
        "last_updated": anchor.get("last_updated"),
        "next_review_due": next_review_due.isoformat(),
        "as_of_date": as_of.isoformat(),
        "age_days": age_days,
        "refresh_interval_days": refresh_days,
        "primary_anchor": anchor.get("primary_anchor"),
        "secondary_anchors": anchor.get("secondary_anchors", []),
        "weak_or_floor_anchors": anchor.get("weak_or_floor_anchors", []),
        "disabled_anchors": anchor.get("disabled_anchors", []),
        "confidence": anchor.get("confidence"),
        "path": anchor.get("_path"),
        "action_required": "update_anchor_before_valuation" if expired else "use_anchor",
    }


def build_missing_payload(anchor_id: Optional[str], sub_industry: Optional[str], as_of: date) -> Dict[str, Any]:
    return {
        "status": "missing",
        "anchor_id": anchor_id,
        "sub_industry": sub_industry,
        "as_of_date": as_of.isoformat(),
        "action_required": "create_anchor_before_valuation",
    }


def list_payload(anchors: Iterable[Dict[str, Any]], as_of: date) -> Dict[str, Any]:
    rows = []
    for anchor in anchors:
        rows.append(check_anchor_freshness(anchor, as_of))
    return {"status": "list", "as_of_date": as_of.isoformat(), "anchors": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check valuation-anchor freshness.")
    parser.add_argument("--anchor-id", help="Exact or alias anchor id, such as semiconductor_memory")
    parser.add_argument("--sub-industry", help="Sub-industry alias to match against anchor aliases")
    parser.add_argument("--anchors-dir", type=Path, default=default_anchors_dir())
    parser.add_argument("--as-of-date", default=date.today().isoformat())
    parser.add_argument("--list", action="store_true", help="List all anchors and freshness statuses")
    args = parser.parse_args()

    as_of = parse_date(args.as_of_date)
    anchors = list(iter_anchors(args.anchors_dir))

    if args.list:
        print(json.dumps(list_payload(anchors, as_of), ensure_ascii=False, indent=2))
        return 0

    if not args.anchor_id and not args.sub_industry:
        parser.error("one of --anchor-id, --sub-industry, or --list is required")

    anchor = match_anchor(anchors, anchor_id=args.anchor_id, sub_industry=args.sub_industry)
    if anchor is None:
        print(json.dumps(build_missing_payload(args.anchor_id, args.sub_industry, as_of), ensure_ascii=False, indent=2))
        return 2

    payload = check_anchor_freshness(anchor, as_of)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if payload["status"] == "expired" else 0


if __name__ == "__main__":
    raise SystemExit(main())
