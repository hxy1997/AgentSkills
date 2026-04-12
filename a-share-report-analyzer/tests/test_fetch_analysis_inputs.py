import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_analysis_inputs.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("fetch_analysis_inputs", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestFetchAnalysisInputs(unittest.TestCase):
    def test_compact_quote_returns_none_for_missing_quote(self):
        module = _load_module()

        self.assertIsNone(module.compact_quote(None))

    def test_build_payload_compacts_manager_outputs(self):
        module = _load_module()

        quote = SimpleNamespace(
            code="600519",
            name="贵州茅台",
            price=1688.0,
            change_pct=1.23,
            pe_ratio=20.5,
            pb_ratio=8.1,
            total_mv=2.1e12,
            circ_mv=2.0e12,
            source=SimpleNamespace(value="mock"),
        )

        class _Manager:
            def get_realtime_quote(self, stock_code):
                self.last_quote_code = stock_code
                return quote

            def get_fundamental_context(self, stock_code, budget_seconds=None):
                self.last_context = (stock_code, budget_seconds)
                return {"status": "ok", "coverage": {"valuation": "ok"}}

            def get_belong_boards(self, stock_code):
                self.last_boards_code = stock_code
                return [{"name": "白酒"}]

            def get_stock_name(self, stock_code):
                self.last_name_code = stock_code
                return "贵州茅台"

        manager = _Manager()

        payload = module.build_payload(manager, "600519", budget_seconds=1.8, include_quote=True)

        self.assertEqual(payload["stock_code"], "600519")
        self.assertEqual(payload["name"], "贵州茅台")
        self.assertEqual(payload["quote"]["price"], 1688.0)
        self.assertEqual(payload["quote"]["source"], "mock")
        self.assertEqual(payload["fundamental_context"]["status"], "ok")
        self.assertEqual(payload["belong_boards"], [{"name": "白酒"}])

    def test_load_manager_rejects_missing_project_root(self):
        module = _load_module()
        missing_root = Path(tempfile.gettempdir()) / "definitely-missing-dsa-project"

        with self.assertRaises(RuntimeError) as exc:
            module.load_manager(missing_root)

        self.assertIn("project root", str(exc.exception).lower())

    def test_load_manager_uses_embedded_provider_by_default(self):
        module = _load_module()

        manager = module.load_manager()

        self.assertTrue(hasattr(manager, "get_fundamental_context"))
        self.assertTrue(hasattr(manager, "get_realtime_quote"))

    def test_main_prints_json_payload(self):
        module = _load_module()

        class _Manager:
            def get_realtime_quote(self, stock_code):
                return None

            def get_fundamental_context(self, stock_code, budget_seconds=None):
                return {"status": "partial"}

            def get_belong_boards(self, stock_code):
                return []

            def get_stock_name(self, stock_code):
                return None

        stdout = io.StringIO()
        with patch.object(module, "load_manager", return_value=_Manager()):
            with patch.object(
                sys,
                "argv",
                [
                    str(SCRIPT_PATH),
                    "600519",
                    "--project-root",
                    tempfile.gettempdir(),
                    "--budget-seconds",
                    "2.0",
                ],
            ):
                with patch("sys.stdout", stdout):
                    exit_code = module.main()

        self.assertEqual(exit_code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["stock_code"], "600519")
        self.assertEqual(payload["fundamental_context"]["status"], "partial")


if __name__ == "__main__":
    unittest.main()
