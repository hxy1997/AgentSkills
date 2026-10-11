import importlib.util
import json
import tempfile
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_valuation_anchor.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_valuation_anchor", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCheckValuationAnchor(unittest.TestCase):
    def test_fresh_anchor_is_ok(self):
        module = _load_module()
        anchor = {
            "anchor_id": "semiconductor_memory",
            "display_name": "半导体存储芯片",
            "sub_industry": "存储芯片",
            "last_updated": "2026-05-01",
            "next_review_due": "2026-08-01",
            "refresh_interval_days": 100,
            "primary_anchor": {"method": "PS"},
        }

        result = module.check_anchor_freshness(anchor, date(2026, 5, 25))

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["action_required"], "verify_sources_and_applicability")

    def test_expired_anchor_requires_update(self):
        module = _load_module()
        anchor = {
            "anchor_id": "semiconductor_memory",
            "display_name": "半导体存储芯片",
            "sub_industry": "存储芯片",
            "last_updated": "2025-12-01",
            "next_review_due": "2026-03-01",
            "refresh_interval_days": 100,
        }

        result = module.check_anchor_freshness(anchor, date(2026, 5, 25))

        self.assertEqual(result["status"], "expired")
        self.assertEqual(result["action_required"], "refresh_evidence_before_valuation")

    def test_future_record_is_unavailable_until_publication(self):
        module = _load_module()
        anchor = {"anchor_id": "bank", "last_updated": "2026-05-26"}
        before = module.check_anchor_freshness(anchor, date(2026, 5, 25))
        on_date = module.check_anchor_freshness(anchor, date(2026, 5, 26))
        self.assertEqual(before["status"], "not_yet_available")
        self.assertEqual(before["action_required"], "use_record_available_at_cutoff")
        self.assertEqual(on_date["status"], "ok")

    def test_future_record_cli_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "bank.json").write_text(
                json.dumps({"anchor_id": "bank", "last_updated": "2026-05-26"}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--anchors-dir", tmp,
                 "--anchor-id", "bank", "--as-of-date", "2026-05-25"],
                capture_output=True, text=True, check=False,
            )
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["status"], "not_yet_available")

    def test_alias_matching(self):
        module = _load_module()
        anchors = [
            {
                "anchor_id": "semiconductor_memory",
                "display_name": "半导体存储芯片",
                "sub_industry": "Fabless 利基型/中小容量存储芯片设计",
                "aliases": ["存储芯片", "memory"],
                "last_updated": "2026-05-01",
            }
        ]

        result = module.match_anchor(anchors, sub_industry="存储芯片")

        self.assertIsNotNone(result)
        self.assertEqual(result["anchor_id"], "semiconductor_memory")

    def test_iter_anchors_skips_index(self):
        module = _load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.json").write_text(json.dumps({"anchors": []}), encoding="utf-8")
            (root / "a.json").write_text(
                json.dumps({"anchor_id": "a", "last_updated": "2026-05-01"}), encoding="utf-8"
            )

            anchors = list(module.iter_anchors(root))

        self.assertEqual(len(anchors), 1)
        self.assertEqual(anchors[0]["anchor_id"], "a")


if __name__ == "__main__":
    unittest.main()
