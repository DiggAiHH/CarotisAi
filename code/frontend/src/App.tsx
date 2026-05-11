import { useCallback, useEffect, useState } from "react";

import { AiPanel } from "./components/AiPanel/AiPanel";
import { AuthGate } from "./components/AuthGate/AuthGate";
import { DicomViewer, type DemoCasePreview } from "./components/DicomViewer/DicomViewer";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { ResearchSplashGate } from "./components/ResearchSplashGate";
import { Watermark } from "./components/Watermark";
import { Walkthrough } from "./components/Walkthrough";
import { useInference } from "./hooks/useInference";
import { apiClient } from "./lib/apiClient";
import { t } from "./lib/i18n";
import { useStore } from "./store";
import type { AnalysisStatus, InferenceResponse } from "./types";

interface DemoCase {
  id: string;
  patientName: string;
  initials: string;
  studyDate: string;
  label: string;
  status: "high" | "medium" | "low";
  downloadPath: string;
  prediction: InferenceResponse;
  preview: DemoCasePreview;
}

const featureFlags = {
  cdsEnabled: false,
};

const DEMO_SHA =
  "8e4b2e32c45c9d48913b9ff61c20f87e4f88b24f27439c45c6b94f1c11f2b8e9";

const DEMO_CASES: DemoCase[] = [
  {
    id: "case_002",
    patientName: "M. Mueller",
    initials: "MM",
    studyDate: "2026-04-28",
    label: "Workflow-Beobachtung rechts ICA",
    status: "high",
    downloadPath: "/demo/dicoms/case_002.dcm",
    prediction: {
      case_id: "demo-case-002",
      confidence_bucket: "high",
      trust_score: 0.78,
      calibrated: true,
      model_version: "mfsd-unet-demo-v0.1",
      model_sha: DEMO_SHA,
      audit_id: "audit-demo-002",
      captured_at: "2026-05-02T10:00:00Z",
      heatmap_b64: null,
    },
    preview: {
      patientName: "M. Mueller",
      initials: "MM",
      studyDate: "2026-04-28",
      attentionFocus: 0.72,
      slice: 42,
      slices: 120,
      lesionSizeMm: 5.2,
      thicknessMm: 0.625,
      confidence: 0.84,
      windowPreset: "Vessel",
    },
  },
  {
    id: "case_001",
    patientName: "A. Schmidt",
    initials: "AS",
    studyDate: "2026-04-27",
    label: "Workflow-Fall, Plaque weich",
    status: "medium",
    downloadPath: "/demo/dicoms/case_001.dcm",
    prediction: {
      case_id: "demo-case-001",
      confidence_bucket: "high",
      trust_score: 0.81,
      calibrated: true,
      model_version: "mfsd-unet-demo-v0.1",
      model_sha: DEMO_SHA,
      audit_id: "audit-demo-001",
      captured_at: "2026-05-02T10:00:00Z",
      heatmap_b64: null,
    },
    preview: {
      patientName: "A. Schmidt",
      initials: "AS",
      studyDate: "2026-04-27",
      attentionFocus: 0.45,
      slice: 37,
      slices: 120,
      lesionSizeMm: 3.9,
      thicknessMm: 0.625,
      confidence: 0.82,
      windowPreset: "Vessel",
    },
  },
  {
    id: "case_003",
    patientName: "K. Weber",
    initials: "KW",
    studyDate: "2026-04-26",
    label: "Fokusbeobachtung stabile Kalzifikation",
    status: "high",
    downloadPath: "/demo/dicoms/case_003.dcm",
    prediction: {
      case_id: "demo-case-003",
      confidence_bucket: "medium",
      trust_score: 0.64,
      calibrated: true,
      model_version: "mfsd-unet-demo-v0.1",
      model_sha: DEMO_SHA,
      audit_id: "audit-demo-003",
      captured_at: "2026-05-02T10:00:00Z",
      heatmap_b64: null,
    },
    preview: {
      patientName: "K. Weber",
      initials: "KW",
      studyDate: "2026-04-26",
      attentionFocus: 0.68,
      slice: 51,
      slices: 120,
      lesionSizeMm: 4.8,
      thicknessMm: 0.625,
      confidence: 0.77,
      windowPreset: "Vessel",
    },
  },
  {
    id: "case_004",
    patientName: "J. Fischer",
    initials: "JF",
    studyDate: "2026-04-25",
    label: "Workflow-Fall mit Motion-Artefakt",
    status: "low",
    downloadPath: "/demo/dicoms/case_004.dcm",
    prediction: {
      case_id: "demo-case-004",
      confidence_bucket: "medium",
      trust_score: 0.56,
      calibrated: true,
      model_version: "mfsd-unet-demo-v0.1",
      model_sha: DEMO_SHA,
      audit_id: "audit-demo-004",
      captured_at: "2026-05-02T10:00:00Z",
      heatmap_b64: null,
    },
    preview: {
      patientName: "J. Fischer",
      initials: "JF",
      studyDate: "2026-04-25",
      attentionFocus: 0.31,
      slice: 29,
      slices: 120,
      lesionSizeMm: 2.7,
      thicknessMm: 0.625,
      confidence: 0.74,
      windowPreset: "Vessel",
    },
  },
];

