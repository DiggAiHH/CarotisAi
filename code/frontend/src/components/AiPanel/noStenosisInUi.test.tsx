import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { AiPanel } from "./AiPanel";

const researchResult = {
  case_id: "research-case-1",
  confidence_bucket: "high",
  trust_score: 0.82,
  calibrated: true,
  model_version: "v0.3.2",
  model_sha: "abc123d",
  audit_id: "audit-1",
  captured_at: "2026-05-11T12:00:00Z",
  heatmap_b64: null,
};

describe("research-mode AI panel terminology", () => {
  it("does not render quantitative stenosis or vulnerability wording", () => {
    const { container } = render(<AiPanel result={researchResult} />);
    const text = container.textContent ?? "";

    expect(screen.getByText(/Forschungs-Overlay/)).toBeInTheDocument();
    expect(text).not.toMatch(/%/);
    expect(text).not.toMatch(new RegExp("NAS" + "CET", "i"));
    expect(text).not.toMatch(new RegExp("Vulner" + "ability", "i"));
  });
});
