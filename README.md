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

## Quick start - how to run

## Step 1 - Clone the repository
git clone https://github.com/shamoon-a/agapi-devsecops.git
cd agapi-devsecops

## Step 2 - Verify prerequisites
Python 3 and Docker are required. Docker Desktop must be running on macOS.
python3 --version
docker --version
docker info

## Step 3 - Run with the default HIGH threshold
./run.sh
echo $?
Expected behavior with the included vulnerable sample: two HIGH findings and one MEDIUM finding are detected. The
security gate fails and the final exit code is 1.
Result: FAILED - security findings exceeded threshold
1

## Step 4 - Run with a different threshold
MIN_SEVERITY=CRITICAL ./run.sh
echo $?
Because the sample contains no CRITICAL findings, this run passes and returns 0.
Result: PASSED
0

## Step 5 - Review generated artifacts
ls -lh artifacts/
python3 -m json.tool artifacts/sast.json
cat artifacts/triage.md
