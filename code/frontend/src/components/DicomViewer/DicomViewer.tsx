import { useCallback, useEffect, useRef, useState } from "react";
import type { RenderingEngine, Types } from "@cornerstonejs/core";

import { HeatmapOverlay } from "./HeatmapOverlay";
import { t } from "../../lib/i18n";

interface Props {
  dicomFileUrl?: string;
  heatmap?: number[][] | string;
  onFileSelected?: (file: File) => void;
  previewCase?: DemoCasePreview;
}

export interface DemoCasePreview {
  patientName: string;
  initials: string;
  studyDate: string;
  attentionFocus: number;
  slice: number;
  slices: number;
  lesionSizeMm: number;
  thicknessMm: number;
  confidence: number;
  windowPreset: "Soft Tissue" | "Bone" | "Vessel";
}

/**
 * Anatomically accurate SVG CTA phantom for the carotid neck cross-section.
 * Axial view at ~C3-C4 level with:
 *   - Vertebral body (posterior, bright)
 *   - Trachea + esophagus (anterior midline)
 *   - Bilateral SCM muscles (anterolateral)
 *   - Bilateral carotid sheaths: ICA, ECA, IJV
 *   - Research focus shown on patient's LEFT ICA (image RIGHT)
 *   - Grad-CAM heatmap overlay when enabled
 *   - Window preset simulation via SVG filter
 */
