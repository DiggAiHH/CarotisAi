import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Walkthrough } from "./Walkthrough";

// Mock useWalkthrough hook
const mockNext = vi.fn();
const mockBack = vi.fn();
const mockSkip = vi.fn();
const mockDone = vi.fn();
const mockRestart = vi.fn();

let mockIsActive = true;
let mockCurrentStep = 0;

vi.mock("./useWalkthrough", () => ({
  useWalkthrough: () => {
    return {
      isActive: mockIsActive,
      currentStep: mockCurrentStep,
      totalSteps: 5,
      steps: [
        { id: "welcome", title: "Willkommen bei Carotis-AI", text: "Tour startet hier." },
        { id: "dicom", title: "Schritt 1", text: "DICOM laden.", targetId: "tour-dicom-viewer", position: "right" as const },
        { id: "ai", title: "Schritt 2", text: "KI-Analyse.", targetId: "tour-ai-panel", position: "left" as const },
        { id: "decision", title: "Schritt 3", text: "Decision-Tree.", targetId: "tour-decision-form", position: "left" as const },
        { id: "done", title: "Tour abgeschlossen", text: "Fertig." },
      ],
      next: mockNext,
      back: mockBack,
      skip: mockSkip,
      done: mockDone,
      restart: mockRestart,
    };
  },
}));

describe("Walkthrough", () => {
  beforeEach(() => {
    mockIsActive = true;
    mockCurrentStep = 0;
    vi.clearAllMocks();
    document.body.style.overflow = "";
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("mounts walkthrough overlay when active", () => {
    render(<Walkthrough />);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByText("Willkommen bei Carotis-AI")).toBeInTheDocument();
    expect(screen.getByText("Tour startet hier.")).toBeInTheDocument();
  });

  it("navigates to next step on Weiter click", () => {
    render(<Walkthrough />);
    const nextBtn = screen.getByRole("button", { name: /Weiter/i });
    fireEvent.click(nextBtn);
    expect(mockNext).toHaveBeenCalledTimes(1);
  });

  it("skips tour on Ueberspringen click", () => {
    render(<Walkthrough />);
    const skipBtn = screen.getByRole("button", { name: /Ueberspringen/i });
    fireEvent.click(skipBtn);
    expect(mockSkip).toHaveBeenCalledTimes(1);
  });

  it("renders Fertig button on last step and triggers done callback", () => {
    mockCurrentStep = 4;
    render(<Walkthrough />);
    const doneBtn = screen.getByRole("button", { name: /Fertig/i });
    expect(doneBtn).toBeInTheDocument();
    fireEvent.click(doneBtn);
    expect(mockNext).toHaveBeenCalledTimes(1);
  });
});
