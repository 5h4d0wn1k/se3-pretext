#!/usr/bin/env python3
"""Offline unit tests for SE3 Pretext Lab Generator."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from se3_cli import (
    LabGuard, GuardError, SyntheticBank, BackstoryBuilder, CallMatrix,
    LogPlausibility, PretextEngine, WATERMARK, DRILL_BRAND,
)


class TestLabGuard(unittest.TestCase):
    def test_requires_lab_root(self):
        with self.assertRaises(GuardError):
            LabGuard(None)

    def test_requires_own(self):
        with self.assertRaises(GuardError):
            LabGuard("/tmp/x", target_org="SomeBank")

    def test_refuses_real_org(self):
        g = LabGuard("/tmp/x")
        with self.assertRaises(GuardError):
            g.refuse_org("Wells Fargo")

    def test_allows_synthetic_org(self):
        g = LabGuard("/tmp/x")
        g.refuse_org("acme-lab.example")


class TestSyntheticBank(unittest.TestCase):
    def test_persona_synthetic(self):
        p = SyntheticBank().persona()
        self.assertTrue(p["email"].endswith("@example.com"))
        self.assertEqual(p["org"], "acme-lab.example")
        self.assertRegex(p["badge"], r"DRILL-\d{4}")

    def test_deterministic(self):
        a = SyntheticBank(seed=3).persona()
        b = SyntheticBank(seed=3).persona()
        self.assertEqual(a, b)


class TestBackstory(unittest.TestCase):
    def test_branded(self):
        b = BackstoryBuilder().build("vishing")
        self.assertIn(DRILL_BRAND, b["premise"])
        self.assertEqual(b["watermark"], WATERMARK)


class TestCallMatrix(unittest.TestCase):
    def test_rows_watermarked(self):
        rows = CallMatrix().rows()
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(r["watermarked"] for r in rows))


class TestLogPlausibility(unittest.TestCase):
    def test_good_log_plausible(self):
        r = LogPlausibility().score(
            "Verified via internal directory; ticketed; set callback; declined to share token.")
        self.assertGreaterEqual(r["plausibility_score"], 50)

    def test_bad_log_review(self):
        r = LogPlausibility().score("gave password and read back pin to caller")
        self.assertEqual(r["verdict"], "trainer_review")


class TestEngine(unittest.TestCase):
    def test_run_writes_json_report(self):
        with tempfile.TemporaryDirectory() as td:
            guard = LabGuard(td)
            report = PretextEngine(guard, seed=9).run()
            self.assertEqual(report["drill_brand"], DRILL_BRAND)
            self.assertEqual(len(report["call_matrix"]), 3)
            self.assertTrue(os.path.exists(report["report_path"]))
            for s in report["scenarios"]:
                self.assertTrue(s["persona"]["email"].endswith("@example.com"))

    def test_markdown_render(self):
        with tempfile.TemporaryDirectory() as td:
            guard = LabGuard(td)
            engine = PretextEngine(guard)
            md = engine.render_markdown(engine.run())
            self.assertIn("# SE3 Pretext Lab Report", md)
            self.assertIn("# Call Matrix", md)


if __name__ == "__main__":
    unittest.main()