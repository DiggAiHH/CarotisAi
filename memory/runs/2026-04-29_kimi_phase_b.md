---
name: 2026-04-29_kimi_phase_b
type: run
---

## Goal
Phase B: Transformers-basierte PII-Detection Layer mit deutschem klinischem NER-Modell.

## Done
- **Modell-Recherche:** `OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1` ausgewaehlt
  - Apache 2.0 Lizenz ✅
  - 76 PII-Labels (B-/I-Tags: FIRSTNAME, LASTNAME, EMAIL, PHONE, SSN, DATEOFBIRTH, etc.)
  - Longformer-Architektur (4096 Token Kontext)
  - Speziell fuer deutsche klinische Texte trainiert
- **ADR-004:** `regulatory/adr/004_transformers_pii_layer.md` — Architektur-Entscheidung dokumentiert
- **Backend Implementation:**
  - `backend/app/services/transformers_pii_layer.py` — Generischer Transformers-PII-Layer
    - Label-Mapping (76 Modell-Labels → 4 PIISpan-Kategorien: PERSON, PHONE, EMAIL, ID)
    - Extended-Labels optional (DATE, ADDRESS, ORG, AGE, GENDER)
    - Lazy-Load via `@lru_cache`
    - Threshold konfigurierbar (default 0.85)
  - `backend/app/services/pii_detection_service.py` — Refactored zu Layered Architecture
    - RegexLayer (deterministisch, immer aktiv)
    - SpacyLayer (legacy, optional)
    - TransformersPIILayer (ML-basiert, optional)
    - Ensemble.merge() — Dedupe mit Praeferenz fuer laengere Spans
  - `backend/app/core/config.py` — Neue Config-Optionen
    - `transformers_pii_enabled` (default False)
    - `transformers_pii_model` (default OpenMed-Modell)
    - `transformers_pii_device` (default cpu)
    - `transformers_pii_threshold` (default 0.85, Range 0-1)
    - `transformers_pii_extended_labels` (default False)
  - `scripts/download_pii_model.py` — Idempotentes Download-Skript
- **Tests:** `tests/test_transformers_pii_layer.py` — 17 Tests
  - RegexLayer-Tests (4)
  - Ensemble-Tests (2)
  - PIIDetectionService-Integration (4)
  - TransformersPIILayer-Tests (5, skippen wenn torch/transformers fehlen)
  - Config-Integration (2)
- **Quality:** ruff 0 Errors, black formatiert

## Surprised by
- `OpenMed-PII-German-ClinicalLongformer` hat 76 Labels — viel umfangreicher als erwartet. Mapping auf 4 Kategorien erforderlich.
- `torch` Download auf Windows dauert >5 Minuten — zu langsam fuer CI. Deshalb: torch/transformers als optionale Dependencies (wie Spacy).
- `huggingface_hub` war nicht installiert — musste nachinstalliert werden fuer Modell-Recherche.

## Avoided
- Kein PyTorch im Base-Image — bleibt optional, Lazy-Load Pattern analog Spacy
- Kein automatisches Modell-Download beim Service-Start — explizites `scripts/download_pii_model.py`
- Keine Frontend-Aenderungen noetig — API bleibt kompatibel

## Next
- Phase C: HiResCAM-Evaluation als Grad-CAM-Alternative
- P1-Prep: Hardware-Spec + AVV-Vorlage (wartet auf Rohde-Go)

## Memory updates
- `regulatory/adr/004_transformers_pii_layer.md` — ADR-004
- `tasks.jsonl` — K-29 als Phase B markieren
