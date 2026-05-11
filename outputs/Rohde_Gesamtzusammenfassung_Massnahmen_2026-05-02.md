# Carotis-AI - Gesamtzusammenfassung, Massnahmen und Rohde-Praesentation

Stand: 2026-05-02  
Zweck: interne Kurzfassung fuer Lou, Aroob/Apo und die Vorbereitung des naechsten Kontakts mit Prof. Rohde.

## 1. Was in den letzten Tagen passiert ist

Aus der urspruenglichen Idee einer KI-gestuetzten Carotis-Stenose-Promotion wurde in wenigen Tagen ein pruefbarer, dokumentierter Demo-Stack:

- Die Projektlogik wurde von "Konzept fuer eine moegliche Promotion" auf "funktionierende Live-Demo mit wissenschaftlichem Fahrplan" gedreht.
- Die Kernthese wurde geschaerft: Carotis-AI ist kein generisches Cloud-KI-Tool, sondern ein Local-First-System fuer CTA-basierte Carotis-Stenose, Plaque-Vulnerability, XAI und aerztliches Reasoning.
- Die Rohde-Unterlagen wurden inhaltlich vorbereitet: Konzept, Expose, technische Beschreibung, Value Proposition, Anschreiben, Video-Skript, Demo-Anleitung und Antwort-Kit.
- Der Software-Stack wurde stabilisiert: FastAPI-Backend, React-Frontend, Demo-Token-Gate, Audit-Trail, Decision-Tree-Capture, Grad-CAM/SHAP-Erklaerbarkeit, Tests und CI/CD.
- Die Demo wurde online gebracht. Fly.io ist wegen beendetem Trial/Billing aktuell blockiert; als funktionierender Fallback laeuft Frontend + Backend jetzt unter:

`https://api.carotis.diggai.de/`

Verifiziert am 2026-05-02:

- Frontend Root: HTTP 200
- Backend Health: `https://api.carotis.diggai.de/health/` -> `status: ok`
- Playwright Chromium Visual Smoke: 1/1 passed gegen `https://api.carotis.diggai.de`

## 2. Wichtige Korrektur zur Personen-/Rolleninformation

Neue Angabe von Lou fuer die naechsten Rohde-Dokumente:

- Aroob/Apo soll in den neuen Unterlagen nicht als aktuell am Klinikum Dortmund taetig dargestellt werden.
- Aktuelle Rolleninformation: arbeitet bei NVIDIA.
- Der Bezug zum Klinikum Dortmund/Rohde wird historisch formuliert: Sie hat damals dort bzw. in Rohdes Umfeld gearbeitet und kennt den klinischen Kontext aus dieser Zeit.
- Rohde wird deshalb nicht ueber eine aktuelle interne Klinikum-Rolle angesprochen, sondern ueber die fachliche Vorgeschichte, den bestehenden Bezug und das Promotionsvorhaben.

Empfohlene Formulierung:

> "Durch ihre fruehere Taetigkeit im Umfeld des Klinikums Dortmund und Prof. Rohde kennt Aroob/Apo den neuroradiologischen Workflow aus der Praxis. Aktuell arbeitet sie bei NVIDIA und moechte diese klinische Erfahrung mit moderner KI-Infrastruktur in ein fokussiertes Promotionsprojekt ueberfuehren."

## 3. Was wir Prof. Rohde liefern

Wir liefern nicht nur eine Anfrage, sondern ein Paket:

1. **Kurzer Brief**: persoenlich, ruhig, nicht ueberverkauft, mit Bitte um fachliche Einschaetzung.
2. **Live-Demo-Link**: aktuell funktionsfaehig unter `https://api.carotis.diggai.de/`.
3. **Kurzpraesentation**: 8-10 Folien, fokussiert auf Problem, Loesung, Datenschutz, wissenschaftliche Fragestellung, Stand und naechste Schritte.
4. **Roadmap**: modular, nicht starr auf zwei Jahre festgelegt. Die Promotion kann kuerzer oder laenger sein, je nach Datenzugang, Ethikprozess und Zielumfang.
5. **Arbeitsangebot an Rohde**: Er muss nicht Software bauen. Seine Rolle waere klinische Schaerfung, Validierungsrahmen, Betreuung und ggf. Co-Autorenschaft.

## 4. Kernbotschaft fuer Rohde

> "Wir moechten nicht mit einer fertigen Medizinsoftware ins Haus kommen, sondern mit einem technisch bereits pruefbaren Promotionsprototypen. Die Frage an Sie ist: Ist diese Fragestellung klinisch relevant, wissenschaftlich tragfaehig und unter Ihrer fachlichen Begleitung sinnvoll weiterzuentwickeln?"

## 5. Neue Praesentation vor Rohde - Vorschlag

### Folie 1 - Titel
Carotis-AI: Local-First KI fuer CTA-basierte Carotis-Stenose und Plaque-Risiko  
Untertitel: Promotionsvorhaben mit erklaerbarer KI und klinischem Decision-Tree-Harvesting

