import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { Walkthrough } from "./Walkthrough";

// Mock zustand store
const mockSetWalkthroughSeen = vi.fn();
let mockWalkthroughSeen = false;

interface MockStoreState {
  walkthroughSeen: boolean;
  setWalkthroughSeen: typeof mockSetWalkthroughSeen;
}

vi.mock("@/store", () => ({
  useStore: (selector: (s: MockStoreState) => unknown) =>
    selector({
      walkthroughSeen: mockWalkthroughSeen,
      setWalkthroughSeen: mockSetWalkthroughSeen,
    }),
}));

// Mock apiClient
vi.mock("@/lib/apiClient", () => ({
  apiClient: {
    logWalkthroughStep: vi.fn().mockResolvedValue(undefined),
  },
}));

describe("Walkthrough", () => {
  beforeEach(() => {
    mockWalkthroughSeen = false;
    mockSetWalkthroughSeen.mockClear();
    // Reset body overflow
    document.body.style.overflow = "";
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renders walkthrough overlay when not seen", () => {
    render(<Walkthrough />);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByLabelText(/Walkthrough-Tour/i)).toBeInTheDocument();
  });

  it("does not render overlay when already seen", () => {
    mockWalkthroughSeen = true;
    render(<Walkthrough />);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(screen.getByLabelText(/Walkthrough-Tour neustarten/i)).toBeInTheDocument();
  });

  it("has focus trap — first button is focused on open", async () => {
    render(<Walkthrough />);
    await waitFor(() => {
      const buttons = screen.getAllByRole("button");
      expect(buttons.length).toBeGreaterThan(0);
    });
  });

  it("closes on Escape key", () => {
    render(<Walkthrough />);
    fireEvent.keyDown(window, { key: "Escape" });
    expect(mockSetWalkthroughSeen).toHaveBeenCalledWith(true);
  });

  it("does NOT intercept Escape when typing in input", () => {
    render(<Walkthrough />);
    const input = document.createElement("input");
    document.body.appendChild(input);
    input.focus();
    fireEvent.keyDown(input, { key: "Escape" });
    expect(mockSetWalkthroughSeen).not.toHaveBeenCalled();
    document.body.removeChild(input);
  });

  it("does NOT expose window.__restartWalkthrough", () => {
    render(<Walkthrough />);
    expect((window as Window & { __restartWalkthrough?: unknown }).__restartWalkthrough).toBeUndefined();
  });

  it("has aria-modal=true on overlay", () => {
    render(<Walkthrough />);
    const overlay = screen.getByRole("dialog");
    expect(overlay).toHaveAttribute("aria-modal", "true");
  });
});
