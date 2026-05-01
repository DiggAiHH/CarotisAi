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
  physicianRoleHash: string | null;
  setPhysicianRoleHash: (hash: string | null) => void;
}

function getInitialWalkthroughSeen(): boolean {
  try {
    return localStorage.getItem("carotis:walkthroughSeen") === "true";
  } catch {
    return false;
  }
}

function getStoredRoleHash(): string | null {
  try {
    return localStorage.getItem("carotis:roleHash");
  } catch {
    return null;
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
  physicianRoleHash: getStoredRoleHash(),
  setPhysicianRoleHash: (hash) => {
    try {
      if (hash) localStorage.setItem("carotis:roleHash", hash);
      else localStorage.removeItem("carotis:roleHash");
    } catch { /* ignore */ }
    set({ physicianRoleHash: hash });
  },
}));