### Folie 2 - Ausgangsproblem
- Carotis-Stenose-Quantifizierung ist klinisch relevant, aber interobserver-abhaengig.
- Viele KI-Loesungen sind cloudbasiert, generisch oder nicht erklaerbar.
- Klinische Akzeptanz haengt nicht nur von Accuracy ab, sondern von Vertrauen, Workflow und Nachvollziehbarkeit.

### Folie 3 - Unser Ansatz
- Local-First Edge AI: keine Patientendaten in die Cloud.
- CTA-Fokus: Stenosegrad, Plaque-Morphologie, Vulnerability-Marker.
- XAI: Grad-CAM/HiResCAM + SHAP.
- Decision-Tree-Harvesting: aerztliche Begruendungen werden strukturiert erfasst.

### Folie 4 - Was schon gebaut wurde
- React-Demo-Frontend mit DICOM/AI-Panel.
- FastAPI-Backend mit Health, Inference, Audit und Demo-Routen.
- Token-Gate, synthetische Demo-Faelle, Audit-Trail.
- CI, Tests, Deploy-Pipeline, Hetzner-Fallback online.

### Folie 5 - Live-Demo
Zeigen:
- Login/Token-Gate
- synthetischer Fall
- KI-Ergebnis + Confidence/Trust
- Heatmap/Erklaerbarkeit
- aerztliche Entscheidung/Override

### Folie 6 - Wissenschaftliche Fragestellung
Moegliche Leitfrage:

> "Kann ein lokal betriebenes, erklaerbares KI-System die CTA-basierte Beurteilung von Carotis-Stenosen und Plaque-Vulnerability unter Beibehaltung aerztlicher Kontrolle reproduzierbarer und nachvollziehbarer machen?"

### Folie 7 - Promotionsumfang realistisch halten
- Nicht zwingend zwei Jahre.
- Moeglich als fokussierte Arbeit in 9-18 Monaten, wenn Datenzugang und Ethik zuegig laufen.
- Produktzulassung/MDR ist ein spaeteres Anschlussprojekt, nicht zwingend Kern der Dissertation.
- Dissertation kann auf klinischer Machbarkeit, Retrospektivvalidierung und XAI/Workflow-Evaluation fokussieren.

### Folie 8 - Rolle von Prof. Rohde
- Klinische Schaerfung der Fragestellung.
- Einschluss-/Ausschlusskriterien.
- Definition Ground Truth / Referenzstandard.
- Zugang zu anonymisierten retrospektiven Faellen nach Ethik/DSGVO.
- Bewertung, ob das als Promotionsprojekt tragfaehig ist.

### Folie 9 - Naechste Schritte
- 30-Minuten-Gespraech.
- Klinische Fragestellung finalisieren.
- Ethik-/Datenschutzpfad aufsetzen.
- Retrospektive Datenbasis definieren.
- P1-Plan beschliessen.

### Folie 10 - Entscheidungspunkt
Frage an Rohde:

> "Sehen Sie darin ein sinnvolles, klinisch relevantes Promotionsprojekt, das wir unter Ihrer fachlichen Begleitung weiter strukturieren duerfen?"

## 6. Massnahmen ab jetzt

| Prioritaet | Massnahme | Owner | Ergebnis |
|---|---|---|---|
| 1 | Rolleninfo in allen neuen Rohde-Texten korrigieren: aktuell NVIDIA, Dortmund historisch | Lou/Agent | Keine falsche aktuelle Klinikum-Zuordnung |
| 2 | Hauptdomain `carotis.diggai.de` von Fly auf Hetzner oder Fly-Billing fixen | Lou | Hauptlink statt Fallback-Link nutzbar |
| 3 | Rohde-Brief final lesen und persoenlich anpassen | Lou + Aroob/Apo | Versandfertige Mail |
| 4 | Praesentation als 8-10 Folien in Stride/PowerPoint erzeugen | Cosima/Stride | Rohde-Deck v4 |
| 5 | Demo-Link vor Versand nochmal testen | Codex/Playwright | Screenshot/Smoke OK |
| 6 | Rohde-Terminoptionen vorbereiten | Aroob/Apo | 3 konkrete Slots |
| 7 | Bei positiver Rueckmeldung P1 starten | Lou + Rohde | Ethik, Daten, Validierungsprotokoll |

## 7. Was bewusst nicht behauptet wird

- Keine fertige Medizinprodukt-Zulassung.
- Keine Nutzung echter Patientendaten in der Demo.
- Keine Cloud-Inferenz fuer Patientendaten.
- Kein Versprechen, dass die Dissertation genau zwei Jahre dauert.
- Keine Behauptung, dass Aroob/Apo aktuell am Klinikum Dortmund angestellt ist.

## 8. Ein-Satz-Zusammenfassung

Carotis-AI ist jetzt ein technisch pruefbarer, local-first und erklaerbarer Promotionsprototyp; der naechste Schritt ist nicht mehr "bauen wir das?", sondern "ist Rohde bereit, die klinische Fragestellung und Validierung fachlich mitzutragen?"
