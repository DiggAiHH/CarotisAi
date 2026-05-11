import { useEffect, useRef, useState } from "react";

export interface StepConfig {
  targetSelector: string;
  title: string;
  description: string;
  position?: "top" | "bottom" | "left" | "right" | "center";
}

interface Props {
  step: StepConfig;
  stepIndex: number;
  totalSteps: number;
  onNext: () => void;
  onPrev: () => void;
  onSkip: () => void;
  isLast: boolean;
}

export function WalkthroughStep({
  step,
  stepIndex,
  totalSteps,
  onNext,
  onPrev,
  onSkip,
  isLast,
}: Props) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [cardPos, setCardPos] = useState<{ top: number; left: number }>({
    top: 0,
    left: 0,
  });

  useEffect(() => {
    const updatePosition = () => {
      const cardWidth = Math.min(352, window.innerWidth - 32);
      const cardHeight = cardRef.current?.offsetHeight || 220;
      const target = document.querySelector(step.targetSelector);

      if (!target) {
        setCardPos({
          top: Math.max(16, window.innerHeight / 2 - cardHeight / 2),
          left: Math.max(16, window.innerWidth / 2 - cardWidth / 2),
        });
        return;
      }

      const rect = target.getBoundingClientRect();
      const pos = step.position || "bottom";
      const margin = 16;
      let top = 0;
      let left = 0;

      switch (pos) {
        case "top":
          top = rect.top - cardHeight - margin;
          left = rect.left + rect.width / 2 - cardWidth / 2;
          break;
        case "bottom":
          top = rect.bottom + margin;
          left = rect.left + rect.width / 2 - cardWidth / 2;
          break;
        case "left":
          top = rect.top + rect.height / 2 - cardHeight / 2;
          left = rect.left - cardWidth - margin;
          break;
        case "right":
          top = rect.top + rect.height / 2 - cardHeight / 2;
          left = rect.right + margin;
          break;
        case "center":
        default:
          top = window.innerHeight / 2 - cardHeight / 2;
          left = window.innerWidth / 2 - cardWidth / 2;
          break;
      }

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
  }, [step]);

  return (
    <div
      ref={cardRef}
      className="fixed z-[60] w-[min(22rem,calc(100vw-2rem))] rounded-xl border border-slate-600 bg-slate-900 p-5 shadow-2xl transition-all duration-300"
      style={{ top: cardPos.top, left: cardPos.left }}
      role="dialog"
      aria-modal="true"
      aria-labelledby={`walkthrough-title-${stepIndex}`}
    >
      {/* Progress dots */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex gap-1.5">
          {Array.from({ length: totalSteps }).map((_, i) => (
            <div
              key={i}
              className={`h-1.5 rounded-full transition-all ${
                i === stepIndex
                  ? "w-4 bg-cyan-500"
                  : i < stepIndex
                    ? "w-1.5 bg-cyan-500/50"
                    : "w-1.5 bg-slate-600"
              }`}
            />
          ))}
        </div>
        <button
          onClick={onSkip}
          className="text-xs text-slate-500 hover:text-slate-300 transition-colors"
          aria-label="Tour überspringen"
        >
          Überspringen
        </button>
      </div>

      {/* Content */}
      <h3
        id={`walkthrough-title-${stepIndex}`}
        className="text-sm font-semibold text-slate-100 mb-2"
      >
        {step.title}
      </h3>
      <p className="text-xs text-slate-400 leading-relaxed mb-4">
        {step.description}
      </p>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <button
          onClick={onPrev}
          disabled={stepIndex === 0}
          className="text-xs text-slate-400 hover:text-slate-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors px-2 py-1 rounded"
        >
          Zurück
        </button>
        <span className="text-[10px] text-slate-600">
          Schritt {stepIndex + 1} von {totalSteps}
        </span>
        <button
          onClick={onNext}
          className="text-xs font-medium bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-1.5 rounded-lg transition-colors"
        >
          {isLast ? "Tour beenden" : "Weiter"}
        </button>
      </div>
    </div>
  );
}
