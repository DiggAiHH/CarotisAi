# Carotis-AI Developer Setup — Windows PowerShell
# Run: .\scripts\dev-setup.ps1
# Prerequisites: Python 3.13.12, Node 22.x, Docker Desktop (optional)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$codeDir = Join-Path $root "code"

function Step($msg) {
    Write-Host "`n==> $msg" -ForegroundColor Cyan
}

function Check($msg) {
    Write-Host "    [OK] $msg" -ForegroundColor Green
}

function Warn($msg) {
    Write-Host "    [WARN] $msg" -ForegroundColor Yellow
}

function Fail($msg) {
    Write-Host "    [FAIL] $msg" -ForegroundColor Red
    exit 1
}

Step "Pre-Flight Checks"

# Python
$py = "C:\Users\tubbeTEC\AppData\Roaming\uv\python\cpython-3.13.12-windows-x86_64-none\python.exe"
if (-not (Test-Path $py)) {
    Fail "Python 3.13.12 not found at $py. Install via: uv python install 3.13.12"
}
$pyVersion = & $py --version 2>&1
Check "Python: $pyVersion"

# Node
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) { Fail "Node.js not found. Install Node 22.x." }
$nodeVersion = & node --version
if ($nodeVersion -notmatch "^v22") { Warn "Node $nodeVersion — v22.x recommended" }
else { Check "Node: $nodeVersion" }

# Docker (optional)
$docker = Get-Command docker -ErrorAction SilentlyContinue
if ($docker) { Check "Docker: $(docker --version)" }
else { Warn "Docker not found — optional for local container tests" }

# Git
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) { Fail "Git not found." }
Check "Git: $(git --version)"

Step "Backend Setup"

Set-Location $codeDir

if (-not (Test-Path ".venv313")) {
    Write-Host "    Creating venv .venv313..."
    & $py -m venv .venv313
}
Check "venv exists"

$pip = Join-Path $codeDir ".venv313\Scripts\python.exe"
& $pip -m pip install -q -r backend\requirements.txt
Check "Backend dependencies installed"

# .env
if (-not (Test-Path "backend\.env")) {
    Copy-Item backend\.env.example backend\.env
    Warn "backend\.env created from example — EDIT API_KEY (min 32 chars) and ANONYMIZATION_SALT (min 16 chars)"
} else {
    Check "backend\.env exists"
}

Step "Frontend Setup"

Set-Location (Join-Path $codeDir "frontend")

npm install --silent
Check "Frontend dependencies installed"

if (-not (Test-Path ".env.local")) {
    @"
VITE_API_URL=http://localhost:8000
VITE_API_KEY=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
"@ | Set-Content -Encoding UTF8 .env.local
    Warn ".env.local created — EDIT VITE_API_KEY"
} else {
    Check ".env.local exists"
}

Step "Verification — Backend Tests"

Set-Location $codeDir
$env:PYTHONPATH = "backend"
$env:DEBUG = "true"

$testOutput = & $pip -m pytest tests\test_smoke.py -v --tb=short 2>&1
$smokePassed = $testOutput | Select-String "passed"
if ($smokePassed) {
    Check "Smoke tests: $smokePassed"
} else {
    Fail "Smoke tests failed"
}

Step "Verification — Frontend Build"

Set-Location (Join-Path $codeDir "frontend")
npm run typecheck 2>$null
if ($?) { Check "Typecheck passed" } else { Warn "Typecheck failed" }

npm run lint 2>$null
if ($?) { Check "Lint passed" } else { Warn "Lint failed" }

npm run build 2>$null
if ($?) { Check "Build passed" } else { Warn "Build failed" }

Step "Summary"

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Carotis-AI Dev Setup Complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nNext steps:"
Write-Host "  1. Edit code\backend\.env (API_KEY, ADMIN_API_KEY, ANONYMIZATION_SALT)"
Write-Host "  2. Edit code\frontend\.env.local (VITE_API_KEY)"
Write-Host "  3. Start backend:  cd code\backend; ..\.venv313\Scripts\python.exe main.py"
Write-Host "  4. Start frontend: cd code\frontend; npm run dev"
Write-Host "  5. Read ULTRAPLAN.md v3 for full protocol"
Write-Host "`nRun full test suite:"
Write-Host "  cd code; `\$env:PYTHONPATH='backend'; `\$env:DEBUG='true'; .\.venv313\Scripts\python.exe -m pytest tests\ -v --tb=short"
