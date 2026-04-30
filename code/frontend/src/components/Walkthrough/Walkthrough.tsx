import { useCallback, useEffect, useState } from "react";
import { useStore } from "@/store";
import { apiClient } from "@/lib/apiClient";
import { WalkthroughStep, type StepConfig } from "./WalkthroughStep";

const STEPS: StepConfig[] = [
  {
    targetSelector: "header",
    title: "Willkommen bei Carotis-AI",
    description:
      "Diese 5-Schritt-Tour zeigt Ihnen die wichtigsten Funktionen des Systems. Carotis-AI ist ein lokales, erklaerbares KI-System zur Carotis-Stenose-Diagnostik.",
    position: "bottom",
  },
  {
    targetSelector: "[data-walkthrough='dicom-viewer']",
    title: "DICOM-Upload",
    description:
      "Laden Sie eine DICOM-Datei per Drag & Drop oder Dateiauswahl. Alle Daten verarbeiten sich lokal auf Ihrem Geraet — keine Daten verlassen das Klinikum.",
    position: "right",
  },
  {
    targetSelector: "[data-walkthrough='ai-panel']",
    title: "KI-Analyse",
    description:
      "Das MFSD-UNet-Modell quantifiziert die Stenose nach NASCET und zeigt Konfidenz sowie Vulnerability-Marker. Der Trust-Score zeigt, wie sehr das Modell seiner eigenen Einschaetzung vertraut.",
    position: "left",
  },
  {
    targetSelector: "[data-walkthrough='dicom-viewer']",
    title: "XAI-Erklaerbarkeit",
    description:
      "Nach der Analyse zeigt HiResCAM pixelgenau, welche Regionen das Modell fuer die Entscheidung herangezogen hat. Die Heatmap-Transparenz ist ueber den Schieberegler einstellbar.",
    position: "right",
  },
  {
    targetSelector: "[data-walkthrough='ai-panel']",
    title: "Decision-Tree-Harvesting",
    description:
      "Nach der Analyse wird die aerztliche Begruendung anonymisiert erfasst und fliesst in den Daily-Learning-Corpus ein. Damit lernt das Modell nicht nur das Bild, sondern die aerztliche Entscheidung.",
    position: "left",
  },
];

export function Walkthrough() {
  const walkthroughSeen = useStore((s) => s.walkthroughSeen);
  const setWalkthroughSeen = useStore((s) => s.setWalkthroughSeen);
  const [active, setActive] = useState(!walkthroughSeen);
  const [currentStep, setCurrentStep] = useState(0);
  const [spotlightPos, setSpotlightPos] = useState<{
    top: number;
    left: number;
    width: number;
    height: number;
  } | null>(null);

  const step = STEPS[currentStep];

  // Calculate spotlight position based on target element
  useEffect(() => {
    if (!active) return;

    const updateSpotlight = () => {
      const target = document.querySelector(step.targetSelector);
      if (target) {
        const rect = target.getBoundingClientRect();
        const padding = 8;
        setSpotlightPos({
          top: rect.top - padding,
          left: rect.left - padding,
          width: rect.width + padding * 2,
          height: rect.height + padding * 2,
        });
      } else {
        // Center fallback
        setSpotlightPos({
          top: window.innerHeight / 2 - 100,
          left: window.innerWidth / 2 - 150,
          width: 300,
          height: 200,
        });
      }
    };

    updateSpotlight();
    window.addEventListener("resize", updateSpotlight);
    window.addEventListener("scroll", updateSpotlight, true);

    // Re-check after a short delay for dynamic content
    const timeout = setTimeout(updateSpotlight, 300);

    return () => {
      window.removeEventListener("resize", updateSpotlight);
      window.removeEventListener("scroll", updateSpotlight, true);
      clearTimeout(timeout);
    };
  }, [active, step]);

  const handleNext = useCallback(() => {
    apiClient.logWalkthroughStep(currentStep, "next");
    if (currentStep >= STEPS.length - 1) {
      setActive(false);
      setWalkthroughSeen(true);
      apiClient.logWalkthroughStep(STEPS.length - 1, "finish");
    } else {
      setCurrentStep((s) => s + 1);
    }
  }, [currentStep, setWalkthroughSeen]);

  const handlePrev = useCallback(() => {
    apiClient.logWalkthroughStep(currentStep, "prev");
    setCurrentStep((s) => Math.max(0, s - 1));
  }, [currentStep]);

  const handleSkip = useCallback(() => {
    apiClient.logWalkthroughStep(currentStep, "skip");
    setActive(false);
    setWalkthroughSeen(true);
  }, [currentStep, setWalkthroughSeen]);

  // Keyboard navigation
  useEffect(() => {
    if (!active) return;

    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        handleSkip();
      } else if (e.key === "ArrowRight" || e.key === "Enter") {
        handleNext();
      } else if (e.key === "ArrowLeft") {
        handlePrev();
      }
    };

    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [active, handleNext, handlePrev, handleSkip]);

  // Prevent body scroll when walkthrough is active
  useEffect(() => {
    if (active) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [active]);

  const restartWalkthrough = useCallback(() => {
    apiClient.logWalkthroughStep(0, "start");
    setCurrentStep(0);
    setActive(true);
  }, []);

  const isLast = currentStep === STEPS.length - 1;

  // Expose restart function globally for dev/debug
  useEffect(() => {
    (window as unknown as Record<string, unknown>).__restartWalkthrough =
      restartWalkthrough;
    return () => {
      delete (window as unknown as Record<string, unknown>)
        .__restartWalkthrough;
    };
  }, [restartWalkthrough]);

  if (!active) {
    return (
      <button
        onClick={restartWalkthrough}
        className="fixed bottom-4 right-4 z-50 rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 text-xs text-slate-400 hover:text-slate-200 hover:border-slate-500 transition-colors shadow-lg"
        title="Tour neustarten"
        aria-label="Walkthrough-Tour neustarten"
      >
        ? Tour
      </button>
    );
  }

  return (
    <div className="fixed inset-0 z-50" aria-label="Walkthrough-Tour">
      {/* Dark overlay */}
      <div className="absolute inset-0 bg-slate-950/80 transition-opacity" />

      {/* Spotlight */}
      {spotlightPos && (
        <div
          className="absolute rounded-xl transition-all duration-300 pointer-events-none"
          style={{
            top: spotlightPos.top,
            left: spotlightPos.left,
            width: spotlightPos.width,
            height: spotlightPos.height,
            boxShadow: "0 0 0 9999px rgba(2, 6, 23, 0.75)",
            border: "2px solid rgb(6, 182, 212)",
          }}
        />
      )}

      {/* Step card */}
      <WalkthroughStep
        step={step}
        stepIndex={currentStep}
        totalSteps={STEPS.length}
        onNext={handleNext}
        onPrev={handlePrev}
        onSkip={handleSkip}
        isLast={isLast}
      />
    </div>
  );
}
