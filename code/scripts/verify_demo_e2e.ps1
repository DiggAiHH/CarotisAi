#Requires -Version 5.1
<#
.SYNOPSIS
    E2E smoke test for Carotis-AI demo stack.
.DESCRIPTION
    ASCII-only output. Checks Health, Demo model, Inference, Decision Capture, Audit Trail.
    Exit code 0 = all passed, 1 = any failed.
.PARAMETER BaseUrl
    Backend base URL (default: http://localhost:8000).
.PARAMETER ApiKey
    API key for authenticated endpoints.
#>
param(
    [string]$BaseUrl = "http://localhost:8000",
    [string]$ApiKey = ""
)

$ErrorActionPreference = "Stop"

function Test-Step {
    param([string]$Name, [scriptblock]$Action)
    Write-Host -NoNewline "[$Name] "
    try {
        & $Action
        Write-Host "PASS" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "FAIL: $_" -ForegroundColor Red
        return $false
    }
}

$pass = $true

# 1. Health (public)
$pass = (Test-Step "HEALTH" {
    $r = Invoke-RestMethod -Uri "$BaseUrl/health" -Method GET
    if ($r.status -ne "ok") { throw "status=$($r.status)" }
}) -and $pass

# 2. Demo model script exists
$pass = (Test-Step "DEMO_SCRIPT" {
    $scriptPath = Join-Path $PSScriptRoot "generate_demo_model.py"
    if (-not (Test-Path $scriptPath)) { throw "generate_demo_model.py missing" }
}) -and $pass

# 3. Generate anonymized DICOM bytes via inline Python
$tmpFile = [System.IO.Path]::GetTempFileName() + ".dcm"
$pass = (Test-Step "GEN_DICOM" {
    $py = @"
import pydicom, numpy as np, sys
ds = pydicom.Dataset()
ds.Rows = 64; ds.Columns = 64; ds.BitsAllocated = 16; ds.BitsStored = 16
ds.PixelRepresentation = 0; ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = 'MONOCHROME2'
ds.PixelData = np.zeros((64,64), dtype=np.uint16).tobytes()
pydicom.dcmwrite(sys.argv[1], ds, little_endian=True, implicit_vr=False)
"@
    python -c $py $tmpFile
    if (-not (Test-Path $tmpFile)) { throw "DICOM not created" }
}) -and $pass

# 4. Inference (auth required; 200 or 503 acceptable)
$pass = (Test-Step "INFERENCE" {
    $headers = @{ "X-API-Key" = $ApiKey }
    $r = Invoke-RestMethod -Uri "$BaseUrl/api/v1/inference/predict" -Method POST `
        -Headers $headers -InFile $tmpFile -ContentType "application/dicom"
    if (-not $r.case_id) { throw "missing case_id" }
}) -and $pass

# 5. Decision Capture
$pass = (Test-Step "DECISION_CAPTURE" {
    $payload = @{
        case_id = "a" * 64
        captured_at = (Get-Date -Format "o")
        physician_role_hash = "b" * 64
        ai_prediction = @{
            stenosis_pct_nascet = 50.0
            confidence = 0.9
            vulnerability_markers = @{
                intraplaque_hemorrhage = 0.5
                thin_fibrous_cap = 0.2
                lipid_rich_necrotic_core = 0.3
                systolic_motion_anomaly = 0.1
            }
            model_version = "v0.3.2"
            model_sha = "abc123d"
        }
        physician_decision = @{
            stenosis_pct_nascet = 50.0
            confirmed_markers = @()
            rejected_markers = @()
            added_markers = @()
        }
        agreement_with_ai = @{
            verdict = "partial_agreement"
            delta_pct = 0.0
            trust_score_for_this_case = 4
        }
        anonymisation = @{
            method = "DICOM_PS_3.15_basic"
            salt_version = "v2026-04"
            audit_id = "AT-001"
            k_anonymity_min = 5
        }
    } | ConvertTo-Json -Depth 10
    $headers = @{ "X-API-Key" = $ApiKey; "Content-Type" = "application/json" }
    $r = Invoke-RestMethod -Uri "$BaseUrl/api/v1/decision-tree/capture" -Method POST `
        -Headers $headers -Body $payload
    if ($r.status -ne "ok") { throw "status=$($r.status)" }
}) -and $pass

# 6. Audit Trail (admin key required; skip if not configured)
$pass = (Test-Step "AUDIT_TRAIL" {
    $headers = @{ "X-API-Key" = $ApiKey }
    $r = Invoke-RestMethod -Uri "$BaseUrl/api/v1/audit/trail" -Method GET -Headers $headers
    if ($r.items -eq $null) { throw "missing items" }
}) -and $pass

# Cleanup
if (Test-Path $tmpFile) { Remove-Item $tmpFile -Force }

Write-Host ""
if ($pass) {
    Write-Host "ALL TESTS PASSED" -ForegroundColor Green
    exit 0
} else {
    Write-Host "SOME TESTS FAILED" -ForegroundColor Red
    exit 1
}
