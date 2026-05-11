import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { DecisionForm, type QuantitativeInferenceResponse } from "./DecisionForm";

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
}

function wrapper({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={createTestQueryClient()}>
      {children}
    </QueryClientProvider>
  );
}

// Mock apiClient
vi.mock("@/lib/apiClient", () => ({
  apiClient: {
    captureDecisionTree: vi.fn().mockResolvedValue({ audit_id: "abc", status: "ok" }),
    checkText: vi.fn().mockResolvedValue({ is_clean: true, pii_spans: [] }),
  },
}));

// Mock FreeTextField to control PII state
vi.mock("@/components/FreeTextField", () => ({
  FreeTextField: ({
    value,
    onChange,
    onPIIStatusChange,
  }: {
    value: string;
    onChange: (v: string) => void;
    onPIIStatusChange?: (hasPII: boolean) => void;
  }) => (
    <textarea
      data-testid="free-text"
      value={value}
      onChange={(e) => {
        onChange(e.target.value);
        onPIIStatusChange?.(e.target.value.includes("PII"));
      }}
    />
  ),
}));

const mockResult: QuantitativeInferenceResponse = {
  case_id: "abc123def456",
  stenosis_pct_nascet: 65.0,
  confidence: 0.85,
  confidence_bucket: "high",
  calibrated: false,
  vulnerability_markers: {
    intraplaque_hemorrhage: 0.0,
    thin_fibrous_cap: 0.0,
    lipid_rich_necrotic_core: 0.0,
    systolic_motion_anomaly: 0.0,
  },
  heatmap_b64: null,
  model_version: "v0.3.2",
  model_sha: "abc123",
  audit_id: "audit-1",
  captured_at: "2026-04-28T12:00:00Z",
  trust_score: 3,
};

describe("DecisionForm", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("renders verdict buttons with role=radio and aria-checked", () => {
    render(<DecisionForm result={mockResult} physicianRoleHash="doc-1" onSubmitted={vi.fn()} />, { wrapper });
    const radios = screen.getAllByRole("radio");
    expect(radios.length).toBeGreaterThanOrEqual(4);
    expect(radios[0]).toHaveAttribute("aria-checked", "true");
  });

  it("renders trust score buttons with role=radio", () => {
    render(<DecisionForm result={mockResult} physicianRoleHash="doc-1" onSubmitted={vi.fn()} />, { wrapper });
    const radios = screen.getAllByRole("radio");
    const trustRadios = radios.filter((r) => /^[1-5]$/.test(r.textContent || ""));
    expect(trustRadios.length).toBe(5);
  });

  it("disables submit when PII is detected in free text", async () => {
    render(<DecisionForm result={mockResult} physicianRoleHash="doc-1" onSubmitted={vi.fn()} />, { wrapper });
    const freeText = screen.getByTestId("free-text");
    fireEvent.change(freeText, { target: { value: "Contains PII" } });
    await waitFor(() => {
      const btn = screen.getByRole("button", { name: /PII entfernen/i });
      expect(btn).toBeDisabled();
    });
  });

  it("resets state when case_id changes", () => {
    const { rerender } = render(
      <DecisionForm result={mockResult} physicianRoleHash="doc-1" onSubmitted={vi.fn()} />,
      { wrapper }
    );
    const stenosisInput = screen.getByRole("spinbutton");
    fireEvent.change(stenosisInput, { target: { value: "80" } });

    const newResult = { ...mockResult, case_id: "new-case-789", stenosis_pct_nascet: 30 };
    rerender(<DecisionForm result={newResult} physicianRoleHash="doc-1" onSubmitted={vi.fn()} />);

    expect(stenosisInput).toHaveValue(30);
  });

  it("clamps stenosis input to valid range via min/max", () => {
    render(<DecisionForm result={mockResult} physicianRoleHash="doc-1" onSubmitted={vi.fn()} />, { wrapper });
    const stenosisInput = screen.getByRole("spinbutton");
    expect(stenosisInput).toHaveAttribute("min", "0");
    expect(stenosisInput).toHaveAttribute("max", "100");
  });
});
