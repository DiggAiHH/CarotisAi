import { useCallback, useEffect, useState } from "react";

import { AiPanel } from "./components/AiPanel/AiPanel";
import { AuthGate } from "./components/AuthGate/AuthGate";
import { useDemoToken } from "./components/AuthGate/useDemoToken";
import { DecisionForm } from "./components/DecisionForm/DecisionForm";
import { DicomViewer } from "./components/DicomViewer";
import { Walkthrough } from "./components/Walkthrough";
import { useInference } from "./hooks/useInference";
import { apiClient } from "./lib/apiClient";
import { t } from "./lib/i18n";
import { useStore } from "./store";
import type { AnalysisStatus, InferenceResponse } from "./types";

function Header() {
  const [health, setHealth] = useState<"ok" | "error">("error");
  const { setToken } = useDemoToken();

  useEffect(() => {
    apiClient
      .getHealth()
      .then(() => setHealth("ok"))
      .catch(() => setHealth("error"));
  }, []);

  const handleLogout = () => {
    setToken(null);
    window.location.reload();
  };

  return (
    <header className="h-14 bg-slate-950 border-b border-slate-800 flex items-center px-4 justify-between shrink-0">
      <div className="flex items-center gap-3">
        <div className="w-3 h-3 rounded-full bg-emerald-500" />
        <h1 className="text-slate-100 font-semibold">
          {t("app.title")}{" "}
          <span className="text-slate-500 text-sm font-normal">
            {t("app.subtitle")}
          </span>
        </h1>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <span
            className={`w-2 h-2 rounded-full ${
              health === "ok" ? "bg-emerald-500" : "bg-red-500"
            }`}
          />
          <span className="text-slate-400 text-sm">
            {health === "ok" ? t("app.online") : t("app.offline")}
          </span>
        </div>
        <button
          onClick={handleLogout}
          className="text-xs text-slate-500 hover:text-slate-300 transition-colors"
        >
          {t("app.logout")}
        </button>
      </div>
    </header>
  );
}

function StatusBadge({ status, error }: { status: AnalysisStatus; error?: string | null }) {
  if (status === "idle") return null;

  const config: Record<Exclude<AnalysisStatus, "idle">, { text: string; cls: string }> = {
    uploading: { text: t("status.uploading"), cls: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
    analysing: { text: t("status.analysing"), cls: "bg-cyan-500/20 text-cyan-400 border-cyan-500/30" },
    done: { text: t("status.done"), cls: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
    error: { text: error || t("status.error"), cls: "bg-red-500/20 text-red-400 border-red-500/30" },
  };

  const { text, cls } = config[status as Exclude<AnalysisStatus, "idle">] || config.error;

  return (
    <div className={`absolute top-3 left-1/2 -translate-x-1/2 z-10 rounded-full border px-4 py-1.5 text-xs font-medium shadow-lg ${cls}`}>
      {status === "analysing" && (
        <span className="inline-block w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin mr-2 align-text-bottom" />
      )}
      {text}
    </div>
  );
}

function AppContent() {
  const [status, setStatus] = useState<AnalysisStatus>("idle");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [result, setResult] = useState<InferenceResponse | null>(null);
  const [heatmap, setHeatmap] = useState<number[][] | string | undefined>(undefined);
  const [formSubmitted, setFormSubmitted] = useState(false);

  const setCurrentPrediction = useStore((s) => s.setCurrentPrediction);
  const inferenceMutation = useInference();

  const handleFileSelected = useCallback(
    (file: File) => {
      setStatus("uploading");
      setErrorMsg(null);
      setResult(null);
      setHeatmap(undefined);
      setFormSubmitted(false);

      inferenceMutation.mutate(file, {
        onSuccess: (data) => {
          setStatus("done");
          setResult(data);
          setCurrentPrediction(data);
          if (data.heatmap_b64) {
            setHeatmap(data.heatmap_b64);
          } else {
            setHeatmap(undefined);
          }
        },
        onError: (err) => {
          setStatus("error");
          setErrorMsg(err instanceof Error ? err.message : t("status.unknownError"));
        },
      });
    },
    [inferenceMutation, setCurrentPrediction]
  );

  // Track analysis state from mutation
  useEffect(() => {
    if (inferenceMutation.isPending && status !== "analysing") {
      setStatus("analysing");
    }
  }, [inferenceMutation.isPending, status]);

  const handleFormSubmitted = useCallback(() => {
    setFormSubmitted(true);
  }, []);

  return (
    <div className="h-screen flex flex-col bg-slate-950 text-slate-100 overflow-hidden">
      <Walkthrough />
      <Header />
      <div className="flex-1 flex overflow-hidden">
        {/* Left: Patient List */}
        <aside className="w-[280px] border-r border-slate-800 bg-slate-900 p-3 overflow-y-auto shrink-0">
          <h2 className="text-sm font-medium text-slate-400 mb-2">
            {t("app.cases")}
          </h2>
          <div className="text-slate-500 text-sm">
            {t("app.casesPlaceholder")}
          </div>
        </aside>

        {/* Center: DICOM Viewer */}
        <main className="flex-1 bg-black relative min-w-0" data-walkthrough="dicom-viewer">
          <StatusBadge status={status} error={errorMsg} />
          <DicomViewer
            dicomFileUrl=""
            heatmap={heatmap}
            onFileSelected={handleFileSelected}
          />
        </main>

        {/* Right: AI Panel */}
        <aside
          className="w-[360px] border-l border-slate-800 bg-slate-900 p-3 overflow-y-auto shrink-0 flex flex-col gap-3"
          data-walkthrough="ai-panel"
        >
          <AiPanel result={result ?? undefined} />

          {result && !formSubmitted && (
            <DecisionForm
              result={result}
              physicianRoleHash="demo-physician"
              onSubmitted={handleFormSubmitted}
            />
          )}

          {formSubmitted && (
            <div className="rounded-lg bg-emerald-500/10 border border-emerald-500/30 p-4 text-center">
              <p className="text-sm text-emerald-400 font-medium">
                {t("form.saved")}
              </p>
              <p className="text-xs text-slate-500 mt-1">
                {t("form.nextCaseHint")}
              </p>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthGate>
      <AppContent />
    </AuthGate>
  );
}
