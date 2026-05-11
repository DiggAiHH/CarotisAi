/**
 * ResearchSplashGate — Pflicht-Bestätigungsdialog beim Start.
 *
 * Quelle: memory/domain/zweckbestimmung_master_2026-05-06.md §E
 * Audit anchor: 2026-05-10 disclaimer audit G1
 *
 * Verhalten:
 * - Pflicht-Klick vor AuthGate
 * - 3 erforderliche Checkboxen + "Ich bestätige" / "Abbrechen"
 * - Bestätigung in sessionStorage (Sitzungs-skopiert)
 * - POST /api/v1/audit/splash-confirmation mit version-Tag, ohne PII
 * - Abbrechen → Sitzung-Ende-Screen
 */

import { useCallback, useState } from "react";

const ZWECKBESTIMMUNG_VERSION = "zweckbestimmung_2026-05-06";
const SESSION_KEY = "carotis_splash_confirmed";
const SESSION_ID_KEY = "carotis_splash_session_id";
const ROLE_HASH_KEY = "carotis_splash_role_hash";

interface Props {
  children: React.ReactNode;
}

interface ConfirmationState {
  research_only: boolean;
  own_clinical_decision: boolean;
  no_diagnostic_record: boolean;
}

const INITIAL_STATE: ConfirmationState = {
  research_only: false,
  own_clinical_decision: false,
  no_diagnostic_record: false,
};

