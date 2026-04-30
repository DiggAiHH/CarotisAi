# Carotis-AI — Copilot Project Instructions

## Project
Local-First, DSGVO-konformes Clinical Decision Support System für die 
Carotis-Stenose-Quantifizierung aus CTA-Bildern. Promotionsprojekt am 
Klinikum Dortmund (Aroob Alrawashdeh, Betreuer Prof. Dr. Stefan Rohde). 
Innovation: Decision-Tree-Harvesting — Modell lernt die ärztliche Begründung, 
nicht nur das Bild. Spec: ../05_DECISION_TREE_HARVESTING.md

## Stack
- Backend: Python 3.11 + FastAPI + Pydantic v2 + SQLAlchemy async + ONNX 
  Runtime + structlog + Prometheus
- Frontend: React 19 + Vite + TypeScript + Tailwind v4 + Cornerstone.js 
  DICOM viewer + Zustand + TanStack Query
- ML: PyTorch 2.5 + MONAI + timm (Swin Transformer) + grad-cam + MLflow + 
  ONNX export
- Local AI: Ollama (localhost:11434) + Hermes Agent (Nous Research) + 
  caveman compression
- Infrastructure: Docker Compose, kein Cloud-Provider für Patientendaten

## Hard Rules (NICHT verhandelbar)
1. Local-First: KEIN Cloud-API-Call für Patientendaten. Ausnahme nur bei 
   bereits anonymisierten aggregierten Modell-Updates. Siehe 
   ../regulatory/adr/ADR-0001-local-first.md
2. Anonymisierung: jeder Patientendaten-Pfad nutzt scripts/anonymize.py 
   (DICOM PS 3.15 + k-Anonymity ≥ 5). Niemals direkter Zugriff auf 
   PII-Felder.
3. Audit-Trail: jede AI-Inferenz und jede Arzt-Entscheidung wird mit 
   timestamp + model_version + model_sha geloggt.
4. Schema-First: alle Daten-Strukturen werden in JSON Schema 2020-12 
   definiert (siehe schemas/decision_tree.schema.json) BEVOR der Code 
   geschrieben wird.
5. Tests: jede Funktion in app/services/ und ml/ braucht mind. 1 pytest. 
   Funktionen mit Patientendaten-Pfad: 100% Coverage.
6. UI-Sprache: Deutsch (Klinikum-Setting). Code-Kommentare + Commit-
   Messages: Englisch.

## Conventions
- Imports: Python — absolute imports vom Package-Root (`from app.services 
  import ...`); TypeScript — `@/...` Alias auf src/
- Type-Hints: Python `from __future__ import annotations` immer. Pydantic 
  v2 BaseModel statt @dataclass für API-Schemas.
- Error-Handling: nie bare `except:`. Strukturierte Errors via 
  custom Exception-Klassen in app/core/exceptions.py.
- Logging: structlog mit `bind()` für Request-Context. Niemals `print()`. 
  Niemals PII in Logs.
- Tests: pytest + pytest-asyncio + httpx AsyncClient. Fixtures in 
  conftest.py.

## Architecture Decisions (lies BEVOR du Architektur änderst)
- ADR-0001 Local-First: ../regulatory/adr/ADR-0001-local-first.md
- ADR-0002 Decision-Tree-Harvesting: ../regulatory/adr/ADR-0002-decision-tree-harvesting.md

## Risk Register
Bevor du etwas an Anonymisierung, Audit-Trail oder Daily-Learning-Loop 
änderst: ../regulatory/risk_register.md lesen. Hazards H-001, H-002, 
H-003, H-006 sind compliance-kritisch.

## Engineering Harness
Übergeordneter Workspace: ../ (das Projekt-Root). 
- ../CLAUDE.md = working memory aller Modelle
- ../MEMORY.md = Index aller Memorys
- ../memory/runs/ = Run-Logs (jede Session schreibt einen)
- ../memory/anomalies/ = bekannte Stolpersteine — vor Code-Änderung lesen

Methodologie: Jake van Clief — Interpretable Context Methodology (MWP). 
Filesystem-Struktur ist die Agent-Architektur. Wenn unklar wo etwas 
hingehört: Numbered-Folder-Convention beachten und in ../00_INDEX.md 
nachschauen.

## When in Doubt
- Architektur-Frage → ADR schreiben unter ../regulatory/adr/
- Patientendaten-Pfad → STOP, an Lou eskalieren
- Schema-Änderung → schemas/ Schema zuerst aktualisieren, dann Code
- Memory-Konflikt → ../memory/anomalies/ lesen
- Modell-Wahl im Routing → ../01_HARNESS.md Routing-Matrix
