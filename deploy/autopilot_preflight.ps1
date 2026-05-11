param(
    [string]$FrontendDomain = "carotis.diggai.de",
    [string]$ApiDomain = "api.carotis.diggai.de",
    [string]$ExpectedApiIp = "204.168.230.127",
    [switch]$SkipPlaywright,
    [switch]$SkipDns,
    [switch]$SkipSecrets,
    [switch]$AllowDirtyWorktree
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$codeRoot = Join-Path $repoRoot "code"
$frontendRoot = Join-Path $codeRoot "frontend"
$venvPython = Join-Path $codeRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    $venvPython = Join-Path $codeRoot ".venv313\Scripts\python.exe"
}

$requiredSecrets = @(
    "FLY_API_TOKEN",
    "HETZNER_SSH_PRIVATE_KEY",
    "HETZNER_SERVER_IP",
    "HETZNER_SSH_USER",
    "ACME_EMAIL",
    "API_KEY",
    "ADMIN_API_KEY",
    "ANONYMIZATION_SALT"
)

$checks = New-Object System.Collections.Generic.List[object]

function Add-DeployResult {
    param(
        [string]$Name,
        [bool]$Passed,
        [string]$Details
    )

    $checks.Add([PSCustomObject]@{
        Name = $Name
        Passed = $Passed
        Details = $Details
    }) | Out-Null
}

function Invoke-DeployAction {
    param(
        [string]$Name,
        [scriptblock]$Script
    )

    try {
        & $Script
        Add-DeployResult -Name $Name -Passed $true -Details "ok"
    }
    catch {
        Add-DeployResult -Name $Name -Passed $false -Details $_.Exception.Message
    }
}

function Test-Command {
    param([string]$Name)

    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

Write-Host "[Autopilot] Carotis deploy preflight started" -ForegroundColor Cyan
Write-Host "[Autopilot] repo: $repoRoot"

Invoke-DeployAction "Tool: git" { if (-not (Test-Command "git")) { throw "git not found" } }
Invoke-DeployAction "Tool: python" { if (-not (Test-Command "python")) { throw "python not found" } }
Invoke-DeployAction "Tool: npm" { if (-not (Test-Command "npm")) { throw "npm not found" } }
Invoke-DeployAction "Tool: docker" { if (-not (Test-Command "docker")) { throw "docker not found" } }

Invoke-DeployAction "Python venv executable" {
    if (-not (Test-Path $venvPython)) {
        throw "No virtualenv python found at .venv or .venv313"
    }
}

Invoke-DeployAction "Git worktree status" {
    Set-Location $repoRoot
    $status = git status --short
    if ($LASTEXITCODE -ne 0) { throw "git status failed" }
    if ($status -and -not $AllowDirtyWorktree) {
        throw "worktree is dirty ($($status.Count) lines). Re-run with -AllowDirtyWorktree to continue"
    }
    if ($status -and $AllowDirtyWorktree) {
        Write-Host "[Autopilot] warning: dirty worktree accepted by flag" -ForegroundColor Yellow
    }
}

Invoke-DeployAction "Frontend typecheck" {
    Set-Location $frontendRoot
    npm run typecheck | Out-Host
    if ($LASTEXITCODE -ne 0) { throw "npm run typecheck failed" }
}

Invoke-DeployAction "Frontend lint" {
    Set-Location $frontendRoot
    npm run lint | Out-Host
    if ($LASTEXITCODE -ne 0) { throw "npm run lint failed" }
}

Invoke-DeployAction "Frontend unit tests" {
    Set-Location $frontendRoot
    npm test -- --run | Out-Host
    if ($LASTEXITCODE -ne 0) { throw "npm test failed" }
}

if (-not $SkipPlaywright) {
    Invoke-DeployAction "Frontend Playwright smoke" {
        Set-Location $frontendRoot
        $testFile = "e2e/chromium_visual_smoke.spec.ts"
        if (-not (Test-Path $testFile)) {
            throw "Playwright test file missing: $testFile"
        }
        npx playwright test --project=chromium $testFile --reporter=list | Out-Host
        if ($LASTEXITCODE -ne 0) { throw "Playwright smoke failed" }
    }
}

Invoke-DeployAction "Backend pytest" {
    Set-Location $codeRoot
    $env:PYTHONPATH = "backend"
    $env:DEBUG = "true"
    $env:API_KEY = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    $env:ADMIN_API_KEY = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    $env:ANONYMIZATION_SALT = "cccccccccccccccccccccccccccccccc"
    & $venvPython -m pytest tests\ -v --tb=short | Out-Host
    if ($LASTEXITCODE -ne 0) { throw "backend pytest failed" }
}

Invoke-DeployAction "Docker compose config" {
    Set-Location $codeRoot
    docker compose config | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "docker compose config failed" }
}

if (-not $SkipDns) {
    Invoke-DeployAction "DNS frontend domain" {
        $front = Resolve-DnsName -Name $FrontendDomain -ErrorAction Stop
        if (-not $front) { throw "no DNS answer for $FrontendDomain" }
    }

    Invoke-DeployAction "DNS API domain" {
        $api = Resolve-DnsName -Name $ApiDomain -ErrorAction Stop
        $ips = @($api | Where-Object { $_.Type -eq "A" } | Select-Object -ExpandProperty IPAddress)
        if (-not $ips) { throw "no A record for $ApiDomain" }
        if ($ExpectedApiIp -and ($ips -notcontains $ExpectedApiIp)) {
            throw "A record mismatch. expected $ExpectedApiIp got $($ips -join ',')"
        }
    }
}

if (-not $SkipSecrets) {
    Invoke-DeployAction "Tool: gh" { if (-not (Test-Command "gh")) { throw "gh not found" } }

    Invoke-DeployAction "GitHub secrets presence" {
        Set-Location $repoRoot
        $raw = gh secret list 2>$null
        if ($LASTEXITCODE -ne 0) { throw "gh secret list failed (check auth and repo context)" }

        $present = @{}
        foreach ($line in $raw) {
            $name = ($line -split "\s+")[0]
            if ($name) { $present[$name] = $true }
        }

        $missing = @()
        foreach ($required in $requiredSecrets) {
            if (-not $present.ContainsKey($required)) {
                $missing += $required
            }
        }

        if ($missing.Count -gt 0) {
            throw "missing secrets: $($missing -join ', ')"
        }
    }
}

Write-Host ""
Write-Host "[Autopilot] Preflight summary" -ForegroundColor Cyan
$checks | Format-Table -AutoSize

$failed = @($checks | Where-Object { -not $_.Passed })
if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "[Autopilot] FAILED checks: $($failed.Count)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[Autopilot] All checks passed. Deployment can proceed." -ForegroundColor Green
exit 0
