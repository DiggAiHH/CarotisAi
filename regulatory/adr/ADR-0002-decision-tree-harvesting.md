# ADR-0002: Decision-Tree-Harvesting als Trainings-Loss-Komponente

| Feld | Wert |
|------|------|
| **Status** | Accepted |
| **Datum** | 2026-04-27 |
| **Autor** | Lou (Laith Alshdaifat) + Opus 4.7 (Architekt-Modell) |
| **Reviewer** | Prof. Rohde (klinisch — pending), Dr. Islam Shdaifat (technisch — pending) |
| **Phase** | P0 (Spec) → P3 (Implementation) → P5 (Aktivierung) |
| **Compliance-Impact** | EU AI Act Art. 10 + 14, DSGVO Art. 9 + 25, MDR Annex XIV |

---

## Kontext

Aktuelle CTA-AI-Systeme lernen aus Pixeln und Labels. Was sie nicht lernen: die ärztliche Begründungs-Struktur — welches Bild-Feature war ausschlaggebend, welche Differenzialdiagnosen wurden ausgeschlossen, mit welcher Konfidenz wurde entschieden. Diese "Tacit Knowledge" ist der eigentliche Wert von 10 Jahren Facharztausbildung; bisher wird er bei jeder Befundung neu produziert und sofort weggeworfen.

Carotis-AI hat die Möglichkeit, diese Lücke zu schließen, weil:
1. Die Edge-UI ohnehin nach jeder Befundung eine Kontroll-Eingabe vom Arzt erfordert (Bestätigen / Korrigieren).
2. Der Daily-Learning-Loop (siehe `05_DECISION_TREE_HARVESTING.md`) ist sowieso geplant — Kosten für ein zusätzliches Reasoning-Signal sind marginal.
3. Wir sind in einer akademischen Promotion — methodische Innovationen sind willkommen, nicht riskant.

Die Entscheidung: Sollen wir Decision-Tree-Harvesting nur als nice-to-have-Feature behandeln, als verpflichtenden Teil des Trainings-Loops, oder als das definierende Differenzierungs-Argument der Promotion?

## Optionen

### Option A — Optional Feature, kein Training-Impact
Decision-Trees werden gesammelt, aber nur zur Wissens-Aufzeichnung. Modell trainiert klassisch auf Pixeln + Labels.
- **Pro:** kein zusätzliches Modell-Komplexitäts-Risiko, einfacher zu implementieren
- **Contra:** wirft den eigentlichen wissenschaftlichen Beitrag weg; Aroob's Promotion bleibt eine "lokale Variante eines bekannten Systems"
- **Aufwand:** S
- **Reversibilität:** trivial

### Option B — Multi-Task-Head mit Reasoning-Vorhersage
Modell bekommt zusätzlichen Output-Kopf, der das `deciding_feature` als Klassifikations-Label vorhersagt. Loss: Cross-Entropy auf diese Vorhersage. Decision-Trees fließen als Trainings-Labels ein.
- **Pro:** klassische Multi-Task-Architektur, bewährt; Modell wird gezwungen, ein "warum" zu lernen
- **Contra:** vorhergesagte Reasoning ist ein Klassifikations-Output, nicht direkt mit dem Bild-Heatmap verknüpft — mittelmäßiger Mehrwert
- **Aufwand:** M
- **Reversibilität:** mittel (Multi-Task-Head kann ausgeschaltet werden, aber Modell muss neu trainiert werden)

### Option C — Reasoning-Alignment-Loss + Multi-Task-Head (full Spec)
Zwei Loss-Komponenten ergänzen den Standard-Dice + Vulnerability-Loss:
1. **Aufmerksamkeits-Regularisierung:** Grad-CAM des Modells für eine Klasse soll mit der vom Befunder markierten Region korrelieren (Cosine-Similarity-Loss)
2. **Feature-Prediction-Head:** zusätzlicher Output-Kopf für `deciding_feature`-Vorhersage (Cross-Entropy)

- **Pro:** maximaler wissenschaftlicher Beitrag; das Modell lernt nicht nur "was", sondern auch "wo der Arzt hingeschaut hätte"; publikationsfähig in Medical Image Analysis / NEJM AI
- **Contra:** komplexer zu implementieren, Loss-Gewichtung muss empirisch tuned werden; Reasoning-Alignment-Loss ist neu in der Literatur (mehr Erklärungs-Aufwand für Reviewer)
- **Aufwand:** L
- **Reversibilität:** mittel (Loss-Gewichte können auf 0 gesetzt werden, aber Trainings-Pipeline ist komplexer geworden)

## Entscheidung

**Option C — Reasoning-Alignment-Loss + Multi-Task-Head.**

