import { useEffect, useState } from "react";

import { AiPanel } from "./components/AiPanel/AiPanel";
import { DicomViewer } from "./components/DicomViewer";
import { Walkthrough } from "./components/Walkthrough";
import { apiClient } from "./lib/apiClient";
import { t } from "./lib/i18n";

function Header() {
  const [health, setHealth] = useState<"ok" | "error">("error");

  useEffect(() => {
    apiClient
      .getHealth()
      .then(() => setHealth("ok"))
      .catch(() => setHealth("error"));
  }, []);

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
    </header>
  );
}

export default function App() {
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
          <DicomViewer dicomFileUrl="" />
        </main>

        {/* Right: AI Panel */}
        <aside className="w-[360px] border-l border-slate-800 bg-slate-900 p-3 overflow-y-auto shrink-0" data-walkthrough="ai-panel">
          <AiPanel />
        </aside>
      </div>
    </div>
  );
}
