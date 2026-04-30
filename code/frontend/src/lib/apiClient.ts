import {
  DecisionTreeRequest,
  HealthResponse,
  InferenceResponse,
} from "../types";

const API_KEY = import.meta.env.VITE_API_KEY as string;
const BASE_URL = import.meta.env.VITE_API_URL as string;
const API_PREFIX = "/api/v1";

function getDemoToken(): string | null {
  try {
    return localStorage.getItem("carotis:demoToken");
  } catch {
    return null;
  }
}

async function fetchJson(input: string, init?: RequestInit) {
  const headers = new Headers(init?.headers);
  headers.set("X-API-Key", API_KEY);
  headers.set("Content-Type", "application/json");
  const demoToken = getDemoToken();
  if (demoToken) headers.set("X-Demo-Token", demoToken);

  const res = await fetch(`${BASE_URL}${input}`, {
    ...init,
    headers,
  });

  if (res.status === 401) {
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }
  if (res.status === 429) {
    window.alert("Rate-Limit erreicht. Bitte warten Sie einen Moment.");
    throw new Error("Rate limited");
  }
  if (res.status === 503) {
    window.alert("Modell nicht geladen. Bitte kontaktieren Sie den Admin.");
    throw new Error("Model not loaded");
  }
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
}

export const apiClient = {
  getHealth: async (): Promise<HealthResponse> => {
    return fetchJson("/health", { method: "GET" });
  },

  predict: async (file: File): Promise<InferenceResponse> => {
    const form = new FormData();
    form.append("file", file);
    const headers = new Headers();
    headers.set("X-API-Key", API_KEY);
    const demoToken = getDemoToken();
    if (demoToken) headers.set("X-Demo-Token", demoToken);
    const res = await fetch(`${BASE_URL}${API_PREFIX}/inference/predict`, {
      method: "POST",
      headers,
      body: form,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },

  captureDecisionTree: async (
    payload: DecisionTreeRequest
  ): Promise<{ audit_id: string; status: string }> => {
    return fetchJson(`${API_PREFIX}/decision-tree/capture`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  checkText: async (
    text: string
  ): Promise<{
    is_clean: boolean;
    pii_spans: Array<{ start: number; end: number; label: string }>;
  }> => {
    return fetchJson(`${API_PREFIX}/decision-tree/check-text`, {
      method: "POST",
      body: JSON.stringify({ text }),
    });
  },

  logWalkthroughStep: async (
    stepId: number,
    event: "start" | "next" | "prev" | "skip" | "finish"
  ): Promise<void> => {
    try {
      await fetchJson(`${API_PREFIX}/demo/log-walkthrough-step`, {
        method: "POST",
        body: JSON.stringify({ step_id: stepId, event }),
      });
    } catch {
      // Silently ignore — walkthrough tracking is best-effort
    }
  },
};
