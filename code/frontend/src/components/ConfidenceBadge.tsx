import React from "react";

interface ConfidenceBadgeProps {
  confidence: number;
  bucket: string;
  calibrated?: boolean;
}

const bucketConfig: Record<string, { label: string; bg: string; text: string; border: string }> = {
  low: {
    label: "Niedrig",
    bg: "bg-red-50",
    text: "text-red-700",
    border: "border-red-200",
  },
  medium: {
    label: "Mittel",
    bg: "bg-yellow-50",
    text: "text-yellow-700",
    border: "border-yellow-200",
  },
  high: {
    label: "Hoch",
    bg: "bg-green-50",
    text: "text-green-700",
    border: "border-green-200",
  },
};

export const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({
  confidence,
  bucket,
  calibrated = false,
}) => {
  const config = bucketConfig[bucket] || bucketConfig.medium;
  const pct = Math.round(confidence * 100);

  return (
    <div
      className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border ${config.bg} ${config.border}`}
      title={calibrated ? "Kalibrierte Konfidenz" : "Roh-Konfidenz"}
    >
      <span className={`text-sm font-semibold ${config.text}`}>
        {config.label}
      </span>
      <span className={`text-xs ${config.text} opacity-80`}>
        {pct}%
      </span>
      {calibrated && (
        <span className="text-[10px] text-slate-400 ml-1">kal.</span>
      )}
    </div>
  );
};

export const ConfidenceBar: React.FC<{ confidence: number }> = ({ confidence }) => {
  const pct = Math.min(100, Math.max(0, confidence * 100));

  const getColor = (p: number) => {
    if (p < 70) return "bg-red-500";
    if (p < 90) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="w-full max-w-xs">
      <div className="flex justify-between text-xs text-slate-500 mb-1">
        <span>Konfidenz</span>
        <span>{Math.round(pct)}%</span>
      </div>
      <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${getColor(pct)}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
};

export const LowConfidenceWarning: React.FC = () => (
  <div className="flex items-start gap-2 p-3 bg-orange-50 border border-orange-200 rounded-lg">
    <svg className="w-5 h-5 text-orange-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
    <div>
      <p className="text-sm font-medium text-orange-800">
        AI-Konfidenz niedrig
      </p>
      <p className="text-xs text-orange-600 mt-0.5">
        Bitte sorgfältige manuelle Prüfung durchführen.
      </p>
    </div>
  </div>
);
