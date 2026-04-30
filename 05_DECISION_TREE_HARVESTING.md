# 05_DECISION_TREE_HARVESTING — Die Innovation

> **Was diese Datei beschreibt:** Wie wir aus den Entscheidungen der Radiologen einen Trainings-Korpus bauen — und das Modell daraus lernt, *wie* ein Arzt denkt, nicht nur *was* er auf das Bild schreibt.
>
> Das ist der eigentliche neue Beitrag, der Carotis-AI von jeder anderen CTA-KI-Lösung trennt. Auch der Punkt, den wir bei Prof. Rohde verkaufen.

---

## 1. Das Problem mit aktuellen KI-Lösungen

Standard-Pipeline aller Carotis-AI-Systeme der letzten 5 Jahre:

```
DICOM-Bild  →  CNN  →  Wahrscheinlichkeit pro Klasse  →  Label
                ↑                                          ↑
            Pixel-Repräsentation                       Was, nicht warum
```

Was verloren geht:
- Welche **Features** hat der Radiologe gewichtet (Echodichte, Plaque-Form, Bewegungs­muster, Kontrast-Verteilung)?
- Welche **Differenzialdiagnosen** wurden erwogen und ausgeschlossen?
- Welche **klinischen Kontexte** (Symptome, Vorerkrankungen, Anamnese-Hinweise) haben mitgespielt?
- Wie **sicher** war der Arzt — und woran hat er das festgemacht?

Das alles ist **Tacit Knowledge**, das in 10 Jahren Facharztausbildung erworben wird. Es bleibt im Kopf des Arztes. Bei jeder Befundung wird es neu produziert und sofort weggeworfen, weil das Befund-System nur das End-Label erfasst.

**Wir harnessen es.**

---

## 2. Die Lösung in einem Satz

Nach jeder Befundung erscheint eine **30-Sekunden-Mini-UI**, die strukturiert nach 4 Dingen fragt: *Auswahl-Feature, Differenzialdiagnose, Konfidenz, Korrektur*. Die Antwort wird anonymisiert, mit dem Bild verknüpft und in einen Decision-Tree-Korpus geschrieben. Das Modell trainiert nachts inkrementell darauf — als zusätzliche Loss-Komponente, die Reasoning-Alignment belohnt.

---

## 3. Decision-Tree-Schema (JSON)

```json
{
  "case_id": "sha256(study_uid + salt)",
  "captured_at": "2026-08-15T14:23:00Z",
  "physician_role_hash": "sha256('aroob' + project_salt)",
  "ai_prediction": {
    "stenosis_pct_nascet": 67.5,
    "confidence": 0.89,
    "vulnerability_markers": {
      "intraplaque_hemorrhage": 0.82,
      "thin_fibrous_cap": 0.41,
      "lipid_rich_necrotic_core": 0.71,
      "systolic_motion_anomaly": 0.13
    },
    "model_version": "v0.3.2",
    "model_sha": "abc123…"
  },
  "physician_decision": {
    "stenosis_pct_nascet": 65,
    "confidence_self_reported": "high",
    "confirmed_markers": ["intraplaque_hemorrhage", "lipid_rich_necrotic_core"],
    "rejected_markers": [],
    "added_markers": ["calcified_shell_partial"]
  },
  "reasoning": {
    "deciding_feature": "echolucent_zone_dorsal",
    "ruled_out": ["fibroadenoma_artifact", "thrombus_acute"],
    "ruled_out_reason": "echo_pattern_chronic + clinical_history_negative",
    "would_consult": null,
    "would_re_image_if": "symptomatic_progression"
  },
  "agreement_with_ai": {
    "verdict": "partial_agreement",
    "delta_pct": -2.5,
    "delta_markers": ["+calcified_shell_partial"],
    "trust_score_for_this_case": 4
  },
  "anonymisation": {
    "method": "DICOM_PS_3.15_basic",
    "salt_version": "v2026-04",
    "audit_id": "auto_generated"
  }
}
```

### Pflichtfelder vs. Optional

- **Pflicht:** `case_id`, `physician_role_hash`, `ai_prediction`, `physician_decision.stenosis_pct_nascet`, `agreement_with_ai.verdict`
- **Optional aber stark erwünscht:** `reasoning.*`, `physician_decision.confidence_self_reported`
- **Auto-generiert:** `anonymisation.*`, `captured_at`, `case_id`

Wenn nur Pflichtfelder ausgefüllt → 5 Sekunden. Wenn alles → 30 Sekunden. UI ermutigt, blockiert nicht.

