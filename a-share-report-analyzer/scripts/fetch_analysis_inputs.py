#!/usr/bin/env python3
"""Fetch analysis inputs using the embedded provider or an explicit external project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_PROJECT_ROOT = None


def compact_quote(quote):
    """Convert the external quote object into plain JSON-friendly data."""
    if quote is None:
        return None

    source = getattr(quote, "source", None)
    if hasattr(source, "value"):
        source = source.value

    return {
        "code": getattr(quote, "code", None),
        "name": getattr(quote, "name", None),
        "price": getattr(quote, "price", None),
        "change_pct": getattr(quote, "change_pct", None),
        "pe_ratio": getattr(quote, "pe_ratio", None),
        "pb_ratio": getattr(quote, "pb_ratio", None),
        "total_mv": getattr(quote, "total_mv", None),
        "circ_mv": getattr(quote, "circ_mv", None),
        "source": source,
    }


def load_manager(project_root: Path | None = None):
    """Load the embedded provider by default, or an explicit external project when requested."""
    if project_root is None:
        skill_root = Path(__file__).resolve().parents[1]
        import sys

        if str(skill_root) not in sys.path:
            sys.path.insert(0, str(skill_root))
        from portable_data_provider import DataFetcherManager

        return DataFetcherManager()

    project_root = Path(project_root).resolve()
    if not project_root.exists():
        raise RuntimeError(f"External project root not found: {project_root}")

    import sys

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    try:
        from data_provider import DataFetcherManager
    except Exception as exc:
        raise RuntimeError(
            f"Failed to import DataFetcherManager from project root {project_root}: {exc}"
        ) from exc

    return DataFetcherManager()


def build_payload(manager, stock_code: str, budget_seconds: float = 1.5, include_quote: bool = True):
    """Build a compact phase-1 input payload for one stock."""
    payload = {
        "stock_code": stock_code,
        "name": None,
        "quote": None,
        "fundamental_context": manager.get_fundamental_context(stock_code, budget_seconds=budget_seconds),
        "belong_boards": [],
    }

    if hasattr(manager, "get_stock_name"):
        try:
            payload["name"] = manager.get_stock_name(stock_code)
        except Exception:
            payload["name"] = None

    if include_quote:
        payload["quote"] = compact_quote(manager.get_realtime_quote(stock_code))

    if hasattr(manager, "get_belong_boards"):
        try:
            payload["belong_boards"] = manager.get_belong_boards(stock_code) or []
        except Exception:
            payload["belong_boards"] = []

    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch analysis inputs for one stock.")
    parser.add_argument("stock_code", help="Stock code, for example 600519")
    parser.add_argument(
        "--project-root",
        default=DEFAULT_PROJECT_ROOT,
        help="Optional path to an external daily_stock_analysis project; defaults to the embedded provider",
    )
    parser.add_argument(
        "--budget-seconds",
        type=float,
        default=1.5,
        help="Budget passed into get_fundamental_context",
    )
    parser.add_argument(
        "--skip-quote",
        action="store_true",
        help="Skip realtime quote fetch",
    )
    args = parser.parse_args()

    try:
        manager = load_manager(Path(args.project_root) if args.project_root else None)
        payload = build_payload(
            manager,
            args.stock_code,
            budget_seconds=args.budget_seconds,
            include_quote=not args.skip_quote,
        )
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
