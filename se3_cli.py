#!/usr/bin/env python3
"""
SE3 — Pretext Lab Generator
Synthetic pretext/call-matrix framework for AUTHORIZED internal drills.

Anti-abuse by default:
  * requires explicit --lab-root and --target-org OWN
  * dry-run by default; reports only written under lab-root/reports/
  * all scenarios carry "AUTHORIZED DRILL" branding and only synthetic personas
  * refuses real organization names / real personal data
"""

import argparse
import json
import random
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

WATERMARK = "SIMULATION / AUTHORIZED TRAINING ONLY"
DRILL_BRAND = "AUTHORIZED INTERNAL DRILL"
ALLOWED_ORGS = (".example", "acme-lab", "internal")


class GuardError(Exception):
    pass


class LabGuard:
    def __init__(self, lab_root, target_org="OWN"):
        if not lab_root:
            raise GuardError("Explicit --lab-root is required.")
        if target_org != "OWN":
            raise GuardError("Only --target-org OWN is permitted in lab mode.")
        self.lab_root = Path(lab_root)
        self.reports = self.lab_root / "reports"
        self.reports.mkdir(parents=True, exist_ok=True)

    def refuse_org(self, org):
        o = org.lower().strip()
        if not (o.endswith(".example") or o in ("acme-lab", "acme-lab internal", "internal drills")):
            raise GuardError(f"Refusing org '{org}': only synthetic (.example) org names allowed.")

    def watermark(self, text):
        return f"[{WATERMARK}]\n{text}"


class AttackType(Enum):
    PHISHING = "phishing"
    VISHING = "vishing"
    SMISHING = "smishing"
    PRETEXTING = "pretexting"
    BAITING = "baiting"
    TAILGATING = "tailgating"
    QUID_PRO_QUO = "quid_pro_quo"


class SyntheticBank:
    CALLER_NAMES = ["Priya Sharma", "James Okafor", "Maria González-Díaz",
                    "Kenji Watanabe", "Ana Petrova", "Tomás Silva"]
    ROLES = ["IT helpdesk", "facilities coordinator", "finance analyst",
             "executive assistant", "office manager", "vendor relations"]

    def __init__(self, seed=42):
        self.rng = random.Random(seed)

    def persona(self):
        name = self.rng.choice(self.CALLER_NAMES)
        role = self.rng.choice(self.ROLES)
        return {
            "name": name,
            "role": role,
            "org": "acme-lab.example",
            "email": f"{re.sub('[^a-z]+', '.', name.lower())}@example.com",
            "badge": f"DRILL-{self.rng.randint(1000, 9999)}",
        }


class BackstoryBuilder:
    """Builds internally consistent synthetic backstories."""

    ANTECEDENTS = [
        "onboarding a new vendor", "resolving yesterday's badge reader outage",
        "handling the quarterly PAM review", "coordinating the fire-drill elevator tie-out",
    ]
    URGENCY = ["by end of shift", "before the 2pm stand-up", "within the change window",
               "ahead of the auditor visit"]

    def __init__(self, seed=42):
        self.bank = SyntheticBank(seed)

    def build(self, pretext_type: str):
        persona = self.bank.persona()
        story = (
            f"{persona['name']}, {persona['role']} at {persona['org']}, is "
            f"{self.bank.rng.choice(self.ANTECEDENTS)} and needs help "
            f"{self.bank.rng.choice(self.URGENCY)}."
        )
        return {
            "persona": persona,
            "pretext_type": pretext_type,
            "premise": f"[{DRILL_BRAND}] {story}",
            "drill_id": f"drill-{self.bank.rng.randint(100000, 999999)}",
            "watermark": WATERMARK,
        }


class CallMatrix:
    """Maps drill role-plays: opening / ask / resistance / expected handling."""

    MATRIX = {
        "helpdesk_triage": {
            "opening": "Hi, this is {caller} from internal IT — we're re-issuing PAM tokens today.",
            "ask": "Please read back the last 4 digits of the asset tag on your badge.",
            "resistance_without_verification": "drops the request; asks for the ticket number",
            "expected_handling": "caller verifies via internal directory before confirming anything",
        },
        "facilities_pickup": {
            "opening": "Facilities here — we're collecting badges for the badge-reader firmware swap.",
            "ask": "Hand over your badge for reprogramming.",
            "resistance_without_verification": "refuses; escalates to security desk",
            "expected_handling": "badge handover happens only against a signed log",
        },
        "finance_adjustment": {
            "opening": "Finance checking the expense feed for {org}.",
            "ask": "Confirm your direct-deposit routing on file.",
            "resistance_without_verification": "declines; asks caller to open a formal ticket",
            "expected_handling": "no account details shared over the phone",
        },
    }

    def __init__(self, bank=None):
        self.bank = bank or SyntheticBank()

    def rows(self):
        rows = []
        for key, m in self.MATRIX.items():
            p = self.bank.persona()
            rows.append({
                "scenario": key,
                "drill_type": "role-play",
                "caller": f"{p['name']} ({p['role']}, {DRILL_BRAND})",
                "opening": m["opening"].format(caller=p["name"], org="acme-lab.example"),
                "ask": m["ask"],
                "resistance_without_verification": m["resistance_without_verification"],
                "expected_handling": m["expected_handling"],
                "watermarked": True,
            })
        return rows


