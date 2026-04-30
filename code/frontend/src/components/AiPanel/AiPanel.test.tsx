import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { AiPanel } from "./AiPanel";

const mockResult = {
  case_id: "abc123",
  stenosis_pct_nascet: 65.5,
  confidence: 0.87,
  confidence_bucket: "high" as const,
  trust_score: 0.82,
  calibrated: true,
  vulnerability_markers: {
    intraplaque_hemorrhage: 0.3,
    thin_fibrous_cap: 0.6,
    lipid_rich_necrotic_core: 0.4,
    systolic_motion_anomaly: 0.1,
  },
  model_version: "v0.3.2",
  model_sha: "abc123d",
  audit_id: "audit-1",
  captured_at: "2026-04-30T12:00:00Z",
  heatmap_b64: null,
};

describe("AiPanel", () => {
  it("renders stenosis percentage", () => {
    render(<AiPanel result={mockResult} />);
    expect(screen.getByText("65.5%")).toBeInTheDocument();
  });

  it("shows severity label", () => {
    render(<AiPanel result={mockResult} />);
    expect(screen.getByText("Mittelgradig")).toBeInTheDocument();
  });

  it("renders placeholder when no result", () => {
    render(<AiPanel />);
    expect(
      screen.getByText(/Keine Vorhersage vorhanden/)
    ).toBeInTheDocument();
  });
});
