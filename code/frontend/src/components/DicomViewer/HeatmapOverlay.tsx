import { useEffect, useRef } from "react";

interface Props {
  heatmap: number[][];
  opacity?: number;
}

export function HeatmapOverlay({ heatmap, opacity = 50 }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !heatmap) return;

    const rows = heatmap.length;
    const cols = heatmap[0]?.length || 0;
    if (rows === 0 || cols === 0) return;

    canvas.width = cols;
    canvas.height = rows;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

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
  }, [heatmap]);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none mix-blend-screen"
      style={{ opacity: opacity / 100 }}
    />
  );
}