class LogPlausibility:
    """Defensive plausibility scorer for simulated drill call logs."""

    GOOD_SIGNS = ["ticket number", "verified", "directory", "escalated", "security desk",
                  "signed log", "declined", "callback"]
    BAD_SIGNS = ["gave password", "shared token", "read back pin", "handed over badge without log"]

    def score(self, log_text: str) -> Dict:
        low = log_text.lower()
        good = sum(1 for s in self.GOOD_SIGNS if s in low)
        bad = sum(1 for s in self.BAD_SIGNS if s in low)
        score = min(100, 40 + good * 10 - bad * 20)
        return {
            "plausibility_score": max(0, score),
            "good_signals": good,
            "bad_signals": bad,
            "verdict": "trainer_review" if bad else ("plausible" if good > 0 else "unremarkable"),
            "watermark": WATERMARK,
        }


class PretextEngine:
    def __init__(self, guard, seed=42):
        self.guard = guard
        self.seed = seed
        self.bank = SyntheticBank(seed)
        self.backstory = BackstoryBuilder(seed)
        self.matrix = CallMatrix(self.bank)
        self.plausibility = LogPlausibility()

    def run(self):
        scenarios = []
        for atype in ("pretexting", "vishing", "tailgating"):
            scenarios.append(self.backstory.build(atype))
        rows = self.matrix.rows()
        sample_log = ("Trainee 02 callback: 'I verified the caller against the internal "
                      "directory and escalated to the security desk; ticket number 00812.'")
        plaus = self.plausibility.score(sample_log)
        report = {
            "watermark": WATERMARK,
            "drill_brand": DRILL_BRAND,
            "generated": datetime.now().isoformat(),
            "seed": self.seed,
            "scenarios": scenarios,
            "call_matrix": rows,
            "plausibility_check": plaus,
        }
        report_path = self.guard.reports / "pretext_report.json"
        report_path.write_text(json.dumps(report, indent=2))
        report["report_path"] = str(report_path)
        return report

    def render_markdown(self, report):
        md = [f"# SE3 Pretext Lab Report [{DRILL_BRAND}]", ""]
        md.append(f"_generated: {report['generated']} — seed {report['seed']}_")
        for s in report["scenarios"]:
            md.append(f"\n## {s['pretext_type']}\n\n{s['premise']}")
        md.append("\n# Call Matrix\n")
        for r in report["call_matrix"]:
            md.append(f"- **{r['scenario']}** — opening: {r['opening']} | ask: {r['ask']} | "
                      f"expected handling: {r['expected_handling']}")
        md.append(f"\n# Plausibility check: {report['plausibility_check']}\n")
        return "\n".join(md)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(
        prog="se3-pretext",
        description="Synthetic pretext / call-matrix lab generator (authorized drills only).")
    p.add_argument("--lab-root", required=True)
    p.add_argument("--target-org", default="OWN")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--demo", action="store_true")
    p.add_argument("--report-md", action="store_true",
                   help="Also write a Markdown report alongside JSON.")
    args = p.parse_args(argv)

    guard = LabGuard(args.lab_root, args.target_org)
    engine = PretextEngine(guard, args.seed)

    print(f"SE3 Pretext Lab Generator [{DRILL_BRAND}] [{WATERMARK}]")
    print("=" * 60)

    report = engine.run()
    print(f"\nDrill scenarios generated: {len(report['scenarios'])}")
    for s in report["scenarios"]:
        print(f"  [{s['pretext_type']}] {s['premise']}")
    print(f"\nCall-matrix entries: {len(report['call_matrix'])}")
    for r in report["call_matrix"]:
        print(f"  * {r['scenario']:<20} expected handling: {r['expected_handling'][:48]}...")
    pchk = report["plausibility_check"]
    print(f"\nPlausibility check: score={pchk['plausibility_score']} "
          f"verdict={pchk['verdict']} (good={pchk['good_signals']} bad={pchk['bad_signals']})")
    if args.report_md:
        md = engine.render_markdown(report)
        md_path = guard.reports / "pretext_report.md"
        md_path.write_text(md)
        print(f"\nMarkdown report: {md_path}")
    print(f"\nJSON report: {report['report_path']}")
    print("\nDemo complete (offline, synthetic, authorized-drill branding). Exit 0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())