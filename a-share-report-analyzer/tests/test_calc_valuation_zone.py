import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "calc_valuation_zone.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("calc_valuation_zone", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCalcValuationZone(unittest.TestCase):
    def test_zone_calculation_matches_user_logic(self):
        module = _load_module()

        result = module.calculate_valuation_zone(
            current_market_cap=1656.0,
            current_price=21.5,
            intrinsic_market_cap=1280.04,
            safe_market_cap=1790.60,
            quality_score_g=0.744,
            dev_5y=-0.2637,
            dev_10y=-0.3091,
        )

        self.assertAlmostEqual(result["E"], 0.2937, places=3)
        self.assertAlmostEqual(result["F"], -0.0752, places=3)
        self.assertAlmostEqual(result["avg_dev"], -0.0886, places=3)
        self.assertAlmostEqual(result["LOW"], -0.2419, places=3)
        self.assertAlmostEqual(result["UP"], 0.1339, places=3)
        self.assertEqual(result["quality_bucket"], "中公司")
        self.assertEqual(result["price_bucket"], "中价")
        self.assertEqual(result["action"], "中性")
        self.assertLess(result["lower_price"], result["upper_price"])


if __name__ == "__main__":
    unittest.main()
