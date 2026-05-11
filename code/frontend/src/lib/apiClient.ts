import {
  DecisionTreeRequest,
  HealthResponse,
  InferenceResponse,
} from "../types";
import {
  ApiError,
  ModelNotLoadedError,
  RateLimitError,
  UnauthorizedError,
  ValidationError,
} from "./apiError";

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

async function fetchWithTimeout(
  input: string,
  init: RequestInit & { timeout?: number } = {}
): Promise<Response> {
  const { timeout = 30000, ...rest } = init;
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    // Merge caller's signal with timeout controller
    if (rest.signal) {
      rest.signal.addEventListener("abort", () => controller.abort());
      if (rest.signal.aborted) {
        controller.abort();
      }
    }
    const res = await fetch(input, { ...rest, signal: controller.signal });
    return res;
  } finally {
    clearTimeout(id);
  }
}

function handleErrorResponse(res: Response): never {
  if (res.status === 401) {
    throw new UnauthorizedError();
  }
  if (res.status === 429) {
    const retryAfter = parseInt(res.headers.get("Retry-After") || "60", 10);
    throw new RateLimitError("Rate limit erreicht. Bitte warten.", retryAfter);
  }
  if (res.status === 503) {
    throw new ModelNotLoadedError();
  }
  if (res.status === 422) {
    throw new ValidationError();
  }
  throw new ApiError(`HTTP ${res.status}`, res.status, `HTTP_${res.status}`);
}

async function fetchJson<T>(input: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  headers.set("X-API-Key", API_KEY);
  headers.set("Content-Type", "application/json");
  const demoToken = getDemoToken();
  if (demoToken) headers.set("X-Demo-Token", demoToken);

  const res = await fetchWithTimeout(`${BASE_URL}${input}`, {
    ...init,
    headers,
  });

  if (!res.ok) {
    handleErrorResponse(res);
  }
  return res.json() as Promise<T>;
}

async function fetchWithRetry<T>(
  input: string,
  init?: RequestInit,
  retries = 3
): Promise<T> {
  let lastError: Error | undefined;
  for (let i = 0; i <= retries; i++) {
    try {
      return await fetchJson<T>(input, init);
    } catch (err) {
      lastError = err as Error;
      // Retry on 503 (model not loaded) with exponential backoff
      if (err instanceof ModelNotLoadedError && i < retries) {
        await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, i)));
        continue;
      }
      // Retry on 429 if Retry-After header present
      if (err instanceof RateLimitError && err.retryAfter && i < retries) {
        await new Promise((r) => setTimeout(r, err.retryAfter * 1000));
        continue;
      }
      throw err;
    }
  }
  throw lastError!;
}

export const apiClient = {
  getHealth: async (): Promise<HealthResponse> => {
    return fetchJson("/health/", { method: "GET" });
  },

  predict: async (file: File): Promise<InferenceResponse> => {
    const form = new FormData();
    form.append("file", file);
    const headers = new Headers();
    headers.set("X-API-Key", API_KEY);
    const demoToken = getDemoToken();
    if (demoToken) headers.set("X-Demo-Token", demoToken);

    // Retry logic for model-loading transient failures
    let lastError: Error | undefined;
    for (let i = 0; i <= 3; i++) {
      try {
        const res = await fetchWithTimeout(
          `${BASE_URL}${API_PREFIX}/inference/predict`,
          { method: "POST", headers, body: form, timeout: 60000 }
        );
        if (!res.ok) handleErrorResponse(res);
        return (await res.json()) as InferenceResponse;
      } catch (err) {
        lastError = err as Error;
        if (err instanceof ModelNotLoadedError && i < 3) {
          await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, i)));
          continue;
        }
        if (err instanceof RateLimitError && (err as RateLimitError).retryAfter && i < 3) {
          await new Promise((r) => setTimeout(r, (err as RateLimitError).retryAfter * 1000));
          continue;
        }
        throw err;
      }
    }
    throw lastError!;
  },

  captureDecisionTree: async (
    payload: DecisionTreeRequest
  ): Promise<{ audit_id: string; status: string }> => {
    return fetchWithRetry(`${API_PREFIX}/decision-tree/capture`, {
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
        body: JSON.stringify({ step_id: String(stepId), event }),
      });
    } catch {
      // Silently ignore — walkthrough tracking is best-effort
    }
  },
};