---

### 3.1 Spec-Erweiterung v0.2 — Freitext-Feld (`free_text_notes`)

**Hinzugefügt:** 2026-04-29 (P0b — Tacit-Knowledge-Capture).

**Begründung:** Strukturierte Felder erfassen den Großteil der ärztlichen Begründung — aber nicht alles. Was der Arzt **nicht entschieden** hat, **was er offen gelassen** hat, **welche Hypothese er noch verfolgen will**, all das ist tacit knowledge das in Standard-Schemas verloren geht. Ein opt-in Freitext-Feld am Ende der Form fängt das auf.

**Schema-Erweiterung in `reasoning`:**

```json
"free_text_notes": {
  "type": ["string", "null"],
  "maxLength": 2000,
  "description": "Optionale freie Notiz: was hast du entschieden, was nicht, was bleibt offen? Wird PII-gefiltert (DE-NER + Regex) BEVOR Speicherung. Bei PII-Treffer: Reject mit Hinweis."
}
```

**Tagesaggregation (Daily-Learning-Loop-Erweiterung):**

Ab P5 läuft jede Nacht zusätzlich `aggregate_free_text.py`:

1. Liest alle neuen `free_text_notes` seit letztem Run
2. NLP-Cluster (BERTopic mit `xlm-roberta` oder Hermes-Local-LLM mit Topic-Prompt)
3. Schreibt `memory/anomalies/triage_week<N>.md` mit:
   - Top-5 wiederkehrende Themen
   - Vorschläge: welche neuen `deciding_feature`-Werte sollen ins Strukturschema aufgenommen werden
   - Beispiele anonymisierter Snippets
4. Lou approved oder rejected die Schema-Erweiterungs-Vorschläge wöchentlich
5. Bei Approve: Schema bekommt neues Enum-Item, `validate_decision_tree.py` wird angepasst

**Damit wächst der strukturierte Entscheidungsbaum kontinuierlich** aus dem Freitext-Korpus heraus. Tag-für-Tag werden lokale Eigenheiten des Klinikum-Workflows zu Standard-Strukturen.

---

## 4. UI-Spec (30-Sek-Form)

Erscheint im Anschluss an die Befund-Bestätigung im Carotis-AI-Panel.

```
┌─────────────────────────────────────────────────────────────┐
│  Befund bestätigt (NASCET 65 %, IPH + LRNC)                 │
│                                                              │
│  Lehre die KI — 30 Sekunden:                                │
│                                                              │
│  ▸ Welches Feature war ausschlaggebend?                     │
│    ○ Echolucent zone   ○ Hemorrhage signal                  │
│    ○ Fibrous cap       ○ Calcified shell                    │
│    ○ Motion pattern    ○ Other (Freitext)                   │
│                                                              │
│  ▸ Was hast du erwogen und ausgeschlossen?                  │
│    [Multi-Select aus Standard-DDx-Liste]                    │
│                                                              │
│  ▸ Wie sicher bist du?                                      │
│    ○ Hoch  ○ Mittel  ○ Niedrig — würde Zweitmeinung holen   │
│                                                              │
│  ▸ KI-Vorschlag:                                            │
│    ○ Stimme zu  ○ Teilweise  ○ Lehne ab — Begründung:       │
│                                                              │
│  ▸ Was ist offen / unsicher? (optional)                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ z.B. „Plaque-Form unklar, würde Verlaufskontrolle in    ││
│  │ 6 Monaten machen wenn Symptome zunehmen. CTA-Phase     ││
│  │ war suboptimal."  (max 2000 Zeichen)                   ││
│  │                                            [0/2000]     ││
│  └─────────────────────────────────────────────────────────┘│
│   Live-PII-Check: kein Patientenname, keine Telefonnummer.   │
│                                                              │
│  [SPEICHERN — 12 s] [SKIP — wird in 24h erneut angezeigt]   │
└─────────────────────────────────────────────────────────────┘
```

### Freitext-Feld (`free_text_notes`)

**Position:** Nach Trust-Score, vor SAVE-Button.

**Component-Verhalten:**
- `<textarea>` mit `maxLength=2000`, character counter rechts unten
- Hint-Text: *"Was ist offen oder unsicher? Was würdest du noch klären? Keine Patientennamen — wir filtern automatisch und lehnen den Eintrag ab, wenn welche drin sind."*
- **Live-Validation** (debounced 500 ms) gegen `POST /api/v1/decision-tree/check-text` → Backend prüft mit Spacy DE-NER + Regex-Fallback (Telefonnummern, IDs)
- PII-Treffer: rote Unterlinge unter dem gefundenen Span + Tooltip *"Mögliche Personennamen — bitte umformulieren"*
- Counter wird rot bei > 1900 Zeichen (Soft-Limit)
- 5-Sek-Auto-Save in `localStorage` für Skip-and-Resume

