#!/usr/bin/env bash
# Pre-deploy test runner for Nissan weekly reports — Phase 2C
# Runs unit tests + unknown venue detector before pushing

set -e
echo "🚀 Pre-deploy checks..."

KKT_DIR="/Users/tatchanon/workspace-MKT/reports/KhonKaen"
UB_DIR="/Users/tatchanon/workspace-MKT/reports/Ubon"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PASS=0
FAIL=0

run_test() {
    local name="$1"
    local path="$2"
    echo ""
    echo "▶ Testing: $name"
    if (cd "$path" && python3 test_section3_filter.py > /tmp/test_output.log 2>&1); then
        echo "  ✅ $name PASSED"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $name FAILED"
        cat /tmp/test_output.log | tail -20
        FAIL=$((FAIL + 1))
    fi
}

# Run tests
run_test "KhonKaen tests" "$KKT_DIR"
run_test "Ubon tests" "$UB_DIR"

# Detect unknown venues
echo ""
echo "▶ Checking for unknown venues..."
for report in "$KKT_DIR/khonkaen-27Jul2026.html" "$UB_DIR/ubon-27Jul2026.html"; do
    if [ -f "$report" ]; then
        python3 "$SCRIPT_DIR/detect_unknown_venues.py" "$report"
    fi
done

echo ""
echo "=================================="
echo "📊 Results: $PASS passed, $FAIL failed"
echo "=================================="

if [ $FAIL -gt 0 ]; then
    echo "❌ Tests FAILED — DO NOT PUSH!"
    exit 1
fi
echo "✅ All checks passed — safe to push"
