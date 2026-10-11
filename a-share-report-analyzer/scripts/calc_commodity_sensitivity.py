#!/usr/bin/env python3
"""Calculate deterministic commodity-price sensitivity for equity research."""

from __future__ import annotations

import argparse
import json
import math


def calculate_commodity_sensitivity(
    *,
    attributable_production: float,
    price_change_usd: float,
    fx_cny_per_usd: float,
    pass_through_low: float,
    pass_through_high: float,
    shares_outstanding: float | None = None,
    multiple_low: float | None = None,
    multiple_high: float | None = None,
) -> dict:
    values = {
        "attributable_production": attributable_production,
        "price_change_usd": price_change_usd,
        "fx_cny_per_usd": fx_cny_per_usd,
        "pass_through_low": pass_through_low,
        "pass_through_high": pass_through_high,
        "shares_outstanding": shares_outstanding,
        "multiple_low": multiple_low,
        "multiple_high": multiple_high,
    }
    for name, value in values.items():
        if value is not None and not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
    if attributable_production < 0:
        raise ValueError("attributable_production must be non-negative")
    if fx_cny_per_usd <= 0:
        raise ValueError("fx_cny_per_usd must be positive")
    if not 0 <= pass_through_low <= pass_through_high <= 1:
        raise ValueError("pass-through assumptions must satisfy 0 <= low <= high <= 1")
    if shares_outstanding is not None and shares_outstanding <= 0:
        raise ValueError("shares_outstanding must be positive")
    if (multiple_low is None) != (multiple_high is None):
        raise ValueError("provide both multiple_low and multiple_high, or neither")
    if multiple_low is not None and shares_outstanding is None:
        raise ValueError("shares_outstanding is required when providing multiples")
    if multiple_low is not None and not 0 <= multiple_low <= multiple_high:
        raise ValueError("multiples must satisfy 0 <= low <= high")

    revenue_change_usd = attributable_production * price_change_usd
    revenue_change_cny = revenue_change_usd * fx_cny_per_usd
    net_profit_candidates = [
        revenue_change_cny * pass_through_low,
        revenue_change_cny * pass_through_high,
    ]
    net_profit_change_low = min(net_profit_candidates)
    net_profit_change_high = max(net_profit_candidates)

    payload = {
        "attributable_production": attributable_production,
        "price_change_usd": price_change_usd,
        "fx_cny_per_usd": fx_cny_per_usd,
        "revenue_change_usd": revenue_change_usd,
        "revenue_change_cny": revenue_change_cny,
        "pass_through_low": pass_through_low,
        "pass_through_high": pass_through_high,
        "net_profit_change_low_cny": net_profit_change_low,
        "net_profit_change_high_cny": net_profit_change_high,
        "assumption_warning": (
            "Pass-through is an analyst assumption. Reconcile costs, taxes, royalties, "
            "minority interests, hedging, product mix, and production response."
        ),
    }

    if shares_outstanding is not None:
        eps_low = net_profit_change_low / shares_outstanding
        eps_high = net_profit_change_high / shares_outstanding
        payload.update(
            {
                "shares_outstanding": shares_outstanding,
                "eps_change_low": eps_low,
                "eps_change_high": eps_high,
            }
        )
        if multiple_low is not None and multiple_high is not None:
            candidates = [
                eps_low * multiple_low,
                eps_low * multiple_high,
                eps_high * multiple_low,
                eps_high * multiple_high,
            ]
            payload.update(
                {
                    "multiple_low": multiple_low,
                    "multiple_high": multiple_high,
                    "implied_price_change_low": min(candidates),
                    "implied_price_change_high": max(candidates),
                }
            )

    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate commodity-price revenue, profit, EPS, and valuation sensitivity. "
            "Production and shares must use matching absolute units."
        )
    )
    parser.add_argument("--attributable-production", type=float, required=True)
    parser.add_argument("--price-change-usd", type=float, required=True)
    parser.add_argument("--fx-cny-per-usd", type=float, required=True)
    parser.add_argument("--pass-through-low", type=float, required=True)
    parser.add_argument("--pass-through-high", type=float, required=True)
    parser.add_argument("--shares-outstanding", type=float)
    parser.add_argument("--multiple-low", type=float)
    parser.add_argument("--multiple-high", type=float)
    args = parser.parse_args()

    payload = calculate_commodity_sensitivity(
        attributable_production=args.attributable_production,
        price_change_usd=args.price_change_usd,
        fx_cny_per_usd=args.fx_cny_per_usd,
        pass_through_low=args.pass_through_low,
        pass_through_high=args.pass_through_high,
        shares_outstanding=args.shares_outstanding,
        multiple_low=args.multiple_low,
        multiple_high=args.multiple_high,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
