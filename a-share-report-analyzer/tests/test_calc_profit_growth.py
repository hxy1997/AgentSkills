import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('growth', Path(__file__).resolve().parents[1] / 'scripts/calc_profit_growth.py')
growth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(growth)


class GrowthTests(unittest.TestCase):
    def test_constant_growth_is_ten_percent_not_zero_slope(self):
        result = growth.calculate_profit_growth_metrics([100, 110, 121], [2023, 2024, 2025])
        self.assertAlmostEqual(result['profit']['cagr'], 0.1)
        self.assertAlmostEqual(result['profit']['median_yoy'], 0.1)
        self.assertNotIn('weighted_compound_growth', result)

    def test_dilution_erases_total_profit_growth(self):
        result = growth.calculate_profit_growth_metrics([100, 150], [2024, 2025], shares=[100, 150])
        self.assertAlmostEqual(result['profit']['cagr'], 0.5)
        self.assertAlmostEqual(result['per_share']['cagr'], 0)

    def test_missing_year_not_mislabeled_yoy(self):
        result = growth.calculate_profit_growth_metrics([100, 121], [2023, 2025])
        self.assertAlmostEqual(result['profit']['cagr'], 0.1)
        self.assertIsNone(result['profit']['intervals'][0]['yoy'])

    def test_turnaround_and_zero_do_not_fake_compound_growth(self):
        for values in ([100, -20, 121], [0, 10, 20], [-100, -50, 10]):
            self.assertIsNone(growth.calculate_profit_growth_metrics(values)['profit']['cagr'])

    def test_invalid_dates_shares_and_nonfinite_fail(self):
        for kwargs in ({'years': [2024, 2024]}, {'shares': [100, 0]}, {'per_share': [1]}, {'shares': [1, 1], 'per_share': [1, 1]}):
            with self.assertRaises(ValueError):
                growth.calculate_profit_growth_metrics([100, 110], **kwargs)
        with self.assertRaises(ValueError):
            growth.calculate_profit_growth_metrics([100, float('nan')])


if __name__ == '__main__':
    unittest.main()
