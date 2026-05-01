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

  // DICOM Viewer
  "viewer.dropHere": "DICOM-Datei hierher ziehen",
  "viewer.orSelect": "oder Datei auswaehlen",
  "viewer.selectFile": "Datei auswaehlen",
  "viewer.heatmap": "Heatmap",

  // AI Panel
  "panel.noPrediction": "Keine Vorhersage vorhanden. Laden Sie einen DICOM-Fall hoch.",
  "panel.nascetStenosis": "NASCET-Stenose",
  "panel.severity.low": "Niedriggradig",
  "panel.severity.moderate": "Mittelgradig",
  "panel.severity.high": "Hochgradig",
  "panel.confidence": "Konfidenz",
  "panel.modelVersion": "Modell",
  "panel.trustScore": "KI-Vertrauen",
  "panel.trust.low": "Niedrig",
  "panel.trust.moderate": "Moderat",
  "panel.trust.high": "Hoch",
  "panel.vulnerabilityMarkers": "Vulnerabilitaetsmarker",
  "panel.calibrated": "Kalibriert",
  "panel.caseId": "Case",

  // Decision Form
  "form.title": "Aerztliche Einschaetzung",
  "form.aiVerdict": "KI-Einschaetzung",
  "form.fullAgreement": "Volle Uebereinstimmung",
  "form.partialAgreement": "Teilweise Uebereinstimmung",
  "form.disagreement": "Keine Uebereinstimmung",
  "form.physicianOverride": "Arzt-Override",
  "form.stenosisEstimate": "Eigene Stenose-Schaetzung (%)",
  "form.confidence": "Eigene Konfidenz",
  "form.decidingFeature": "Entscheidendes Merkmal",
  "form.decidingFeaturePlaceholder": "z.B. Plaque-Morphologie, Gefaesslumen",
  "form.trustScore": "KI-Vertrauen (1-5)",
  "form.freeTextLabel": "Was ist offen / unsicher?",
  "form.freeTextOptional": "(optional)",
  "form.freeTextHint":
    "Was ist offen oder unsicher? Was wuerdest du noch klaeren? Keine Patientennamen — wir filtern automatisch und lehnen den Eintrag ab, wenn welche drin sind.",
  "form.overrideTitle": "Override-Begruendung (CDSiC)",
  "form.overrideReason": "Grund fuer Override",
  "form.submit": "Einschaetzung speichern",
  "form.submitting": "Wird gespeichert ...",
  "form.saved": "Gespeichert ✓",
  "form.error": "Fehler beim Speichern",
  "form.nextCaseHint": "Laden Sie einen neuen Fall hoch, um fortzufahren.",

  // Confidence Badge
  "badge.low": "Niedrig",
  "badge.medium": "Mittel",
  "badge.high": "Hoch",
  "badge.calibrated": "Kalibrierte Konfidenz",
  "badge.raw": "Roh-Konfidenz",
  "badge.cal": "kal.",
  "warning.lowConfidence": "AI-Konfidenz niedrig",
  "warning.checkManually": "Bitte sorgfaeltige manuelle Pruefung durchfuehren.",

  // Free Text Field
  "freetext.checking": "pruefe...",
  "freetext.piiFound": "Moegliche personenbezogene Daten gefunden:",
  "freetext.rephrase":
    "Bitte umformulieren — wir koennen den Eintrag sonst nicht speichern.",

  // Walkthrough
  "tour.step1Title": "Willkommen bei Carotis-AI",
  "tour.step1Desc":
    "Diese 5-Schritt-Tour zeigt Ihnen die wichtigsten Funktionen des Systems. Carotis-AI ist ein lokales, erklaerbares KI-System zur Carotis-Stenose-Diagnostik.",
  "tour.step2Title": "DICOM-Upload",
  "tour.step2Desc":
    "Laden Sie eine DICOM-Datei per Drag & Drop oder Dateiauswahl. Alle Daten verarbeiten sich lokal auf Ihrem Geraet — keine Daten verlassen das Klinikum.",
  "tour.step3Title": "KI-Analyse",
  "tour.step3Desc":
    "Das MFSD-UNet-Modell quantifiziert die Stenose nach NASCET und zeigt Konfidenz sowie Vulnerability-Marker. Der Trust-Score zeigt, wie sehr das Modell seiner eigenen Einschaetzung vertraut.",
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
  "error.description": "Ein unerwarteter Fehler ist aufgetreten. Bitte laden Sie die Seite neu.",
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
 */
export function t(key: I18nKey, replacements?: Record<string, string | number>): string {
  let text: string = de[key];
  if (replacements) {
    for (const [k, v] of Object.entries(replacements)) {
      text = text.replaceAll(`{${k}}`, String(v));
    }
  }
  return text;
}
