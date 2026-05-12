import { useEffect, useRef, useState } from "react";

export interface StepConfig {
  targetId?: string;
  title: string;
  text: string;
  position?: "top" | "bottom" | "left" | "right";
}

interface Props {
  step: StepConfig;
  stepIndex: number;
  totalSteps: number;
  onNext: () => void;
  onBack: () => void;
  onSkip: () => void;
  onTryDemo?: () => void;
  isLast: boolean;
}

export function WalkthroughStep({
  step,
  stepIndex,
  totalSteps,
  onNext,
  onBack,
  onSkip,
  onTryDemo,
  isLast,
}: Props) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [cardPos, setCardPos] = useState<{ top: number; left: number } | null>(null);
  const [arrowDir, setArrowDir] = useState<"top" | "bottom" | "left" | "right" | null>(null);
  const isModal = !step.targetId;

  useEffect(() => {
    const updatePosition = () => {
      if (isModal) {
        setCardPos(null);
        setArrowDir(null);
        return;
      }

      const cardWidth = Math.min(384, window.innerWidth - 32);
      const cardHeight = cardRef.current?.offsetHeight || 240;
      const target = document.querySelector(`[data-tour-id="${step.targetId}"]`);

      if (!target) {
        // Fallback to center if target not found
        setCardPos({
          top: Math.max(16, window.innerHeight / 2 - cardHeight / 2),
          left: Math.max(16, window.innerWidth / 2 - cardWidth / 2),
        });
        setArrowDir(null);
        return;
      }

      const rect = target.getBoundingClientRect();
      const margin = 16;
      const pos = step.position || "bottom";
      let top = 0;
      let left = 0;

      switch (pos) {
        case "top":
          top = rect.top - cardHeight - margin - 8;
          left = rect.left + rect.width / 2 - cardWidth / 2;
          setArrowDir("bottom");
          break;
        case "bottom":
          top = rect.bottom + margin + 8;
          left = rect.left + rect.width / 2 - cardWidth / 2;
          setArrowDir("top");
          break;
        case "left":
          top = rect.top + rect.height / 2 - cardHeight / 2;
          left = rect.left - cardWidth - margin - 8;
          setArrowDir("right");
          break;
        case "right":
          top = rect.top + rect.height / 2 - cardHeight / 2;
          left = rect.right + margin + 8;
          setArrowDir("left");
          break;
        default:
          top = rect.bottom + margin + 8;
          left = rect.left + rect.width / 2 - cardWidth / 2;
          setArrowDir("top");
      }

      // Clamp to viewport
      top = Math.max(16, Math.min(top, window.innerHeight - cardHeight - 16));
      left = Math.max(16, Math.min(left, window.innerWidth - cardWidth - 16));
      setCardPos({ top, left });
    };

    updatePosition();
    window.addEventListener("resize", updatePosition);
    window.addEventListener("scroll", updatePosition, true);
    const timeout = setTimeout(updatePosition, 100);

    return () => {
      window.removeEventListener("resize", updatePosition);
      window.removeEventListener("scroll", updatePosition, true);
      clearTimeout(timeout);
    };
  }, [step, isModal]);

  const progressDots = (
    <div className="flex gap-1.5">
      {Array.from({ length: totalSteps }).map((_, i) => (
        <div
          key={i}
          className={`h-1.5 rounded-full transition-all ${
            i === stepIndex
              ? "w-4 bg-emerald-400"
              : i < stepIndex
                ? "w-1.5 bg-emerald-400/50"
                : "w-1.5 bg-slate-600"
          }`}
        />
      ))}
    </div>
  );

  const cardContent = (
    <>
      <div className="flex items-center justify-between mb-3">
        {progressDots}
        <button
          onClick={onSkip}
          className="text-xs text-slate-500 hover:text-slate-300 transition-colors"
          aria-label="Tour ueberspringen"
        >
          Ueberspringen
        </button>
      </div>

      <h3
        id={`walkthrough-title-${stepIndex}`}
        className="text-sm font-semibold text-slate-100 mb-2"
      >
        {step.title}
      </h3>
      <p className="text-xs text-slate-400 leading-relaxed mb-4">
        {step.text}
      </p>

      {isLast && onTryDemo && (
        <button
          onClick={onTryDemo}
          className="mb-3 w-full rounded-lg bg-emerald-600 hover:bg-emerald-500 px-4 py-2 text-xs font-medium text-white transition-colors"
        >
          Eigenen Demo-Fall ausprobieren
        </button>
      )}

      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          disabled={stepIndex === 0}
          className="text-xs text-slate-400 hover:text-slate-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors px-2 py-1 rounded"
        >
          Zurueck
        </button>
        <span className="text-[10px] text-slate-600">
          Schritt {stepIndex + 1} von {totalSteps}
        </span>
        <button
          onClick={onNext}
          className="text-xs font-medium bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-lg transition-colors"
        >
          {isLast ? "Fertig" : "Weiter"}
        </button>
      </div>
    </>
  );

  if (isModal) {
    return (
      <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
        <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm" />
        <div
          ref={cardRef}
          className="relative z-10 w-full max-w-md rounded-xl border border-slate-600 bg-slate-900 p-5 shadow-2xl"
          role="dialog"
          aria-modal="true"
          aria-labelledby={`walkthrough-title-${stepIndex}`}
        >
          {cardContent}
        </div>
      </div>
    );
  }

  const arrowClass =
    arrowDir === "top"
      ? "absolute -top-1.5 left-1/2 -translate-x-1/2 w-3 h-3 rotate-45 bg-slate-900 border-t border-l border-emerald-400"
      : arrowDir === "bottom"
        ? "absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 rotate-45 bg-slate-900 border-b border-r border-emerald-400"
        : arrowDir === "left"
          ? "absolute -left-1.5 top-1/2 -translate-y-1/2 w-3 h-3 rotate-45 bg-slate-900 border-t border-l border-emerald-400"
          : arrowDir === "right"
            ? "absolute -right-1.5 top-1/2 -translate-y-1/2 w-3 h-3 rotate-45 bg-slate-900 border-b border-r border-emerald-400"
            : "";

  return (
    <div
      ref={cardRef}
      className="fixed z-[60] w-[min(24rem,calc(100vw-2rem))] rounded-xl border border-emerald-400 bg-slate-900 p-5 shadow-2xl transition-all duration-300"
      style={
        cardPos
          ? { top: cardPos.top, left: cardPos.left }
          : { top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
      }
      role="dialog"
      aria-modal="true"
      aria-labelledby={`walkthrough-title-${stepIndex}`}
    >
      {arrowClass && <div className={arrowClass} />}
      {cardContent}
    </div>
  );
}
