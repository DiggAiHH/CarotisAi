# Carotis-AI Pre-Flight Check (PowerShell)
#
# Pflicht-Lauf am Anfang JEDER Modell-Session.
# Prüft: Working Memory geladen, Memory-Index aktuell, letzte Run-Logs gesehen,
# in_progress Tasks bekannt, bekannte Anomalien notiert.
#
# Usage:
#   .\scripts\preflight.ps1
#   .\scripts\preflight.ps1 "decision-tree"

param(
    [Parameter(Position=0)]
    [string]$Keyword = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Workspace = Resolve-Path (Join-Path $ScriptDir "..")
Set-Location $Workspace

function Write-Header($Text) {
    Write-Host ""
    Write-Host $Text -ForegroundColor Cyan
}

Write-Host "=== Carotis-AI Pre-Flight Check ===" -ForegroundColor Cyan
Write-Host "Workspace: $Workspace"
Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC')"

# --- 1. CLAUDE.md ---
Write-Header "[1/6] Working Memory"
if (Test-Path "CLAUDE.md") {
    $phaseLine = Select-String -Path "CLAUDE.md" -Pattern '^\| P\d+ \| 🔄' | Select-Object -First 1
    $phase = if ($phaseLine) { ($phaseLine.Line -split '\|')[1].Trim() } else { "unknown" }
    Write-Host "  [OK] CLAUDE.md vorhanden — aktive Phase: " -NoNewline -ForegroundColor Green
    Write-Host $phase -ForegroundColor Yellow
} else {
    Write-Host "  [FAIL] CLAUDE.md FEHLT — STOP" -ForegroundColor Red
    exit 1
}

# --- 2. MEMORY.md ---
Write-Header "[2/6] Memory-Index"
if (Test-Path "MEMORY.md") {
    $entries = (Select-String -Path "MEMORY.md" -Pattern '^- \[').Count
    Write-Host "  [OK] MEMORY.md vorhanden — $entries Einträge" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] MEMORY.md FEHLT" -ForegroundColor Red
    exit 1
}

# --- 3. Run-Logs ---
Write-Header "[3/6] Letzte 3 Run-Logs"
if (Test-Path "memory/runs") {
    $runs = Get-ChildItem "memory/runs/*.md" -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 3
    if (-not $runs) {
        Write-Host "  [INFO] Noch keine Run-Logs — du bist die erste Session" -ForegroundColor Yellow
    } else {
        foreach ($r in $runs) {
            Write-Host "  $($r.Name)"
        }
    }
} else {
    Write-Host "  [INFO] memory/runs/ existiert nicht" -ForegroundColor Yellow
}

# --- 4. Tasks ---
Write-Header "[4/6] In-Progress Tasks"
if (Test-Path "tasks.jsonl") {
    $content = Get-Content "tasks.jsonl"
    $inProgress = ($content | Select-String '"status":"in_progress"').Count
    $pending = ($content | Select-String '"status":"pending"').Count
    $done = ($content | Select-String '"status":"done"').Count
    Write-Host "  [OK] tasks.jsonl: " -NoNewline -ForegroundColor Green
    Write-Host "$inProgress in_progress" -NoNewline -ForegroundColor Yellow
    Write-Host " · $pending pending · $done done"

    if ($inProgress -gt 0) {
        Write-Host "  In-Progress Tasks:"
        $content | Select-String '"status":"in_progress"' | ForEach-Object {
            if ($_.Line -match '"id":"([^"]*)".*"title":"([^"]*)"') {
                Write-Host "    - $($matches[1]): $($matches[2])"
            }
        }
    }
} else {
    Write-Host "  [INFO] tasks.jsonl existiert nicht" -ForegroundColor Yellow
}

# --- 5. Anomalies ---
Write-Header "[5/6] Bekannte Anomalien"
if (Test-Path "memory/anomalies") {
    $anomalies = Get-ChildItem "memory/anomalies/" -ErrorAction SilentlyContinue
    if ($anomalies.Count -gt 0) {
        Write-Host "  [WARN] $($anomalies.Count) Anomalie-Einträge — vor Code-Änderung lesen!" -ForegroundColor Yellow
        foreach ($a in $anomalies) {
            Write-Host "    - $($a.Name)"
        }
    } else {
        Write-Host "  [OK] Keine Anomalien bekannt" -ForegroundColor Green
    }
} else {
    Write-Host "  [OK] Keine Anomalien bekannt" -ForegroundColor Green
}

# --- 6. Keyword Search ---
Write-Header "[6/6] Keyword-Suche"
if ($Keyword) {
    Write-Host "  Suche nach: '$Keyword'"
    $hits = Get-ChildItem "memory/" -Recurse -Include "*.md" -ErrorAction SilentlyContinue |
            Select-String -Pattern $Keyword -List
    if (-not $hits) {
        Write-Host "  [OK] Kein Vorkommen in memory/ — sicher, neuen Eintrag anzulegen" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] Vorkommen gefunden — vor Doppelarbeit prüfen:" -ForegroundColor Yellow
        foreach ($h in $hits) {
            Write-Host "    $($h.Path)"
        }
    }
} else {
    Write-Host "  (Kein Keyword übergeben — überspringe Suche)"
}

Write-Host ""
Write-Host "Pre-Flight done. Du kannst arbeiten." -ForegroundColor Green
$today = Get-Date -Format "yyyy-MM-dd"
Write-Host "Reminder: Am Ende der Session memory/runs/${today}_<modell>_<thema>.md schreiben."
