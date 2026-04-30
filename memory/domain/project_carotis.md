---
name: project_carotis
description: Carotis-AI — lokales, erklärbares KI-CDSS für die Carotis-Stenose-Quantifizierung aus CTA. Promotionsprojekt am Klinikum Dortmund. Innovation: Decision-Tree-Harvesting (Modell lernt die ärztliche Begründung, nicht nur das Bild).
type: project
last_updated: 2026-04-27
---

# Carotis-AI

## In One Sentence

Ein lokal betriebenes, erklärbares KI-System, das die Carotis-Stenose-Diagnostik aus CTA-Bildern unterstützt — und sich täglich aus den Entscheidungen der Radiologen verbessert.

## What's IN

- **Technische Basis:** MFSD-UNet (U-Net + Swin Transformer + Deep Supervision), Dice ≥ 0.90, Sens ≥ 0.99 nach Xie et al. 2024 QIMS
- **Plaque-Vulnerability-Multi-Task:** Klassifikation für IPH (Intraplaque Hemorrhage), ThinCap (Thin Fibrous Cap), LRNC (Lipid-Rich Necrotic Core), Systolic Motion Anomaly
- **XAI-Schicht:** Grad-CAM für Heatmaps, SHAP für tabulare Vulnerability-Features
- **Decision-Tree-Harvesting** (Innovation): 30-Sek-UI nach jeder Befundung, anonymisierter Korpus
- **Daily-Learning-Loop:** Cron-Job, inkrementelles Training, Auto-Rollback
- **Local-First Edge:** ONNX Runtime auf Praxis-Server, FastAPI-Backend, React-UI
- **Transnationale Validierung:** Klinikum Dortmund (DE) + Sarah Specialty Hospital (JO)

## What's OUT (für die 24-Monats-Promotion)

- Andere Gefäße als Carotis (kein Aorta, kein Coronary, kein Periphere)
- Andere Modalitäten als CTA (kein MRA, kein Sonographie als Primär-Input — Sonographie nur zur Sekundär-Validierung)
- Generelle Radiologie-AI / "Medical Foundation Model"
- US/Kanada-Markt (DACH zuerst, dann EU, dann Welt)
- Kommerzialisierung (kommt nach Disputation in P7)

## What Differentiates

| Aspect | Existing solutions (Floy, Aidoc, Viz.ai) | Carotis-AI |
|--------|------------------------------------------|------------|
| Architektur | Cloud | Local-First Edge |
| DSGVO | erhöhte Anforderungen | by Design konform |
| Carotis-Fokus | Generalist | Spezialist |
| XAI | Bounding-Box + Konfidenz | Grad-CAM + SHAP + Reasoning-Capture |
| Lernen aus Arzt-Begründung | nein | ja (Decision-Tree-Harvesting) |
| Daily Learning | nein | ja |
| Multi-Center DE/JO | nein | ja |
| Lock-In | hoch | null (Open-Source-Stack) |

## Stack

Siehe `CLAUDE.md` Sektion "Stack (April 2026)". Frontend React 19 + Vite + Tailwind v4. Backend FastAPI + ONNX. DB SQLite + DICOM-Filesystem. Anonymisierung DICOM PS 3.15.

## Critical Path

P0 (Rohde) → P1 (Ethik+Datenvertrag) → P2 (Daten n≥500) → P3 (Modell) → P4 (Edge+UI+Decision-Tree) → P5 (Validierung+Daily-Loop) → P6 (Manuskript+Disputation) → P7 (MDR+Skalierung).

24 Monate bis Disputation. Detail in `02_ROADMAP.md`.

## Stakeholder-Map (Kurzfassung)

- **Aroob:** Kandidatin, Ärztin in Weiterbildung Radiologie, Klinikum Dortmund
- **Prof. Rohde:** Ziel-Betreuer, Klinikum Dortmund, Neuroradiologie
- **HAW-Beratung:** Margaritoff (62304), Tolg (SIMLab/VR), van Stevendaal (Med. Devices)
- **Tech:** Lou (Lead), Dr. Islam Shdaifat (CV/AI Architect), Yassine Daghfous (Data Eng)
- **Klinik-Validierung:** Sarah Hospital JO, ggf. Praxis Klaproth DE als Sekundär

Detail in `04_MASTER_PLAN.md` Sektion 8.
