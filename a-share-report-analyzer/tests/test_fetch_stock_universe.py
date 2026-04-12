import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_stock_universe.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("fetch_stock_universe", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestFetchStockUniverse(unittest.TestCase):
    def test_query_tushare_posts_expected_payload(self):
        module = _load_module()
        response = MagicMock(
            status_code=200,
            raise_for_status=MagicMock(),
            json=MagicMock(
                return_value={
                    "code": 0,
                    "data": {"fields": ["ts_code", "name"], "items": [["600519.SH", "贵州茅台"]]},
                }
            ),
        )

        with patch.object(module.requests, "post", return_value=response) as post_mock:
            rows = module.query_tushare("demo-token", "stock_basic", {"list_status": "L"})

        post_mock.assert_called_once_with(
            module.TUSHARE_PRO_API,
            json={
                "api_name": "stock_basic",
                "token": "demo-token",
                "params": {"list_status": "L"},
                "fields": "",
            },
            timeout=20,
        )
        self.assertEqual(rows, [{"ts_code": "600519.SH", "name": "贵州茅台"}])

    def test_fetch_stock_universe_uses_single_call_for_a_share(self):
        module = _load_module()

        with patch.object(
            module,
            "query_tushare",
            return_value=[{"ts_code": "600519.SH", "name": "贵州茅台"}],
        ) as query_mock:
            rows = module.fetch_stock_universe("demo-token", market="a")

        query_mock.assert_called_once_with("demo-token", "stock_basic", {"exchange": "", "list_status": "L"})
        self.assertEqual(rows[0]["ts_code"], "600519.SH")

    def test_fetch_stock_universe_paginates_us_market(self):
        module = _load_module()

        calls = [
            [{"ts_code": "AAPL", "name": "Apple"}],
            [{"ts_code": "MSFT", "name": "Microsoft"}],
            [],
        ]

        with patch.object(module, "query_tushare", side_effect=calls) as query_mock:
            rows = module.fetch_stock_universe("demo-token", market="us", page_limit=1)

        self.assertEqual(query_mock.call_count, 3)
        self.assertEqual([row["ts_code"] for row in rows], ["AAPL", "MSFT"])

    def test_write_output_supports_json(self):
        module = _load_module()
        rows = [{"ts_code": "600519.SH", "name": "贵州茅台"}]

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "stocks.json"
            module.write_output(rows, output_path)
            payload = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(payload[0]["name"], "贵州茅台")


if __name__ == "__main__":
    unittest.main()
