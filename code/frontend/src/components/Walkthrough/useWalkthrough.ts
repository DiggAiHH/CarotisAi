import { useCallback, useEffect, useState } from "react";

export interface TourStep {
  id: string;
  title: string;
  text: string;
  targetId?: string;
  position?: "top" | "bottom" | "left" | "right";
}

export const TOUR_STEPS: TourStep[] = [
  {
    id: "welcome",
    title: "Willkommen bei Carotis-AI",
    text: "Diese Tour zeigt Ihnen in 3 Minuten, wie das System einen CTA-Datensatz analysiert. Sie koennen jederzeit ueberspringen.",
  },
  {
    id: "dicom",
    title: "Schritt 1 — Synthetischer Fall geladen",
    text: "Hier sehen Sie einen synthetischen CTA-Datensatz. Die App laeuft mit anonymisierten Demo-Faellen — keine echten Patientendaten.",
    targetId: "tour-dicom-viewer",
    position: "right",
  },
  {
    id: "ai",
    title: "Schritt 2 — KI-Vorschlag mit Vertrauenswert",
    text: "Das Modell schaetzt Stenosegrad nach NASCET, Plaque-Vulnerability und liefert einen Trust-Score. Die HiResCAM-Heatmap zeigt, worauf das Modell sich stuetzt.",
    targetId: "tour-ai-panel",
    position: "left",
  },
  {
    id: "decision",
    title: "Schritt 3 — Ihre Entscheidung in 30 Sekunden",
    text: "Bestaetigen oder korrigieren Sie den Vorschlag. Ihre Begruendung wird anonymisiert gespeichert und am naechsten Tag fliesst sie ins Modell-Update.",
    targetId: "tour-decision-form",
    position: "left",
  },
  {
    id: "done",
    title: "Tour abgeschlossen",
    text: "Sie haben gerade einen kompletten Befundungsvorgang gesehen. Der reale Workflow im Klinikum waere identisch — nur mit echten DICOM-Daten via PVS. Fragen? Kontakt: aroob.alrawashdeh@klinikumdo.de",
  },
];

const STORAGE_KEY = "carotis_tour_done";

function getDemoToken(): string | null {
  try {
    return localStorage.getItem("carotis:demoToken");
  } catch {
    return null;
  }
}

async function checkRohdeLabel(): Promise<boolean> {
  const token = getDemoToken();
  if (!token) return false;
  try {
    const baseUrl = import.meta.env.VITE_API_URL as string;
    const apiKey = import.meta.env.VITE_API_KEY as string;
    const res = await fetch(`${baseUrl}/api/v1/demo/whoami`, {
      headers: {
        "X-API-Key": apiKey,
        "X-Demo-Token": token,
      },
    });
    if (!res.ok) return false;
    const data = (await res.json()) as { label?: string };
    return typeof data.label === "string" && data.label.startsWith("rohde-");
  } catch {
    return false;
  }
}

export interface UseWalkthroughReturn {
  isActive: boolean;
  currentStep: number;
  totalSteps: number;
  steps: TourStep[];
  next: () => void;
  back: () => void;
  skip: () => void;
  done: () => void;
  restart: () => void;
}

export function useWalkthrough(onDone?: () => void): UseWalkthroughReturn {
  const [isActive, setIsActive] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  useEffect(() => {
    let cancelled = false;
    const init = async () => {
      const params = new URLSearchParams(window.location.search);
      const forcedTour = params.get("tour") === "1";
      const alreadyDone = localStorage.getItem(STORAGE_KEY) === "true";

      if (forcedTour) {
        if (!cancelled) {
          setIsActive(true);
          setCurrentStep(0);
        }
        return;
      }

      if (alreadyDone) {
        return;
      }

      const isRohde = await checkRohdeLabel();
      if (!cancelled) {
        setIsActive(isRohde);
        setCurrentStep(0);
      }
    };

    init();
    return () => {
      cancelled = true;
    };
  }, []);

  const finish = useCallback(() => {
    setIsActive(false);
    try {
      localStorage.setItem(STORAGE_KEY, "true");
    } catch { /* ignore */ }
    onDone?.();
  }, [onDone]);

  const next = useCallback(() => {
    setCurrentStep((s) => {
      if (s >= TOUR_STEPS.length - 1) {
        finish();
        return s;
      }
      return s + 1;
    });
  }, [finish]);

  const back = useCallback(() => {
    setCurrentStep((s) => Math.max(0, s - 1));
  }, []);

  const skip = useCallback(() => {
    finish();
  }, [finish]);

  const done = useCallback(() => {
    finish();
  }, [finish]);

  const restart = useCallback(() => {
    setCurrentStep(0);
    setIsActive(true);
  }, []);

  return {
    isActive,
    currentStep,
    totalSteps: TOUR_STEPS.length,
    steps: TOUR_STEPS,
    next,
    back,
    skip,
    done,
    restart,
  };
}
