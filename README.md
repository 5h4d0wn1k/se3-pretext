# SE3 — Pretext Lab Generator

Synthetic pretext / call-matrix framework for **AUTHORIZED INTERNAL DRILLS** only.
Generates branded drill scenarios, a call matrix, backstory builder, and a defensive
log-plausibility checker. No real organizations, no real personal data: only
`acme-lab.example` personas and `example.com` addresses.

## Features

- **Backstory builder** — internally consistent, synthetic caller personas and drill premises.
- **Call matrix** — scenario → opening / ask / resistance / expected handling table.
- **Log plausibility check (defensive)** — scores simulated drill call logs for realism
  and red flags (trained vs. risky handling).
- **JSON + Markdown reports** under `lab-root/reports/`.

## IMPORTANT: Read before use.

Provided for **educational and authorized security testing purposes only**.

### Authorization Requirements
- Must be an approved internal drill with informed participants and a signed scope.
- `--target-org` is locked to `OWN`; synthetic `.example` org names only.
- Requests to remove drill branding or synthetic-only constraints will be refused.

### Anti-Abuse Safeguards
- Every run requires an explicit `--lab-root`.
- All scenarios carry `AUTHORIZED INTERNAL DRILL` branding and the watermark
  "SIMULATION / AUTHORIZED TRAINING ONLY".
- Dry-run free; reports only ever contain synthetic personas.

### Legal Framework
- **CFAA (18 U.S.C. § 1030)**, **wire fraud (18 U.S.C. § 1343)**, state wiretap and
  fraud statutes, **GDPR/CCPA**.

### Prohibited Use
- Using generated pretexts against real people or organizations.
- Non-consensual testing of any person.

### No Warranty
Provided "AS IS". Author accepts no liability for misuse.

### Responsible Disclosure
Report findings privately with a remediation window.

## Live Lab Test Plan

1. `python3 se3_cli.py --lab-root ./lab --demo` → exit 0, JSON report.
2. `python3 se3_cli.py --lab-root ./lab --demo --report-md` → also writes Markdown.
3. `python3 pretext_generator.py --lab-root ./lab` → legacy generator, sealed.
4. Negative: `python3 se3_cli.py --lab-root ./lab --target-org WellsFargo` exits non-zero.
5. `python -m unittest discover -s tests` → 12 offline tests pass.

## Metrics

- Synthetic personas: 7 names × roles, deterministic per seed.
- Call-matrix entries: 3 role-plays.
- Plausibility verdicts: `plausible` / `unremarkable` / `trainer_review`.
- Test count: 12.
- Reports: `pretext_report.json` (+ optional `.md`).

## Usage

```bash
python3 se3_cli.py --lab-root ./lab --demo
python3 se3_cli.py --lab-root ./lab --demo --report-md
python3 se3_cli.py --lab-root ./lab --seed 7
```

## License

MIT