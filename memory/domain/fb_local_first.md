---
name: fb_local_first
description: Local-First ist religiös, nicht-verhandelbar. Kein Modell schlägt Cloud-API für Patientendaten vor. Diggai-Prinzip Nr. 1.
type: feedback
last_updated: 2026-04-27
---

# Local-First ist nicht-verhandelbar

**Regel:** In allen Carotis-AI-Komponenten, die Patientendaten berühren, gibt es **keinen Cloud-Aufruf**. Punkt. Kein "wir könnten ja als Notlösung mal..." Keine OpenAI-API für Befund-Klassifikation. Kein AWS S3 für DICOM-Backup. Keine Google-Translate-Integration für arabische UI-Strings, wenn die Strings echte klinische Befunde enthalten könnten.

## Why

Drei Gründe, drei Schutz-Schichten:

1. **DSGVO Art. 9** Gesundheitsdaten verlangen explizite Einwilligung pro Verarbeitungs-Vorgang. Bei Cloud-Verarbeitung würde jeder Patient eine separate, AVV-konforme Einwilligung für jeden Cloud-Anbieter brauchen. Das skaliert nicht.

2. **EU AI Act Art. 10** verlangt Data Governance bei High-Risk AI. Cloud-Trainings­daten sind schwer auditierbar — du kannst nicht nachweisen, dass nur autorisierte Daten ins Modell geflossen sind, wenn das Training auf einer fremden Infrastruktur lief.

3. **Lou's Reverse-Social-Engineering-Doktrin:** Mittelsmänner werden eliminiert. Cloud-Provider sind Mittelsmänner. Bei Diggai gilt: kein SaaS, kein externes IT-Outsourcing, keine Drittpartei zwischen Patient und Diagnose.

## How to apply

- **Trigger:** Wenn ein Modell überlegt *„könnten wir nicht für diesen Use-Case..."* mit einer Cloud-Lösung — STOPPE und schreib stattdessen: *„Local-First: kein externer API-Call. Alternativen: lokales Modell, On-Premise-Service, Offline-Tool."*
- **Ausnahmen** (vollkommen ok als Cloud):
  - Modell-Training auf bereits anonymisierten Daten (Sarah Hospital → HAW Workstation, signiertes Bundle)
  - Generelle Doku, Recherche, Stakeholder-Mails (das sind keine Patientendaten)
  - Code-Suche (GitHub, Stack Overflow)
  - AI-Modelle für Code-Generation (Anthropic Claude, GitHub Copilot) — solange kein Patientendaten-Snippet im Kontext steht
- **Audit-Pfad:** Jedes externe Netzwerk-API-Call eines Carotis-AI-Skripts muss in einem Allowlist-File stehen (`scripts/.allowed_endpoints.txt`). Wenn ein Modell ein neues Call hinzufügt, muss es das File erweitern + Begründung in commit-Message.

## Edge case

**„Aber für die Demo will ich kurz die Vercel-API nutzen, um einen Test-Endpoint hochzuziehen, ist ja nur Mock-Data..."** — NEIN. Auch Mock-DICOM-Daten sind Mock von echten Daten — wenn das Setup in Produktion geht, bleibt der Cloud-Pfad versehentlich drin. Lieber von Anfang an lokal.
