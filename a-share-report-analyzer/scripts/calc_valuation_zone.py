#!/usr/bin/env python3
"""Explicit scenario valuation; retained filename, version-2 JSON interface."""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path


def finite(value, name: str, positive: bool = False) -> float:
    if isinstance(value, bool):
        raise ValueError(f'{name} must be numeric, not boolean')
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0):
        raise ValueError(f'{name} must be finite' + (' and positive' if positive else ''))
    return result


def value_scenario(scenario: dict, share_count: float) -> tuple[float, dict]:
    method = scenario['method']
    extra = {}
    if method == 'pe':
        price = finite(scenario['eps'], 'eps', True) * finite(scenario['multiple'], 'multiple', True)
    elif method == 'bank_pb':
        bvps = finite(scenario['bvps'], 'bvps', True)
        roe = finite(scenario['roe'], 'roe', True)
        ke = finite(scenario['cost_of_equity'], 'cost_of_equity', True)
        growth = finite(scenario['growth'], 'growth')
        if not 0 <= growth < min(ke, roe):
            raise ValueError('bank_pb requires 0 <= growth < both Ke and ROE; use an explicit runoff model otherwise')
        pb = (roe - growth) / (ke - growth)
        price = bvps * pb
        extra = {'implied_pb': pb, 'implied_retention': growth / roe,
                 'implied_payout': 1 - growth / roe, 'model_scope': 'steady_state_not_transition_forecast'}
    elif method == 'dividend':
        dividend = finite(scenario['next_dividend'], 'next_dividend', True)
        ke = finite(scenario['cost_of_equity'], 'cost_of_equity', True)
        growth = finite(scenario['growth'], 'growth')
        if not -1 < growth < ke:
            raise ValueError('dividend requires -1 < growth < Ke')
        price = dividend / (ke - growth)
    elif method == 'ev_ebit':
        ev = finite(scenario['operating_profit'], 'operating_profit', True) * finite(scenario['multiple'], 'multiple', True)
        claims = finite(scenario['net_claims'], 'net_claims')
        price = (ev - claims) / share_count
        extra = {'enterprise_value': ev, 'net_claims': claims}
    elif method == 'equity_value':
        price = finite(scenario['equity_value'], 'equity_value', True) / share_count
    else:
        raise ValueError(f'Unknown method: {method}')
    return finite(price, 'intrinsic_price', True), extra


def calculate_scenarios(payload: dict) -> dict:
    shares = finite(payload['share_count'], 'share_count', True)
    current = payload.get('current_price')
    if current is not None:
        current = finite(current, 'current_price', True)
    scenarios = payload['scenarios']
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError('scenarios must be a nonempty list')
    results = []
    names = set()
    for scenario in scenarios:
        name = scenario['name']
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError('Scenario names must be nonempty and unique')
        names.add(name)
        margin = finite(scenario['margin_of_safety'], 'margin_of_safety')
        if not 0 <= margin < 1:
            raise ValueError('margin_of_safety must be in [0, 1)')
        price, extra = value_scenario(scenario, shares)
        safe = price * (1 - margin)
        results.append({'name': name, 'method': scenario['method'], 'inputs': scenario,
            'intrinsic_price': price, 'model_ordinary_equity_value': price * shares,
            'margin_of_safety': margin, 'safety_margin_price': safe,
            'discount_to_intrinsic': None if current is None else 1 - current / price,
            'price_at_or_below_safety_margin': None if current is None else current <= safe, **extra})
    return {'schema_version': 2, 'current_price': current, 'share_count': shares,
        'quote_date': payload.get('quote_date'), 'currency': payload.get('currency'), 'scenarios': results,
        'intrinsic_price_range': [min(x['intrinsic_price'] for x in results), max(x['intrinsic_price'] for x in results)],
        'warnings': ['Scenario range is not a statistical confidence interval or trading instruction.',
                     'Model equity values are not observed A+H market capitalization.',
                     'Historical percentiles and quality scores are not averaged into intrinsic values.']}


def main() -> int:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    args = parser.parse_args()
    try:
        payload = calculate_scenarios(json.loads(args.input.read_text(encoding='utf-8-sig')))
    except (ValueError, TypeError, KeyError, OSError, OverflowError) as exc:
        parser.error(str(exc))
    print(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
