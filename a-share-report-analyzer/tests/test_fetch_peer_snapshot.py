import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_peer_snapshot.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("fetch_peer_snapshot", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestFetchPeerSnapshot(unittest.TestCase):
    def test_build_peer_table_for_general_sector(self):
        module = _load_module()

        payloads = {
            "600519": {
                "stock_code": "600519",
                "name": "贵州茅台",
                "quote": {"total_mv": 2100.0, "pe_ratio": 25.0, "pb_ratio": 8.5},
                "fundamental_context": {
                    "growth": {"data": {"revenue_yoy": 0.15, "net_profit_yoy": 0.12, "roe": 0.31}}
                },
            },
            "000858": {
                "stock_code": "000858",
                "name": "五粮液",
                "quote": {"total_mv": 520.0, "pe_ratio": 18.0, "pb_ratio": 5.2},
                "fundamental_context": {
                    "growth": {"data": {"revenue_yoy": 0.10, "net_profit_yoy": 0.09, "roe": 0.24}}
                },
            },
        }

        table = module.build_peer_table(
            payloads=payloads,
            target_code="600519",
            peer_codes=["000858"],
            sector="general",
        )

        self.assertEqual(table["target"]["stock_code"], "600519")
        self.assertEqual(table["fields"], ["market_cap", "pe", "pb", "roe", "revenue_yoy", "net_profit_yoy"])
        self.assertEqual(table["rows"][1]["name"], "五粮液")

    def test_build_peer_table_merges_sector_specific_metrics(self):
        module = _load_module()
        payloads = {
            "600036": {
                "stock_code": "600036",
                "name": "招商银行",
                "quote": {"total_mv": 9962.0, "pe_ratio": 6.7, "pb_ratio": 0.94},
                "fundamental_context": {
                    "growth": {"data": {"roe": 0.1344}},
                },
            },
            "601166": {
                "stock_code": "601166",
                "name": "兴业银行",
                "quote": {"total_mv": 4100.0, "pe_ratio": 5.8, "pb_ratio": 0.71},
                "fundamental_context": {
                    "growth": {"data": {"roe": 0.108}},
                },
            },
        }
        supplemental = {
            "600036": {"nim": 0.0187, "npl_ratio": 0.0094, "provision_coverage": 3.9179, "cet1_ratio": 0.1393},
            "601166": {"nim": 0.0182, "npl_ratio": 0.0107, "provision_coverage": 2.45, "cet1_ratio": 0.0995},
        }

        table = module.build_peer_table(
            payloads=payloads,
            target_code="600036",
            peer_codes=["601166"],
            sector="bank",
            supplemental_metrics=supplemental,
        )

        self.assertEqual(table["fields"], ["market_cap", "pb", "roe", "nim", "npl_ratio", "provision_coverage", "cet1_ratio"])
        self.assertEqual(table["rows"][0]["nim"], 0.0187)
        self.assertEqual(table["rows"][1]["cet1_ratio"], 0.0995)


if __name__ == "__main__":
    unittest.main()
