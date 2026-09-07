#!/usr/bin/env python3
"""
SE3 — Pretext Generator (lab-sealed)
Pretext scenario generation, victim profiling, attack path planning, reporting.

ANTI-ABUSE: requires an explicit --lab-root and --target-org OWN. Only synthetic
personas and .example org names are accepted. All scenarios carry
"AUTHORIZED INTERNAL DRILL" branding.
"""

import argparse
import json
import random
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

WATERMARK = "SIMULATION / AUTHORIZED TRAINING ONLY"
DRILL_BRAND = "AUTHORIZED INTERNAL DRILL"


class GuardError(Exception):
    pass


class LabGuard:
    def __init__(self, lab_root=None, target_org="OWN"):
        if not lab_root:
            raise GuardError("Explicit --lab-root is required.")
        if target_org != "OWN":
            raise GuardError("Only --target-org OWN is permitted in lab mode.")
        self.lab_root = Path(lab_root)
        self.reports = self.lab_root / "reports"
        self.reports.mkdir(parents=True, exist_ok=True)

    def refuse_org(self, org):
        if not str(org).lower().endswith((".example", ".lab")):
            raise GuardError(f"Refusing org '{org}': only synthetic .example names allowed.")

    def watermark(self, text):
        return f"[{WATERMARK}]\n{text}"


class AttackType(Enum):
    """Types of social engineering attacks"""
    PHISHING = "phishing"
    VISHING = "vishing"
    SMISHING = "smishing"
    PRETEXTING = "pretexting"
    BAITING = "baiting"
    TAILGATING = "tailgating"
    QUID_PRO_QUO = "quid_pro_quo"


class PretextScenario:
    """Generate pretext scenarios"""
    
    def __init__(self):
        self.scenarios = {
            AttackType.PRETEXTING: [
                {
                    "name": "IT Support",
                    "description": "Impersonate IT support to gain access to systems",
                    "approach": "Call target claiming to be from IT helpdesk",
                    "objective": "Obtain login credentials or remote access",
                    "tools_needed": ["Caller ID spoofing", "Internal knowledge"],
                    "risk_level": "medium"
                },
                {
                    "name": "New Employee",
                    "description": "Pose as a new employee needing assistance",
                    "approach": "Visit office claiming to be new hire",
                    "objective": "Physical access or credential harvesting",
                    "tools_needed": ["Fake badge", "Business attire"],
                    "risk_level": "high"
                },
                {
                    "name": "Vendor Delivery",
                    "description": "Pose as vendor delivering equipment",
                    "approach": "Arrive with boxes claiming delivery",
                    "objective": "Physical access to server room or offices",
                    "tools_needed": ["Uniform", "Fake delivery form"],
                    "risk_level": "high"
                }
            ],
            AttackType.PHISHING: [
                {
                    "name": "Password Reset",
                    "description": "Send password reset email from fake domain",
                    "approach": "Craft email mimicking internal IT",
                    "objective": "Harvest credentials",
                    "tools_needed": ["Lookalike domain", "Email templates"],
                    "risk_level": "medium"
                },
                {
                    "name": "Invoice Scam",
                    "description": "Send fake invoice requiring payment",
                    "approach": "Email with urgent payment request",
                    "objective": "Financial fraud or credential theft",
                    "tools_needed": ["Fake invoice", "Urgent language"],
                    "risk_level": "medium"
                }
            ],
            AttackType.VISHING: [
                {
                    "name": "Bank Fraud Alert",
                    "description": "Call claiming suspicious account activity",
                    "approach": "Call from spoofed bank number",
                    "objective": "Obtain account details or PIN",
                    "tools_needed": ["VoIP setup", "Script"],
                    "risk_level": "medium"
                },
                {
                    "name": "Tax Authority",
                    "description": "Impersonate IRS or tax authority",
                    "approach": "Urgent call about tax issues",
                    "objective": "Payment or personal information",
                    "tools_needed": ["Authority persona", "Threats of legal action"],
                    "risk_level": "high"
                }
            ],
            AttackType.SMISHING: [
                {
                    "name": "Package Delivery",
                    "description": "SMS about package requiring action",
                    "approach": "Text with malicious link",
                    "objective": "Install malware or harvest credentials",
                    "tools_needed": ["Shortened URL", "Urgency"],
                    "risk_level": "low"
                },
                {
                    "name": "Account Verification",
                    "description": "SMS claiming account needs verification",
                    "approach": "Text from 'bank' or service",
                    "objective": "Credential harvesting",
                    "tools_needed": ["Spoofed number", "Fake link"],
                    "risk_level": "low"
                }
            ]
        }
    
    def generate_scenario(self, attack_type: AttackType, custom_params: Optional[Dict] = None) -> Dict:
        """Generate a pretext scenario"""
        scenarios = self.scenarios.get(attack_type, [])
        if not scenarios:
            raise ValueError(f"No scenarios for attack type: {attack_type}")
        
        scenario = random.choice(scenarios).copy()
        scenario["attack_type"] = attack_type.value
        scenario["generated"] = datetime.now().isoformat()
        scenario["drill_brand"] = DRILL_BRAND
        scenario["watermark"] = WATERMARK
        scenario["approach"] = f"[{DRILL_BRAND}] {scenario['approach']}"
        
        if custom_params:
            scenario.update(custom_params)
        
        return scenario
    
    def list_scenarios(self, attack_type: Optional[AttackType] = None) -> List[Dict]:
        """List available scenarios"""
        if attack_type:
            return self.scenarios.get(attack_type, [])
        
        all_scenarios = []
        for scenarios in self.scenarios.values():
            all_scenarios.extend(scenarios)
        return all_scenarios


