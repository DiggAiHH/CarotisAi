import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { ResearchSplashGate } from "./ResearchSplashGate";

const ZWECKBESTIMMUNG_VERSION = "zweckbestimmung_2026-05-06";

describe("ResearchSplashGate", () => {
  beforeEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
    global.fetch = vi.fn(() =>
      Promise.resolve(new Response(null, { status: 200 })),
    ) as unknown as typeof fetch;
  });

  it("blocks children until confirmation", () => {
    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    expect(screen.queryByText("protected")).not.toBeInTheDocument();
    expect(screen.getByText(/Forschungs-Bestätigung/i)).toBeInTheDocument();
  });

  it("shows RESEARCH USE ONLY watermark", () => {
    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    expect(
      screen.getByText(/RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt/i),
    ).toBeInTheDocument();
  });

  it("renders all three required checkboxes with wording from Master-Zweckbestimmung", () => {
    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    expect(
      screen.getByText(/ausschließlich zu Forschungszwecken/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/eigenständig und stütze sie nicht/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/keine Werkzeug-Ausgaben in Patientenakten/i),
    ).toBeInTheDocument();
  });

  it("confirm button is disabled until all three boxes checked", () => {
    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    const button = screen.getByRole("button", { name: /Ich bestätige/i });
    expect(button).toBeDisabled();

    const checkboxes = screen.getAllByRole("checkbox");
    fireEvent.click(checkboxes[0]);
    fireEvent.click(checkboxes[1]);
    expect(button).toBeDisabled();
    fireEvent.click(checkboxes[2]);
    expect(button).not.toBeDisabled();
  });

  it("unlocks children after confirmation and persists in sessionStorage", async () => {
    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    const checkboxes = screen.getAllByRole("checkbox");
    checkboxes.forEach((cb) => fireEvent.click(cb));
    fireEvent.click(screen.getByRole("button", { name: /Ich bestätige/i }));

    await waitFor(() => {
      expect(screen.getByText("protected")).toBeInTheDocument();
    });
    expect(sessionStorage.getItem("carotis_splash_confirmed")).toBe(
      ZWECKBESTIMMUNG_VERSION,
    );
  });

  it("does not show dialog if sessionStorage already has confirmation", () => {
    sessionStorage.setItem("carotis_splash_confirmed", ZWECKBESTIMMUNG_VERSION);
    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    expect(screen.getByText("protected")).toBeInTheDocument();
    expect(screen.queryByText(/Forschungs-Bestätigung/i)).not.toBeInTheDocument();
  });

  it("shows session-end screen on abort", () => {
    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    fireEvent.click(screen.getByRole("button", { name: /Abbrechen/i }));
    expect(screen.getByText(/Sitzung beendet/i)).toBeInTheDocument();
    expect(screen.queryByText("protected")).not.toBeInTheDocument();
  });

  it("posts confirmation to backend audit endpoint with version tag and no PII", async () => {
    import.meta.env.VITE_API_URL = "http://localhost:8000";
    const fetchSpy = vi.fn(() =>
      Promise.resolve(new Response(null, { status: 200 })),
    );
    global.fetch = fetchSpy as unknown as typeof fetch;

    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    const checkboxes = screen.getAllByRole("checkbox");
    checkboxes.forEach((cb) => fireEvent.click(cb));
    fireEvent.click(screen.getByRole("button", { name: /Ich bestätige/i }));

    await waitFor(() => {
      expect(fetchSpy).toHaveBeenCalled();
    });

    const callArgs = fetchSpy.mock.calls[0] as unknown as [string, RequestInit];
    expect(callArgs[0]).toMatch(/\/api\/v1\/audit\/splash-confirmation$/);
    const init = callArgs[1];
    expect(init.method).toBe("POST");
    const body = JSON.parse(init.body as string);
    expect(body.version).toBe(ZWECKBESTIMMUNG_VERSION);
    expect(body.session_id).toBeDefined();
    expect(body.role_hash).toBeDefined();
    expect(body.confirmed_at).toBeDefined();
    // Pflicht: kein PII im Payload
    expect(body.patient_name).toBeUndefined();
    expect(body.patient_id).toBeUndefined();
    expect(body.user_email).toBeUndefined();
    expect(body.user_id).toBeUndefined();
    expect(body.token).toBeUndefined();
  });

  it("still unlocks children if audit backend is unreachable (fail-open for UX)", async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error("network"))) as unknown as typeof fetch;
    render(
      <ResearchSplashGate>
        <div>protected</div>
      </ResearchSplashGate>,
    );
    const checkboxes = screen.getAllByRole("checkbox");
    checkboxes.forEach((cb) => fireEvent.click(cb));
    fireEvent.click(screen.getByRole("button", { name: /Ich bestätige/i }));

    await waitFor(() => {
      expect(screen.getByText("protected")).toBeInTheDocument();
    });
  });
});
