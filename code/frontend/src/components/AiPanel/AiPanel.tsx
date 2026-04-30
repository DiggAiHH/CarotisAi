/**
 * AI results panel — stenosis %, confidence bar, vulnerability markers.
 */
import { useStore } from "@/store";
import type { InferenceResponse, VulnerabilityMarkers } from "@/types";

interface Props {
  result?: InferenceResponse;
}

const MARKER_TOOLTIPS: Record<keyof VulnerabilityMarkers, string> = {
  intraplaque_hemorrhage:
    "Blutung innerhalb der Plaque — starker Prädiktor für zerebrale Embolien",
  thin_fibrous_cap:
    "Kapseldicke < 65 µm — erhöhtes Rupturrisiko",
  lipid_rich_necrotic_core:
    "Nekrotischer Lipidkern > 40 % der Plaque — destabilisierend",
  systolic_motion_anomaly:
    "Wandbewegungsstörung in der Systole — Hinweis auf Plaque-Instabilität",
};

function MarkerRow({
  label,
  value,
  tooltip,
}: {
  label: string;
  value: number;
  tooltip: string;
}) {
  const pct = Math.round(value * 100);
  const activeSegments = Math.min(3, Math.max(0, Math.ceil(value * 3)));
  const colorClass =
    pct >= 70 ? "bg-red-500" : pct >= 40 ? "bg-amber-500" : "bg-emerald-500";

  return (
    <div className="group relative flex items-center gap-3">
      <span className="xl:w-52 w-36 shrink-0 text-sm text-slate-300 truncate">
        {label}
      </span>
      <div className="flex gap-1 h-2 flex-1">
        {[1, 2, 3].map((segment) => (
          <div
            key={segment}
            className={`flex-1 rounded-sm transition-all ${
              segment <= activeSegments ? colorClass : "bg-slate-700"
            }`}
          />
        ))}
      </div>
      <span className="w-10 text-right text-xs text-slate-400 tabular-nums">
        {pct}%
      </span>

      {/* Tooltip */}
      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 hidden group-hover:block bg-slate-900 text-slate-200 text-xs rounded px-2 py-1 whitespace-nowrap z-10 shadow-lg border border-slate-700 pointer-events-none">
        {tooltip}
        <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-px border-4 border-transparent border-t-slate-900" />
      </div>
    </div>
  );
}

const MARKER_LABELS: Record<keyof VulnerabilityMarkers, string> = {
  intraplaque_hemorrhage: "Intraplaque-Haemorrhagie",
  thin_fibrous_cap: "Duenne Fibrokapsel",
  lipid_rich_necrotic_core: "Lipidreicher Kern (LRNC)",
  systolic_motion_anomaly: "Systolische Bewegungsanomalie",
};

export function AiPanel({ result }: Props) {
  const currentPrediction = useStore((s) => s.currentPrediction);
  const r = result ?? currentPrediction;

  if (!r) {
    return (
      <div className="text-slate-500 text-sm p-4">
        Keine Vorhersage vorhanden. Laden Sie einen DICOM-Fall hoch.
      </div>
    );
  }

  const severityColor =
    r.stenosis_pct_nascet >= 70
      ? "text-red-400"
      : r.stenosis_pct_nascet >= 50
        ? "text-amber-400"
        : "text-emerald-400";

  const severityLabel =
    r.stenosis_pct_nascet >= 70
      ? "Hochgradig"
      : r.stenosis_pct_nascet >= 50
        ? "Mittelgradig"
        : "Niedriggradig";

  const trustPercent =
    r.trust_score !== null ? Math.round(r.trust_score * 100) : null;
  const activeTrustSegments =
    r.trust_score !== null
      ? Math.min(5, Math.max(0, Math.ceil(r.trust_score * 5)))
      : 0;
  const trustColor =
    r.trust_score !== null
      ? r.trust_score < 0.55
        ? "text-red-400"
        : r.trust_score < 0.8
          ? "text-amber-400"
          : "text-emerald-400"
      : null;
  const trustBgColor =
    r.trust_score !== null
      ? r.trust_score < 0.55
        ? "bg-red-500"
        : r.trust_score < 0.8
          ? "bg-amber-500"
          : "bg-emerald-500"
      : null;
  const trustLabel =
    r.trust_score !== null
      ? r.trust_score < 0.55
        ? "Niedrig"
        : r.trust_score < 0.8
          ? "Moderat"
          : "Hoch"
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
    <div className="rounded-xl bg-slate-800 xl:p-5 p-3 flex flex-col xl:gap-5 gap-3">
      {/* Stenosis headline */}
      <div>
        <p className="text-xs uppercase tracking-widest text-slate-500 mb-1">
          NASCET-Stenose
        </p>
        <div className="flex items-baseline gap-2">
          <span
            className={`xl:text-5xl text-4xl font-bold tabular-nums ${severityColor}`}
          >
            {r.stenosis_pct_nascet.toFixed(1)}%
          </span>
          <span className={`text-sm font-medium ${severityColor}`}>
            {severityLabel}
          </span>
        </div>
        <p className="mt-1 text-xs text-slate-500">
          Konfidenz:{" "}
          <span className="text-slate-300">
            {Math.round(r.confidence * 100)}%
          </span>
          {bucketBadgeClass && (
            <span
              className={`ml-1.5 inline-block rounded px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${bucketBadgeClass}`}
            >
              {r.confidence_bucket}
            </span>
          )}{" "}
          · Modell: <span className="text-slate-300">{r.model_version}</span>
        </p>
      </div>

      {/* Trust-Score Section */}
      {trustPercent !== null && trustColor && trustBgColor && trustLabel && (
        <div className="rounded-lg bg-slate-700/50 p-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">KI-Vertrauen</span>
            <span className={`text-sm font-bold ${trustColor}`}>
              {trustPercent}% — {trustLabel}
            </span>
          </div>

          {/* Segmented bar instead of continuous */}
          <div className="flex gap-1 h-2">
            {[1, 2, 3, 4, 5].map((segment) => (
              <div
                key={segment}
                className={`flex-1 rounded-sm transition-all ${
                  segment <= activeTrustSegments ? trustBgColor : "bg-slate-600"
                }`}
              />
            ))}
          </div>

          {/* Confidence bucket badge */}
          <div className="mt-2 flex gap-2 flex-wrap">
            {bucketBadgeClass && (
              <span
                className={`text-xs px-2 py-0.5 rounded ${bucketBadgeClass}`}
              >
                Konfidenz: {r.confidence_bucket}
              </span>
            )}
            {r.calibrated && (
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
                Kalibriert
              </span>
            )}
          </div>
        </div>
      )}

      {/* Vulnerability markers */}
      <div>
        <p className="text-xs uppercase tracking-widest text-slate-500 mb-3">
          Vulnerabilitaetsmarker
        </p>
        <div className="flex flex-col gap-2">
          {(
            Object.entries(r.vulnerability_markers) as [
              keyof VulnerabilityMarkers,
              number,
            ][]
          ).map(([key, val]) => (
            <MarkerRow
              key={key}
              label={MARKER_LABELS[key]}
              value={val}
              tooltip={MARKER_TOOLTIPS[key]}
            />
          ))}
        </div>
      </div>

      {/* Case ID (anonymised) */}
      <p className="text-xs text-slate-600 break-all font-mono">
        Case: {r.case_id}
      </p>
    </div>
  );
}
