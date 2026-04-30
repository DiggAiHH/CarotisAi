# ADR-0001: Local-First-Architektur statt Cloud-basierter Inferenz

| Feld | Wert |
|------|------|
| **Status** | Accepted |
| **Datum** | 2026-04-27 |
| **Autor** | Lou (Laith Alshdaifat) |
| **Reviewer** | Prof. Margaritoff (HAW, DIN EN 62304) — review pending |
| **Phase** | P0 |
| **Compliance-Impact** | DSGVO Art. 9 + 25 + 32, EU AI Act Art. 10 + 12, MDR Art. 5 + Annex II |

---

## Kontext

Die Mehrheit kommerzieller Carotis-AI-Lösungen am Markt (Floy, Aidoc, Viz.ai, Gleamer) sind cloud-basiert. Bilder werden zur Inferenz an einen externen Anbieter gesendet, dort prozessiert und das Ergebnis zurück an den Befunder geliefert.

Für Carotis-AI am Klinikum Dortmund stellt sich die Frage: cloud-basiert (mit dem Marktstandard gehen) oder local-first (anders machen)?

Die Frage ist nicht akademisch. Drei Faktoren machen sie scharf:
1. Aroob's Promotion betrifft Patientendaten in einem deutschen Universitäts-Klinikum — DSGVO-Compliance ist nicht-verhandelbar.
2. EU AI Act tritt für High-Risk-Systeme ab 02.08.2026 in Kraft — Carotis-AI fällt klar darunter.
3. Diggai's Markenidentität ("Local-First für die deutsche Gesundheitsbranche") wird durch jede Cloud-Komponente in Carotis-AI fundamental kompromittiert.

## Optionen

### Option A — Cloud-First (wie der Marktstandard)
- **Pro:** schnellere Entwicklung (managed Inference auf AWS / GCP), kein Hardware-Setup im Klinikum, einfachere Skalierung
- **Contra:** Patientendaten verlassen das Klinikum (DSGVO Art. 9 erhöhte Anforderungen), Auftragsverarbeitungs­vertrag mit Cloud-Provider erforderlich, Audit unter EU AI Act schwer, Vendor-Lock-In
- **Aufwand:** S
- **Reversibilität:** teuer (Datenflüsse müssen rückgebaut werden, AVV gekündigt)

### Option B — Hybrid (Inferenz lokal, Training in Cloud auf anonymisierten Daten)
- **Pro:** Inferenz bleibt local (DSGVO-OK), Training kann auf Cloud-GPUs (schneller, billiger), Modell-Bundle wird signiert zurück
- **Contra:** zwei Systeme zu warten, Anonymisierungs-Pipeline muss extra robust sein, Cloud-Training braucht eigenen DPIA-Pfad
- **Aufwand:** M
- **Reversibilität:** mittel (Training kann zurück on-premise verlagert werden)

### Option C — Local-First komplett (Inferenz UND Training on-premise / HAW-Workstation)
- **Pro:** kein Patientendaten-Pfad in die Cloud, einfacher Audit-Trail, EU-AI-Act-konform by design, kompatibel mit Diggai-Branding, kein Vendor-Lock-In
- **Contra:** langsamere Trainings-Iterationen (HAW-Workstation statt Cloud-GPU-Cluster), eigene Edge-Hardware im Klinikum nötig, Skalierung an mehrere Kliniken bedeutet Hardware-Roll-out
- **Aufwand:** L
- **Reversibilität:** trivial (jederzeit könnte man später eine Cloud-Komponente hinzufügen, falls Use-Case es rechtfertigt)

## Entscheidung

**Option C — Local-First komplett.**

Begründung:
1. Patientendaten verlassen das Klinikum Dortmund niemals. Zero Risk in DSGVO-Kontext.
2. EU-AI-Act-Audit-Trail ist trivial, wenn alles auf einer einzigen Hardware läuft, statt über mehrere Provider verteilt.
3. Die "langsamere Trainings-Iteration" ist im Carotis-Kontext irrelevant: wir trainieren inkrementell pro Nacht (Daily-Learning-Loop in `05_DECISION_TREE_HARVESTING.md`), nicht in massiven Batch-Runs. Eine HAW-Workstation reicht.
4. Reversibilität ist trivial in Richtung Cloud (man kann später hybrid gehen), aber teuer in der anderen Richtung. Wir wählen die unkostenintensive Richtung als Default.
5. Diggai's Glaubwürdigkeit als Local-First-Vorreiter steht und fällt mit dieser Entscheidung. Sie ist nicht-verhandelbar.

