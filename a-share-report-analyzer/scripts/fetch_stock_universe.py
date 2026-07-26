#!/usr/bin/env python3
"""Fetch stock-universe lists from Tushare Pro without extra abstraction."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

import requests


TUSHARE_PRO_API = "https://api.tushare.pro"


def query_tushare(token: str, api_name: str, params: dict | None = None, timeout: int = 20):
    """Send one official Tushare Pro HTTP request and return row dicts."""
    response = requests.post(
        TUSHARE_PRO_API,
        json={
            "api_name": api_name,
            "token": token,
            "params": params or {},
            "fields": "",
        },
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("code") != 0:
        raise RuntimeError(payload.get("msg") or f"Tushare query failed: {api_name}")

    data = payload.get("data") or {}
    fields = data.get("fields") or []
    items = data.get("items") or []
    return [dict(zip(fields, item)) for item in items]


def fetch_stock_universe(token: str, market: str = "a", page_limit: int = 5000):
    """Fetch one market's stock universe."""
    normalized = market.lower()
    if normalized == "a":
        return query_tushare(token, "stock_basic", {"exchange": "", "list_status": "L"})
    if normalized == "hk":
        return query_tushare(token, "hk_basic", {"list_status": "L"})
    if normalized != "us":
        raise ValueError(f"Unsupported market: {market}")

    rows = []
    offset = 0
    while True:
        page = query_tushare(token, "us_basic", {"offset": offset, "limit": page_limit})
        if not page:
            break
        rows.extend(page)
        if len(page) < page_limit:
            break
        offset += page_limit
    return rows


def write_output(rows, output_path: Path):
    """Write rows to json or csv based on suffix."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() == ".json":
        output_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    fieldnames = sorted({key for row in rows for key in row.keys()})
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch one Tushare stock universe.")
    parser.add_argument("--market", choices=["a", "hk", "us"], default="a")
    parser.add_argument("--token", default=os.getenv("TUSHARE_TOKEN"))
    parser.add_argument("--output", required=True, help="Output path, .csv or .json")
    parser.add_argument("--page-limit", type=int, default=5000)
    args = parser.parse_args()

    if not args.token:
        print(json.dumps({"error": "Missing TUSHARE_TOKEN or --token"}, ensure_ascii=False))
        return 1

    try:
        rows = fetch_stock_universe(args.token, market=args.market, page_limit=args.page_limit)
        write_output(rows, Path(args.output))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "market": args.market,
                "count": len(rows),
                "output": str(Path(args.output).resolve()),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
