import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { AiPanel } from "./AiPanel";

const mockResult = {
  case_id: "abc123",
  confidence_bucket: "high" as const,
  trust_score: 0.82,
  calibrated: true,
  model_version: "v0.3.2",
  model_sha: "abc123d",
  audit_id: "audit-1",
  captured_at: "2026-04-30T12:00:00Z",
  heatmap_b64: null,
};

describe("AiPanel", () => {
  it("renders research overlay focus", () => {
    render(<AiPanel result={mockResult} />);
    expect(screen.getAllByText("Hoch").length).toBeGreaterThan(0);
  });

  it("shows overlay focus label", () => {
    render(<AiPanel result={mockResult} />);
    expect(screen.getByText("Starker Overlay-Fokus")).toBeInTheDocument();
  });

  it("renders placeholder when no result", () => {
    render(<AiPanel />);
    expect(
      screen.getByText(/Keine Analyse vorhanden/)
    ).toBeInTheDocument();
  });

  it("does not require quantitative CDS fields", () => {
    render(<AiPanel result={mockResult} />);
    expect(screen.getByText(/Entscheidungsmodul deaktiviert/)).toBeInTheDocument();
  });
});
