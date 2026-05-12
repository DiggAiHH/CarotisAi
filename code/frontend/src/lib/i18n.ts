/**
 * Minimal i18n dictionary for Carotis-AI frontend.
 *
 * No heavy i18n library — just a typed key-value map.
 * All UI text is in GERMAN per project spec.
 */

export const de = {
  // App / Layout
  "app.title": "Carotis-AI",
  "app.subtitle": "Klinikum Dortmund",
  "app.online": "Online",
  "app.offline": "Offline",
  "app.cases": "Faelle",
  "app.casesPlaceholder": "Patientenliste wird hier angezeigt...",
  "app.logout": "Abmelden",
  "app.dicomTab": "DICOM",
  "app.overlayTab": "Overlay",
  "app.carotisAI": "Carotis AI",
  "app.workflowCapture": "Workflow Capture",
  "app.version": "v0.1 Demo",
  "app.searchCases": "Forschungsfaelle suchen...",
  "app.researchCases": "Forschungsfaelle",
  "app.records": "records",
  "app.syntheticTestData": "Synthetische Testdaten",
  "app.downloadDicom": "Ausgewaehltes DICOM herunterladen",
  "app.demoFilesNote": "Demo-Dateien sind generierte, anonymisierte DICOMs. Keine Patientendaten.",
  "app.workflowCaptureMode": "Workflow-Capture im Forschungsmodus",
  "app.workflowCaptureDesc":
    "Entscheidungsunterstuetzende Module sind deaktiviert. Fuer diesen Demonstrationsstand werden nur Overlay-, Konfidenz- und Workflow-Daten angezeigt.",

  // DICOM Viewer
  "viewer.dropHere": "DICOM-Datei hierher ziehen",
  "viewer.orSelect": "oder Datei auswaehlen",
  "viewer.selectFile": "Datei auswaehlen",
  "viewer.heatmap": "Heatmap",
  "viewer.demoBanner": "Demo · Nur Forschungsprototyp · Kein Medizinprodukt",
  "viewer.heatmapOn": "AN",
  "viewer.heatmapOff": "AUS",
  "viewer.softTissue": "Soft Tissue",
  "viewer.bone": "Bone",
  "viewer.vessel": "Vessel",
  "viewer.dob": "DOB: synthetic",
  "viewer.study": "Study",
  "viewer.ctaNeckAxial": "CTA Neck · Axial",
  "viewer.ww": "WW",
  "viewer.wl": "WL",
  "viewer.zoom": "Zoom",
  "viewer.slice": "Slice",
  "viewer.thickness": "Thickness",
  "viewer.fov": "FOV",
  "viewer.overlayFocus": "Overlay-Fokus",
  "viewer.focusHigh": "hoch",
  "viewer.focusModerate": "moderat",
  "viewer.focusLow": "niedrig",
  "viewer.confidenceHigh": "hohe Konfidenz",
  "viewer.confidenceMedium": "mittlere Konfidenz",
  "viewer.confidenceLow": "niedrige Konfidenz",
  "viewer.syntheticPreview":
    "Synthetische CTA-Vorschau. Upload nutzt echte DICOM-Inferenz.",
  "viewer.heatmapOpacityHigh": "hoch",
  "viewer.heatmapOpacityMedium": "mittel",
  "viewer.heatmapOpacityLow": "niedrig",
  "viewer.ariaLabel": "DICOM-Datei hier ablegen oder auswaehlen",

  // AI Panel
  "ai_panel.noAnalysis": "Keine Analyse vorhanden. Laden Sie einen DICOM-Fall hoch.",
  "ai_panel.researchOverlay": "Forschungsmodus",
  "ai_panel.ctaNeckSynthetic": "CTA Hals — synthetische Demo",
  "ai_panel.researchOnly": "Nur Forschung",
  "ai_panel.forschungsOverlay": "Forschungs-Overlay",
  "ai_panel.focusHigh": "Hoch",
  "ai_panel.focusMedium": "Mittel",
  "ai_panel.focusLow": "Niedrig",
  "ai_panel.focusLabelStrong": "Starker Overlay-Fokus",
  "ai_panel.focusLabelModerate": "Moderater Overlay-Fokus",
  "ai_panel.focusLabelLow": "Niedriger Overlay-Fokus",
  "ai_panel.fokus": "Fokus",
  "ai_panel.heatmapFocusText":
    "Heatmap-Fokus liegt auf einer synthetischen ROI. Das Overlay ist keine quantitative Messung und keine klinische Entscheidungsgrundlage.",
  "ai_panel.confidenceBucket": "Konfidenz-Bucket",
  "ai_panel.research": "research",
  "ai_panel.model": "Modell",
  "ai_panel.researchTrust": "Forschungs-Vertrauen",
  "ai_panel.trustLow": "Niedrig",
  "ai_panel.trustModerate": "Moderat",
  "ai_panel.trustHigh": "Hoch",
  "ai_panel.confidence": "Konfidenz",
  "ai_panel.calibrated": "Kalibriert",
  "ai_panel.decisionModuleDisabled": "Entscheidungsmodul deaktiviert",
  "ai_panel.decisionModuleText":
    "Der Forschungsbuild zeigt keine Lumenwerte, keine Therapieempfehlung und keine klinische Entscheidungsgrundlage.",
  "ai_panel.exportSnapshot": "Snapshot exportieren",
  "ai_panel.captureWorkflow": "Workflow erfassen",
  "ai_panel.case": "Fall",

  // Decision Form
  "decision_form.title": "Aerztliche Einschaetzung",
  "decision_form.aiVerdict": "Research-Referenz",
  "decision_form.verdictAgreement": "Uebereinstimmung mit KI",
  "decision_form.ownEstimate": "Eigene Workflow-Einschaetzung",
  "decision_form.difference": "Differenz",
  "decision_form.ownConfidence": "Eigene Konfidenz",
  "decision_form.decidingFeature": "Entscheidendes Merkmal",
  "decision_form.decidingFeaturePlaceholder":
    "z.B. Plaque-Morphologie, Gefaesslumen",
  "decision_form.trustScore": "KI-Vertrauen (1-5)",
  "decision_form.trustAriaLabel": "KI-Vertrauen",
  "decision_form.overrideTitle": "Override-Begruendung (CDSiC)",
  "decision_form.aiLabel": "KI",
  "decision_form.physicianLabel": "Arzt",
  "decision_form.arrow": "->",
  "decision_form.overrideReason": "Grund fuer Override",
  "decision_form.overridePlaceholder":
    "Optionale Begruendung (max. 500 Zeichen)",
  "decision_form.saving": "Wird gespeichert ...",
  "decision_form.removePII": "PII entfernen um zu speichern",
  "decision_form.save": "Einschaetzung speichern",
  "decision_form.saveError": "Fehler beim Speichern",
  "decision_form.saved": "Gespeichert ✓",
  "decision_form.savedLocally": "(lokal gespeichert — kein Netzwerk)",

  // Verdict labels
  "verdict.full_agreement": "Volle Uebereinstimmung",
  "verdict.partial_agreement": "Teilweise Uebereinstimmung",
  "verdict.disagreement": "Keine Uebereinstimmung",
  "verdict.physician_override": "Arzt-Override",

  // Confidence level labels
  "confidence_level.low": "Niedrig",
  "confidence_level.medium": "Mittel",
  "confidence_level.high": "Hoch",
  "confidence_level.very_high": "Sehr hoch",

  // Override reason labels
  "override_reason.patient_specific": "Patient-spezifische Umstaende",
  "override_reason.clinical_judgment": "Widerspruch zu klinischem Urteil",
  "override_reason.insufficient_evidence": "Unzureichende Evidenz",
  "override_reason.alert_fatigue": "Alert-Fatigue / irrelevant",
  "override_reason.other": "Sonstiger Grund",

  // Confidence Badge
  "confidence.niedrig": "Niedrig",
  "confidence.mittel": "Mittel",
  "confidence.hoch": "Hoch",
  "confidence.calibratedTooltip": "Kalibrierte Konfidenz",
  "confidence.rawTooltip": "Roh-Konfidenz",
  "confidence.calAbbrev": "kal.",
  "confidence.barLabel": "Konfidenz",
  "confidence.warningTitle": "AI-Konfidenz niedrig",
  "confidence.warningText":
    "Bitte sorgfaeltige manuelle Pruefung durchfuehren.",

  // Free Text Field
  "freetext.label": "Was ist offen / unsicher?",
  "freetext.optional": "(optional)",
  "freetext.checking": "pruefe...",
  "freetext.piiFound": "Moegliche personenbezogene Daten gefunden:",
  "freetext.rephrase":
    "Bitte umformulieren — wir koennen den Eintrag sonst nicht speichern.",

  // Walkthrough
  "tour.step1Title": "Willkommen bei Carotis-AI",
  "tour.step1Desc":
    "Diese 5-Schritt-Tour zeigt die wichtigsten Funktionen des Forschungsprototyps. Carotis-AI ist ein lokales, erklaerbares Workflow-Capture-System fuer Carotis-CTA-Forschung.",
  "tour.step2Title": "DICOM-Upload",
  "tour.step2Desc":
    "Laden Sie eine DICOM-Datei per Drag & Drop oder Dateiauswahl. Alle Daten verarbeiten sich lokal auf Ihrem Geraet — keine Daten verlassen das Klinikum.",
  "tour.step3Title": "KI-Analyse",
  "tour.step3Desc":
    "Das Forschungs-Overlay zeigt Aufmerksamkeitsbereiche, Konfidenz und Workflow-Metadaten. Der Trust-Score ist eine Forschungsmetrik, keine klinische Empfehlung.",
  "tour.step4Title": "XAI-Erklaerbarkeit",
  "tour.step4Desc":
    "Nach der Analyse zeigt HiResCAM pixelgenau, welche Regionen das Modell fuer die Entscheidung herangezogen hat. Die Heatmap-Transparenz ist ueber den Schieberegler einstellbar.",
  "tour.step5Title": "Decision-Tree-Harvesting",
  "tour.step5Desc":
    "Nach der Analyse wird die aerztliche Begruendung anonymisiert erfasst und fliesst in den Daily-Learning-Corpus ein. Damit lernt das Modell nicht nur das Bild, sondern die aerztliche Entscheidung.",
  "tour.next": "Weiter",
  "tour.back": "Zurueck",
  "tour.skip": "Ueberspringen",
  "tour.finish": "Tour beenden",
  "tour.progress": "Schritt {current} von {total}",
  "tour.restart": "? Tour",

  // Error Boundary
  "error.title": "Fehler aufgetreten",
  "error.description":
    "Ein unerwarteter Fehler ist aufgetreten. Bitte laden Sie die Seite neu.",
  "error.reload": "Seite neu laden",

  // Status badges
  "status.uploading": "Wird hochgeladen...",
  "status.analysing": "KI analysiert...",
  "status.done": "Analyse abgeschlossen",
  "status.error": "Fehler bei der Analyse",
  "status.unknownError": "Unbekannter Fehler",
} as const;

export type I18nKey = keyof typeof de;

/**
 * Translate a key into its German string.
 *
 * Falls back to the raw key + console.warn when a translation is missing.
 */
export function t(
  key: I18nKey | string,
  replacements?: Record<string, string | number>,
): string {
  const dict = de as unknown as Record<string, string | undefined>;
  let text = dict[key];
  if (text === undefined) {
    console.warn("missing-i18n-key", key);
    return key;
  }
  if (replacements) {
    for (const [k, v] of Object.entries(replacements)) {
      text = text.replaceAll(`{${k}}`, String(v));
    }
  }
  return text;
}