function CarotidCtaSvg({
  attentionFocus,
  lesionSizeMm,
  heatmapEnabled,
  windowPreset,
}: {
  attentionFocus: number;
  lesionSizeMm: number;
  heatmapEnabled: boolean;
  windowPreset: string;
}) {
  // Lumen radius for the synthetic research focus (outer vessel r = 11).
  const lumanR = Math.max(1.5, 11 * (1 - attentionFocus * 0.9));
  // Plaque: calcified (bright) vs soft (dark) based on synthetic focus intensity.
  const plaqueIsBright = attentionFocus > 0.5;
  const plaqueFill = plaqueIsBright ? "#9e9e9e" : "#484848";
  // Lumen offset (eccentric plaque pushes lumen)
  const lumanOffset = Math.min(5, attentionFocus * 7);

  // Window preset filter
  const filterStyle: React.CSSProperties =
    windowPreset === "Bone"
      ? { filter: "contrast(2.2) brightness(0.75)" }
      : windowPreset === "Soft Tissue"
        ? { filter: "contrast(0.75) brightness(1.15)" }
        : {};

  return (
    <svg
      viewBox="0 0 512 512"
      preserveAspectRatio="xMidYMid meet"
      style={{ width: "100%", height: "100%", display: "block", ...filterStyle }}
    >
      <defs>
        <radialGradient id="bodyGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#2a2a2a" />
          <stop offset="85%" stopColor="#242424" />
          <stop offset="100%" stopColor="#181818" />
        </radialGradient>
        <radialGradient id="hmGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#ff1111" stopOpacity="0.90" />
          <stop offset="28%" stopColor="#ff7700" stopOpacity="0.78" />
          <stop offset="55%" stopColor="#ffe000" stopOpacity="0.52" />
          <stop offset="78%" stopColor="#44ff44" stopOpacity="0.25" />
          <stop offset="100%" stopColor="#00ccff" stopOpacity="0.0" />
        </radialGradient>
        <filter id="softBlur">
          <feGaussianBlur stdDeviation="0.5" />
        </filter>
      </defs>

      {/* Absolute black background */}
      <rect width="512" height="512" fill="#000000" />

      {/* CT scan FOV circle */}
      <circle cx="256" cy="256" r="252" fill="#080808" />

      {/* Neck cross-section body (soft tissue average density) */}
      <ellipse cx="256" cy="268" rx="210" ry="193" fill="url(#bodyGrad)" />

      {/* Skin + subcutaneous fat ring */}
      <ellipse cx="256" cy="268" rx="210" ry="193" fill="none" stroke="#3d3434" strokeWidth="16" opacity="0.65" />

      {/* ── Paraspinal muscles (bilateral, deep posterior) ── */}
      <ellipse cx="196" cy="340" rx="44" ry="42" fill="#2e2e2e" />
      <ellipse cx="316" cy="340" rx="44" ry="42" fill="#2e2e2e" />

      {/* ── SCM muscles (bilateral anterolateral) ── */}
      <ellipse cx="133" cy="205" rx="52" ry="31" fill="#343434" transform="rotate(-12,133,205)" />
      <ellipse cx="379" cy="205" rx="52" ry="31" fill="#343434" transform="rotate(12,379,205)" />

      {/* ── Trachea (air-filled, very dark anterior midline) ── */}
      <circle cx="256" cy="148" r="27" fill="#060606" />
      {/* Tracheal cartilage ring (open posteriorly = horseshoe) */}
      <path d="M 231 148 A 25 25 0 0 1 281 148" stroke="#8a8a8a" strokeWidth="3.5" fill="none" />
      <line x1="231" y1="148" x2="231" y2="165" stroke="#8a8a8a" strokeWidth="3" />
      <line x1="281" y1="148" x2="281" y2="165" stroke="#8a8a8a" strokeWidth="3" />

      {/* ── Esophagus (posterior to trachea, collapsed) ── */}
      <ellipse cx="256" cy="178" rx="12" ry="9" fill="#181818" stroke="#505050" strokeWidth="1.5" />

      {/* ── Thyroid gland lobes (bilateral, slightly bright — iodine) ── */}
      <ellipse cx="228" cy="170" rx="20" ry="14" fill="#464646" opacity="0.85" />
      <ellipse cx="284" cy="170" rx="20" ry="14" fill="#464646" opacity="0.85" />

      {/* ── Vertebral body (posterior, very bright — cortical + cancellous bone) ── */}
      <ellipse cx="256" cy="362" rx="47" ry="34" fill="#b8b8b8" />
      <ellipse cx="256" cy="362" rx="47" ry="34" fill="none" stroke="#e6e6e6" strokeWidth="3.5" />
      {/* Cancellous pattern */}
      <ellipse cx="256" cy="362" rx="32" ry="21" fill="#b0b0b0" />
      {/* Anterior osteophyte */}
      <ellipse cx="256" cy="331" rx="9" ry="6" fill="#cacaca" />
      {/* Spinal canal (dark) */}
      <ellipse cx="256" cy="337" rx="21" ry="16" fill="#0c0c0c" />
      {/* Spinal cord (medium gray, CSF halo) */}
      <ellipse cx="256" cy="337" rx="14" ry="12" fill="#585858" />
      <ellipse cx="256" cy="337" rx="8" ry="7" fill="#6e6e6e" />

      {/* Transverse foramina with vertebral arteries */}
      <ellipse cx="206" cy="358" rx="11" ry="13" fill="#131313" />
      <ellipse cx="306" cy="358" rx="11" ry="13" fill="#131313" />
      <circle cx="206" cy="358" r="5" fill="#cacaca" filter="url(#softBlur)" />
      <circle cx="306" cy="358" r="5" fill="#cacaca" filter="url(#softBlur)" />

      {/* ════ RIGHT CAROTID SHEATH (image LEFT = patient's RIGHT) — Normal ════ */}
      {/* Internal Jugular Vein (large, unenhanced/dark) */}
      <circle cx="150" cy="252" r="18" fill="#101010" stroke="#3e3e3e" strokeWidth="1.5" />
      {/* ICA outer wall */}
      <circle cx="174" cy="229" r="12" fill="#6a6a6a" />
      {/* ICA lumen (contrast-enhanced, very bright) */}
      <circle cx="174" cy="229" r="8.5" fill="#f0f0f0" />
      <circle cx="174" cy="229" r="5" fill="#fafafa" />
      {/* ECA (External Carotid — anterior, slightly smaller) */}
      <circle cx="164" cy="212" r="7" fill="#5e5e5e" />
      <circle cx="164" cy="212" r="4.5" fill="#e4e4e4" />

      {/* ════ LEFT CAROTID SHEATH (image RIGHT = patient's LEFT) — Stenotic ════ */}
      {/* Internal Jugular Vein */}
      <circle cx="362" cy="252" r="18" fill="#101010" stroke="#3e3e3e" strokeWidth="1.5" />
      {/* Research focus ICA: eccentric plaque + narrowed lumen */}
      <circle cx="338" cy="229" r="13" fill={plaqueFill} />
      {/* Calcified plaque highlight (bright nodule) when calcified */}
      {plaqueIsBright && (
        <circle cx="331" cy="223" r="5" fill="#d0d0d0" />
      )}
      {/* Narrowed lumen (offset due to eccentric plaque) */}
      <circle
        cx={338 + lumanOffset * 0.7}
        cy={229 + lumanOffset * 0.3}
        r={lumanR}
        fill="#f0f0f0"
      />
      {/* ECA left */}
      <circle cx="348" cy="212" r="7" fill="#5e5e5e" />
      <circle cx="348" cy="212" r="4.5" fill="#e4e4e4" />

      {/* ════ HEATMAP OVERLAY (Grad-CAM style) ════ */}
      {heatmapEnabled && (
        <>
          <circle cx="338" cy="229" r="48" fill="url(#hmGrad)" />
          {/* Callout line + label */}
          <line x1="338" y1="216" x2="362" y2="193" stroke="#00ff99" strokeWidth="1.2" strokeDasharray="4,3" />
          <rect x="360" y="183" width="78" height="17" fill="#071022" fillOpacity="0.88" rx="3" />
          <text x="399" y="195" fill="#00ff99" fontSize="10.5" fontFamily="monospace" textAnchor="middle">
            {lesionSizeMm.toFixed(1)} mm focus
          </text>
          {/* Research focus ring on vessel */}
          <circle cx="338" cy="229" r={lumanR + 1.5} fill="none" stroke="#ff4444" strokeWidth="1.5" strokeDasharray="3,2" />
        </>
      )}
    </svg>
  );
}

