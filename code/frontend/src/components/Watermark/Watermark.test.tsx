import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Watermark } from "./Watermark";

describe("Watermark", () => {
  it("renders the canonical RESEARCH USE ONLY string", () => {
    render(<Watermark />);
    expect(
      screen.getByText(
        /RESEARCH USE ONLY · Forschungsverwendung · Kein Medizinprodukt/i,
      ),
    ).toBeInTheDocument();
  });

  it("is rendered with the testid 'research-watermark'", () => {
    render(<Watermark />);
    expect(screen.getByTestId("research-watermark")).toBeInTheDocument();
  });

  it("has role=note for accessibility", () => {
    render(<Watermark />);
    expect(screen.getByRole("note")).toBeInTheDocument();
  });

  it("is positioned fixed and pointer-events-none to never block interactions", () => {
    render(<Watermark />);
    const node = screen.getByTestId("research-watermark");
    expect(node.className).toMatch(/fixed/);
    expect(node.className).toMatch(/pointer-events-none/);
  });

  it("supports override text prop for export/PDF reuse", () => {
    render(<Watermark text="Custom Export Watermark" />);
    expect(screen.getByText("Custom Export Watermark")).toBeInTheDocument();
  });
});
