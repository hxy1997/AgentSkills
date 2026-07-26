import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "calc_commodity_sensitivity.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("calc_commodity_sensitivity", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCalcCommoditySensitivity(unittest.TestCase):
    def test_gold_sensitivity_example(self):
        module = _load_module()

        result = module.calculate_commodity_sensitivity(
            attributable_production=3_380_000,
            price_change_usd=100,
            fx_cny_per_usd=7.15,
            pass_through_low=0.50,
            pass_through_high=0.70,
            shares_outstanding=26_590_000_000,
            multiple_low=12,
            multiple_high=14,
        )

        self.assertAlmostEqual(result["revenue_change_cny"], 2_416_700_000)
        self.assertAlmostEqual(result["net_profit_change_low_cny"], 1_208_350_000)
        self.assertAlmostEqual(result["net_profit_change_high_cny"], 1_691_690_000)
        self.assertAlmostEqual(result["eps_change_low"], 0.04544, places=4)
        self.assertAlmostEqual(result["eps_change_high"], 0.06362, places=4)
        self.assertAlmostEqual(result["implied_price_change_low"], 0.5453, places=3)
        self.assertAlmostEqual(result["implied_price_change_high"], 0.8907, places=3)

    def test_validation(self):
        module = _load_module()

        with self.assertRaises(ValueError):
            module.calculate_commodity_sensitivity(
                attributable_production=1,
                price_change_usd=100,
                fx_cny_per_usd=7,
                pass_through_low=0.8,
                pass_through_high=0.2,
            )

        with self.assertRaises(ValueError):
            module.calculate_commodity_sensitivity(
                attributable_production=1,
                price_change_usd=100,
                fx_cny_per_usd=7,
                pass_through_low=0.2,
                pass_through_high=0.8,
                multiple_low=10,
            )

    def test_negative_price_change_keeps_range_ordered(self):
        module = _load_module()

        result = module.calculate_commodity_sensitivity(
            attributable_production=1_000,
            price_change_usd=-100,
            fx_cny_per_usd=7,
            pass_through_low=0.50,
            pass_through_high=0.70,
            shares_outstanding=100_000,
            multiple_low=10,
            multiple_high=12,
        )

        self.assertAlmostEqual(result["net_profit_change_low_cny"], -490_000)
        self.assertAlmostEqual(result["net_profit_change_high_cny"], -350_000)
        self.assertLessEqual(result["eps_change_low"], result["eps_change_high"])
        self.assertLessEqual(
            result["implied_price_change_low"],
            result["implied_price_change_high"],
        )


if __name__ == "__main__":
    unittest.main()