class VictimProfile:
    """Profile potential targets"""
    
    def __init__(self):
        self.profiles = {}
    
    def create_profile(self, target_id: str, data: Dict) -> Dict:
        """Create a victim profile"""
        profile = {
            "target_id": target_id,
            "created": datetime.now().isoformat(),
            "demographics": data.get("demographics", {}),
            "behavioral": data.get("behavioral", {}),
            "technical": data.get("technical", {}),
            "organizational": data.get("organizational", {}),
            "vulnerabilities": [],
            "susceptibility_score": 0
        }
        
        # Calculate susceptibility score
        profile["susceptibility_score"] = self.calculate_susceptibility(profile)
        
        self.profiles[target_id] = profile
        return profile
    
    def calculate_susceptibility(self, profile: Dict) -> int:
        """Calculate susceptibility score (0-100)"""
        score = 50  # Base score
        
        # Behavioral factors
        behavioral = profile.get("behavioral", {})
        if behavioral.get("helpful", False):
            score += 10
        if behavioral.get("trusting", False):
            score += 15
        if behavioral.get("busy", False):
            score += 10
        if behavioral.get("authority_responsive", False):
            score += 15
        
        # Technical factors
        technical = profile.get("technical", {})
        if technical.get("technical_savvy", False):
            score -= 20
        if technical.get("security_aware", False):
            score -= 25
        
        return max(0, min(100, score))
    
    def add_vulnerability(self, target_id: str, vulnerability: str):
        """Add vulnerability to profile"""
        if target_id in self.profiles:
            self.profiles[target_id]["vulnerabilities"].append({
                "vulnerability": vulnerability,
                "added": datetime.now().isoformat()
            })
            # Update susceptibility
            self.profiles[target_id]["susceptibility_score"] = self.calculate_susceptibility(
                self.profiles[target_id]
            )
    
    def get_profile(self, target_id: str) -> Optional[Dict]:
        """Get profile by ID"""
        return self.profiles.get(target_id)
    
    def get_high_value_targets(self, threshold: int = 70) -> List[Dict]:
        """Get high-value targets based on susceptibility"""
        high_value = []
        for target_id, profile in self.profiles.items():
            if profile["susceptibility_score"] >= threshold:
                high_value.append(profile)
        return high_value


