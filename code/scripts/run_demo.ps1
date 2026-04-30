<#
.SYNOPSIS
    Carotis-AI 5-Min-Demo Launcher for Windows.

.DESCRIPTION
    1. Runs pre-flight
    2. Checks Docker Desktop
    3. Creates data directories and starts containers
    4. Generates demo ONNX model (if not present)
    5. Generates demo data (if not present)
    6. Seeds decision trees to backend
    7. Waits for backend health
    8. Opens browser
    9. Prompts to open walkthrough in VS Code

.EXAMPLE
    cd code
    .\scripts\run_demo.ps1
#>
[CmdletBinding()]
param(
    [switch]$KeepData
)

$ErrorActionPreference = "Stop"

# -- Port check ----------------------------------------------------------------
function Test-PortInUse {
    param([int]$Port)
    $conn = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -ne $conn
}

foreach ($port in @(3000, 8000)) {
    if (Test-PortInUse -Port $port) {
        Write-Warning "Port $port is already in use. The demo may fail to start."
    }
}

# -- Helpers -------------------------------------------------------------------

function Write-Banner {
    param([string]$Text)
    $line = "-" * ($Text.Length + 4)
    Write-Host ""
    Write-Host "  $line"  -ForegroundColor Cyan
    Write-Host "  | $Text |" -ForegroundColor Cyan
    Write-Host "  $line"  -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Text)
    Write-Host "  > $Text" -ForegroundColor Yellow
}

function Write-Ok {
    param([string]$Text)
    Write-Host "  [OK] $Text" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Text)
    Write-Host "  [FAIL] $Text" -ForegroundColor Red
    exit 1
}

# -- Locate the code/ directory ------------------------------------------------

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CodeRoot  = Split-Path -Parent $ScriptDir

Set-Location $CodeRoot

Write-Banner "Carotis-AI Demo Launcher"

# -- Step 1: Pre-Flight --------------------------------------------------------

Write-Step "Running pre-flight..."
if (Test-Path "..\scripts\preflight.ps1") {
    try {
        & "..\scripts\preflight.ps1"
        Write-Ok "Pre-flight done."
    } catch {
        Write-Fail "Pre-flight failed: $_"
    }
} else {
    Write-Step "Skipping pre-flight (not found)"
}

# -- Step 2: Docker Desktop ----------------------------------------------------

Write-Step "Checking Docker Desktop..."
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Ok "Docker is running."
} catch {
    Write-Fail "Docker Desktop is not running!"
}

# -- Step 3: Data directories + containers -------------------------------------

Write-Step "Creating data directories and starting containers..."
foreach ($dir in @("data/models", "data/db", "data/dicom_temp")) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# Ensure .env exists
if (-not (Test-Path "backend/.env")) {
    if (Test-Path "backend/.env.example") {
        Copy-Item "backend/.env.example" "backend/.env"
        Write-Ok "Created backend/.env from .env.example"
    } else {
        Write-Warning "backend/.env missing and no .env.example found"
    }
}

docker compose up -d
if ($LASTEXITCODE -ne 0) { Write-Fail "docker compose up failed" }
Write-Ok "Containers started."

# -- Step 4: Demo ONNX model ---------------------------------------------------

Write-Step "Checking demo ONNX model..."
if (-not (Test-Path "data/models/mfsd_unet.onnx")) {
    $Python = $null
    foreach ($candidate in @("backend\.venv\Scripts\python.exe", "backend\.venv\bin\python", (Get-Command python -ErrorAction SilentlyContinue).Source, (Get-Command python3 -ErrorAction SilentlyContinue).Source)) {
        if ($candidate -and (Test-Path $candidate)) { $Python = $candidate; break }
    }
    if (-not $Python) { Write-Fail "Python not found." }
    & $Python "scripts/generate_demo_model.py"
    if ($LASTEXITCODE -ne 0) { Write-Fail "Demo model generation failed." }
    Write-Ok "Demo model generated."
} else {
    Write-Ok "Demo model already present."
}

# -- Step 5: Demo data ---------------------------------------------------------

Write-Step "Checking demo data..."
$dicomCount = (Get-ChildItem "data/demo/dicoms/*.dcm" -ErrorAction SilentlyContinue).Count
if ($dicomCount -lt 10) {
    $Python = $null
    foreach ($candidate in @("backend\.venv\Scripts\python.exe", "backend\.venv\bin\python", (Get-Command python -ErrorAction SilentlyContinue).Source, (Get-Command python3 -ErrorAction SilentlyContinue).Source)) {
        if ($candidate -and (Test-Path $candidate)) { $Python = $candidate; break }
    }
    if (-not $Python) { Write-Fail "Python not found." }
    & $Python "scripts/generate_demo_data.py" --count 10
    if ($LASTEXITCODE -ne 0) { Write-Fail "Demo data generation failed." }
    Write-Ok "Demo data generated."
} else {
    Write-Ok "Demo data already present ($dicomCount files)."
}

# -- Step 6: Seed decision trees -----------------------------------------------

Write-Step "Seeding decision trees into backend..."
$envFile = Get-Content "backend/.env" -ErrorAction SilentlyContinue
$apiKey = "carotis-dev-key-change-in-prod"
if ($envFile) {
    $match = $envFile | Select-String "^API_KEY=(.+)$"
    if ($match) { $apiKey = $match.Matches[0].Groups[1].Value.Trim().Trim('"', "'") }
}

$treeFiles = Get-ChildItem "data/demo/decision_trees/*.json" -ErrorAction SilentlyContinue
foreach ($f in $treeFiles) {
    try {
        $body = Get-Content $f -Raw
        Invoke-WebRequest -Uri "http://localhost:8000/api/v1/decision-tree/capture" `
            -Method POST `
            -Headers @{ "Content-Type" = "application/json"; "X-API-Key" = $apiKey } `
            -Body $body `
            -UseBasicParsing -TimeoutSec 5 | Out-Null
    } catch {
        # ignore individual failures
    }
}
Write-Ok "Decision trees seeded."

# -- Step 7: Wait for backend health -------------------------------------------

Write-Step "Waiting for backend health..."
$maxAttempts = 40
$attempt = 0
$healthy = $false

while ($attempt -lt $maxAttempts) {
    $attempt++
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) {
            $healthy = $true
            break
        }
    } catch {
        # Not ready yet
    }
    Write-Host "  . (attempt $attempt/$maxAttempts)" -ForegroundColor Gray
    Start-Sleep -Seconds 3
}

if (-not $healthy) {
    Write-Fail "Backend did not become healthy after $($maxAttempts * 3) seconds."
}
Write-Ok "Backend is healthy."

# -- Step 8: Open browser ------------------------------------------------------

Write-Step "Opening browser..."
$DashboardPath = (Resolve-Path "..\dashboard.html").Path

Start-Process "http://localhost:3000"
Start-Process "file:///$DashboardPath"
Write-Ok "Browser opened."

# -- Step 9: Done --------------------------------------------------------------

Write-Banner "DEMO READY"

Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Green
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor Green
Write-Host "  Dashboard: file:///$DashboardPath" -ForegroundColor Green
Write-Host ""
Write-Host "  Press any key to open VS Code with demo_walkthrough.md" -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

$codeCmd = Get-Command code -ErrorAction SilentlyContinue
if ($codeCmd) {
    & $codeCmd.Source "scripts/demo_walkthrough.md"
}

Write-Host ""
Write-Host "  Stop: .\scripts\teardown_demo.ps1" -ForegroundColor Gray
Write-Host ""
