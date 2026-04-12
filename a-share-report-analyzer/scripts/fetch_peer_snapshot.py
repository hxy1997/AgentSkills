#!/usr/bin/env python3
"""Build normalized peer-comparison tables for the analyzer skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional


DEFAULT_PROJECT_ROOT = Path(r"H:\Project\PyProject\daily_stock_analysis")

FIELD_SETS = {
    "general": ["market_cap", "pe", "pb", "roe", "revenue_yoy", "net_profit_yoy"],
    "bank": ["market_cap", "pb", "roe", "nim", "npl_ratio", "provision_coverage", "cet1_ratio"],
    "broker": ["market_cap", "pb", "roe", "ib_rank", "institutional_revenue_share", "risk_coverage_ratio"],
    "insurance": ["market_cap", "pb", "roe", "combined_ratio", "solvency_ratio", "investment_yield"],
}


def load_manager(project_root: Path):
    project_root = Path(project_root).resolve()
    if not project_root.exists():
        raise RuntimeError(f"External project root not found: {project_root}")
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    try:
        from data_provider import DataFetcherManager
    except Exception as exc:
        raise RuntimeError(
            f"Failed to import DataFetcherManager from project root {project_root}: {exc}"
        ) from exc
    return DataFetcherManager()


def compact_quote(quote):
    if quote is None:
        return {}
    return {
        "market_cap": getattr(quote, "total_mv", None),
        "pe": getattr(quote, "pe_ratio", None),
        "pb": getattr(quote, "pb_ratio", None),
    }


def build_payload(manager, stock_code: str, budget_seconds: float = 1.5):
    payload = {
        "stock_code": stock_code,
        "name": None,
        "quote": compact_quote(manager.get_realtime_quote(stock_code)),
        "fundamental_context": manager.get_fundamental_context(stock_code, budget_seconds=budget_seconds),
    }
    if hasattr(manager, "get_stock_name"):
        try:
            payload["name"] = manager.get_stock_name(stock_code)
        except Exception:
            payload["name"] = None
    return payload


def _get_nested(mapping: dict, *keys):
    current = mapping
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _extract_base_row(payload: dict) -> dict:
    growth_data = _get_nested(payload, "fundamental_context", "growth", "data") or {}
    quote = payload.get("quote") or {}
    return {
        "stock_code": payload.get("stock_code"),
        "name": payload.get("name"),
        "market_cap": quote.get("market_cap") or quote.get("total_mv"),
        "pe": quote.get("pe") or quote.get("pe_ratio"),
        "pb": quote.get("pb") or quote.get("pb_ratio"),
        "roe": growth_data.get("roe"),
        "revenue_yoy": growth_data.get("revenue_yoy"),
        "net_profit_yoy": growth_data.get("net_profit_yoy"),
    }


def build_peer_table(
    *,
    payloads: Dict[str, dict],
    target_code: str,
    peer_codes: Iterable[str],
    sector: str = "general",
    supplemental_metrics: Optional[Dict[str, dict]] = None,
) -> dict:
    sector = sector.lower()
    if sector not in FIELD_SETS:
        raise ValueError(f"Unsupported sector: {sector}")

    supplemental_metrics = supplemental_metrics or {}
    ordered_codes = [target_code] + [code for code in peer_codes if code != target_code]
    rows = []
    for code in ordered_codes:
        payload = payloads[code]
        row = _extract_base_row(payload)
        row.update(supplemental_metrics.get(code, {}))
        rows.append(row)

    return {
        "sector": sector,
        "fields": FIELD_SETS[sector],
        "target": rows[0],
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch peer comparison snapshots.")
    parser.add_argument("target_code")
    parser.add_argument("--peers", required=True, help="Comma-separated peer stock codes")
    parser.add_argument("--sector", default="general", choices=sorted(FIELD_SETS.keys()))
    parser.add_argument("--project-root", default=str(DEFAULT_PROJECT_ROOT))
    parser.add_argument("--budget-seconds", type=float, default=1.5)
    parser.add_argument("--supplemental-json", help="Optional path to supplemental metric JSON")
    args = parser.parse_args()

    peer_codes = [item.strip() for item in args.peers.split(",") if item.strip()]
    all_codes = [args.target_code] + [code for code in peer_codes if code != args.target_code]
    supplemental = {}
    if args.supplemental_json:
        supplemental = json.loads(Path(args.supplemental_json).read_text(encoding="utf-8"))

    try:
        manager = load_manager(Path(args.project_root))
        payloads = {
            code: build_payload(manager, code, budget_seconds=args.budget_seconds)
            for code in all_codes
        }
        result = build_peer_table(
            payloads=payloads,
            target_code=args.target_code,
            peer_codes=peer_codes,
            sector=args.sector,
            supplemental_metrics=supplemental,
        )
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
