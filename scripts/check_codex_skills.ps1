param(
    [string]$CodexSkillsRoot = "$env:USERPROFILE\.codex\skills"
)

$ErrorActionPreference = "Stop"

$requiredSkills = @(
    "browser-harness",
    "caveman",
    "compress",
    "obsidian",
    "remotion-best-practices"
)

Write-Host "Carotis-AI Codex skill check"
Write-Host "Root: $CodexSkillsRoot"
Write-Host ""

$missing = @()

foreach ($skill in $requiredSkills) {
    $skillDir = Join-Path $CodexSkillsRoot $skill
    $skillMd = Join-Path $skillDir "SKILL.md"
    if (Test-Path -LiteralPath $skillMd) {
        Write-Host "[OK]   $skill"
    } else {
        Write-Host "[MISS] $skill"
        $missing += $skill
    }
}

Write-Host ""

$browserHarness = Get-Command browser-harness -ErrorAction SilentlyContinue
if ($browserHarness) {
    Write-Host "[OK]   browser-harness command on PATH: $($browserHarness.Source)"
} else {
    Write-Host "[WARN] browser-harness command not visible on PATH in this shell."
    Write-Host "       Skill files exist, but command may require Codex/shell restart or package install."
}

Write-Host ""
Write-Host "Harness docs:"
Write-Host "- memory/domain/skill_team_harness_2026-05-02.md"
Write-Host "- memory/domain/skill_team_operating_board_2026-05-02.md"

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing skills: $($missing -join ', ')"
    exit 1
}

exit 0
