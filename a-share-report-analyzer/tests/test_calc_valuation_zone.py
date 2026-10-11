import importlib.util
from pathlib import Path
import unittest
import json
import os
import subprocess
import sys
import tempfile

spec = importlib.util.spec_from_file_location('valuation', Path(__file__).resolve().parents[1] / 'scripts/calc_valuation_zone.py')
valuation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(valuation)


class ValuationTests(unittest.TestCase):
    def run_one(self, method, **kwargs):
        return valuation.calculate_scenarios({'current_price': 10, 'share_count': 100,
            'scenarios': [{'name': 'base', 'method': method, 'margin_of_safety': 0.2, **kwargs}]})['scenarios'][0]

    def test_value_and_safety_margin_are_distinct(self):
        result = self.run_one('pe', eps=1, multiple=12)
        self.assertAlmostEqual(result['intrinsic_price'], 12)
        self.assertAlmostEqual(result['safety_margin_price'], 9.6)
        self.assertFalse(result['price_at_or_below_safety_margin'])

    def test_bank_pb_payout_consistency(self):
        result = self.run_one('bank_pb', bvps=40, roe=0.12, growth=0.03, cost_of_equity=0.10)
        self.assertAlmostEqual(result['intrinsic_price'], 40 * 0.09 / 0.07)
        self.assertAlmostEqual(result['implied_payout'], 0.75)

    def test_bank_invalid_growth_rejected(self):
        for g in (0.10, 0.12, -0.01):
            with self.assertRaises(ValueError):
                self.run_one('bank_pb', bvps=40, roe=0.12, growth=g, cost_of_equity=0.10)

    def test_ev_claims_reduce_equity(self):
        self.assertAlmostEqual(self.run_one('ev_ebit', operating_profit=200, multiple=10, net_claims=500)['intrinsic_price'], 15)
        with self.assertRaises(ValueError):
            self.run_one('ev_ebit', operating_profit=20, multiple=10, net_claims=500)

    def test_missing_quote_does_not_become_zero(self):
        result = valuation.calculate_scenarios({'share_count': 100, 'scenarios': [
            {'name': 'base', 'method': 'equity_value', 'equity_value': 1000, 'margin_of_safety': 0.2}]})
        self.assertIsNone(result['scenarios'][0]['discount_to_intrinsic'])

    def test_dividend_and_invalid_margin(self):
        self.assertAlmostEqual(self.run_one('dividend', next_dividend=1, growth=0.02, cost_of_equity=0.10)['intrinsic_price'], 12.5)
        with self.assertRaises(ValueError):
            self.run_one('pe', eps=1, multiple=10, margin_of_safety=1)

    def test_cli_outputs_utf8_even_with_ascii_console(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            path.write_text(json.dumps({'share_count': 100, 'scenarios': [
                {'name': '保守', 'method': 'pe', 'eps': 1, 'multiple': 10,
                 'margin_of_safety': 0.2}]}, ensure_ascii=False), encoding='utf-8')
            env = {**os.environ, 'PYTHONIOENCODING': 'ascii'}
            result = subprocess.run([sys.executable, str(Path(valuation.__file__)), '--input', str(path)],
                                    capture_output=True, env=env, check=True)
            self.assertEqual(json.loads(result.stdout.decode('utf-8'))['scenarios'][0]['name'], '保守')


if __name__ == '__main__':
    unittest.main()
