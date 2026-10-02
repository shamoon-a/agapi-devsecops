#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"

RAW_FILE = ARTIFACTS / "sast.raw.json"
NORMALIZED_FILE = ARTIFACTS / "sast.json"

MIN_SEVERITY = os.getenv("MIN_SEVERITY", "HIGH").upper()

SEVERITY_ORDER = {
    "INFO": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}

SEMGREP_MAP = {
    "INFO": "LOW",
    "WARNING": "MEDIUM",
    "ERROR": "HIGH",
}

if MIN_SEVERITY not in SEVERITY_ORDER:
    print(
        f"ERROR: Invalid MIN_SEVERITY={MIN_SEVERITY}. "
        "Use INFO, LOW, MEDIUM, HIGH or CRITICAL."
    )
    sys.exit(2)

ARTIFACTS.mkdir(exist_ok=True)

cmd = [
    "docker",
    "run",
    "--rm",
    "-v",
    f"{ROOT}:/src",
    "-w",
    "/src",
    "semgrep/semgrep@sha256:32e459968daabe7ab86968184a29109b9564aa00392401156f9788452b42786b",
    "semgrep",
    "scan",
    "--config",
    "config/semgrep.yml",
    "--json",
    "agapi_app",
]

print("Running Semgrep SAST scan...")

result = subprocess.run(
    cmd,
    capture_output=True,
    text=True
)

if not result.stdout.strip():
    print("ERROR: Semgrep produced no JSON output.")
    print(result.stderr)
    sys.exit(2)

try:
    raw = json.loads(result.stdout)
except json.JSONDecodeError:
    print("ERROR: Unable to parse Semgrep JSON.")
    print(result.stdout)
    sys.exit(2)

with RAW_FILE.open("w") as f:
    json.dump(raw, f, indent=2, sort_keys=True)

findings = []

for item in raw.get("results", []):
    extra = item.get("extra", {})

    semgrep_severity = extra.get("severity", "INFO").upper()
    severity = SEMGREP_MAP.get(semgrep_severity, "LOW")

    metadata = extra.get("metadata", {})

    finding = {
        "rule_id": item.get("check_id", "unknown"),
        "severity": severity,
        "category": metadata.get("category", "uncategorized"),
        "path": item.get("path", "unknown"),
        "line": item.get("start", {}).get("line", 0),
        "message": extra.get("message", ""),
    }

    findings.append(finding)

findings.sort(
    key=lambda x: (
        -SEVERITY_ORDER[x["severity"]],
        x["path"],
        x["line"],
        x["rule_id"],
    )
)

normalized = {
    "scanner": "Semgrep",
    "minimum_severity": MIN_SEVERITY,
    "total_findings": len(findings),
    "findings": findings,
}

with NORMALIZED_FILE.open("w") as f:
    json.dump(normalized, f, indent=2, sort_keys=True)

blocking = [
    finding
    for finding in findings
    if SEVERITY_ORDER[finding["severity"]]
    >= SEVERITY_ORDER[MIN_SEVERITY]
]

print()
print("SAST scan completed")
print(f"Total findings   : {len(findings)}")
print(f"Minimum severity : {MIN_SEVERITY}")
print(f"Blocking findings: {len(blocking)}")
print(f"Artifact         : {NORMALIZED_FILE.relative_to(ROOT)}")

for finding in findings:
    print(
        f'{finding["severity"]:8} '
        f'{finding["path"]}:{finding["line"]} '
        f'{finding["rule_id"]}'
    )

if blocking:
    print()
    print("Security gate: FAILED")
    sys.exit(1)

print()
print("Security gate: PASSED")
sys.exit(0)
