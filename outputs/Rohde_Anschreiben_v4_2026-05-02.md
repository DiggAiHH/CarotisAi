# Entwurf: Anschreiben an Prof. Rohde - Version 4

Betreff: Promotionsvorhaben Carotis-AI - kurze fachliche Einschaetzung und Demo

Sehr geehrter Herr Prof. Rohde,

ich hoffe, es geht Ihnen gut.

Ich moechte Ihnen ein Promotionsvorhaben vorstellen, das aus meiner frueheren klinischen Erfahrung im Umfeld des Klinikums Dortmund und meiner aktuellen Arbeit im KI-/Technologieumfeld entstanden ist. Aktuell arbeite ich bei NVIDIA; der Bezug zu Dortmund und zu Ihrem neuroradiologischen Workflow ist fuer mich aber weiterhin fachlich praegend.

Gemeinsam mit Laith Alshdaifat haben wir in den letzten Tagen einen ersten, lokal betriebenen Prototypen fuer die CTA-basierte Beurteilung von Carotis-Stenosen aufgebaut. Das Projekt heisst **Carotis-AI** und verbindet vier Punkte:

1. Quantifizierung des Stenosegrades aus CTA-Bildern,
2. Analyse von Plaque-Vulnerability-Merkmalen,
3. erklaerbare KI-Ausgaben ueber Heatmaps und strukturierte Begruendungen,
4. ein Decision-Tree-Harvesting-Ansatz, bei dem aerztliche Entscheidungen und Overrides systematisch dokumentiert werden.

Wichtig ist uns: Die Demo verwendet keine echten Patientendaten. Die spaetere Zielarchitektur ist local-first gedacht, also ohne Cloud-Upload sensibler Bilddaten.

Der aktuelle Prototyp ist bereits online pruefbar:

`https://api.carotis.diggai.de/`

Der Link ist im Moment bewusst als technischer Demo-Fallback unter der API-Subdomain erreichbar, weil die Hauptdomain noch von Fly.io auf Hetzner umgestellt werden muss. Inhaltlich ist die Demo aber nutzbar: Frontend, Backend-Health und ein visueller Smoke-Test sind geprueft.

Meine Bitte waere nicht, dass Sie jetzt sofort eine Betreuung zusagen. Mir waere zunaechst Ihre fachliche Einschaetzung wichtig:

- Ist die Fragestellung aus Ihrer Sicht klinisch relevant?
- Waere ein fokussiertes Promotionsprojekt in diesem Bereich sinnvoll?
- Welche Endpunkte und welche Datenbasis waeren aus neuroradiologischer Sicht tragfaehig?
- Sollte der Schwerpunkt eher auf diagnostischer Genauigkeit, Plaque-Risiko, Erklaerbarkeit oder klinischem Workflow liegen?

Mir ist auch wichtig, den Umfang realistisch zu halten. Die Promotion muss nicht zwingend als zweijaehriges Grossprojekt angelegt werden. Je nach Datenzugang, Ethikprozess und Zielsetzung koennte eine fokussierte Arbeit auch kuerzer strukturiert werden, zum Beispiel als retrospektive Validierungs- und Machbarkeitsstudie mit klar begrenzter Fragestellung. Eine spaetere Produktzulassung waere davon getrennt zu betrachten.

Wenn Sie offen dafuer sind, wuerden wir Ihnen gern in einem kurzen 30-Minuten-Termin die Demo und die geplante Roadmap zeigen. Danach koennten wir gemeinsam entscheiden, ob und in welcher Form das als Promotionsprojekt unter Ihrer fachlichen Begleitung Sinn ergibt.

Mit freundlichen Gruessen

Aroob/Apo  

Anlagen / Links fuer den Termin:

- Demo-Link: `https://api.carotis.diggai.de/`
- Kurzpraesentation: Carotis-AI Rohde v4
- Roadmap: P0 bis P6, mit schlankem Promotionspfad

## Interne Hinweise vor Versand

- Namen final klaeren: Aroob oder Apo, akademischer Titel, aktuelle Signatur.
- NVIDIA-Rolle exakt so formulieren, wie sie beruflich korrekt ist.
- Keine Behauptung einer aktuellen Anstellung am Klinikum Dortmund.
- Demo-Link kurz vor Versand erneut testen.
- Falls Hauptdomain korrigiert wird, Link auf `https://carotis.diggai.de/` ersetzen.
- Ton ruhig halten: keine Uebertreibung, keine "fertige Medizinsoftware".
