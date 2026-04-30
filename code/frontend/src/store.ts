import { create } from "zustand";

import { InferenceResponse } from "./types";

interface AppState {
  selectedCaseId: string | null;
  setSelectedCaseId: (id: string | null) => void;
  currentPrediction: InferenceResponse | null;
  setCurrentPrediction: (p: InferenceResponse | null) => void;
  decisionTreeDraft: Record<string, unknown> | null;
  setDecisionTreeDraft: (d: Record<string, unknown> | null) => void;
  walkthroughSeen: boolean;
  setWalkthroughSeen: (seen: boolean) => void;
}

function getInitialWalkthroughSeen(): boolean {
  try {
    return localStorage.getItem("carotis:walkthroughSeen") === "true";
  } catch {
    return false;
  }
}

export const useStore = create<AppState>((set) => ({
  selectedCaseId: null,
  setSelectedCaseId: (id) => set({ selectedCaseId: id }),
  currentPrediction: null,
  setCurrentPrediction: (p) => set({ currentPrediction: p }),
  decisionTreeDraft: null,
  setDecisionTreeDraft: (d) => set({ decisionTreeDraft: d }),
  walkthroughSeen: getInitialWalkthroughSeen(),
  setWalkthroughSeen: (seen) => {
    try {
      localStorage.setItem("carotis:walkthroughSeen", String(seen));
    } catch { /* ignore */ }
    set({ walkthroughSeen: seen });
  },
}));