function caseColor(status: DemoCase["status"]) {
  if (status === "high") return "border-red-500/50 bg-red-500/10 text-red-300";
  if (status === "medium") return "border-amber-500/50 bg-amber-500/10 text-amber-300";
  return "border-emerald-500/50 bg-emerald-500/10 text-emerald-300";
}

function Header() {
  const [health, setHealth] = useState<"ok" | "error">("error");

  useEffect(() => {
    let mounted = true;
    const check = () => {
      apiClient
        .getHealth()
        .then(() => { if (mounted) setHealth("ok"); })
        .catch(() => { if (mounted) setHealth("error"); });
    };
    check();
    const id = setInterval(check, 30000);
    return () => {
      mounted = false;
      clearInterval(id);
    };
  }, []);

  const handleLogout = () => {
    try {
      localStorage.removeItem("carotis:demoToken");
      localStorage.removeItem("carotis:roleHash");
    } catch { /* ignore */ }
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

type MobileTab = "viewer" | "ai" | "cases";

function MobileTabBar({ active, onChange }: { active: MobileTab; onChange: (t: MobileTab) => void }) {
  const tabs: { id: MobileTab; label: string }[] = [
    { id: "cases", label: t("app.cases") },
    { id: "viewer", label: "DICOM" },
    { id: "ai", label: "Overlay" },
  ];
  return (
    <nav className="flex border-t border-slate-800 bg-slate-950 shrink-0 md:hidden">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={`flex-1 py-3 text-xs font-medium transition-colors ${
            active === tab.id
              ? "text-emerald-400 border-t-2 border-emerald-400 -mt-px"
              : "text-slate-500 hover:text-slate-300"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </nav>
  );
}

function AppContent() {
  const [status, setStatus] = useState<AnalysisStatus>("idle");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [selectedCaseId, setSelectedCaseId] = useState(DEMO_CASES[0].id);
  const [result, setResult] = useState<InferenceResponse | null>(
    DEMO_CASES[0].prediction
  );
  const [heatmap, setHeatmap] = useState<number[][] | string | undefined>(undefined);
  const [mobileTab, setMobileTab] = useState<MobileTab>("viewer");

  const setCurrentPrediction = useStore((s) => s.setCurrentPrediction);
  const setStoreSelectedCaseId = useStore((s) => s.setSelectedCaseId);
  const inferenceMutation = useInference();
  const selectedCase =
    DEMO_CASES.find((demoCase) => demoCase.id === selectedCaseId) ??
    DEMO_CASES[0];

  useEffect(() => {
    setCurrentPrediction(selectedCase.prediction);
    setStoreSelectedCaseId(selectedCase.id);
  }, [selectedCase, setCurrentPrediction, setStoreSelectedCaseId]);

  const handleDemoCaseSelected = useCallback(
    (demoCase: DemoCase) => {
      setSelectedCaseId(demoCase.id);
      setResult(demoCase.prediction);
      setHeatmap(undefined);
      setStatus("idle");
      setErrorMsg(null);
      setCurrentPrediction(demoCase.prediction);
      setStoreSelectedCaseId(demoCase.id);
      if (window.innerWidth < 768) setMobileTab("viewer");
    },
    [setCurrentPrediction, setStoreSelectedCaseId]
  );

  const handleFileSelected = useCallback(
    (file: File) => {
      setStatus("uploading");
      setErrorMsg(null);
      setResult(null);
      setHeatmap(undefined);
      inferenceMutation.mutate(file, {
        onSuccess: (data) => {
          setStatus("done");
          setSelectedCaseId("");
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

  return (
    <div className="h-[100dvh] flex flex-col bg-slate-950 text-slate-100 overflow-hidden">
      <Walkthrough />
      <Header />

      {/* Desktop: 3-column layout  /  Mobile: single panel controlled by tab */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left: Patient List — always visible on md+, hidden on mobile unless "cases" tab */}
        <aside
          className={`
            md:w-[280px] md:block md:border-r md:border-slate-800 md:bg-slate-900 md:shrink-0
            ${mobileTab === "cases" ? "flex flex-col w-full" : "hidden"}
            md:flex md:flex-col overflow-y-auto
          `}
        >
          <div className="border-b border-slate-800 p-4">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded bg-emerald-500 text-sm font-bold text-slate-950">
                C
              </div>
              <div>
                <h2 className="text-base font-semibold text-slate-100">
                  Carotis AI
                </h2>
                <p className="text-xs text-slate-500">
                  Workflow Capture
                </p>
              </div>
              <span className="ml-auto rounded bg-slate-800 px-2 py-0.5 text-[10px] text-slate-400">
                v0.1 Demo
              </span>
            </div>
            <div className="mt-4 rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-500">
              Forschungsfaelle suchen...
            </div>
          </div>

          <div className="flex items-center justify-between px-4 py-3 text-[11px] uppercase tracking-[0.18em] text-slate-500">
            <span>Forschungsfaelle</span>
            <span>{DEMO_CASES.length} records</span>
          </div>

          <div className="flex flex-col gap-2 px-3">
            {DEMO_CASES.map((demoCase) => {
              const active = demoCase.id === selectedCaseId;
              return (
                <button
                  key={demoCase.id}
                  type="button"
                  onClick={() => handleDemoCaseSelected(demoCase)}
                  className={[
                    "grid grid-cols-[40px_1fr_auto] items-center gap-3 rounded-lg border p-3 text-left transition-colors",
                    active
                      ? "border-slate-600 bg-slate-700/80"
                      : "border-transparent bg-transparent hover:bg-slate-800",
                  ].join(" ")}
                >
                  <span className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-700 text-sm font-bold text-slate-200">
                    {demoCase.initials}
                  </span>
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-semibold text-slate-100">
                      {demoCase.patientName}
                    </span>
                    <span className="block truncate text-xs text-slate-500">
                      {demoCase.label}
                    </span>
                    <span className="block text-xs text-slate-600">
                      {demoCase.studyDate}
                    </span>
                  </span>
                  <span
                    className={`rounded border px-2 py-1 text-xs font-bold ${caseColor(demoCase.status)}`}
                  >
                    {demoCase.prediction.confidence_bucket ?? "research"}
                  </span>
                </button>
              );
            })}
          </div>

          <div className="mt-auto border-t border-slate-800 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
              Synthetic test data
            </p>
            <a
              href={selectedCase.downloadPath}
              download
              className="mt-2 block rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-3 py-2 text-center text-sm font-semibold text-emerald-300 hover:bg-emerald-500/20"
            >
              Download selected DICOM
            </a>
            <p className="mt-2 text-xs leading-5 text-slate-500">
              Demo files are generated, anonymized DICOMs. No patient data.
            </p>
          </div>
        </aside>

        {/* Center: DICOM Viewer */}
        <main
          className={`
            flex-1 bg-black relative min-w-0 overflow-hidden
            ${mobileTab === "viewer" ? "flex flex-col" : "hidden"}
            md:flex md:flex-col
          `}
          data-walkthrough="dicom-viewer"
        >
          <StatusBadge status={status} error={errorMsg} />
          <DicomViewer
            dicomFileUrl=""
            heatmap={heatmap}
            onFileSelected={handleFileSelected}
            previewCase={selectedCaseId ? selectedCase.preview : undefined}
          />
        </main>

        {/* Right: AI Panel */}
        <aside
          className={`
            md:w-[360px] md:block md:border-l md:border-slate-800 md:bg-slate-900 md:shrink-0
            ${mobileTab === "ai" ? "flex flex-col w-full p-3" : "hidden"}
            md:flex md:flex-col md:p-3 overflow-y-auto gap-3
          `}
          data-walkthrough="ai-panel"
        >
          <AiPanel result={result ?? undefined} />

          {result && !featureFlags.cdsEnabled && (
              <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-4">
                <p className="text-sm font-semibold text-amber-200">
                  Workflow-Capture im Forschungsmodus
                </p>
                <p className="mt-2 text-xs leading-5 text-slate-400">
                  Entscheidungsunterstuetzende Module sind deaktiviert. Fuer diesen
                  Demonstrationsstand werden nur Overlay-, Konfidenz- und
                  Workflow-Daten angezeigt.
                </p>
              </div>
            )}
        </aside>
      </div>

      {/* Mobile bottom tab bar */}
      <MobileTabBar active={mobileTab} onChange={setMobileTab} />
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <ResearchSplashGate>
        <AuthGate>
          <AppContent />
          <Watermark />
        </AuthGate>
      </ResearchSplashGate>
    </ErrorBoundary>
  );
}
