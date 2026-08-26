# SE3 — Pretext Generator

Pretext scenario generation, victim profiling, attack path planning, reporting templates.

## Overview

This project implements a social engineering pretext generation system that:
- Creates realistic pretext scenarios for various attack types
- Profiles potential victims based on behavioral factors
- Plans detailed attack paths with step-by-step procedures
- Generates professional engagement reports
- Manages full social engineering engagements

## Features

- **Scenario Generation**: Multiple pretext templates for phishing, vishing, pretexting
- **Victim Profiling**: Susceptibility scoring and vulnerability assessment
- **Attack Path Planning**: Step-by-step attack procedures
- **Report Templates**: Executive summaries, detailed reports, incident reports
- **Engagement Management**: Track multiple engagements and objectives

## Installation

No external dependencies required — uses Python standard library only.

```bash
python3 pretext_generator.py
```

## Usage

### Generate Pretext Scenario
```python
from pretext_generator import PretextScenario, AttackType

scenario_gen = PretextScenario()
scenario = scenario_gen.generate_scenario(AttackType.PRETEXTING)
print(f"Scenario: {scenario['name']}")
print(f"Approach: {scenario['approach']}")
```

### Create Victim Profile
```python
from pretext_generator import VictimProfile

profiler = VictimProfile()
profile = profiler.create_profile("target_001", {
    "demographics": {"role": "manager"},
    "behavioral": {"helpful": True, "busy": True}
})
print(f"Susceptibility: {profile['susceptibility_score']}")
```

### Plan Attack Path
```python
from pretext_generator import AttackPathPlanner

planner = AttackPathPlanner()
path = planner.create_path("credential_harvest", "credential_harvest")
print(f"Steps: {len(path['steps'])}")
```

### Generate Report
```python
from pretext_generator import PretextGenerator

generator = PretextGenerator()
generator.create_engagement("Test", "Target Corp", ["Test awareness"])
report = generator.generate_report("Test", "executive_summary")
print(report)
```

### Full Engagement
```python
from pretext_generator import PretextGenerator, AttackType

generator = PretextGenerator()
engagement = generator.create_engagement(
    name="Red Team Assessment",
    target_org="Example Corp",
    objectives=["Test employee awareness", "Identify gaps"]
)

plan = generator.generate_full_plan(
    "Red Team Assessment",
    [AttackType.PRETEXTING, AttackType.PHISHING]
)
```

## Example Output

```
SE3 — Pretext Generator
========================================

[*] Creating sample engagement...
[*] Generating attack plan...

Engagement: Test Engagement
Target: Example Corp
Scenarios generated: 2

Generated scenarios:
  1. IT Support (pretexting)
     Risk: medium
  2. Invoice Scam (phishing)
     Risk: medium

[*] Generating executive summary...

EXECUTIVE SUMMARY
================

Engagement: Test Engagement
Date: 2026-03-15
...
```

## Attack Types Supported

- **Phishing**: Email-based attacks
- **Vishing**: Voice-based attacks
- **Smishing**: SMS-based attacks
- **Pretexting**: In-person deception
- **Baiting**: Leaving诱饵 devices
- **Tailgating**: Following authorized personnel
- **Quid Pro Quo**: Exchange of services

## Legal Disclaimer

**IMPORTANT: Read before use.**

This project is provided for **educational and authorized security testing purposes only**. 

### Authorization Requirements
- You MUST have explicit written permission from the network owner before using this tool
- Unauthorized interception of network communications is illegal under federal and state laws
- This tool should ONLY be used on networks you own or have written authorization to test

### Legal Framework
- **Computer Fraud and Abuse Act (CFAA)**: Unauthorized access to computer systems is a federal crime
- **Wiretap Act (18 U.S.C. § 2511)**: Interception of electronic communications without consent is illegal
- **State Laws**: Many states have additional computer crime and wiretapping statutes
- **GDPR/CCPA**: Data collection may be subject to privacy regulations

### Acceptable Use
- Testing security of your own networks
- Authorized penetration testing with written scope
- Academic research in controlled lab environments
- Security education and training

### Prohibited Use
- Intercepting communications on networks you do not own
- Attacking infrastructure without authorization
- Any activity that violates applicable laws or regulations
- Commercial use without proper licensing

### No Warranty
This software is provided "AS IS" without warranty of any kind. The author is not responsible for any misuse or damage caused by this software.

### Responsible Disclosure
If you discover vulnerabilities using this tool, follow responsible disclosure practices:
1. Report to the vendor/owner privately
2. Allow reasonable time for remediation
3. Do not exploit beyond proof of concept

## License

MIT
