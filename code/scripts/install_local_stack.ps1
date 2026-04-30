#Requires -RunAsAdministrator
# Hinweis: PowerShell -ExecutionPolicy Bypass -File install_local_stack.ps1

$ErrorActionPreference = "Stop"

$LOG_FILE = "$env:TEMP\install_local_stack.log"
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] [$Level] $Message"
    Add-Content -Path $LOG_FILE -Value $line
    switch ($Level) {
        "BANNER" { Write-Host $Message -ForegroundColor Cyan }
        "STEP"   { Write-Host $Message -ForegroundColor Yellow }
        "OK"     { Write-Host $Message -ForegroundColor Green }
        "FAIL"   { Write-Host $Message -ForegroundColor Red }
        default  { Write-Host $Message }
    }
}

Write-Log "=== Carotis-AI Local Stack Installer ===" "BANNER"

# 1. OS erkennen
if (-not $IsWindows) {
    Write-Log "Nicht-Windows erkannt. Bitte install_local_stack.sh verwenden." "FAIL"
    exit 1
}
Write-Log "Windows erkannt" "OK"

# 2. Ollama installieren
$OLLAMA_PATH = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
if (-not (Test-Path $OLLAMA_PATH)) {
    Write-Log "Ollama wird installiert..." "STEP"
    $OLLAMA_SETUP = "$env:TEMP\OllamaSetup.exe"
    Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $OLLAMA_SETUP
    Start-Process -Wait -FilePath $OLLAMA_SETUP -ArgumentList "/S"
    if (Test-Path $OLLAMA_PATH) {
        Write-Log "Ollama installiert" "OK"
    } else {
        Write-Log "Ollama-Installation fehlgeschlagen" "FAIL"
        exit 1
    }
} else {
    Write-Log "Ollama bereits vorhanden" "OK"
}

# 3. Ollama-Service starten
$OLLAMA_PROC = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if (-not $OLLAMA_PROC) {
    Write-Log "Ollama-Service wird gestartet..." "STEP"
    Start-Process -FilePath $OLLAMA_PATH -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    $OLLAMA_PROC = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
    if ($OLLAMA_PROC) {
        Write-Log "Ollama gestartet" "OK"
    } else {
        Write-Log "Ollama konnte nicht gestartet werden" "FAIL"
        exit 1
    }
} else {
    Write-Log "Ollama laeuft bereits" "OK"
}

# Port-Konflikt pruefen
$PORT_CHECK = Get-NetTCPConnection -LocalPort 11434 -ErrorAction SilentlyContinue
if ($PORT_CHECK) {
    Write-Log "Port 11434 ist belegt (Ollama)" "OK"
} else {
    Write-Log "Port 11434 nicht belegt - Ollama laeuft nicht korrekt" "FAIL"
    exit 1
}

# 4. Modelle pullen (idempotent)
function Pull-Model {
    param([string]$ModelName)
    $LIST = & $OLLAMA_PATH list 2>$null
    if ($LIST -match $ModelName) {
        Write-Log "Modell $ModelName bereits vorhanden" "OK"
    } else {
        Write-Log "Modell $ModelName wird heruntergeladen..." "STEP"
        & $OLLAMA_PATH pull $ModelName
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Modell $ModelName heruntergeladen" "OK"
        } else {
            Write-Log "Download von $ModelName fehlgeschlagen (optional?)" "STEP"
        }
    }
}

Pull-Model "nous-hermes-3-llama-3.1"
Pull-Model "qwen2.5-coder:7b"
Pull-Model "llava-llama3:8b"  # optional

# 5. Python venv
if (-not (Test-Path ".venv")) {
    Write-Log "Python venv wird erstellt..." "STEP"
    python -m venv .venv
    Write-Log "venv erstellt" "OK"
} else {
    Write-Log "venv bereits vorhanden" "OK"
}

# 6. Hermes Agent
Write-Log "Hermes Agent wird installiert..." "STEP"
& .venv\Scripts\python.exe -m pip install --quiet git+https://github.com/NousResearch/hermes-agent.git
if ($LASTEXITCODE -ne 0) {
    Write-Log "Installation aus Git fehlgeschlagen, versuche PyPI..." "STEP"
    & .venv\Scripts\python.exe -m pip install --quiet hermes-agent
}
Write-Log "Hermes Agent installiert" "OK"

# 7. Verify
Write-Log "Verifiziere Ollama-API..." "STEP"
$RESPONSE = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -UseBasicParsing
$MODELS = $RESPONSE.models.name
if ($MODELS -contains "nous-hermes-3-llama-3.1") {
    Write-Log "API erreichbar und Modelle gelistet" "OK"
} else {
    Write-Log "API-Verifizierung fehlgeschlagen" "FAIL"
    exit 1
}

# 8. Summary
Write-Log "=== Setup Summary ===" "BANNER"
Write-Log "Installations-Log: $LOG_FILE"
Write-Log "Ollama-Log: $env:TEMP\ollama.log"
Write-Log "Gepullte Modelle: $($MODELS -join ', ')"
Write-Log ""
Write-Log "Naechste Schritte:"
Write-Log "1. cp backend/.env.example backend/.env"
Write-Log "2. API_KEY in backend/.env anpassen (min. 32 Zeichen)"
Write-Log "3. docker compose up --build   oder   make demo"