function generateSessionId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  // Fallback
  return `sess-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function getSessionScopedValue(key: string): string {
  try {
    const existing = sessionStorage.getItem(key);
    if (existing) return existing;
    const id = generateSessionId();
    sessionStorage.setItem(key, id);
    return id;
  } catch {
    return generateSessionId();
  }
}

export function ResearchSplashGate({ children }: Props) {
  const [confirmed, setConfirmed] = useState<boolean>(() => {
    try {
      return sessionStorage.getItem(SESSION_KEY) === ZWECKBESTIMMUNG_VERSION;
    } catch {
      return false;
    }
  });
  const [aborted, setAborted] = useState(false);
  const [checks, setChecks] = useState<ConfirmationState>(INITIAL_STATE);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const allChecked =
    checks.research_only && checks.own_clinical_decision && checks.no_diagnostic_record;

  const logConfirmation = useCallback(async () => {
    const baseUrl = import.meta.env.VITE_API_URL as string | undefined;
    if (!baseUrl) return; // backend missing — fail silently, do not block UX
    const sessionId = getSessionScopedValue(SESSION_ID_KEY);
    const roleHash = getSessionScopedValue(ROLE_HASH_KEY);
    try {
      await fetch(`${baseUrl}/api/v1/audit/splash-confirmation`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": (import.meta.env.VITE_API_KEY as string) ?? "",
        },
        body: JSON.stringify({
          session_id: sessionId,
          role_hash: roleHash,
          confirmed_at: new Date().toISOString(),
          version: ZWECKBESTIMMUNG_VERSION,
        }),
      });
    } catch {
      // Audit-Log-Failure darf UX nicht blockieren. Backend hat eigene Recovery.
    }
  }, []);

  const handleConfirm = async () => {
    if (!allChecked || submitting) return;
    setSubmitting(true);
    setError(null);
    try {
      await logConfirmation();
      sessionStorage.setItem(SESSION_KEY, ZWECKBESTIMMUNG_VERSION);
      setConfirmed(true);
    } catch {
      setError("Bestätigung konnte nicht protokolliert werden.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleAbort = () => {
    setAborted(true);
  };

  // Aborted view
  if (aborted) {
    return (
      <div className="h-screen flex items-center justify-center bg-slate-950 text-slate-100 p-6">
        <div className="max-w-md text-center space-y-4">
          <h1 className="text-xl font-semibold">Sitzung beendet</h1>
          <p className="text-sm text-slate-400">
            Sie haben die Forschungs-Bestätigung abgebrochen. Bitte schließen Sie das
            Fenster, um die Sitzung zu beenden.
          </p>
        </div>
      </div>
    );
  }

  // Bereits bestätigt — Kinder rendern
  if (confirmed) return <>{children}</>;

  // Bestätigungsdialog
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="splash-title"
      className="h-screen flex items-center justify-center bg-slate-950 text-slate-100 p-4 overflow-auto"
    >
      <div className="w-full max-w-2xl rounded-xl border border-amber-700/40 bg-slate-900 p-6 sm:p-8 shadow-2xl my-4">
        <div className="mb-4 inline-flex items-center gap-2 rounded-md bg-amber-500/10 px-3 py-1.5 text-xs font-medium text-amber-200 border border-amber-500/30">
          <span>RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt</span>
        </div>

        <h1 id="splash-title" className="text-xl sm:text-2xl font-semibold mb-3">
          Forschungs-Bestätigung
        </h1>

        <p className="text-sm sm:text-base text-slate-300 mb-5 leading-relaxed">
          Sie sind im Begriff, Carotis-AI zu starten — einen{" "}
          <strong>Forschungsprototyp</strong> zur Erfassung von Workflow- und
          Entscheidungspfad-Daten in der Carotis-CTA-Begutachtung.
        </p>

        <p className="text-sm font-medium text-slate-200 mb-3">
          Mit der Bestätigung erklären Sie:
        </p>

        <ul className="space-y-3 mb-6">
          <li>
            <label className="flex items-start gap-3 cursor-pointer group">
              <input
                type="checkbox"
                checked={checks.research_only}
                onChange={(e) =>
                  setChecks((c) => ({ ...c, research_only: e.target.checked }))
                }
                className="mt-1 h-4 w-4 rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500 focus:ring-offset-slate-900"
                aria-label="Punkt 1 bestätigen"
              />
              <span className="text-sm text-slate-300 group-hover:text-slate-100">
                1. Ich nutze dieses Werkzeug ausschließlich zu Forschungszwecken.
              </span>
            </label>
          </li>
          <li>
            <label className="flex items-start gap-3 cursor-pointer group">
              <input
                type="checkbox"
                checked={checks.own_clinical_decision}
                onChange={(e) =>
                  setChecks((c) => ({ ...c, own_clinical_decision: e.target.checked }))
                }
                className="mt-1 h-4 w-4 rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500 focus:ring-offset-slate-900"
                aria-label="Punkt 2 bestätigen"
              />
              <span className="text-sm text-slate-300 group-hover:text-slate-100">
                2. Ich treffe alle klinischen Entscheidungen eigenständig und stütze sie
                nicht auf die Ausgaben dieses Werkzeugs.
              </span>
            </label>
          </li>
          <li>
            <label className="flex items-start gap-3 cursor-pointer group">
              <input
                type="checkbox"
                checked={checks.no_diagnostic_record}
                onChange={(e) =>
                  setChecks((c) => ({ ...c, no_diagnostic_record: e.target.checked }))
                }
                className="mt-1 h-4 w-4 rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500 focus:ring-offset-slate-900"
                aria-label="Punkt 3 bestätigen"
              />
              <span className="text-sm text-slate-300 group-hover:text-slate-100">
                3. Ich werde keine Werkzeug-Ausgaben in Patientenakten als diagnostische
                Aussagen übernehmen.
              </span>
            </label>
          </li>
        </ul>

        {error && (
          <div
            role="alert"
            className="mb-3 rounded-md border border-red-600/40 bg-red-900/20 px-3 py-2 text-sm text-red-300"
          >
            {error}
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-3 sm:justify-end">
          <button
            type="button"
            onClick={handleAbort}
            className="rounded-md border border-slate-700 bg-slate-800 px-4 py-2 text-sm text-slate-200 hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500"
          >
            Abbrechen
          </button>
          <button
            type="button"
            onClick={handleConfirm}
            disabled={!allChecked || submitting}
            aria-disabled={!allChecked || submitting}
            className="rounded-md bg-amber-600 px-4 py-2 text-sm font-medium text-white hover:bg-amber-500 disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            {submitting ? "Wird protokolliert…" : "Ich bestätige"}
          </button>
        </div>

        <p className="mt-5 text-xs text-slate-500 leading-relaxed">
          Diese Bestätigung wird mit Zeitstempel und Sitzungs-ID lokal protokolliert.
          Keine Patientendaten oder personenbezogenen Daten werden übertragen. Version
          der Zweckbestimmung:{" "}
          <code className="text-slate-400">{ZWECKBESTIMMUNG_VERSION}</code>.
        </p>
      </div>
    </div>
  );
}