class AttackPathPlanner:
    """Plan attack paths and sequences"""
    
    def __init__(self):
        self.paths = {}
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load attack path templates"""
        return {
            "credential_harvest": [
                {"step": 1, "action": "Reconnaissance", "details": "Gather target information"},
                {"step": 2, "action": "Pretext Selection", "details": "Choose appropriate pretext"},
                {"step": 3, "action": "Initial Contact", "details": "Make first contact with target"},
                {"step": 4, "action": "Trust Building", "details": "Establish rapport and credibility"},
                {"step": 5, "action": "Credential Request", "details": "Request credentials under pretext"},
                {"step": 6, "action": "Validation", "details": "Verify captured credentials work"}
            ],
            "physical_access": [
                {"step": 1, "action": "Site Survey", "details": "Map building layout and security"},
                {"step": 2, "action": "Persona Creation", "details": "Develop cover identity"},
                {"step": 3, "action": "Entry Attempt", "details": "Gain physical access"},
                {"step": 4, "action": "Navigation", "details": "Move through facility undetected"},
                {"step": 5, "action": "Objective", "details": "Complete primary objective"},
                {"step": 6, "action": "Exfiltration", "details": "Exit without detection"}
            ],
            "data_exfiltration": [
                {"step": 1, "action": "Target Selection", "details": "Identify valuable data"},
                {"step": 2, "action": "Access Method", "details": "Determine access approach"},
                {"step": 3, "action": "Data Discovery", "details": "Locate target data"},
                {"step": 4, "action": "Extraction", "details": "Copy or transfer data"},
                {"step": 5, "action": "Cover Tracks", "details": "Remove evidence"},
                {"step": 6, "action": "Delivery", "details": "Securely deliver data"}
            ]
        }
    
    def create_path(self, path_name: str, template_type: str, 
                    custom_steps: Optional[List[Dict]] = None) -> Dict:
        """Create a new attack path"""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template: {template_type}")
        
        steps = custom_steps or self.templates[template_type]
        
        path = {
            "name": path_name,
            "template": template_type,
            "created": datetime.now().isoformat(),
            "steps": steps,
            "status": "planned",
            "estimated_duration": f"{len(steps) * 30} minutes"
        }
        
        self.paths[path_name] = path
        return path
    
    def update_step_status(self, path_name: str, step_number: int, 
                          status: str, notes: Optional[str] = None):
        """Update status of a step in the path"""
        if path_name in self.paths:
            for step in self.paths[path_name]["steps"]:
                if step["step"] == step_number:
                    step["status"] = status
                    step["notes"] = notes
                    step["updated"] = datetime.now().isoformat()
    
    def get_path(self, path_name: str) -> Optional[Dict]:
        """Get path by name"""
        return self.paths.get(path_name)
    
    def get_all_paths(self) -> Dict:
        """Get all paths"""
        return self.paths


class ReportingTemplates:
    """Generate reports for social engineering engagements"""
    
    def __init__(self):
        self.templates = {
            "executive_summary": """
EXECUTIVE SUMMARY
================

Engagement: {engagement_name}
Date: {date}
Tester: {tester_name}
Target Organization: {target_org}

Objective:
{objective}

Key Findings:
{key_findings}

Risk Assessment: {risk_level}
Recommendations: {recommendations}
""",
            "detailed_report": """
DETAILED ENGAGEMENT REPORT
=========================

1. ENGAGEMENT OVERVIEW
----------------------
{overview}

2. METHODOLOGY
--------------
{methodology}

3. TIMELINE
-----------
{timeline}

4. FINDINGS
-----------
{findings}

5. VULNERABILITIES IDENTIFIED
----------------------------
{vulnerabilities}

6. RECOMMENDATIONS
-----------------
{recommendations}

7. APPENDIX
-----------
{appendix}
""",
            "incident_report": """
INCIDENT REPORT
===============

Incident ID: {incident_id}
Reported By: {reporter}
Date/Time: {datetime}
Severity: {severity}

Description:
{description}

Impact:
{impact}

Response Actions:
{response_actions}

