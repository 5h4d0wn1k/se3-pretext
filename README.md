> **⚠️ EDUCATIONAL USE ONLY — AUTHORIZED TESTING ONLY.**
> This project exists for education, research, and **defense of systems you own
> or hold explicit written authorization to assess**. Unauthorized use is
> prohibited and may be illegal. Read [ETHICS.md](ETHICS.md) and
> [SCOPE.md](SCOPE.md) before use. Use at your own risk; **AS IS**, no warranty.

# SE3 — Pretext Scenario Builder

A consent-first **social engineering** engagement planner: builds synthetic
call personas, a scenario→response call matrix, and a defensive log-plausibility
checker for **authorized internal security awareness drills**.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/5h4d0wn1k/se3-pretext)](https://github.com/5h4d0wn1k/se3-pretext)
[![Last commit](https://img.shields.io/github/last-commit/5h4d0wn1k/se3-pretext)](https://github.com/5h4d0wn1k/se3-pretext)
[![Issues](https://img.shields.io/github/issues/5h4d0wn1k/se3-pretext)](https://github.com/5h4d0wn1k/se3-pretext)

## Why SE3

The human layer is the weakest link — and the only ethical way to test it is a
fully consented, synthetic drill. SE3 generates branded, internally consistent
pretext scenarios using only `acme-lab.example` personas and `example.com`
addresses: no real organizations, no real personal data. It supports the
**consent-first** drill workflow — backstories, a call matrix, expected-handling
tables, and a defensive log-plausibility scorer so awareness teams can see
whether participants followed procedure. It is for **authorized internal
drills only**; using generated pretexts against real people is prohibited.

## Features

- **Backstory builder** — synthetic, internally consistent caller personas and drill premises
- **Call matrix** — scenario → opening / ask / resistance / expected handling table
- **Log plausibility checker (defensive)** — scores simulated drill call logs for realism and red flags
- **Guard rails** — `--target-org` locked to `OWN`; synthetic `.example` org names only
- **Reports** — JSON and Markdown under `lab-root/reports/`
- **Deterministic** — reproducible personas per `--seed`
- **Legacy generator** — `pretext_generator.py` sealed/read-only

## Quickstart

```bash
# Offline demo (JSON report)
python3 se3_cli.py --lab-root ./lab --demo

# Demo with Markdown report
python3 se3_cli.py --lab-root ./lab --demo --report-md

# Deterministic persona generation
python3 se3_cli.py --lab-root ./lab --seed 7

# Tests
python3 -m unittest discover -s tests
```

Every run requires an explicit `--lab-root`; all scenarios carry
`AUTHORIZED INTERNAL DRILL` branding and the watermark
`SIMULATION / AUTHORIZED TRAINING ONLY`.

## Project structure

- `se3_cli.py` — modern consent-first CLI
- `pretext_generator.py` — legacy generator (sealed)
- `tests/` — 12 offline tests covering guards, matrices, and plausibility

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

MIT — see [LICENSE](LICENSE).

## Legal

- [ETHICS.md](ETHICS.md) · [SCOPE.md](SCOPE.md) · [SECURITY.md](SECURITY.md)