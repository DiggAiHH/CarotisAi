import { useCallback, useEffect, useState } from "react";
import { useWalkthrough } from "./useWalkthrough";
import { WalkthroughStep } from "./WalkthroughStep";

export function Walkthrough() {
  const [tryDemoPending, setTryDemoPending] = useState(false);

  const handleTryDemo = useCallback(() => {
    setTryDemoPending(true);
    const url = new URL(window.location.href);
    url.searchParams.set("tour", "0");
    window.location.href = url.toString();
  }, []);

  const { isActive, currentStep, totalSteps, steps, next, back, skip, restart } =
    useWalkthrough();

  const step = steps[currentStep];
  const isLast = currentStep === totalSteps - 1;

  // Keyboard navigation
  useEffect(() => {
    if (!isActive) return;

    const previousFocus = document.activeElement as HTMLElement | null;

    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.tagName === "SELECT" ||
        target.isContentEditable
      ) {
        return;
      }

      if (e.key === "Escape") {
        e.preventDefault();
        skip();
      } else if (e.key === "ArrowRight" || e.key === "Enter") {
        e.preventDefault();
        next();
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        back();
      }
    };

    window.addEventListener("keydown", onKey);
    return () => {
      window.removeEventListener("keydown", onKey);
      previousFocus?.focus();
    };
  }, [isActive, next, back, skip]);

  // Prevent body scroll when active
  useEffect(() => {
    if (isActive) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isActive]);

  if (!isActive) {
    return (
      <button
        onClick={restart}
        className="fixed bottom-4 right-4 z-50 rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 text-xs text-slate-400 hover:text-slate-200 hover:border-slate-500 transition-colors shadow-lg"
        title="Tour neustarten"
        aria-label="Walkthrough-Tour neustarten"
      >
        Tour
      </button>
    );
  }

  return (
    <div className="fixed inset-0 z-50" aria-label="Walkthrough-Tour" data-walkthrough-overlay="true">
      {/* Dark overlay */}
      <div className="absolute inset-0 bg-slate-950/55 transition-opacity" />

      {/* Spotlight for targeted steps */}
      {step.targetId && <Spotlight targetId={step.targetId} />}

      {/* Step card */}
      <WalkthroughStep
        step={step}
        stepIndex={currentStep}
        totalSteps={totalSteps}
        onNext={next}
        onBack={back}
        onSkip={skip}
        onTryDemo={tryDemoPending ? undefined : handleTryDemo}
        isLast={isLast}
      />
    </div>
  );
}

function Spotlight({ targetId }: { targetId: string }) {
  const [rect, setRect] = useState<DOMRect | null>(null);

  useEffect(() => {
    const update = () => {
      const el = document.querySelector(`[data-tour-id="${targetId}"]`);
      setRect(el ? el.getBoundingClientRect() : null);
    };

    update();
    window.addEventListener("resize", update);
    window.addEventListener("scroll", update, true);
    const t = setTimeout(update, 300);

    return () => {
      window.removeEventListener("resize", update);
      window.removeEventListener("scroll", update, true);
      clearTimeout(t);
    };
  }, [targetId]);

  if (!rect) return null;

  const padding = 8;
  const top = rect.top - padding;
  const left = rect.left - padding;
  const width = rect.width + padding * 2;
  const height = rect.height + padding * 2;

  return (
    <div
      className="absolute rounded-xl transition-all duration-300 pointer-events-none"
      style={{
        top,
        left,
        width,
        height,
        boxShadow: "0 0 0 9999px rgba(2, 6, 23, 0.55)",
        border: "2px solid rgb(52, 211, 153)",
      }}
    />
  );
}
