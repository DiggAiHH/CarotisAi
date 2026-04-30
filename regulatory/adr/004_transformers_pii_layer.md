# ADR-004: Transformers-basierter PII-Detection Layer

## Status
Accepted — Phase B (P0c)

## Context

Der existierende `PIIDetectionService` verwendet Regex + Spacy `de_core_news_lg` für PII-Detection in freien Arzttexten. Die Regex-Layer ist zuverlässig für strukturierte Daten (Telefonnummern, E-Mail), aber Spacy's `de_core_news_lg` ist ein **allgemeines** deutsches Sprachmodell ohne medizinische Domänen-Anpassung. Es erkennt Personennamen, aber keine klinischen PII-Typen (Patienten-ID, Krankenversicherungsnummer, etc.) und hat Schwierigkeiten mit medizinischen Fachbegriffen.

Eine 2025 Studie (Diaz Ochoa et al., Frontiers Digital Health) zeigt, dass fine-tuned klinische BERT-Modelle zero-shot LLMs bei deutscher klinischer NER deutlich übertreffen (F1 0.84 vs. 0.65).

## Decision

Wir führen einen optionalen, generischen **TransformersPIILayer** ein, der beliebige HuggingFace Token-Classification Modelle für PII-Detection unterstützt.

### Architektur

```
PIIDetectionService.detect(text)
├── RegexLayer.detect()        # PHONE, EMAIL, ID (immer aktiv, deterministisch)
├── TransformersPIILayer.detect()  # 76 PII-Labels via Longformer (optional, lazy)
└── Ensemble.merge()           # Dedupe, längere Span gewinnt
```

### Modell-Auswahl

**Default:** `OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1`
- Apache 2.0 Lizenz ✅
- 76 PII-Labels (B-/I-Tags: FIRSTNAME, LASTNAME, EMAIL, PHONE, SSN, DATEOFBIRTH, etc.)
- Longformer-Architektur (4096 Token Kontext)
- Speziell für deutsche klinische Texte trainiert
- ~440MB PyTorch weights

**Alternative:** Konfigurierbar via `TRANSFORMERS_PII_MODEL` — jeder HuggingFace Token-Classification Checkpoint ist möglich.

### Label-Mapping

Die 76 Modell-Labels werden auf unsere 4 PIISpan-Kategorien gemappt:

| Modell-Label | PIISpan.label |
|-------------|---------------|
| FIRSTNAME, LASTNAME, MIDDLENAME, PREFIX, OCCUPATION, JOBTITLE | PERSON |
| EMAIL | EMAIL |
| PHONE | PHONE |
| ACCOUNTNAME, SSN, IBAN, BANKACCOUNT, CREDITCARD, IPADDRESS, USERNAME, PASSWORD, VIN, VRM, IMEI, MASKEDNUMBER | ID |
| DATE, DATEOFBIRTH, AGE, STREET, CITY, ZIPCODE, STATE, ORGANIZATION | (optional, konfigurierbar) |

### Lazy-Load Pattern

Analog zu `_get_nlp()`:
- `@lru_cache` für Model + Tokenizer
- `torch` + `transformers` sind **optionale** Dependencies (nicht in base `requirements.txt`)
- Fallback auf Regex-only wenn Modell fehlt oder `transformers` nicht installiert
- Modell-Download via `scripts/download_pii_model.py` (idempotent, SHA-Check)

## Consequences

### Positive
- **Höherer Recall** bei Personennamen in klinischen Kontexten ("Dr. Schmidt", "Patient Müller")
- **Neue PII-Typen** erkennbar: Straße, PLZ, Geburtsdatum, Organisation, Beruf
- **Langer Kontext** (4096 Token) für Arztbriefe statt 512 Token
- **Austauschbar** — jeder HuggingFace Token-Classification Checkpoint

### Negative
- **+440MB** Modell-Größe (im `data/models/nlp/` Verzeichnis)
- **+torch** Dependency (~200MB CPU-only)
- **Inference-Zeit** ~100-500ms pro Text (vs. <10ms Regex)
- **Komplexität** — Ensemble-Logik, Label-Mapping, Token-to-Span-Konversion

### Risiken
- **Modell-Drift** — HuggingFace Modell könnte geupdated werden; wir pinnen auf Commit-Hash
- **Out-of-Memory** — 149M Longformer braucht ~1GB RAM beim Laden; Edge-Server hat 64GB
- **Lizenz-Konflikt** — Apache 2.0 ist kompatibel mit unserem Projekt

## Compliance

- **B-14 (Backend autoritativ):** Transformers-Layer läuft serverseitig, nie im Frontend
- **B-15 (Kein PII in Logs):** `PIISpan.text` wird nur im Reject-Response verwendet, nie in Logs
- **Local-First:** Kein Cloud-Call; Modell läuft lokal auf Edge-Server
- **DSGVO:** Kein Daten-Export; Modell-Inferenz geschieht vollständig lokal

## Alternatives Considered

1. **Spacy-Transformers mit BioGottBERT** — BioGottBERT ist ein Pre-trained LM (kein fine-tuned NER). Eigenes Training wäre nötig (Wochen).
2. **GLiNER zero-shot** — F1 ~0.65 auf deutschen Kliniktexten, zu niedrig.
3. **Eigenes BERT-Training** — Zu aufwändig für P0; Datenannotation nötig.
4. **Nur Regex ausbauen** — Deterministisch, aber keine semantische Personenerkennung.

## References

- Diaz Ochoa et al., "Critical assessment of transformer-based AI models for German clinical notes", Frontiers Digital Health 2025
- `OpenMed/OpenMed-PII-German-ClinicalLongformer-Base-149M-v1` — HuggingFace Model Card
- `memory/runs/2026-04-29_research_deep_dive.md` — Sektion 5.2
