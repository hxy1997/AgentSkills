#!/usr/bin/env python3
"""Historical growth diagnostics; no forecast aggregation. Standard library only."""
from __future__ import annotations
import argparse
import json
import math
import statistics
import sys
from typing import Sequence


def numbers(values: Sequence[float], label: str) -> list[float]:
    result = [float(x) for x in values]
    if not all(math.isfinite(x) for x in result):
        raise ValueError(f'{label} must be finite')
    return result


def summarize(values: list[float], years: list[int]) -> dict:
    intervals = []
    for a, b, y0, y1 in zip(values, values[1:], years, years[1:]):
        valid = a > 0 and b > 0
        span = y1 - y0
        intervals.append({
            'from_year': y0, 'to_year': y1, 'year_span': span,
            'absolute_change': b - a,
            'period_change': b / a - 1 if valid else None,
            'annualized_change': (b / a) ** (1 / span) - 1 if valid else None,
            'yoy': b / a - 1 if valid and span == 1 else None,
            'reason': None if valid else 'Nonpositive value: conventional growth is not meaningful',
        })
    positive = all(x > 0 for x in values)
    yoy = [x['yoy'] for x in intervals if x['yoy'] is not None]
    return {
        'values': values, 'intervals': intervals,
        'cagr': (values[-1] / values[0]) ** (1 / (years[-1] - years[0])) - 1 if positive else None,
        'cagr_reason': None if positive else 'Nonpositive observation in period; inspect levels and turnaround',
        'median_yoy': statistics.median(yoy) if yoy else None, 'median_yoy_count': len(yoy),
    }


def calculate_profit_growth_metrics(profits: Sequence[float], years: Sequence[int] | None = None,
                                    *, shares: Sequence[float] | None = None,
                                    per_share: Sequence[float] | None = None) -> dict:
    profits = numbers(profits, 'profits')
    if len(profits) < 2:
        raise ValueError('Need at least two observations')
    if years is None:
        years = list(range(len(profits)))
    else:
        years = list(years)
        if any(isinstance(y, bool) or not isinstance(y, int) for y in years):
            raise ValueError('years must be integers')
    if len(years) != len(profits) or any(b <= a for a, b in zip(years, years[1:])):
        raise ValueError('years must match observations and increase strictly')
    if shares is not None and per_share is not None:
        raise ValueError('Provide shares OR official per_share, not both')
    result = {'schema_version': 2, 'purpose': 'historical_diagnostics_not_forecast',
              'years': years, 'profit': summarize(profits, years),
              'warnings': ['Historical statistics are not forecasts; no blended growth rate is produced.']}
    if any(b - a != 1 for a, b in zip(years, years[1:])):
        result['warnings'].append('Missing years: multi-year intervals are not labeled YoY.')
    if shares is not None:
        shares = numbers(shares, 'shares')
        if len(shares) != len(profits) or any(s <= 0 for s in shares):
            raise ValueError('shares must be positive and match observations')
        result['shares'] = summarize(shares, years)
        per_share = [p / s for p, s in zip(profits, shares)]
        result['per_share_basis'] = 'profit / supplied weighted-average diluted shares; units must match'
    elif per_share is not None:
        result['per_share_basis'] = 'supplied official per-share series; reconcile ordinary-share profit separately'
    if per_share is not None:
        per_share = numbers(per_share, 'per_share')
        if len(per_share) != len(profits):
            raise ValueError('per_share must match observations')
        result['per_share'] = summarize(per_share, years)
    else:
        result['warnings'].append('Per-share data missing: total profit growth does not establish owner growth.')
    return result


def parse_number_list(raw: str) -> list[float]:
    return [float(x.strip()) for x in raw.split(',')]


def main() -> int:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profits', required=True)
    parser.add_argument('--years')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--shares')
    group.add_argument('--per-share')
    args = parser.parse_args()
    try:
        payload = calculate_profit_growth_metrics(parse_number_list(args.profits),
            [int(x.strip()) for x in args.years.split(',')] if args.years else None,
            shares=parse_number_list(args.shares) if args.shares else None,
            per_share=parse_number_list(args.per_share) if args.per_share else None)
    except (ValueError, OverflowError) as exc:
        parser.error(str(exc))
    print(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
