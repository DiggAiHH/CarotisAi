<#
.SYNOPSIS
    Carotis-AI one-shot demo launcher for Windows.

.DESCRIPTION
    1. Verifies Docker Desktop is running
    2. Creates data directories
    3. Copies .env.example -> .env (if not present)
    4. Generates the demo ONNX model (if not present)
    5. Builds and starts all containers
    6. Waits for the backend health endpoint
    7. Prints access URLs

.EXAMPLE
    cd code
    .\scripts\demo.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# ── Helpers ──────────────────────────────────────────────────────────────────

function Write-Banner {
    param([string]$Text)
    $line = "─" * ($Text.Length + 4)
    Write-Host ""
    Write-Host "  $line"  -ForegroundColor Cyan
    Write-Host "  │ $Text │" -ForegroundColor Cyan
    Write-Host "  $line"  -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Text)
    Write-Host "  ► $Text" -ForegroundColor Yellow
}

function Write-Ok {
    param([string]$Text)
    Write-Host "  ✓ $Text" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Text)
    Write-Host "  ✗ $Text" -ForegroundColor Red
}

# ── Locate the code/ directory ───────────────────────────────────────────────

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CodeRoot  = Split-Path -Parent $ScriptDir   # scripts/ is one level below code/

Set-Location $CodeRoot

Write-Banner "Carotis-AI Demo Launcher"

# ── Step 1: Docker Desktop ────────────────────────────────────────────────────

Write-Step "Checking Docker Desktop..."
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Ok "Docker is running."
} catch {
    Write-Fail "Docker Desktop is not running!"
    Write-Host ""
    Write-Host "  Please start Docker Desktop and re-run this script." -ForegroundColor White
    Write-Host "  Start menu → 'Docker Desktop' → wait for the whale icon." -ForegroundColor Gray
    exit 1
}

# ── Step 2: Data directories ──────────────────────────────────────────────────

Write-Step "Creating data directories..."
foreach ($dir in @("data/models", "data/db", "data/dicom_temp")) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}
Write-Ok "data/ ready."

# ── Step 3: .env file ─────────────────────────────────────────────────────────

Write-Step "Checking backend/.env..."
if (-not (Test-Path "backend/.env")) {
    Copy-Item "backend/.env.example" "backend/.env"
    Write-Ok "Copied .env.example → .env  (edit API_KEY before going to production!)"
} else {
    Write-Ok ".env already present."
}

# ── Step 4: Demo ONNX model ───────────────────────────────────────────────────

Write-Step "Checking demo ONNX model..."
if (-not (Test-Path "data/models/mfsd_unet.onnx")) {
    Write-Host "  Generating demo model (first run — ~30 s)..." -ForegroundColor Gray

    # Try backend venv first, fall back to system python
    $Python = $null
    foreach ($candidate in @("backend\.venv\Scripts\python.exe", "backend\.venv\bin\python")) {
        if (Test-Path $candidate) { $Python = $candidate; break }
    }
    if (-not $Python) {
        $Python = (Get-Command python -ErrorAction SilentlyContinue).Source
        if (-not $Python) { $Python = (Get-Command python3 -ErrorAction SilentlyContinue).Source }
    }
    if (-not $Python) {
        Write-Fail "Python not found. Install Python 3.11+ and re-run."
        exit 1
    }

    & $Python "scripts/generate_demo_model.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Demo model generation failed."
        exit 1
    }
    Write-Ok "Demo model generated."
} else {
    Write-Ok "Demo model already present."
}

# ── Step 5: Docker Compose build + start ─────────────────────────────────────

Write-Step "Building and starting containers (first build can take a few minutes)..."
docker compose up --build -d
if ($LASTEXITCODE -ne 0) {
    Write-Fail "docker compose up failed — see errors above."
    exit 1
}
Write-Ok "Containers started."

# ── Step 6: Wait for backend health ──────────────────────────────────────────

Write-Step "Waiting for backend to be healthy..."
$maxAttempts = 40
$attempt     = 0
$healthy     = $false

while ($attempt -lt $maxAttempts) {
    $attempt++
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:8000/health" `
                                  -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
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
    Write-Host "  Run:  docker compose logs backend" -ForegroundColor Gray
    exit 1
}

Write-Ok "Backend is healthy."

# ── Step 7: Done — print URLs ────────────────────────────────────────────────

Write-Banner "Carotis-AI is running!"

Write-Host "  Frontend  →  http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Backend   →  http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API docs  →  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Health    →  http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Stop:   docker compose down" -ForegroundColor Gray
Write-Host "  Logs:   docker compose logs -f" -ForegroundColor Gray
Write-Host ""