Begründung:
1. Wissenschaftlicher Beitrag ist der eigentliche Promotions-Wert. Aroob's Promotion lebt nicht vom Pixel-Modell (das ist State-of-the-Art und replizierbar) — sie lebt von der Methodik.
2. Mit den HAW-Beratern (Margaritoff, Tolg) und Dr. Islam haben wir das Know-how für komplexe Loss-Architekturen.
3. Die Reversibilitäts-Kosten sind beherrschbar: wenn der Reasoning-Loss in P3 als zu komplex sich herausstellt, können wir Loss-Gewichte auf 0 setzen und auf Option B zurückfallen, ohne die Promotion zu gefährden.
4. Veröffentlichungs-Linie: zwei Papers (klinisch + methodisch) statt einem. Doppelte Output für Aroob + Senior-Author-Credit für Rohde.

## Konsequenzen

### Positiv
- Promotion hat klar abgegrenzten methodischen Beitrag
- Zwei Publikationsmöglichkeiten (Radiology / JNIS für klinisch + Medical Image Analysis / NEJM AI für methodisch)
- Modell-Erklärbarkeit wird bewusst trainiert, nicht nur post-hoc visualisiert
- Engineering-Harnessing-Story passt — wir harnessen Wissen, das sonst verloren geht

### Negativ
- Implementations-Komplexität in P3 deutlich höher (PyTorch Multi-Task + Custom Loss + Heatmap-Annotation-Pipeline)
- Loss-Gewichtungs-Tuning erfordert eigene Hyperparam-Search
- Decision-Tree-Adoption muss > 30% sein, sonst hat der Reasoning-Loss zu wenig Trainingsdaten — Risiko-Mitigation in `05_DECISION_TREE_HARVESTING.md` Sektion 8
- Rohde-Akzeptanz steht und fällt mit dem Verständnis dieser Methodik — `06_ROHDE_MEETING_KIT.md` Sektion 3 muss das in 5 Min vermitteln

### Folge-Tasks
- T-019 (P3): Loss-Funktion mit konfigurierbaren Gewichten α/β/γ implementieren
- T-020 (P3): Heatmap-Annotation-Pipeline (Grad-CAM-Output → Annotated-Region-Cosine-Similarity)
- T-021 (P3): Multi-Task-Head für deciding_feature
- T-022 (P3): Hyperparam-Search-Skript für Loss-Gewichte
- T-023 (P5): Adoption-Monitoring + Pflicht-Modus-Trigger
- T-024 (P6): Methodisches Paper schreiben (Lou Erst-Autor / Aroob Co-Autor / Rohde Senior)

## Reversibilität

Wenn in P5 sich zeigt, dass der Reasoning-Loss schädlich (Performance-Degradation) oder unwirksam (keine messbare Verbesserung) ist:
- **Mittlere Kosten:** Loss-Gewichte γ → 0 setzen, Modell neu trainieren ohne Reasoning-Komponente. Decision-Trees bleiben gesammelt für ein Folge-Paper.
- **Auswirkung auf Promotion:** Ein Paper statt zwei. Methodisches Paper wird zu "Negative Results"-Paper (auch publikationsfähig, z.B. in *Annals of Internal Medicine* oder *JAMIA*).

## Compliance-Impact

- [x] **EU AI Act Art. 10** (Data Governance) — Decision-Trees sind Trainings­daten und unterliegen damit der Anonymisierungs- und Bias-Audit-Pflicht. `schemas/decision_tree.schema.json` enforced PII-Freiheit auf Schema-Ebene.
- [x] **EU AI Act Art. 14** (Human Oversight) — der Decision-Tree-Capture-Prozess ist explizit Human-in-the-Loop und stärkt die menschliche Kontroll-Position
- [x] **DSGVO Art. 9** (Gesundheitsdaten) — Decision-Trees enthalten keine direkten Patientendaten; nur anonymisierte case_ids
- [x] **DSGVO Art. 25** (Privacy by Design) — k-Anonymity ≥ 5 ist auf Pipeline-Ebene durchgesetzt
- [x] **MDR Annex XIV** (Klinische Bewertung) — Decision-Trees liefern zusätzliche Evidenz für die klinische Performance des Systems
- [ ] **ISO 14971** — neuer Hazard: "Modell lernt verzerrte Reasoning-Patterns von einzelnem Befunder" → Risk Control Measure in `risk_register.md` ergänzt

## Referenzen

- `05_DECISION_TREE_HARVESTING.md` (vollständige Spec)
- `schemas/decision_tree.schema.json` (technische Validierung)
- `08_RESEARCH_ATTENTION_2020-2026.md` Sektion 9 (Lücken in der Literatur — wir füllen Lücke #2)
- ADR-0001 (Local-First — Voraussetzung für lokales inkrementelles Training)
- Le et al. 2024 Circ Imaging (frühe Diskussion über die Notwendigkeit von Reasoning-Capture)
