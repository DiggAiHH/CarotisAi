/**
 * Grad-CAM heatmap overlay rendered on top of the DICOM canvas.
 *
 * The backend returns a base64-encoded PNG (base64: string).
 * We render it as a semi-transparent <img> positioned absolutely over the viewer.
 */
interface Props {
  gradcamB64: string;
  visible: boolean;
}

export function GradCamOverlay({ gradcamB64, visible }: Props) {
  if (!visible || !gradcamB64) return null;

  return (
    <div className="pointer-events-none absolute inset-0">
      <img
        src={`data:image/png;base64,${gradcamB64}`}
        alt="Grad-CAM Heatmap"
        className="h-full w-full object-cover opacity-60 rounded-xl"
      />
    </div>
  );
}
