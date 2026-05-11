import { useEffect, useRef } from "react";

interface Props {
  /** 2-D array of values 0..1, OR base64 PNG string (data:image/png;base64,... or raw b64). */
  heatmap: number[][] | string;
  opacity?: number;
}

function drawNumberHeatmap(
  ctx: CanvasRenderingContext2D,
  heatmap: number[][],
  rows: number,
  cols: number
) {
  const imageData = ctx.createImageData(cols, rows);
  const data = imageData.data;

  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const val = heatmap[y]?.[x] ?? 0;
      const idx = (y * cols + x) * 4;
      // Jet colormap approximation: blue -> cyan -> yellow -> red
      const r = Math.min(255, Math.max(0, Math.round(val * 255 * 2 - 255)));
      const g = Math.min(255, Math.max(0, Math.round(val * 255 * 2)));
      const b = Math.min(255, Math.max(0, Math.round(255 - val * 255 * 2)));
      data[idx] = r;
      data[idx + 1] = g;
      data[idx + 2] = b;
      data[idx + 3] = 180; // alpha
    }
  }

  ctx.putImageData(imageData, 0, 0);
}

function drawBase64Heatmap(
  ctx: CanvasRenderingContext2D,
  canvas: HTMLCanvasElement,
  b64: string
) {
  const img = new Image();
  const cleanup = () => {
    img.onload = null;
    img.onerror = null;
  };
  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
    cleanup();
  };
  img.onerror = () => {
    cleanup();
  };
  img.src = b64.startsWith("data:") ? b64 : `data:image/png;base64,${b64}`;
}

export function HeatmapOverlay({ heatmap, opacity = 50 }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !heatmap) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    if (typeof heatmap === "string") {
      drawBase64Heatmap(ctx, canvas, heatmap);
    } else {
      const rows = heatmap.length;
      const cols = heatmap[0]?.length || 0;
      if (rows === 0 || cols === 0) return;
      canvas.width = cols;
      canvas.height = rows;
      drawNumberHeatmap(ctx, heatmap, rows, cols);
    }
  }, [heatmap]);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none mix-blend-screen"
      style={{ opacity: opacity / 100 }}
    />
  );
}
