import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "calc_profit_growth.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("calc_profit_growth", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCalcProfitGrowth(unittest.TestCase):
    def test_screenshot_example_matches_expected_outputs(self):
        module = _load_module()
        profits = [95.09, 102.38, 75.07, 70.34, 72.23, 94.39]
        years = [2020, 2021, 2022, 2023, 2024, 2025]

        result = module.calculate_profit_growth_metrics(profits, years)

        self.assertAlmostEqual(result["methods"]["linear_regression"], -0.0332, places=3)
        self.assertAlmostEqual(result["methods"]["median_growth"], 0.0269, places=3)
        self.assertAlmostEqual(result["methods"]["exp_smoothing_alpha_0_5"], -0.0224, places=3)
        self.assertAlmostEqual(result["methods"]["weighted_moving_average"], 0.0538, places=3)
        self.assertAlmostEqual(result["methods"]["theil_sen"], -0.0235, places=3)
        self.assertAlmostEqual(result["methods"]["quantile_regression_q0_4"], 0.1849, places=3)
        self.assertAlmostEqual(result["estimated_avg_profit_growth"], 0.0086, places=3)
        self.assertAlmostEqual(result["profit_cagr"], -0.0015, places=3)
        self.assertAlmostEqual(result["weighted_compound_growth"], 0.0036, places=3)

    def test_filtering_and_trimming_drop_extremes(self):
        module = _load_module()
        method_results = {
            "a": 0.02,
            "b": 0.03,
            "c": -0.01,
            "d": 0.08,
            "e": 0.60,
            "f": -0.04,
        }

        filtered = module.filter_method_results(method_results, max_abs_value=0.5)
        trimmed = module.trim_extremes(filtered)

        self.assertNotIn("e", filtered)
        self.assertEqual(set(trimmed.keys()), {"a", "b", "c"})


if __name__ == "__main__":
    unittest.main()
