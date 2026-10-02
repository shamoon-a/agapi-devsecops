#!/usr/bin/env bash

set -u

echo "========================================"
echo " AGAPI DevSecOps Take-Home Assessment"
echo " Tasks: SAST + Triage Reporting"
echo "========================================"
echo

MIN_SEVERITY="${MIN_SEVERITY:-HIGH}"
export MIN_SEVERITY

# Remove previous generated artifacts to prevent stale results.
rm -f artifacts/sast.raw.json
rm -f artifacts/sast.json
rm -f artifacts/triage.md

echo "[1/2] Running Semgrep SAST scan..."
python3 scripts/scan_sast.py
SAST_EXIT=$?

# Exit immediately for scanner/configuration/runtime errors.
# Exit code 1 is different: it means the scan succeeded but
# security findings exceeded the configured threshold.
if [ "$SAST_EXIT" -ne 0 ] && [ "$SAST_EXIT" -ne 1 ]; then
    echo
    echo "========================================"
    echo " Execution Summary"
    echo "========================================"
    echo "MIN_SEVERITY : $MIN_SEVERITY"
    echo "SAST status  : $SAST_EXIT"
    echo "Triage status: NOT RUN"
    echo
    echo "Result: ERROR - SAST execution failed"
    exit 2
fi

echo
echo "[2/2] Generating triage report..."
python3 scripts/triage_report.py
TRIAGE_EXIT=$?

echo
echo "========================================"
echo " Execution Summary"
echo "========================================"
echo "MIN_SEVERITY : $MIN_SEVERITY"
echo "SAST status  : $SAST_EXIT"
echo "Triage status: $TRIAGE_EXIT"
echo
echo "Generated artifacts:"
echo "  artifacts/sast.raw.json"
echo "  artifacts/sast.json"
echo "  artifacts/triage.md"
echo

if [ "$TRIAGE_EXIT" -ne 0 ]; then
    echo "Result: ERROR - triage generation failed"
    exit 2
fi

if [ "$SAST_EXIT" -eq 1 ]; then
    echo "Result: FAILED - security findings exceeded threshold"
    exit 1
fi

echo "Result: PASSED"
exit 0
