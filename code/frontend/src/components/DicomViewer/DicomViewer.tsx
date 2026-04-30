import { useCallback, useEffect, useRef, useState } from "react";

import { RenderingEngine, Types, Enums } from "@cornerstonejs/core";
import { ToolGroupManager } from "@cornerstonejs/tools";
import { initCornerstone, createDefaultToolGroup, TOOL_GROUP_ID } from "../../lib/cornerstoneSetup";
import { HeatmapOverlay } from "./HeatmapOverlay";
import { t } from "../../lib/i18n";

interface Props {
  dicomFileUrl?: string;
  heatmap?: number[][];
  onFileSelected?: (file: File) => void;
}

export function DicomViewer({ dicomFileUrl, heatmap, onFileSelected }: Props) {
  const elementRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [viewportReady, setViewportReady] = useState(false);
  const [heatmapOpacity, setHeatmapOpacity] = useState(50);
  const engineRef = useRef<RenderingEngine | null>(null);
  const viewportIdRef = useRef(`viewport-${Math.random().toString(36).slice(2)}`);
  const renderingEngineIdRef = useRef(`engine-${Math.random().toString(36).slice(2)}`);

  const cleanup = useCallback(() => {
    try {
      ToolGroupManager.destroyToolGroup(TOOL_GROUP_ID);
    } catch { /* ignore */ }
    if (engineRef.current) {
      engineRef.current.destroy();
      engineRef.current = null;
    }
  }, []);

  const setupViewport = useCallback(async (imageId: string) => {
    const el = elementRef.current;
    if (!el) return;

    cleanup();
    await initCornerstone();

    const renderingEngine = new RenderingEngine(renderingEngineIdRef.current);
    engineRef.current = renderingEngine;

    const viewportInput: Types.PublicViewportInput = {
      viewportId: viewportIdRef.current,
      element: el,
      type: Enums.ViewportType.STACK,
    };

    renderingEngine.enableElement(viewportInput);
    const viewport = renderingEngine.getViewport(viewportIdRef.current) as Types.IStackViewport;

    const toolGroup = createDefaultToolGroup();
    toolGroup.addViewport(viewportIdRef.current, renderingEngineIdRef.current);

    await viewport.setStack([imageId]);
    viewport.render();
    setViewportReady(true);
  }, [cleanup]);

  const handleFile = useCallback(
    async (file: File) => {
      setFileName(file.name);
      onFileSelected?.(file);
      const objectUrl = URL.createObjectURL(file);
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
    return () => cleanup();
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

  return (
    <div className="flex flex-col gap-3 w-full h-full">
      <div
        ref={elementRef}
        onDrop={onDrop}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        className={[
          "relative flex h-full w-full items-center justify-center rounded-xl border-2 border-dashed",
          "bg-slate-900 transition-colors overflow-hidden",
          isDragging ? "border-cyan-400 bg-slate-800" : "border-slate-600",
          viewportReady ? "border-solid border-slate-700" : "",
        ].join(" ")}
      >
        {!viewportReady && (
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
            {heatmapOpacity}%
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
