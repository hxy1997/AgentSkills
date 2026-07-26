import importlib.util
import json
import tempfile
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
        self.assertEqual(result["action_required"], "use_anchor")

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
        self.assertEqual(result["action_required"], "update_anchor_before_valuation")

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
