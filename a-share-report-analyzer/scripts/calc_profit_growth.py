#!/usr/bin/env python3
"""Calculate multi-method profit growth metrics for the analyzer skill."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from typing import Dict, Iterable, List, Sequence

DEFAULT_WMA_WEIGHTS = [0.1, 0.15, 0.2, 0.25, 0.3]


def parse_number_list(raw: str) -> List[float]:
    return [float(item.strip()) for item in raw.split(",") if item.strip()]


def normalize_years(profits: Sequence[float], years: Sequence[int] | None = None) -> List[float]:
    if years is None:
        return [float(index) for index in range(len(profits))]
    if len(years) != len(profits):
        raise ValueError("years and profits must have the same length")
    normalized = [float(value) for value in years]
    if any(current <= previous for previous, current in zip(normalized, normalized[1:])):
        raise ValueError("years must be strictly increasing")
    return normalized


def compute_yoy_rates(profits: Sequence[float], years: Sequence[float] | None = None) -> List[float]:
    if len(profits) < 2:
        raise ValueError("Need at least two profit observations")
    time_points = normalize_years(profits, years)
    yoy = []
    for previous, current, year_before, year_after in zip(
        profits[:-1], profits[1:], time_points[:-1], time_points[1:]
    ):
        if previous == 0:
            raise ValueError("Profit series contains zero, cannot compute yoy growth")
        interval = year_after - year_before
        if previous > 0 and current > 0:
            yoy.append((current / previous) ** (1.0 / interval) - 1.0)
        else:
            yoy.append((current - previous) / abs(previous) / interval)
    return yoy


def compute_profit_cagr(profits: Sequence[float], years: Sequence[float] | None = None) -> float:
    if len(profits) < 2:
        raise ValueError("Need at least two profit observations")
    if profits[0] <= 0 or profits[-1] <= 0:
        raise ValueError("CAGR requires positive first and last profit values")
    time_points = normalize_years(profits, years)
    span = time_points[-1] - time_points[0]
    return (profits[-1] / profits[0]) ** (1.0 / span) - 1.0


def linear_regression_growth_rate(
    profits: Sequence[float], years: Sequence[float] | None = None
) -> float:
    x = normalize_years(profits, years)
    mean_x = statistics.mean(x)
    mean_y = statistics.mean(profits)
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, profits))
    denominator = sum((xi - mean_x) ** 2 for xi in x)
    slope = numerator / denominator if denominator else 0.0
    return slope / mean_y


def median_growth_rate(yoy_rates: Sequence[float]) -> float:
    return statistics.median(yoy_rates)


def exp_smoothing_growth_rate(
    profits: Sequence[float], alpha: float = 0.5, years: Sequence[float] | None = None
) -> float:
    smoothed = profits[0]
    for value in profits[1:]:
        smoothed = alpha * value + (1.0 - alpha) * smoothed
    if smoothed <= 0 or profits[0] <= 0:
        raise ValueError("Exponential smoothing growth requires positive profits")
    time_points = normalize_years(profits, years)
    return (smoothed / profits[0]) ** (1.0 / (time_points[-1] - time_points[0])) - 1.0


def weighted_moving_average_growth_rate(
    yoy_rates: Sequence[float], weights: Sequence[float] = DEFAULT_WMA_WEIGHTS
) -> float:
    if not yoy_rates:
        raise ValueError("Need yoy rates for weighted moving average")
    slice_len = min(len(yoy_rates), len(weights))
    sliced_rates = list(yoy_rates)[-slice_len:]
    sliced_weights = list(weights)[-slice_len:]
    weight_sum = sum(sliced_weights)
    normalized_weights = [weight / weight_sum for weight in sliced_weights]
    return sum(rate * weight for rate, weight in zip(sliced_rates, normalized_weights))


def theil_sen_growth_rate(
    profits: Sequence[float], years: Sequence[float] | None = None
) -> float:
    time_points = normalize_years(profits, years)
    slopes = []
    for i in range(len(profits)):
        for j in range(i + 1, len(profits)):
            slopes.append((profits[j] - profits[i]) / (time_points[j] - time_points[i]))
    if not slopes:
        raise ValueError("Need at least two profits for Theil-Sen")
    return statistics.median(slopes) / statistics.mean(profits)


def quantile_regression_growth_rate(yoy_rates: Sequence[float], q: float = 0.4) -> float:
    if not 0 < q < 1:
        raise ValueError("Quantile must be between 0 and 1")
    if not yoy_rates:
        raise ValueError("Need at least one growth rate for quantile regression")
    ordered = sorted(float(value) for value in yoy_rates)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def filter_method_results(method_results: Dict[str, float], max_abs_value: float = 0.5) -> Dict[str, float]:
    return {
        key: value
        for key, value in method_results.items()
        if value is not None and math.isfinite(value) and abs(value) <= max_abs_value
    }


def trim_extremes(method_results: Dict[str, float]) -> Dict[str, float]:
    if len(method_results) < 4:
        return dict(method_results)
    sorted_items = sorted(method_results.items(), key=lambda item: item[1])
    trimmed = sorted_items[1:-1]
    return dict(trimmed)


def average_values(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        raise ValueError("No values to average")
    return statistics.mean(values)


def calculate_profit_growth_metrics(
    profits: Sequence[float],
    years: Sequence[int] | None = None,
    *,
    alpha: float = 0.5,
    q: float = 0.4,
    max_abs_value: float = 0.5,
) -> Dict[str, object]:
    profits = [float(value) for value in profits]
    if len(profits) < 3:
        raise ValueError("Need at least three profit observations")
    time_points = normalize_years(profits, years)

    yoy_rates = compute_yoy_rates(profits, time_points)
    method_results = {
        "linear_regression": linear_regression_growth_rate(profits, time_points),
        "median_growth": median_growth_rate(yoy_rates),
        "exp_smoothing_alpha_0_5": exp_smoothing_growth_rate(
            profits, alpha=alpha, years=time_points
        ),
        "weighted_moving_average": weighted_moving_average_growth_rate(yoy_rates),
        "theil_sen": theil_sen_growth_rate(profits, time_points),
        "quantile_regression_q0_4": quantile_regression_growth_rate(yoy_rates, q=q),
    }

    valid_results = filter_method_results(method_results, max_abs_value=max_abs_value)
    trimmed_results = trim_extremes(valid_results)
    estimated_avg_profit_growth = average_values(trimmed_results.values())
    profit_cagr = compute_profit_cagr(profits, time_points)
    weighted_compound_growth = (profit_cagr + estimated_avg_profit_growth) / 2.0

    return {
        "years": list(years) if years is not None else list(range(len(profits))),
        "profits": profits,
        "yoy_rates": yoy_rates,
        "methods": method_results,
        "filter_rule": f"abs(x) <= {max_abs_value}",
        "valid_results": valid_results,
        "trimmed_results": trimmed_results,
        "estimated_avg_profit_growth": estimated_avg_profit_growth,
        "profit_cagr": profit_cagr,
        "weighted_compound_growth": weighted_compound_growth,
        "wma_weights": DEFAULT_WMA_WEIGHTS,
        "alpha": alpha,
        "quantile": q,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate multi-method profit growth metrics.")
    parser.add_argument("--profits", required=True, help="Comma-separated profit series")
    parser.add_argument("--years", help="Optional comma-separated year series")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--quantile", type=float, default=0.4)
    parser.add_argument("--max-abs-value", type=float, default=0.5)
    args = parser.parse_args()

    profits = parse_number_list(args.profits)
    years = [int(value) for value in parse_number_list(args.years)] if args.years else None
    payload = calculate_profit_growth_metrics(
        profits,
        years,
        alpha=args.alpha,
        q=args.quantile,
        max_abs_value=args.max_abs_value,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
