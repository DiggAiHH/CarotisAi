/**
 * Decision-Tree capture form — 30-second physician reasoning capture.
 *
 * Shows after AI result is displayed. Physician selects verdict,
 * optionally adjusts stenosis %, rates trust, notes deciding feature.
 * If physician disagrees with AI, structured override capture (CDSiC) is shown.
 */
import { useCallback, useEffect, useMemo, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { apiClient } from "@/lib/apiClient";
import { FreeTextField } from "@/components/FreeTextField";
import type {
  AgreementVerdict,
  ConfidenceLevel,
  DecisionTreeRequest,
  InferenceResponse,
  OverrideReason,
  ResearchMarkers,
  StenosisVerdict,
} from "@/types";

export type QuantitativeInferenceResponse = InferenceResponse & {
  stenosis_pct_nascet: number;
  confidence: number;
  vulnerability_markers: ResearchMarkers;
};

interface Props {
  result: QuantitativeInferenceResponse;
  physicianRoleHash: string;
  onSubmitted: () => void;
}

const VERDICT_LABELS: Record<AgreementVerdict, string> = {
  full_agreement: "Volle Uebereinstimmung",
  partial_agreement: "Teilweise Uebereinstimmung",
  disagreement: "Keine Uebereinstimmung",
  physician_override: "Arzt-Override",
};

const CONFIDENCE_LABELS: Record<ConfidenceLevel, string> = {
  low: "Niedrig",
  medium: "Mittel",
  high: "Hoch",
  very_high: "Sehr hoch",
};

const OVERRIDE_REASON_LABELS: Record<OverrideReason, string> = {
  patient_specific: "Patient-spezifische Umstaende",
  clinical_judgment: "Widerspruch zu klinischem Urteil",
  insufficient_evidence: "Unzureichende Evidenz",
  alert_fatigue: "Alert-Fatigue / irrelevant",
  other: "Sonstiger Grund",
};

function stenosisPctToVerdict(pct: number): StenosisVerdict {
  if (pct >= 99) return "critical";
  if (pct >= 70) return "severe";
  if (pct >= 50) return "moderate";
  if (pct >= 20) return "mild";
  return "normal";
}

/** True if the user-selected verdict indicates active disagreement / override. */
function isDisagreementVerdict(v: AgreementVerdict): boolean {
  return v === "disagreement" || v === "physician_override";
}

export function DecisionForm({ result, physicianRoleHash, onSubmitted }: Props) {
  const aiVerdict = useMemo(
    () => stenosisPctToVerdict(result.stenosis_pct_nascet),
    [result.stenosis_pct_nascet]
  );

  const [verdict, setVerdict] = useState<AgreementVerdict>("full_agreement");
  const [stenosisPct, setStenosisPct] = useState(result.stenosis_pct_nascet);
  const [confidence, setConfidence] = useState<ConfidenceLevel>("high");
  const [decidingFeature, setDecidingFeature] = useState("");
  const [trust, setTrust] = useState(3);

  // Per-case draft key to prevent cross-case leakage
  const draftKey = `dt:free_text_draft:${result.case_id}`;
  const [freeText, setFreeText] = useState(() =>
    localStorage.getItem(draftKey) || ""
  );
  const [hasPII, setHasPII] = useState(false);
  const [overrideHasPII, setOverrideHasPII] = useState(false);

  // Sync form state when a new case is loaded
  useEffect(() => {
    setStenosisPct(result.stenosis_pct_nascet);
    setVerdict("full_agreement");
    setConfidence("high");
    setDecidingFeature("");
    setTrust(3);
    setFreeText(localStorage.getItem(`dt:free_text_draft:${result.case_id}`) || "");
    setHasPII(false);
    setOverrideReason("clinical_judgment");
    setOverrideFreeText("");
    setOverrideHasPII(false);
  }, [result.case_id, result.stenosis_pct_nascet]);

  // --- Override / Disagreement state ---
  const [overrideReason, setOverrideReason] = useState<OverrideReason>("clinical_judgment");
  const [overrideFreeText, setOverrideFreeText] = useState("");

  const showDisagreement = isDisagreementVerdict(verdict);
  const physicianVerdict = stenosisPctToVerdict(stenosisPct);

  const mutation = useMutation({
    mutationFn: async (body: DecisionTreeRequest) => {
      try {
        return await apiClient.captureDecisionTree(body);
      } catch {
        // Demo / offline fallback: persist to localStorage so Rohde-Demo works without backend
        const savedKey = `dt:saved:${body.case_id}`;
        try {
          localStorage.setItem(savedKey, JSON.stringify(body));
        } catch { /* ignore quota errors */ }
        return { audit_id: `local-${Date.now()}`, status: "saved_locally" };
      }
    },
    onSuccess: () => {
      localStorage.removeItem(draftKey);
      onSubmitted();
    },
  });

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();

      const payload: DecisionTreeRequest = {
        case_id: result.case_id,
        captured_at: new Date().toISOString(),
        physician_role_hash: physicianRoleHash,
        ai_prediction: {
          stenosis_pct_nascet: result.stenosis_pct_nascet,
          confidence: result.confidence,
          vulnerability_markers: result.vulnerability_markers,
          model_version: result.model_version,
          model_sha: result.model_sha,
        },
        physician_decision: {
          stenosis_pct_nascet: stenosisPct,
          confidence_self_reported: confidence,
          confirmed_markers: [],
          rejected_markers: [],
          added_markers: [],
        },
        reasoning: {
          deciding_feature: decidingFeature || null,
          ruled_out: [],
          ruled_out_reason: null,
          would_consult: null,
          would_re_image_if: null,
          free_text_notes: freeText || null,
        },
        agreement_with_ai: {
          verdict,
          delta_pct: stenosisPct - result.stenosis_pct_nascet,
          delta_markers: [],
          trust_score_for_this_case: trust,
        },
        anonymisation: {
          method: "DICOM_PS_3.15_basic",
          salt_version: "v2026-04",
          audit_id: result.audit_id,
          k_anonymity_min: 5,
        },
      };

      if (showDisagreement) {
        payload.disagreement = {
          ai_verdict: aiVerdict,
          physician_verdict: physicianVerdict,
          override_reason: overrideReason,
          override_free_text: overrideFreeText || undefined,
        };
      }

      mutation.mutate(payload);
    },
    [
      mutation,
      result,
      physicianRoleHash,
      stenosisPct,
      verdict,
      confidence,
      decidingFeature,
      trust,
      freeText,
      showDisagreement,
      aiVerdict,
      physicianVerdict,
      overrideReason,
      overrideFreeText,
    ]
  );

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-xl border border-slate-700 bg-slate-800/60 p-5 flex flex-col gap-4"
    >
      <p className="text-sm font-semibold text-slate-200 uppercase tracking-wider">
        Aerztliche Einschaetzung
      </p>

      {/* AI Verdict hint */}
      <div className="flex items-center gap-2 text-xs text-slate-400">
        <span className="font-medium text-slate-300">Research-Referenz:</span>
        <span className="rounded bg-slate-700 px-2 py-0.5 text-slate-200">
          {result.stenosis_pct_nascet.toFixed(1)}% ({aiVerdict})
        </span>
      </div>

      {/* Verdict */}
      <div className="grid grid-cols-2 gap-2" role="radiogroup" aria-label="Uebereinstimmung mit KI">
        {(Object.keys(VERDICT_LABELS) as AgreementVerdict[]).map((v) => (
          <button
            key={v}
            type="button"
            role="radio"
            aria-checked={verdict === v}
            onClick={() => setVerdict(v)}
            className={[
              "rounded-lg border px-3 py-2 text-xs text-left transition-colors",
              verdict === v
                ? "border-cyan-500 bg-cyan-900/40 text-cyan-300"
                : "border-slate-600 text-slate-400 hover:border-slate-400",
            ].join(" ")}
          >
            {VERDICT_LABELS[v]}
          </button>
        ))}
      </div>

      {/* Physician stenosis estimate */}
      <div className="flex items-center gap-3">
        <label className="text-xs text-slate-400 w-48 shrink-0">
          Eigene Workflow-Einschaetzung
        </label>
        <input
          type="number"
          min={0}
          max={100}
          step={0.5}
          value={stenosisPct}
          onChange={(e) => setStenosisPct(Number(e.target.value))}
          className="w-24 rounded-lg bg-slate-700 px-3 py-1.5 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
        <span className="text-xs text-slate-500">
          Differenz {(stenosisPct - result.stenosis_pct_nascet).toFixed(1)}
        </span>
      </div>

      {/* Confidence */}
      <div className="flex items-center gap-3">
        <label className="text-xs text-slate-400 w-48 shrink-0">
          Eigene Konfidenz
        </label>
        <select
          value={confidence}
          onChange={(e) => setConfidence(e.target.value as ConfidenceLevel)}
          className="rounded-lg bg-slate-700 px-3 py-1.5 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        >
          {(Object.keys(CONFIDENCE_LABELS) as ConfidenceLevel[]).map((c) => (
            <option key={c} value={c}>
              {CONFIDENCE_LABELS[c]}
            </option>
          ))}
        </select>
      </div>

      {/* Deciding feature */}
      <div className="flex items-center gap-3">
        <label className="text-xs text-slate-400 w-48 shrink-0">
          Entscheidendes Merkmal
        </label>
        <input
          type="text"
          value={decidingFeature}
          onChange={(e) => setDecidingFeature(e.target.value)}
          placeholder="z.B. Plaque-Morphologie, Gefaesslumen"
          className="flex-1 rounded-lg bg-slate-700 px-3 py-1.5 text-sm text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        />
      </div>

      {/* Trust score */}
      <div className="flex items-center gap-3">
        <label className="text-xs text-slate-400 w-48 shrink-0">
          KI-Vertrauen (1-5)
        </label>
        <div className="flex gap-1" role="radiogroup" aria-label="KI-Vertrauen">
          {[1, 2, 3, 4, 5].map((n) => (
            <button
              key={n}
              type="button"
              role="radio"
              aria-checked={trust === n}
              onClick={() => setTrust(n)}
              className={[
                "h-8 w-8 rounded-lg text-sm font-medium transition-colors",
                trust === n
                  ? "bg-cyan-600 text-white"
                  : "bg-slate-700 text-slate-400 hover:bg-slate-600",
              ].join(" ")}
            >
              {n}
            </button>
          ))}
        </div>
      </div>

      {/* Free text notes */}
      <FreeTextField value={freeText} onChange={setFreeText} onPIIStatusChange={setHasPII} />

      {/* --- Disagreement / Override block (conditional) --- */}
      {showDisagreement && (
        <div className="rounded-lg border border-amber-600/40 bg-amber-900/20 p-4 flex flex-col gap-3">
          <p className="text-xs font-semibold text-amber-300 uppercase tracking-wider">
            Override-Begruendung (CDSiC)
          </p>

          <div className="flex items-center gap-2 text-xs text-slate-400">
            <span>KI:</span>
            <span className="rounded bg-slate-700 px-1.5 py-0.5 text-slate-200">{aiVerdict}</span>
            <span className="text-slate-500">-&gt;</span>
            <span>Arzt:</span>
            <span className="rounded bg-slate-700 px-1.5 py-0.5 text-slate-200">{physicianVerdict}</span>
          </div>

          <div className="flex items-center gap-3">
            <label className="text-xs text-slate-400 w-48 shrink-0">
              Grund fuer Override
            </label>
            <select
              value={overrideReason}
              onChange={(e) => setOverrideReason(e.target.value as OverrideReason)}
              className="flex-1 rounded-lg bg-slate-700 px-3 py-1.5 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-amber-500"
            >
              {(Object.keys(OVERRIDE_REASON_LABELS) as OverrideReason[]).map((r) => (
                <option key={r} value={r}>
                  {OVERRIDE_REASON_LABELS[r]}
                </option>
              ))}
            </select>
          </div>

          <FreeTextField
            value={overrideFreeText}
            onChange={setOverrideFreeText}
            onPIIStatusChange={setOverrideHasPII}
            maxLength={500}
            placeholder="Optionale Begruendung (max. 500 Zeichen)"
          />
        </div>
      )}

      <button
        type="submit"
        disabled={mutation.isPending || hasPII || (showDisagreement && overrideHasPII)}
        className="mt-1 self-end rounded-lg bg-cyan-600 px-6 py-2 text-sm font-medium text-white hover:bg-cyan-500 disabled:opacity-50 transition-colors"
      >
        {mutation.isPending
          ? "Wird gespeichert ..."
          : hasPII || (showDisagreement && overrideHasPII)
          ? "PII entfernen um zu speichern"
          : "Einschaetzung speichern"}
      </button>

      {mutation.isError && (
        <p className="text-xs text-red-400">
          {mutation.error instanceof Error
            ? mutation.error.message
            : "Fehler beim Speichern"}
        </p>
      )}
      {mutation.isSuccess && (
        <p className="text-xs text-emerald-400">
          Gespeichert ✓{" "}
          {(mutation.data as { status?: string } | undefined)?.status === "saved_locally" && (
            <span className="text-slate-500">(lokal gespeichert — kein Netzwerk)</span>
          )}
        </p>
      )}
    </form>
  );
}
