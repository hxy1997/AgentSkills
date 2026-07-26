from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from portable_data_provider.manager import _market_tag, normalize_stock_code  # noqa: E402


class PortableProviderRoutingTest(unittest.TestCase):
    def test_msft_us_is_routed_to_us(self):
        self.assertEqual(normalize_stock_code("MSFT.US"), "MSFT.US")
        self.assertEqual(_market_tag(normalize_stock_code("MSFT.US")), "us")

    def test_us_class_share_is_routed_to_us(self):
        self.assertEqual(_market_tag(normalize_stock_code("BRK.B.US")), "us")

    def test_a_share_is_not_misclassified_as_us(self):
        self.assertEqual(_market_tag(normalize_stock_code("600519")), "cn")


if __name__ == "__main__":
    unittest.main()
