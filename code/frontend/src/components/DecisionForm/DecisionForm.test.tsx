import { describe, expect, it } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { DecisionForm } from "./DecisionForm";

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

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

function Wrapper({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe("DecisionForm", () => {
  it("renders form title", () => {
    render(
      <DecisionForm
        result={mockResult}
        physicianRoleHash="hash123"
        onSubmitted={() => {}}
      />,
      { wrapper: Wrapper }
    );
    expect(screen.getByText(/Aerztliche Einschaetzung/)).toBeInTheDocument();
  });

  it("selects verdict on click", () => {
    render(
      <DecisionForm
        result={mockResult}
        physicianRoleHash="hash123"
        onSubmitted={() => {}}
      />,
      { wrapper: Wrapper }
    );
    const btn = screen.getByText("Volle Uebereinstimmung");
    fireEvent.click(btn);
    expect(btn.className).toContain("border-cyan-500");
  });
});
