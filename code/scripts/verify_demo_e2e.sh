#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
API_KEY="${API_KEY:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASS=0
FAIL=0

step() {
    local name="$1"
    shift
    printf '[%s] ' "$name"
    if "$@" >/dev/null 2>&1; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL"
        FAIL=$((FAIL + 1))
    fi
}

# 1. Health
step "HEALTH" curl -fsS "${BASE_URL}/health"

# 2. Demo model script exists
step "DEMO_SCRIPT" test -f "${SCRIPT_DIR}/generate_demo_model.py"

# 3. Generate anonymized DICOM bytes via inline Python
TMP_DICOM=$(mktemp --suffix=.dcm)
step "GEN_DICOM" python3 -c "
import pydicom, numpy as np, sys
ds = pydicom.Dataset()
ds.Rows = 64; ds.Columns = 64; ds.BitsAllocated = 16; ds.BitsStored = 16
ds.PixelRepresentation = 0; ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = 'MONOCHROME2'
ds.PixelData = np.zeros((64,64), dtype=np.uint16).tobytes()
pydicom.dcmwrite(sys.argv[1], ds, little_endian=True, implicit_vr=False)
" "$TMP_DICOM"

# 4. Inference (auth required)
step "INFERENCE" curl -fsS -X POST "${BASE_URL}/api/v1/inference/predict" \
    -H "X-API-Key: ${API_KEY}" \
    -H "Content-Type: application/dicom" \
    --data-binary "@${TMP_DICOM}"

# 5. Decision Capture
step "DECISION_CAPTURE" curl -fsS -X POST "${BASE_URL}/api/v1/decision-tree/capture" \
    -H "X-API-Key: ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{
        "case_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "captured_at": "2026-04-30T12:00:00Z",
        "physician_role_hash": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "ai_prediction": {
            "stenosis_pct_nascet": 50.0,
            "confidence": 0.9,
            "vulnerability_markers": {
                "intraplaque_hemorrhage": 0.5,
                "thin_fibrous_cap": 0.2,
                "lipid_rich_necrotic_core": 0.3,
                "systolic_motion_anomaly": 0.1
            },
            "model_version": "v0.3.2",
            "model_sha": "abc123d"
        },
        "physician_decision": {
            "stenosis_pct_nascet": 50.0,
            "confirmed_markers": [],
            "rejected_markers": [],
            "added_markers": []
        },
        "agreement_with_ai": {
            "verdict": "partial_agreement",
            "delta_pct": 0.0,
            "trust_score_for_this_case": 4
        },
        "anonymisation": {
            "method": "DICOM_PS_3.15_basic",
            "salt_version": "v2026-04",
            "audit_id": "AT-001",
            "k_anonymity_min": 5
        }
    }'

# 6. Audit Trail
step "AUDIT_TRAIL" curl -fsS "${BASE_URL}/api/v1/audit/trail" \
    -H "X-API-Key: ${API_KEY}"

# Cleanup
rm -f "$TMP_DICOM"

echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "ALL TESTS PASSED ($PASS)"
    exit 0
else
    echo "SOME TESTS FAILED (pass=$PASS fail=$FAIL)"
    exit 1
fi
