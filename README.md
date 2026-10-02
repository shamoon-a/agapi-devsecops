# AGAPI Tooling & DevSecOps Take-Home Assessment

## Selected Tasks

This submission implements:

- Task 2: SAST scanning using Semgrep
- Task 3: Automated security triage reporting

The solution is designed to run locally on Linux or macOS using Python 3 and Docker.

---

## Architecture

The workflow is:

Code
  |
  v
Semgrep SAST
  |
  v
Raw JSON
  |
  v
Normalization + Severity Mapping
  |
  +--> Security Gate
  |
  v
Deterministic Triage Report

---

## Project Structure

```text
.
├── README.md
├── run.sh
├── agapi_app/
│   └── example.py
├── config/
│   └── semgrep.yml
├── scripts/
│   ├── scan_sast.py
│   └── triage_report.py
└── artifacts/
    ├── sast.raw.json
    ├── sast.json
    └── triage.md