Lessons Learned:
{lessons_learned}
"""
        }
    
    def generate_report(self, template_type: str, data: Dict) -> str:
        """Generate report from template"""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template: {template_type}")
        
        template = self.templates[template_type]
        return template.format(**data)
    
    def save_report(self, content: str, filepath: str):
        """Save report to file"""
        with open(filepath, "w") as f:
            f.write(content)


class PretextGenerator:
    """Main pretext generation system (lab-sealed)"""

    def __init__(self, lab_root=None, target_org="OWN"):
        self.guard = LabGuard(lab_root, target_org)
        self.scenario_gen = PretextScenario()
        self.victim_profiler = VictimProfile()
        self.path_planner = AttackPathPlanner()
        self.reporter = ReportingTemplates()
        self.engagements = {}
    
    def create_engagement(self, name: str, target_org: str, 
                         objectives: List[str]) -> Dict:
        """Create a new engagement (synthetic org only)"""
        self.guard.refuse_org(target_org)
        engagement = {
            "name": name,
            "target_org": target_org,
            "created": datetime.now().isoformat(),
            "objectives": objectives,
            "scenarios": [],
            "profiles": [],
            "paths": [],
            "status": "planning"
        }
        
        self.engagements[name] = engagement
        return engagement
    
    def generate_full_plan(self, engagement_name: str, 
                          attack_types: List[AttackType]) -> Dict:
        """Generate a complete attack plan"""
        if engagement_name not in self.engagements:
            raise ValueError(f"Engagement not found: {engagement_name}")
        
        engagement = self.engagements[engagement_name]
        
        # Generate scenarios for each attack type
        for attack_type in attack_types:
            scenario = self.scenario_gen.generate_scenario(attack_type)
            engagement["scenarios"].append(scenario)
        
        # Create attack path
        path = self.path_planner.create_path(
            f"{engagement_name}_path",
            "credential_harvest"
        )
        engagement["paths"].append(path["name"])
        
        return engagement
    
    def generate_report(self, engagement_name: str, report_type: str = "executive_summary") -> str:
        """Generate report for engagement"""
        if engagement_name not in self.engagements:
            raise ValueError(f"Engagement not found: {engagement_name}")
        
        engagement = self.engagements[engagement_name]
        
        data = {
            "engagement_name": engagement_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tester_name": "Security Consultant",
            "target_org": engagement["target_org"],
            "objective": "\n".join(f"- {obj}" for obj in engagement["objectives"]),
            "key_findings": self._generate_findings(engagement),
            "risk_level": "Medium",
            "recommendations": self._generate_recommendations(),
            "overview": f"Social engineering engagement against {engagement['target_org']}",
            "methodology": "Pretexting and phishing combined approach",
            "timeline": "See detailed logs",
            "findings": "See executive summary",
            "vulnerabilities": "Employee awareness gaps identified",
            "appendix": "Supporting documentation"
        }
        
        return self.reporter.generate_report(report_type, data)
    
    def _generate_findings(self, engagement: Dict) -> str:
        """Generate findings based on engagement"""
        findings = []
        for scenario in engagement.get("scenarios", []):
            findings.append(f"- {scenario['name']}: {scenario['description']}")
        return "\n".join(findings) if findings else "No findings yet"
    
    def _generate_recommendations(self) -> str:
        """Generate recommendations"""
        return """1. Conduct security awareness training
2. Implement multi-factor authentication
3. Establish verification procedures for sensitive requests
4. Create clear reporting channels for suspicious activity
5. Regular phishing simulation exercises"""
    
    def export_engagement(self, engagement_name: str, filepath: str):
        """Export engagement to JSON"""
        if engagement_name not in self.engagements:
            raise ValueError(f"Engagement not found: {engagement_name}")
        
        with open(filepath, "w") as f:
            json.dump(self.engagements[engagement_name], f, indent=2, default=str)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="SE3 Pretext Generator (lab-sealed).")
    ap.add_argument("--lab-root", required=True)
    ap.add_argument("--target-org", default="OWN")
    args = ap.parse_args(sys.argv[1:])

    generator = PretextGenerator(args.lab_root, args.target_org)
    print(f"SE3 — Pretext Generator [{DRILL_BRAND}]")
    print("=" * 40)

    print("\n[*] Creating sample engagement...")
    engagement = generator.create_engagement(
        name="Test Engagement",
        target_org="acme-lab.example",
        objectives=["Test employee awareness", "Identify security gaps"]
    )
    
    # Generate full plan
    print("[*] Generating attack plan...")
    plan = generator.generate_full_plan(
        "Test Engagement",
        [AttackType.PRETEXTING, AttackType.PHISHING]
    )
    
    print(f"\nEngagement: {plan['name']}")
    print(f"Target: {plan['target_org']}")
    print(f"Scenarios generated: {len(plan['scenarios'])}")
    
    # Show generated scenarios
    print("\nGenerated scenarios:")
    for i, scenario in enumerate(plan["scenarios"], 1):
        print(f"  {i}. {scenario['name']} ({scenario['attack_type']})")
        print(f"     Risk: {scenario['risk_level']}")
    
    # Generate report
    print("\n[*] Generating executive summary...")
    report = generator.generate_report("Test Engagement", "executive_summary")
    print(report)
    
    print("\nUsage:")
    print("  generator = PretextGenerator()")
    print("  engagement = generator.create_engagement('My Engagement', 'Target Org', ['Objective 1'])")
    print("  plan = generator.generate_full_plan('My Engagement', [AttackType.PRETEXTING])")
    print("  report = generator.generate_report('My Engagement')")
