#!/usr/bin/env python3

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "artifacts" / "sast.json"
OUTPUT_FILE = ROOT / "artifacts" / "triage.md"

SEVERITY_ORDER = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "INFO": 0,
}

if not INPUT_FILE.exists():
    print(f"ERROR: Input file not found: {INPUT_FILE}")
    sys.exit(2)

try:
    with INPUT_FILE.open() as f:
        data = json.load(f)
except (json.JSONDecodeError, OSError) as exc:
    print(f"ERROR: Unable to read {INPUT_FILE}: {exc}")
    sys.exit(2)

findings = data.get("findings", [])

# Deterministic sorting:
# 1. Severity descending
# 2. File path ascending
# 3. Line number ascending
# 4. Rule ID ascending
findings = sorted(
    findings,
    key=lambda x: (
        -SEVERITY_ORDER.get(x.get("severity", "INFO"), 0),
        x.get("path", ""),
        x.get("line", 0),
        x.get("rule_id", ""),
    ),
)

severity_counts = Counter(
    finding.get("severity", "INFO")
    for finding in findings
)

category_counts = Counter(
    finding.get("category", "uncategorized")
    for finding in findings
)

lines = []

lines.append("# SAST Triage Report")
lines.append("")
lines.append(f"Total findings: {len(findings)}")
lines.append(
    f"Configured minimum severity: "
    f"{data.get('minimum_severity', 'UNKNOWN')}"
)
lines.append("")

lines.append("## Counts by Severity")
lines.append("")
lines.append("| Severity | Count |")
lines.append("|---|---:|")

for severity in [
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFO",
]:
    lines.append(
        f"| {severity} | {severity_counts.get(severity, 0)} |"
    )

lines.append("")
lines.append("## Counts by Category")
lines.append("")
lines.append("| Category | Count |")
lines.append("|---|---:|")

for category in sorted(category_counts):
    lines.append(
        f"| {category} | {category_counts[category]} |"
    )

lines.append("")
lines.append("## Top 5 Findings")
lines.append("")

if not findings:
    lines.append("No findings detected.")
else:
    for index, finding in enumerate(findings[:5], start=1):
        severity = finding.get("severity", "INFO")
        category = finding.get("category", "uncategorized")
        path = finding.get("path", "unknown")
        line = finding.get("line", 0)
        rule_id = finding.get("rule_id", "unknown")
        message = finding.get("message", "")

        lines.append(
            f"{index}. **{severity}** - {category}"
        )
        lines.append(f"   - Rule: `{rule_id}`")
        lines.append(f"   - Location: `{path}:{line}`")
        lines.append(f"   - Message: {message}")
        lines.append("")

lines.append("## Summary")
lines.append("")

blocking_count = sum(
    1
    for finding in findings
    if SEVERITY_ORDER.get(finding.get("severity", "INFO"), 0)
    >= SEVERITY_ORDER.get(
        data.get("minimum_severity", "HIGH"),
        3,
    )
)

lines.append(
    f"{blocking_count} finding(s) meet or exceed the "
    f"`{data.get('minimum_severity', 'HIGH')}` threshold."
)

OUTPUT_FILE.write_text("\n".join(lines) + "\n")

print("Triage report generated successfully")
print(f"Input          : {INPUT_FILE.relative_to(ROOT)}")
print(f"Output         : {OUTPUT_FILE.relative_to(ROOT)}")
print(f"Total findings : {len(findings)}")
print(f"Top findings   : {min(5, len(findings))}")

sys.exit(0)