## Konsequenzen

### Positiv
- DSGVO-Compliance by Design statt by Compliance — kein zusätzliches Vertragswerk nötig
- EU-AI-Act-Audit-Trail trivial (eine Hardware, eine Log-Datei)
- Marketing-Argument "Erste 100% Local-First Carotis-KI in Deutschland"
- Methodisch publikationsfähig (siehe Lücken-Sektion in `08_RESEARCH_ATTENTION_2020-2026.md`)
- Kompatibel mit Sarah-Hospital-Setup (identische Hardware in JO)

### Negativ
- Hardware-Investment im Klinikum nötig (geschätzt 5–10k€ für Edge-Server mit GPU für Inferenz)
- Trainings-Workstation an der HAW muss verfügbar bleiben über die 24-Monats-Promotion
- Skalierung an weitere Kliniken (P7) bedeutet Hardware-Roll-out, nicht nur Software-Account
- Modell-Updates müssen als signierte Bundles verteilt werden (kein "einfach das Cloud-Modell upgraden")

### Folge-Tasks
- T-014 (P1): Hardware-Spec für Edge-Server schreiben (CPU, GPU, RAM, Storage, Netzwerk-Profil)
- T-015 (P1): AVV-Variante für Local-First-Setup zwischen Klinikum und Lou/HAW (statt klassischem Cloud-AVV)
- T-016 (P3): Modell-Signing-Pipeline aufsetzen (Sigstore o. ä.)
- T-017 (P4): Modell-Update-Verfahren dokumentieren (USB-Delivery oder gesicherter Klinikum-Netzwerk-Pfad)
- T-018 (P5): Identische Hardware bei Sarah Hospital aufstellen + Validierung

## Reversibilität

In 6 Monaten zurückzudrehen wäre **trivial in eine Hybrid-Richtung** (lokales Inferenz behalten, Cloud-Training für massivere Batches dazu). Komplette Cloud-Migration wäre **teuer**, weil die Klinikum-DSGVO-Vereinbarung neu verhandelt werden müsste. Wir bleiben in der einfacheren Richtung.

## Compliance-Impact

- [x] **EU AI Act Art. 10** (Data Governance) — Trainings­daten verlassen Klinikum nicht ohne Anonymisierung; Auditierung trivial
- [x] **EU AI Act Art. 12** (Record-keeping) — alle Inferenzen geloggt in lokaler Audit-DB
- [x] **DSGVO Art. 9** (Gesundheitsdaten) — Patientendaten verlassen die Verarbeitungs­stätte nicht; keine Cloud-Verarbeitung
- [x] **DSGVO Art. 25** (Privacy by Design) — Local-First-Architektur ist die strengste Form von Privacy by Design
- [x] **DSGVO Art. 32** (Sicherheit der Verarbeitung) — keine externe Angriffsfläche durch Cloud-API
- [x] **MDR Art. 5** (Allgemeine Pflichten) — Hersteller (Lou/HAW) hat volle Kontrolle über Trainings-Datensatz
- [x] **MDR Annex II** (Technische Doku) — Datenfluss-Diagramm wird einfacher und damit besser auditierbar
- [x] **DIN EN 62304** Sektion 5.1 — Software-Architektur-Klarheit erhöht
- [x] **ISO 14971** Risk Control Measure: Wegfall des Cloud-Provider-Hazard-Pfads

## Referenzen

- `04_MASTER_PLAN.md` Sektion 4 (Architektur-Diagramm Local-First)
- `memory/domain/fb_local_first.md` (Feedback-Memory: Local-First nicht-verhandelbar)
- `memory/domain/refs_regulatory.md` (regulatorische Quellen)
- DSGVO Art. 9 + 25 + 32 ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj))
- EU AI Act Art. 10 + 12 ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj))