function SyntheticCtaPreview({
  previewCase,
  heatmapEnabled,
  windowPreset,
  onWindowPresetChange,
}: {
  previewCase: DemoCasePreview;
  heatmapEnabled: boolean;
  windowPreset: string;
  onWindowPresetChange: (preset: "Soft Tissue" | "Bone" | "Vessel") => void;
}) {
  const severityClass =
    previewCase.attentionFocus >= 0.7
      ? "border-red-500/60 bg-red-950/30 text-red-300"
      : previewCase.attentionFocus >= 0.5
        ? "border-amber-500/60 bg-amber-950/30 text-amber-300"
        : "border-emerald-500/60 bg-emerald-950/30 text-emerald-300";
  const focusLabel =
    previewCase.attentionFocus >= 0.7
      ? t("viewer.focusHigh")
      : previewCase.attentionFocus >= 0.5
        ? t("viewer.focusModerate")
        : t("viewer.focusLow");
  const confidenceLabel =
    previewCase.confidence >= 0.8
      ? t("viewer.confidenceHigh")
      : previewCase.confidence >= 0.6
        ? t("viewer.confidenceMedium")
        : t("viewer.confidenceLow");

  const ww = windowPreset === "Bone" ? 2000 : windowPreset === "Soft Tissue" ? 400 : 600;
  const wl = windowPreset === "Bone" ? 400 : windowPreset === "Soft Tissue" ? 40 : 150;

  const presetMap: Record<string, string> = {
    "Soft Tissue": t("viewer.softTissue"),
    Bone: t("viewer.bone"),
    Vessel: t("viewer.vessel"),
  };

  return (
    <div className="absolute inset-0 overflow-hidden bg-[#020611] text-slate-200">
      {/* Demo banner */}
      <div className="absolute left-0 right-0 top-0 z-20 border-b border-violet-500/30 bg-violet-950/55 px-4 py-1 text-center font-mono text-[10px] uppercase tracking-[0.22em] text-violet-300">
        {t("viewer.demoBanner")}
      </div>

      {/* Window preset buttons (top left) */}
      <div className="absolute left-4 right-4 top-7 z-20 flex flex-wrap items-center gap-1.5 sm:gap-2">
        {(["Soft Tissue", "Bone", "Vessel"] as const).map((preset) => (
          <button
            key={preset}
            type="button"
            onClick={() => onWindowPresetChange(preset)}
            className={[
              "rounded border px-2 py-0.5 text-[11px] sm:px-3 sm:py-1 sm:text-xs transition-colors",
              windowPreset === preset
                ? "border-emerald-400/70 bg-emerald-500/15 text-emerald-300"
                : "border-slate-700 bg-slate-900/80 text-slate-400 hover:border-slate-500 hover:text-slate-300",
            ].join(" ")}
          >
            {presetMap[preset]}
          </button>
        ))}
        <span className="ml-auto rounded border border-orange-500/40 bg-orange-950/40 px-2 py-0.5 text-[11px] font-semibold text-orange-300 sm:px-3 sm:py-1 sm:text-xs">
          {t("viewer.heatmap")} {heatmapEnabled ? t("viewer.heatmapOn") : t("viewer.heatmapOff")}
        </span>
      </div>

      {/* Patient info overlay (left) */}
      <div className="absolute left-4 top-[4.5rem] z-20 font-mono text-[11px] leading-5 text-slate-300 sm:text-xs sm:leading-6">
        <div className="font-semibold text-slate-100">{previewCase.patientName}</div>
        <div>{t("viewer.dob")}</div>
        <div>{t("viewer.study")}: {previewCase.studyDate}</div>
        <div>{t("viewer.ctaNeckAxial")}</div>
      </div>

      {/* Window / zoom info (right) */}
      <div className="absolute right-4 top-[4.5rem] z-20 text-right font-mono text-[11px] leading-5 text-slate-300 sm:text-xs sm:leading-6">
        <div>{t("viewer.ww")}: {ww} HU</div>
        <div>{t("viewer.wl")}: {wl} HU</div>
        <div>{t("viewer.zoom")}: ×1.7</div>
      </div>

      {/* SVG anatomical CTA phantom — fills available space */}
      <div className="absolute inset-x-[2%] top-[30%] bottom-[14%] flex items-center justify-center">
        <CarotidCtaSvg
          attentionFocus={previewCase.attentionFocus}
          lesionSizeMm={previewCase.lesionSizeMm}
          heatmapEnabled={heatmapEnabled}
          windowPreset={windowPreset}
        />
      </div>

      {/* Bottom-left info */}
      <div className="absolute bottom-14 left-4 z-20 font-mono text-[11px] leading-5 text-slate-300 sm:text-xs sm:leading-6">
        <div>{t("viewer.slice")}: {previewCase.slice}/{previewCase.slices}</div>
        <div>{t("viewer.thickness")}: {previewCase.thicknessMm.toFixed(3)} mm</div>
        <div>{t("viewer.fov")}: 180×180 mm</div>
      </div>

      {/* Research focus badge (bottom right) */}
      <div className={`absolute bottom-[3.8rem] right-4 z-20 rounded border px-2 py-1 font-mono text-[11px] font-bold sm:px-3 sm:py-2 sm:text-xs ${severityClass}`}>
        {t("viewer.overlayFocus")}: {focusLabel}
      </div>

      {/* Slice progress bar */}
      <div className="absolute bottom-0 left-0 right-0 z-20 border-t border-slate-800 bg-[#071022] px-3 py-2 sm:px-4 sm:py-3">
        <div className="grid grid-cols-[64px_1fr_88px] items-center gap-3 font-mono text-[11px] text-slate-400 sm:grid-cols-[72px_1fr_96px] sm:text-xs">
          <span>{t("viewer.slice")} {previewCase.slice}/{previewCase.slices}</span>
          <div className="h-1.5 rounded-full bg-slate-800">
            <div
              className="h-1.5 rounded-full bg-emerald-400"
              style={{ width: `${(previewCase.slice / previewCase.slices) * 100}%` }}
            />
          </div>
          <span className="text-right">{confidenceLabel}</span>
        </div>
      </div>
    </div>
  );
}

