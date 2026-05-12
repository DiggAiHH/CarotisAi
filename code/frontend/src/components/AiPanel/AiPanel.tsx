/**
 * Research results panel: attention overlay, confidence bucket, and model metadata.
 */
import { useStore } from "@/store";
import { t } from "@/lib/i18n";
import type { InferenceResponse } from "@/types";

interface Props {
  result?: InferenceResponse;
}

function focusTone(value: number) {
  if (value >= 0.7) {
    return {
      text: t("ai_panel.focusHigh"),
      color: "text-red-400",
      label: t("ai_panel.focusLabelStrong"),
      ring: "#f87171",
    };
  }
  if (value >= 0.5) {
    return {
      text: t("ai_panel.focusMedium"),
      color: "text-amber-400",
      label: t("ai_panel.focusLabelModerate"),
      ring: "#fbbf24",
    };
  }
  return {
    text: t("ai_panel.focusLow"),
    color: "text-emerald-400",
    label: t("ai_panel.focusLabelLow"),
    ring: "#34d399",
  };
}

function AttentionGauge({ value }: { value: number }) {
  const tone = focusTone(value);
  const degrees = Math.round(value * 360);

  return (
    <div className="relative mx-auto flex h-36 w-36 items-center justify-center rounded-full">
      <div
        className="absolute inset-0 rounded-full"
        style={{
          background: `conic-gradient(${tone.ring} ${degrees}deg, #1e293b 0deg)`,
        }}
      />
      <div className="absolute inset-3 rounded-full bg-slate-900" />
      <div className="relative text-center">
        <div className={`text-3xl font-bold tabular-nums ${tone.color}`}>
          {tone.text}
        </div>
        <div className="mt-1 text-[10px] uppercase tracking-[0.18em] text-slate-500">
          {t("ai_panel.fokus")}
        </div>
      </div>
    </div>
  );
}

export function AiPanel({ result }: Props) {
  const currentPrediction = useStore((s) => s.currentPrediction);
  const r = result ?? currentPrediction;

  if (!r) {
    return (
      <div className="p-4 text-sm text-slate-500">
        {t("ai_panel.noAnalysis")}
      </div>
    );
  }

  const focusValue = r.trust_score ?? 0.5;
  const tone = focusTone(focusValue);
  const activeTrustSegments =
    r.trust_score !== null
      ? Math.min(5, Math.max(0, Math.ceil(r.trust_score * 5)))
      : 0;
  const trustLabel =
    r.trust_score !== null
      ? r.trust_score < 0.55
        ? t("ai_panel.trustLow")
        : r.trust_score < 0.8
          ? t("ai_panel.trustModerate")
          : t("ai_panel.trustHigh")
      : null;
  const trustBgColor =
    r.trust_score !== null
      ? r.trust_score < 0.55
        ? "bg-red-500"
        : r.trust_score < 0.8
          ? "bg-amber-500"
          : "bg-emerald-500"
      : null;

  const bucketBadgeClass =
    r.confidence_bucket === "low"
      ? "bg-red-500/20 text-red-400"
      : r.confidence_bucket === "medium"
        ? "bg-amber-500/20 text-amber-400"
        : r.confidence_bucket === "high"
          ? "bg-emerald-500/20 text-emerald-400"
          : null;

  return (
    <div data-tour-id="tour-ai-panel" className="flex flex-col gap-4 rounded-lg border border-slate-700 bg-slate-900 p-4 shadow-xl shadow-black/20">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-emerald-400">
            {t("ai_panel.researchOverlay")}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {t("ai_panel.ctaNeckSynthetic")}
          </p>
        </div>
        <span className="rounded border border-amber-500/40 bg-amber-500/10 px-2 py-1 text-xs font-semibold text-amber-200">
          {t("ai_panel.researchOnly")}
        </span>
      </div>

      <div data-tour-id="tour-ai-overlay" className="rounded-lg bg-slate-950/70 p-4">
        <p className="mb-1 text-xs uppercase tracking-widest text-slate-500">
          {t("ai_panel.forschungsOverlay")}
        </p>
        <div className="grid grid-cols-[150px_1fr] items-center gap-4">
          <AttentionGauge value={focusValue} />
          <div>
            <span className={`text-sm font-medium ${tone.color}`}>
              {tone.label}
            </span>
            <p className="mt-2 text-xs leading-5 text-slate-400">
              {t("ai_panel.heatmapFocusText")}
            </p>
          </div>
        </div>
        <p className="mt-1 text-xs text-slate-500">
          {t("ai_panel.confidenceBucket")}:{" "}
          <span className="text-slate-300">
            {r.confidence_bucket ?? t("ai_panel.research")}
          </span>
          {bucketBadgeClass && (
            <span
              className={`ml-1.5 inline-block rounded px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${bucketBadgeClass}`}
            >
              {r.confidence_bucket}
            </span>
          )}{" "}
          - {t("ai_panel.model")}: <span className="text-slate-300">{r.model_version}</span>
        </p>
      </div>

      {trustLabel && trustBgColor && (
        <div data-tour-id="tour-ai-trust" className="rounded-lg bg-slate-700/50 p-3">
          <div className="mb-2 flex items-center justify-between">
            <span className="text-xs text-slate-400">{t("ai_panel.researchTrust")}</span>
            <span className={`text-sm font-bold ${tone.color}`}>{trustLabel}</span>
          </div>
          <div className="flex h-2 gap-1">
            {[1, 2, 3, 4, 5].map((segment) => (
              <div
                key={segment}
                className={`flex-1 rounded-sm transition-all ${
                  segment <= activeTrustSegments ? trustBgColor : "bg-slate-600"
                }`}
              />
            ))}
          </div>
          <div className="mt-2 flex flex-wrap gap-2">
            {bucketBadgeClass && (
              <span className={`rounded px-2 py-0.5 text-xs ${bucketBadgeClass}`}>
                {t("ai_panel.confidence")}: {r.confidence_bucket}
              </span>
            )}
            {r.calibrated && (
              <span className="rounded bg-emerald-500/20 px-2 py-0.5 text-xs text-emerald-400">
                {t("ai_panel.calibrated")}
              </span>
            )}
          </div>
        </div>
      )}

      <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-3">
        <p className="mb-2 text-xs uppercase tracking-widest text-amber-200">
          {t("ai_panel.decisionModuleDisabled")}
        </p>
        <p className="text-xs leading-5 text-slate-400">
          {t("ai_panel.decisionModuleText")}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-2">
        <button
          type="button"
          className="rounded border border-slate-700 bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-700"
        >
          {t("ai_panel.exportSnapshot")}
        </button>
        <button
          type="button"
          className="rounded border border-slate-700 bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-700"
        >
          {t("ai_panel.captureWorkflow")}
        </button>
      </div>

      <p className="break-all font-mono text-xs text-slate-600">
        {t("ai_panel.case")}: {r.case_id}
      </p>
    </div>
  );
}
