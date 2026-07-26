#!/usr/bin/env python3
"""Calculate valuation zone and price interval from the user's conclusion logic."""

from __future__ import annotations

import argparse
import json


STANCE_MATRIX = {
    ("好公司", "低价"): "估值偏低，组合增配复核",
    ("中公司", "低价"): "估值偏低，谨慎复核",
    ("差公司", "低价"): "高风险观察",
    ("好公司", "中价"): "估值合理，维持复核",
    ("中公司", "中价"): "估值合理，中性复核",
    ("差公司", "中价"): "质量风险复核",
    ("好公司", "高价"): "估值偏高，等待复核",
    ("中公司", "高价"): "估值偏高，降配复核",
    ("差公司", "高价"): "高风险降配复核",
}


def quality_score_to_g(score_10: float) -> float:
    if not 0 <= score_10 <= 10:
        raise ValueError("10-point quality score must be between 0 and 10")
    return max(0.4, min(1.0, score_10 / 10.0))


def classify_quality(g: float) -> str:
    if g >= 0.8:
        return "好公司"
    if g > 0.6:
        return "中公司"
    return "差公司"


def classify_price(avg_dev: float, low: float, up: float) -> str:
    if avg_dev < low:
        return "低价"
    if avg_dev <= up:
        return "中价"
    return "高价"


def calculate_valuation_zone(
    *,
    current_market_cap: float,
    current_price: float,
    intrinsic_market_cap: float,
    safe_market_cap: float,
    quality_score_g: float,
    dev_5y: float,
    dev_10y: float,
) -> dict:
    for name, value in {
        "current_market_cap": current_market_cap,
        "current_price": current_price,
        "intrinsic_market_cap": intrinsic_market_cap,
        "safe_market_cap": safe_market_cap,
    }.items():
        if value <= 0:
            raise ValueError(f"{name} must be positive")
    if not 0.2 <= quality_score_g <= 1.0:
        raise ValueError("quality_score_g must be between 0.2 and 1.0; use quality_score_to_g for a 10-point score")
    if dev_5y <= -1 or dev_10y <= -1:
        raise ValueError("historical valuation deviations must be greater than -1")
    e = (current_market_cap - intrinsic_market_cap) / intrinsic_market_cap
    f = (current_market_cap - safe_market_cap) / safe_market_cap
    avg_dev = (dev_5y + dev_10y + e + f) / 4.0
    low = -0.18 / quality_score_g
    up = 0.18 * quality_score_g

    denominator = 1.0 + avg_dev
    if denominator <= 0:
        raise ValueError("Average deviation makes price interval invalid")

    lower_factor = (1.0 + low) / denominator
    upper_factor = (1.0 + up) / denominator
    quality_bucket = classify_quality(quality_score_g)
    price_bucket = classify_price(avg_dev, low, up)
    stance = STANCE_MATRIX[(quality_bucket, price_bucket)]

    return {
        "E": e,
        "F": f,
        "avg_dev": avg_dev,
        "LOW": low,
        "UP": up,
        "quality_bucket": quality_bucket,
        "price_bucket": price_bucket,
        "stance": stance,
        "action": stance,
        "lower_factor": lower_factor,
        "upper_factor": upper_factor,
        "lower_market_cap": current_market_cap * lower_factor,
        "upper_market_cap": current_market_cap * upper_factor,
        "lower_price": current_price * lower_factor,
        "upper_price": current_price * upper_factor,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate valuation zone and price interval.")
    parser.add_argument("--current-market-cap", type=float, required=True)
    parser.add_argument("--current-price", type=float, required=True)
    parser.add_argument("--intrinsic-market-cap", type=float, required=True)
    parser.add_argument("--safe-market-cap", type=float, required=True)
    quality_group = parser.add_mutually_exclusive_group(required=True)
    quality_group.add_argument("--quality-score-g", type=float)
    quality_group.add_argument("--quality-score-10", type=float)
    parser.add_argument("--dev-5y", type=float, required=True)
    parser.add_argument("--dev-10y", type=float, required=True)
    args = parser.parse_args()

    quality_score_g = (
        quality_score_to_g(args.quality_score_10)
        if args.quality_score_10 is not None
        else args.quality_score_g
    )
    payload = calculate_valuation_zone(
        current_market_cap=args.current_market_cap,
        current_price=args.current_price,
        intrinsic_market_cap=args.intrinsic_market_cap,
        safe_market_cap=args.safe_market_cap,
        quality_score_g=quality_score_g,
        dev_5y=args.dev_5y,
        dev_10y=args.dev_10y,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