export function DicomViewer({ dicomFileUrl, heatmap, onFileSelected, previewCase }: Props) {
  const elementRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [viewportReady, setViewportReady] = useState(false);
  const [heatmapOpacity, setHeatmapOpacity] = useState(50);
  const [syntheticHeatmapEnabled, setSyntheticHeatmapEnabled] = useState(true);
  const [windowPreset, setWindowPreset] = useState<"Soft Tissue" | "Bone" | "Vessel">(
    previewCase?.windowPreset ?? "Vessel"
  );
  const engineRef = useRef<RenderingEngine | null>(null);
  const viewportIdRef = useRef(`viewport-${crypto.randomUUID()}`);
  const renderingEngineIdRef = useRef(`engine-${crypto.randomUUID()}`);
  const objectUrlRef = useRef<string | null>(null);

  const cleanup = useCallback(() => {
    if (engineRef.current) {
      engineRef.current.destroy();
      engineRef.current = null;
    }
  }, []);

  const setupViewport = useCallback(async (imageId: string) => {
    const el = elementRef.current;
    if (!el) return;

    const [{ RenderingEngine, Enums }, { ToolGroupManager }, setup] =
      await Promise.all([
        import("@cornerstonejs/core"),
        import("@cornerstonejs/tools"),
        import("../../lib/cornerstoneSetup"),
      ]);
    const { initCornerstone, createDefaultToolGroup, TOOL_GROUP_ID } = setup;

    await initCornerstone();

    // Reuse existing engine if possible
    let renderingEngine = engineRef.current;
    if (!renderingEngine) {
      renderingEngine = new RenderingEngine(renderingEngineIdRef.current);
      engineRef.current = renderingEngine;
    } else {
      try {
        renderingEngine.disableElement(viewportIdRef.current);
      } catch { /* ignore if not enabled */ }
    }
    if (!renderingEngine) return;

    const viewportInput: Types.PublicViewportInput = {
      viewportId: viewportIdRef.current,
      element: el,
      type: Enums.ViewportType.STACK,
    };

    renderingEngine.enableElement(viewportInput);
    const viewport = renderingEngine.getViewport(viewportIdRef.current) as unknown as {
      setStack: (imageIds: string[]) => Promise<void>;
      render: () => void;
    };

    // Only create tool group once
    let toolGroup = ToolGroupManager.getToolGroup(TOOL_GROUP_ID);
    if (!toolGroup) {
      toolGroup = createDefaultToolGroup();
    }
    toolGroup.addViewport(viewportIdRef.current, renderingEngineIdRef.current);

    await viewport.setStack([imageId]);
    viewport.render();
    setViewportReady(true);
  }, []);

  const handleFile = useCallback(
    async (file: File) => {
      setFileName(file.name);
      onFileSelected?.(file);
      // Revoke previous object URL to prevent memory leak
      if (objectUrlRef.current) {
        URL.revokeObjectURL(objectUrlRef.current);
      }
      const objectUrl = URL.createObjectURL(file);
      objectUrlRef.current = objectUrl;
      const imageId = `wadouri:${objectUrl}`;
      await setupViewport(imageId);
    },
    [onFileSelected, setupViewport]
  );

  useEffect(() => {
    if (dicomFileUrl && dicomFileUrl.trim() !== "") {
      const imageId = dicomFileUrl.startsWith("wadouri:")
        ? dicomFileUrl
        : `wadouri:${dicomFileUrl}`;
      setupViewport(imageId);
      setFileName(dicomFileUrl.split("/").pop() || dicomFileUrl);
    }
    return () => {
      cleanup();
      if (objectUrlRef.current) {
        URL.revokeObjectURL(objectUrlRef.current);
        objectUrlRef.current = null;
      }
    };
  }, [dicomFileUrl, setupViewport, cleanup]);

  const onDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const onInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const opacityLabel =
    heatmapOpacity >= 70
      ? t("viewer.heatmapOpacityHigh")
      : heatmapOpacity >= 40
        ? t("viewer.heatmapOpacityMedium")
        : t("viewer.heatmapOpacityLow");

  return (
    <div className="flex flex-col gap-3 w-full flex-1 min-h-0">
      <div
        ref={elementRef}
        onDrop={onDrop}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        role="button"
        tabIndex={0}
        aria-label={t("viewer.ariaLabel")}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            const input = e.currentTarget.querySelector('input[type="file"]') as HTMLInputElement | null;
            input?.click();
          }
        }}
        className={[
          "relative flex flex-1 min-h-0 w-full items-center justify-center rounded-xl border-2 border-dashed",
          "bg-slate-900 transition-colors overflow-hidden",
          isDragging ? "border-cyan-400 bg-slate-800" : "border-slate-600",
          viewportReady ? "border-solid border-slate-700" : "",
        ].join(" ")}
      >
        {!viewportReady && previewCase && (
          <SyntheticCtaPreview
            previewCase={previewCase}
            heatmapEnabled={syntheticHeatmapEnabled}
            windowPreset={windowPreset}
            onWindowPresetChange={setWindowPreset}
          />
        )}

        {!viewportReady && !previewCase && (
          <div className="text-center text-slate-500 select-none absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            {fileName ? (
              <p className="text-sm text-slate-300 font-mono">{fileName}</p>
            ) : (
              <>
                <p className="text-4xl mb-2">&#x2B06;</p>
                <p className="text-sm">{t("viewer.dropHere")}</p>
                <p className="text-xs mt-1">{t("viewer.orSelect")}</p>
              </>
            )}
          </div>
        )}

        {heatmap && viewportReady && (
          <HeatmapOverlay heatmap={heatmap} opacity={heatmapOpacity} />
        )}
      </div>

      {!viewportReady && previewCase && (
        <div className="flex flex-wrap items-center gap-2 bg-slate-900/80 px-3 py-2 rounded shrink-0">
          <button
            type="button"
            onClick={() => setSyntheticHeatmapEnabled((value) => !value)}
            className={[
              "rounded border px-3 py-1.5 text-xs font-semibold transition-colors",
              syntheticHeatmapEnabled
                ? "border-orange-500/50 bg-orange-950/40 text-orange-300"
                : "border-slate-700 bg-slate-800 text-slate-400",
            ].join(" ")}
          >
            {t("viewer.heatmap")} {syntheticHeatmapEnabled ? t("viewer.heatmapOn") : t("viewer.heatmapOff")}
          </button>
          <span className="text-xs text-slate-500">
            {t("viewer.syntheticPreview")}
          </span>
        </div>
      )}

      {heatmap && viewportReady && (
        <div className="flex items-center gap-2 bg-slate-900/80 px-3 py-2 rounded shrink-0">
          <span className="text-xs text-slate-300">{t("viewer.heatmap")}</span>
          <input
            type="range"
            min={0}
            max={100}
            value={heatmapOpacity}
            onChange={(e) => setHeatmapOpacity(Number(e.target.value))}
            className="flex-1 accent-cyan-500 w-32"
          />
          <span className="text-xs text-slate-300 w-8 text-right">
            {opacityLabel}
          </span>
        </div>
      )}

      <label className="cursor-pointer self-start shrink-0">
        <span className="rounded-lg bg-slate-700 px-4 py-2 text-sm text-slate-200 hover:bg-slate-600 transition-colors">
          {t("viewer.selectFile")}
        </span>
        <input
          type="file"
          accept=".dcm,application/dicom"
          className="sr-only"
          onChange={onInputChange}
        />
      </label>
    </div>
  );
}
