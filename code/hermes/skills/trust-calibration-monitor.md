---
name: trust-calibration-monitor
trigger_phrases: ["Trust-Score Monitor", "Calibration Status", "Konfidenz-Drift", "Alert Trust"]
schedule: "0 */6 * * *"  # Alle 6 Stunden
required_tools: [http, filesystem]
---
# Trust & Calibration Monitor Skill

Zweck: Kontinuierliches Monitoring der Kalibrierungsqualität.

## Checks
1. **ECE-Drift** — Vergleiche aktuelle ECE mit Baseline
2. **Override-Rate** — Wenn > 40%: Alert an Lou
3. **Trust-Score-Verteilung** — Wenn > 30% "low": Alert
4. **Calibration-Model-Age** — Wenn > 30 Tage alt: Retrain-Reminder

## Alerts
- POST an Backend /health/ready mit erweiterten Metriken
- Log-Eintrag in `memory/anomalies/calibration_alerts.md`
- Bei Kritisch: Hermes sendet Notification an Lou