**Backend-Verhalten:**
- `decision_tree_service.capture()` macht PII-Check **vor** Speicherung
- Bei PII-Treffer: HTTP 422 mit `{detail, pii_spans, suggestion}` — UI hebt Spans hervor, Lou kann Lou neu submit
- Audit-Event für jeden Reject (kein Patientendaten-Leak im Audit-Trail — nur "PII-Reject mit N Spans")

**Daily-Aggregation:**
- Nightly Cron `aggregate_free_text.py` (siehe Sektion 3.1)
- Output: `memory/anomalies/triage_week<N>.md` mit Topic-Clustern + Schema-Erweiterungs-Vorschlägen


### UX-Regeln

- **Keine Pflicht-Submission.** Skip ist immer möglich. Adoption-Rate ≥ 30 % ist das Ziel.
- **Default-Werte sind die KI-Vorschläge** — Arzt klickt nur, wo er widerspricht. Reduziert Aufwand drastisch.
- **Auto-Skip nach 24 h** — wenn der Fall nicht binnen einem Tag begründet wurde, geht er ohne Decision-Tree in den Audit-Trail (gilt nur als „Befund bestätigt", nicht als „Trainings-Datenpunkt").
- **Pflicht-Modus** für 4 Wochen / Quartal aktivierbar (Aroob's Wahl, falls Coverage zu niedrig).
- **Badges / Gamification** — wöchentliches Stat-Email an die Radiologie: *"15 Trees diese Woche → Modell um 0.7 % Sensitivity verbessert"*. Wenn die Verbesserung sichtbar wird, steigt die Adoption.

---

## 5. Anonymisierungs-Pipeline

```
Decision-Tree-Eingabe (im Klinikum-PVS)
    ↓
[Schritt 1] PII-Strip (DICOM PS 3.15 Profile "Basic")
    - Alle 33 Standard-PII-Tags entfernt
    - Patient-Name → null
    - Geburtsdatum → Geburtsjahr
    - Studientag → +/- 7 Tage Jitter
    ↓
[Schritt 2] Re-Identification-Risk-Assessment
    - k-anonymity-Check (k≥5 für jede Quasi-Identifier-Kombination)
    - Wenn k<5: study_uid wird mit Projekt-Salt re-gehashed
    ↓
[Schritt 3] Hash-Stamp
    - case_id = sha256(study_uid + salt_version + timestamp_bucket)
    - audit_id wird in lokaler Audit-DB gespeichert (nur dort, nie exportiert)
    ↓
[Schritt 4] Schreibe in memory/decisions/<YYYY-MM-DD>_<case_id_short>.json
    ↓
[Schritt 5] Wenn agreement_with_ai.verdict == "disagreement":
    Zusätzlich Eintrag in memory/anomalies/<YYYY-MM-DD>_<case_id_short>.json
```

**Was niemals exportiert wird:**
- Audit-DB-Mapping (case_id ↔ patient_id)
- Original-Studientag
- Klar-Patient-Name oder DOB
- Kontextdaten, die Re-Identifikation ermöglichen würden (z.B. seltene Diagnose-Kombinationen)

**Sicherheits­netz:** Quartalsweise penetration test des Anonymisierungs-Outputs durch Prof. Margaritoff oder externen Auditor.

---

## 6. Trainings-Pfad — wie das Modell lernt

### 6.1 Loss-Komponenten

```python
total_loss = (
    α * segmentation_dice_loss              # Standard MFSD-UNet
    + β * vulnerability_classification_loss # Multi-Task-Head
    + γ * reasoning_alignment_loss          # NEU
)
```

`reasoning_alignment_loss` belohnt Modell-Outputs, die mit den `deciding_feature`-Markierungen der Radiologen übereinstimmen. Implementiert als:

- **Aufmerksamkeits-Regularisierung:** Grad-CAM des Modells für eine Klasse soll mit der vom Radiologen markierten Region korrelieren (Cosine-Similarity-Loss zwischen Heatmap und annotierter Bounding-Box).
- **Feature-Prediction-Head:** zusätzlicher Output-Kopf, der das `deciding_feature` als Klassifikations-Label vorhersagt.

### 6.2 Daily-Learning-Loop

```
22:00 Klinikum-Schließung
    ↓
22:15 Cron startet `nightly_retrain.py`:
    1. Lese alle neuen Decision-Trees seit letztem Run
    2. Validiere Anonymisierung (Re-Audit)
    3. Lade aktuelles Modell als Checkpoint
    4. Inkrementelles Training (1-3 Epochs auf neuen + Replay-Buffer)
    5. Evaluation auf Hold-Out-Test-Set
    6. Vergleich vor/nach:
       - Sensitivity, Specificity, Dice, AUC
       - Falls Verbesserung ≥ 0.1 % auf Composite-Metric: deploy
       - Falls Verschlechterung > 0.5 %: Rollback + Alert an Lou
       - Anomaly-Pattern-Detection: häufige Disagreements → Mail an Aroob
    7. Logge in memory/runs/<datum>_nightly_retrain.md:
       - Welche Trees verwendet
       - Performance-Delta
       - Deploy / Rollback / Skip
    ↓
06:00 Modell ist fit für den nächsten Klinikum-Tag.
```

### 6.3 Anomaly-Triage (Wöchentlich, Opus 4.7)

Einmal pro Woche läuft eine Opus-4.7-Session über alle `memory/anomalies/`-Einträge der Woche und sucht Patterns:

- *"In 7 von 9 Disagreements hat Aroob `calcified_shell_partial` markiert, das Modell hat das nicht in seiner Marker-Liste."* → Folge-Task: Marker zur Klassifikator-Ausgabe hinzufügen.
- *"In 4 Disagreements lag das Bild in der Modalität CT mit niedriger Dosis (LDCT) — wir haben dafür kaum Trainings-Daten."* → Folge-Task: gezielte Daten-Akquise LDCT.

Diese Triage-Reports werden als `memory/anomalies/triage_<woche>.md` gespeichert und sind die wichtigste Quelle für Roadmap-Updates ab P5.

---

## 7. Wie der Tree zur Promotionsarbeit beiträgt

Aroob's Dissertation hat dadurch **zwei** Hauptbeiträge:

1. **Klinisches Validierungs-Paper:** Carotis-AI vs. Konsens-Ground-Truth, n≥300, Klinikum DE + Sarah JO, primärer Endpunkt Inter-Observer-Variabilitäts-Reduktion.
2. **Methodisches Paper:** Decision-Tree-Harvesting als Trainings­paradigma — neuer Beitrag zur Medical-AI-Literatur, da bisher nur als Vision in 2024er Papers diskutiert. Veröffentlichung in *Medical Image Analysis* oder *NEJM AI*.

Plus optional: ein **Methods-Paper** mit Lou als Erst-Autor und Margaritoff/Tolg/Rohde als Senior-Autoren über das Engineering-Harnessing-Framework an sich (separate Akademische Linie für Lou).

---

## 8. Risiken & Mitigationen

| Risiko | Mitigation |
|--------|------------|
| Adoption < 30 % | UI-Optimierung, wöchentliche Performance-Mails, Pflicht-Modus quartalsweise |
| Bias durch nur einen Befunder (Aroob als Hauptlabeller) | Inter-Observer-Subset n=50 mit Zweit-Radiologe; Sarah-Hospital-Daten als kulturelles Korrektiv |
| Re-Identification-Risiko trotz Anonymisierung | k-anonymity-Check, Quartals-Audit, Salt-Rotation |
| Modell-Drift durch falsche Decision-Trees | Quality-Score pro Tree (basiert auf Konfidenz-Self-Report + Konsens mit anderen Trees), gewichtetes Training |
| Daily-Retraining destabilisiert Performance | Auto-Rollback + Hold-Out-Testset + Alerting; Wöchentliche Sanity-Checks |

---

## 9. Status

| Komponente | Status | Phase |
|------------|--------|-------|
| Schema-Spec | ✅ v0.1 (diese Datei) | P0 |
| UI-Spec | ✅ v0.1 (diese Datei) | P0 |
| Anonymisierungs-Pipeline | 🔒 Spec only | P2 |
| Trainings-Loss-Implementation | 🔒 Spec only | P3 |
| Daily-Learning-Loop | 🔒 Spec only | P4 |
| Anomaly-Triage-Workflow | 🔒 Spec only | P5 |

Implementierung beginnt mit P2 (Anonymisierungs-Pipeline). Bis dahin: dieses Dokument ist die einzige verbindliche Spec.

---

**Letztes Update:** 2026-04-27 · Opus 4.7 · Erster Wurf
