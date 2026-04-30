import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { ConfidenceBadge, ConfidenceBar, LowConfidenceWarning } from "./ConfidenceBadge";

describe("ConfidenceBadge", () => {
  it("renders bucket label and percentage", () => {
    render(<ConfidenceBadge confidence={0.85} bucket="high" calibrated />);
    expect(screen.getByText("Hoch")).toBeInTheDocument();
    expect(screen.getByText("85%")).toBeInTheDocument();
    expect(screen.getByText("kal.")).toBeInTheDocument();
  });

  it("falls back to medium for unknown bucket", () => {
    render(<ConfidenceBadge confidence={0.5} bucket="unknown" />);
    expect(screen.getByText("Mittel")).toBeInTheDocument();
  });
});

describe("ConfidenceBar", () => {
  it("renders confidence bar", () => {
    render(<ConfidenceBar confidence={0.75} />);
    expect(screen.getByText("75%")).toBeInTheDocument();
  });
});

describe("LowConfidenceWarning", () => {
  it("renders warning text", () => {
    render(<LowConfidenceWarning />);
    expect(screen.getByText(/AI-Konfidenz niedrig/)).toBeInTheDocument();
  });
});
