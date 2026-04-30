<#
.SYNOPSIS
    Carotis-AI Demo Teardown for Windows.

.DESCRIPTION
    Stops containers and optionally removes demo data.

.PARAMETER KeepData
    If set, demo data in data/demo/ is preserved.

.EXAMPLE
    .\scripts\teardown_demo.ps1
    .\scripts\teardown_demo.ps1 -KeepData
#>
[CmdletBinding()]
param([switch]$KeepData)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CodeRoot = Split-Path -Parent $ScriptDir
Set-Location $CodeRoot

Write-Host "Stopping containers..."
docker compose down --volumes
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: docker compose down returned exit code $LASTEXITCODE" -ForegroundColor Yellow
}

if (-not $KeepData) {
    Write-Host "Removing demo data..."
    if (Test-Path "data/demo") {
        Remove-Item -Recurse -Force "data/demo"
    }
    Write-Host "Demo data removed."
} else {
    Write-Host "Keeping demo data (-KeepData flag set)."
}

Write-Host "Teardown complete." -ForegroundColor Green
