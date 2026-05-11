/**
 * Watermark — globaler "RESEARCH USE ONLY"-Hinweis am Bildschirmrand.
 *
 * Quelle: memory/domain/zweckbestimmung_master_2026-05-06.md §D
 * Audit anchor: 2026-05-10 disclaimer audit G2
 *
 * Sichtbar auf jedem Screen nach Splash + AuthGate. Halbtransparent, nicht klickbar,
 * print-friendly (Display: inline beim Drucken).
 */

interface Props {
  /** optional override for unit testing */
  text?: string;
}

const DEFAULT_TEXT = "RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt";

export function Watermark({ text = DEFAULT_TEXT }: Props) {
  return (
    <div
      data-testid="research-watermark"
      role="note"
      aria-label="Forschungsverwendungs-Hinweis"
      className="fixed bottom-0 inset-x-0 z-50 pointer-events-none print:static print:bg-amber-100 print:text-amber-900"
    >
      <div className="mx-auto max-w-screen-2xl px-3 py-1 text-center text-[10px] sm:text-xs font-medium tracking-wide bg-amber-500/10 text-amber-200 border-t border-amber-500/30 backdrop-blur-sm">
        {text}
      </div>
    </div>
  );
}
